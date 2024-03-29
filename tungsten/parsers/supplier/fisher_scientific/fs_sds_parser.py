import re
from io import IOBase
import string
from typing import IO
from tungsten.parsers.parsing_hierarchy import HierarchyElement
from tungsten.parsers.supplier.sigma_aldrich.sds_parser import (
    SigmaAldrichSdsParser
)



class FisherParser:
    def parse_fisher_scientific(io: IO[bytes]) -> list:
        
        pre_parsing_elements = SigmaAldrichSdsParser.import_parsing_elements(io)

        parsing_elements = []
        results = []
        element_name = ".....................................1111111111111111111122222222222222222222---"
        for k in range(0, len(pre_parsing_elements)):
            
            if not FisherParser.should_skip_element(pre_parsing_elements[k]):
                if "Product Name" in pre_parsing_elements[k].text_content:
                    element_name = pre_parsing_elements[k + 1].text_content

                if not (element_name in pre_parsing_elements[k].text_content and "_____" in pre_parsing_elements[k+1].text_content):
                    parsing_elements.append(pre_parsing_elements[k])

        # with open(f'test.txt', 'w') as file:
        #     for elem in parsing_elements:
        #         file.write(elem.text_content)
        #     return

        with open(f'out.txt', 'w') as file:
            section_num = 0
            found_cas = False
            found_comp = False
            for i in range(len(parsing_elements)):
                file.write(parsing_elements[i].text_content)
            for i in range(len(parsing_elements)):
                # file.write(parsing_elements[i].text_content)
                # reg = r'^\d+\.\s[^\d]+$'
                # if re.search(reg, parsing_elements[i].text_content):
                #     section_num += 1
                #     file.write("\n\nNEW SECTION\n")

                # section 1
                if "Product Name" in parsing_elements[i].text_content:
                    product_name = "Product Name", parsing_elements[i + 1].text_content.strip()
                    results.append(product_name)

                if "CAS No" in parsing_elements[i].text_content and not found_cas:
                    found_cas = True
                    cas_num = "CAS No", parsing_elements[i - 1].text_content.strip()
                    results.append(cas_num)

                if "Synonyms" in parsing_elements[i].text_content:
                    syn = parsing_elements[i - 1].text_content.split(";")
                    for i in range(len(syn)):
                        syn[i] = syn[i].strip()
                    synonyms = "Synonyms", syn
                    results.append(synonyms)
                
                if "Cat No" in parsing_elements[i].text_content:
                    cat_list = []
                    letters = tuple(string.ascii_letters)
                    i += 1
                    while parsing_elements[i].text_content.startswith(letters):
                        temp = parsing_elements[i].text_content.split(";")
                        if len(temp) == 1:
                            cat_list.append(temp)
                        else:
                            for elem in temp:
                                if not elem == '\n':
                                    cat_list.append(elem.strip())
                        i += 1
                    cat_no = "Cat No", cat_list
                    results.append(cat_no)

                if "Recommended Use" in parsing_elements[i].text_content:
                    rec_use = "Recommended Use", parsing_elements[i - 1].text_content.strip()
                    results.append(rec_use)

                if "Uses advised against" in parsing_elements[i].text_content:
                    use_against = "Uses advised against", parsing_elements[i - 1].text_content.strip()
                    results.append(use_against)

                if "Company" in parsing_elements[i].text_content and not found_comp:
                    found_comp = True
                    companies = []
                    i += 1
                    while not "Fisher" in parsing_elements[i].text_content:
                        if not parsing_elements[i].text_content.strip() == '':
                            companies.append(parsing_elements[i].text_content.strip())
                        i += 1
                    companies.append(parsing_elements[i].text_content.strip())    
                    company = "Company", companies
                    results.append(company)

                    info = []
                    i += 1
                    while not "Emergency" in parsing_elements[i].text_content:
                            info.append(parsing_elements[i].text_content.strip())
                            i += 1
                    comp_info = "Company Info", info
                    results.append(comp_info)
                    i += 1
                    nums = []
                    while not "Hazard" in parsing_elements[i].text_content:
                            if not parsing_elements[i].text_content.strip() == '':
                                nums.append(parsing_elements[i].text_content.strip())
                            i += 1
                    emergancy_contact = "Emergency Telephone Number", nums
                    results.append(emergancy_contact)
                # end section 1 

                # Section 2   
                if "Hazard Statements" in parsing_elements[i].text_content:
                    i += 1
                    hazards = []
                    while not "Precautionary" in parsing_elements[i].text_content:
                        if not parsing_elements[i].text_content.strip() == '':
                            hazards.append(parsing_elements[i].text_content.strip())
                        i += 1
                    hazards_statement = "Hazard(s) Identification", hazards
                    results.append(hazards_statement)

                    precautionary = []
                    while not "Hazards not otherwise classified (HNOC)" in parsing_elements[i].text_content:
                        if not parsing_elements[i].text_content.strip() == '':
                            precautionary.append(parsing_elements[i].text_content.strip())
                        i += 1
                    precautionary_statement = "Precautionary Statements", precautionary
                    results.append(precautionary_statement)

                    # other = []
                    # while not "Composition" in parsing_elements[i].text_content:
                    #     if not parsing_elements[i].text_content.strip() == '':
                    #         other.append(parsing_elements[i].text_content.strip())
                    #     i += 1
                    # other_statement = "Other hazards", other
                    # results.append(other_statement)
            
                # section 3
                if "3. Composition" in parsing_elements[i].text_content:
                    i += 4
                    reg = r'^\d+\.\s[^\d]+$'
                    components = []
                    temp_component = []
                    while not re.search(reg, parsing_elements[i].text_content):
                        temp_component = [parsing_elements[i].text_content.strip(),
                                            parsing_elements[i+1].text_content.strip(),
                                            parsing_elements[i+2].text_content.strip()]
                        components.append(temp_component)
                        i += 3
                    composition = "Composition", components
                    results.append(composition)
                # end of section 3
                    
                # section 6
                if "6. Accidental release measures" in parsing_elements[i].text_content:
                    i += 1
                    personal_precautions = ""
                    while not "Environmental Precautions" in parsing_elements[i + 1].text_content:
                        if not parsing_elements[i].text_content.strip() == '' and not "Personal Precautions" in parsing_elements[i].text_content:
                            personal_precautions += parsing_elements[i].text_content.strip() + " "
                        i += 1
                    
                    personal_precautions_section = "Personal Precautions", personal_precautions
                    results.append(personal_precautions_section)

                    environmental_precautions = ""
                    while not "Methods for Containment" in parsing_elements[i + 1].text_content:
                        if not parsing_elements[i].text_content.strip() == '' and not "Environmental Precautions" in parsing_elements[i].text_content:
                            environmental_precautions += parsing_elements[i].text_content.strip() + " "
                        i += 1
                    
                    environmental_precautions_section = "Environmental Precautions", environmental_precautions
                    results.append(environmental_precautions_section) 

                    methods = ""
                    while not "7. Handling" in parsing_elements[i + 1].text_content:
                        if not parsing_elements[i].text_content.strip() == '' and not "Methods for Containment and Clean" in parsing_elements[i].text_content and not "Up" in parsing_elements[i].text_content:
                            methods += parsing_elements[i].text_content.strip() + " "
                        i += 1
                    
                    methods_section = "Methods for Containment and Clean Up", methods
                    results.append(methods_section)
                    
                # section 7
                if "7. Handling and storage" in parsing_elements[i].text_content:
                    i += 1
                    handling = ""
                    while not "Storage" in parsing_elements[i + 1].text_content:
                        if not parsing_elements[i].text_content.strip() == '' and not "Handling" in parsing_elements[i].text_content:
                            handling += parsing_elements[i].text_content.strip() + " "
                        i += 1
                    
                    handling_section = "Handling", handling
                    results.append(handling_section)

                    storage = ""
                    while not "8. Exposure" in parsing_elements[i + 1].text_content:
                        if not parsing_elements[i].text_content.strip() == '' and not "Storage" in parsing_elements[i].text_content:
                            storage += parsing_elements[i].text_content.strip() + " "
                        i += 1
                    
                    storage_section = "Storage", storage
                    results.append(storage_section)
                    
                # section 13
                if "13. Disposal considerations" in parsing_elements[i].text_content:
                    i += 1
                    waste = ""
                    while not "Component" in parsing_elements[i].text_content:
                        if not "Waste Disposal Methods" in parsing_elements[i].text_content:
                            waste = waste + parsing_elements[i].text_content.strip()
                        i += 1
                    temp = [("Waste Disposal Methods", waste)]

                    # look for each component
                    while not "RCRA - P Series Wastes" in parsing_elements[i].text_content:
                        i += 1
                    i += 1
                    temp_comp = []
                    all_components = []
                    while not "14. Transport information" in parsing_elements[i].text_content:
                        temp_comp.append(parsing_elements[i].text_content.strip())
                        temp_comp.append(parsing_elements[i+1].text_content.strip())
                        temp_comp.append(parsing_elements[i+2].text_content.strip())
                        all_components.append(temp_comp)
                        i += 3
                    results.append(("Disposal considerations", [temp, all_components]))

                # end of section 13

                # section 14
                if "DOT" in parsing_elements[i].text_content and section_num == 14:
                    transport_results = []
                    transport_info = []
                    while not "UN" in parsing_elements[i].text_content:
                        i += 1
                    temp = []
                    temp.append(("UN-No", parsing_elements[i].text_content.strip()))
                    while not "Proper Shipping Name" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Proper Shipping Name", parsing_elements[i - 1].text_content.strip()))
                    while not "Hazard Class" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Hazard Class", parsing_elements[i - 1].text_content.strip()))

                    for j in range(0, 6):
                        if "Subsidiary Hazard Class" in parsing_elements[i+j].text_content:
                            temp.append(("Subsidiary Hazard Class", parsing_elements[i + j - 1].text_content.strip()))
                    while not "Packing Group" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Packing Group", parsing_elements[i - 1].text_content.strip()))
                    transport_info.append(("DOT", temp))

                if "TDG" in parsing_elements[i].text_content and section_num == 14:
                    while not "UN" in parsing_elements[i].text_content:
                        i += 1
                    temp = []
                    temp.append(("UN-No", parsing_elements[i].text_content.strip()))
                    while not "Proper Shipping Name" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Proper Shipping Name", parsing_elements[i - 1].text_content.strip()))
                    while not "Hazard Class" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Hazard Class", parsing_elements[i - 1].text_content.strip()))

                    for j in range(0, 6):
                        if "Subsidiary Hazard Class" in parsing_elements[i+j].text_content:
                            temp.append(("Subsidiary Hazard Class", parsing_elements[i + j - 1].text_content.strip()))
                    while not "Packing Group" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Packing Group", parsing_elements[i - 1].text_content.strip()))
                    transport_info.append(("TDG", temp))
                                        
                if "IATA" in parsing_elements[i].text_content and section_num == 14:
                    while not "UN" in parsing_elements[i].text_content:
                        i += 1
                    temp = []
                    temp.append(("UN-No", parsing_elements[i].text_content.strip()))
                    while not "Proper Shipping Name" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Proper Shipping Name", parsing_elements[i - 1].text_content.strip()))
                    while not "Hazard Class" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Hazard Class", parsing_elements[i - 1].text_content.strip()))

                    for j in range(0, 6):
                        if "Subsidiary Hazard Class" in parsing_elements[i+j].text_content:
                            temp.append(("Subsidiary Hazard Class", parsing_elements[i + j - 1].text_content.strip()))
                    while not "Packing Group" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Packing Group", parsing_elements[i - 1].text_content.strip()))
                    transport_info.append(("IATA", temp))
                                        
                if "IMDG" in parsing_elements[i].text_content and section_num == 14:
                    while not "UN" in parsing_elements[i].text_content:
                        i += 1
                    temp = []
                    temp.append(("UN-No", parsing_elements[i].text_content.strip()))
                    while not "Proper Shipping Name" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Proper Shipping Name", parsing_elements[i - 1].text_content.strip()))
                    while not "Hazard Class" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Hazard Class", parsing_elements[i - 1].text_content.strip()))

                    for j in range(0, 6):
                        if "Subsidiary Hazard Class" in parsing_elements[i+j].text_content:
                            temp.append(("Subsidiary Hazard Class", parsing_elements[i + j - 1].text_content.strip()))
                    while not "Packing Group" in parsing_elements[i].text_content:
                        i += 1
                    temp.append(("Packing Group", parsing_elements[i - 1].text_content.strip()))
                    transport_info.append(("IMDG/IMO", temp))

                    transport_results.append(("Transport Information", transport_info))
                    results.append(transport_results)
                # end of section 14

                # section 16
                if "16. Other information" in parsing_elements[i].text_content:
                    info = []
                    while not "Email: " in parsing_elements[i].text_content:
                        i +=1
                    email = parsing_elements[i].text_content.replace("Email: ", "")
                    info.append(("Email", email.strip()))
                    info.append(("Creation Date", parsing_elements[i + 1].text_content.strip()))
                    info.append(("Revision Date", parsing_elements[i + 3].text_content.strip()))
                    info.append(("Print Date", parsing_elements[i + 4].text_content.strip()))
                    i += 4
                    information = "Other Information", info
                    results.append(information)
                # do I need the extra information from this section???


                # end of section 16

            print(results)
            print()
            return results

    @staticmethod
    def should_skip_element(element: HierarchyElement) -> bool:
        """Returns whether this parsing element should not be added to initial hierarchy.
        Currently, all elements which are non-text data, or within the footer are removed."""
        should_skip = False
        # Skip if the text entry is empty
        should_skip = should_skip or element.text_content.strip() == ""

        should_skip = should_skip or "US Pharmacopeia - " in element.text_content
        should_skip = should_skip or "Sigma - " in element.text_content
        should_skip = should_skip or "Aldrich - " in element.text_content
        should_skip = should_skip or "SIGALD - " in element.text_content
        should_skip = should_skip or "ThermoFisher - " in element.text_content
        should_skip = should_skip or "Scientific - " in element.text_content

        should_skip = should_skip or ("_____" in element.text_content)
        should_skip = should_skip or (element.text_content.startswith("Page ") and " / " in element.text_content)
        should_skip = should_skip or ("Revision Date" in element.text_content)

        return should_skip
