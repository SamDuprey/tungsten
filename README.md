# Transfer Learning Approach

**Author:** Aditya Kangune (adityakangs@gmail.com)

## Overview

This Jupyter Notebook demonstrates a transfer learning approach to parse through Material Safety Data Sheets (MSDS) using a custom dataset. The project explores multiple methodologies with each section heading in the notebook representing a different approach. The final section focuses on the transfer learning approach, which has been used for the conclusive results.

## Project Context

Initially, this project was introduced as an alternative to traditional rule-based approaches. The promising results from the transfer learning model led decision-makers, Terri and Steven, to opt for a hybrid approach combining both rule-based techniques and transfer learning. This decision aims to harness the strengths of both methodologies for enhanced accuracy and efficiency.

## Setup

Before running this notebook, ensure you have the necessary Python environment and libraries installed. Here are general steps to prepare your environment:

1. Clone or download this repository to your local machine.
2. Ensure Python 3.x is installed.
3. Manually install any libraries used in the notebook (e.g., TensorFlow, PyTorch, pandas) using pip or conda. Example:

pip install tensorflow pandas

4. Ensure the custom dataset attached with this notebook is located in the same directory or appropriately referenced within the notebook.

## Usage

To use this notebook:

1. Open the notebook in JupyterLab or Jupyter Notebook.
2. Execute the cells sequentially. It's important to note that each section in the notebook explores a different methodology. The last section regarding transfer learning should be referred to for observing the final approach's effectiveness.
3. Observe the output to evaluate the model's performance and accuracy in parsing MSDS files. Keep in mind that the model is initially trained on a limited amount of annotated data; thus, variability in results can be expected. The accuracy and robustness of the model are anticipated to improve significantly with the addition of more annotated data to the custom dataset.

## Additional Notes

This project is intended for educational and research purposes. The transfer learning model can be adapted and fine-tuned for similar tasks involving document parsing and data extraction.

# SDS PDF Scraper for Chemicals

## Description

This Python script allows users to search for Safety Data Sheets (SDS) for various chemicals by querying the Fisher Scientific and Sigma Aldrich websites. Users can input chemical names, CAS numbers, or product numbers to retrieve the corresponding SDS links. The script is designed to handle multiple queries and supports continuous input until the user terminates the process.

## Features

- Collects multiple chemical identifiers (names, CAS numbers, or product numbers) from the user.
- Generates search URLs for these identifiers to query on Fisher Scientific's SDS search page.
- Scrapes the resultant web page to find all SDS links and prints them out.
- Additionally allows the search of product names on Sigma Aldrich's website and constructs URLs for their SDS pages.

## Prerequisites

Before running the script, ensure that the following Python libraries are installed:
- `requests`: For making HTTP requests.
- `beautifulsoup4`: For parsing HTML content.

## Usage

1. Run the script using a Python interpreter.
2. When prompted, enter either a chemical name, CAS number, or product number for each query. Type 'done' when you finish entering all chemicals.
3. Each valid input will generate an SDS link search on Fisher Scientific's website.
4. After finishing the chemical inputs, you can enter product names for Sigma Aldrich's SDS searches. Again, type 'done' when finished.
5. The script will output all SDS links found for each input chemical and product name.

## Important Notes

- The script requires an active internet connection to fetch the SDS pages.
- Ensure the terms of use of the Fisher Scientific and Sigma Aldrich websites allow for automated scraping before using this script.

## Contact

Email: [kalidin1@purdue.edu](mailto:kalidin1@purdue.edu)

# SDS PDF Scraper for Chemicals

## Description

This Python script allows users to search for Safety Data Sheets (SDS) for various chemicals by querying the Fisher Scientific and Sigma Aldrich websites. Users can input chemical names, CAS numbers, or product numbers to retrieve the corresponding SDS links. The script is designed to handle multiple queries and supports continuous input until the user terminates the process.

## Features

- **Text Parsing**: Utilizes the spaCy library and manual regex parsing for text processing to extract relevant information from the first aid measures section of SDS.
- **Subsection Identification**: Identifies subsections such as "Ingestion," "Inhalation," "Most important symptoms and effects," and "Notes to Physician" within the text.
- **Flexible Matching**: Implements fuzzy matching to handle slight variations in subsection headers and improve accuracy in identifying relevant information.
- **Output Formatting**: Presents the parsed information in a structured format, making it easy to read and understand.

## Limitations

- Currently only supports ThermoFisher and Sigma-Aldrich reliably.
- May not handle all variations and formats of first aid measures sections, leading to potential parsing errors.

## Prerequisites

Before running the script, ensure that the following Python libraries are installed:
- Python 3.x
- spaCy library: `pip install spacy`
- tungsten-sds: `pip install tungsten-sds`

## Usage

1. Install the required dependencies:
pip install spacy
pip install tungsten-sds
2. Run the script with the SDS text as input through the MSDS folder.
3. The parsed info will be displayed in the console output and produced as `.json` files.

## Important Notes

- The script requires an active internet connection to fetch the SDS pages.
- Ensure the terms of use of the Fisher Scientific and Sigma Aldrich websites allow for automated scraping before using this script.

## Contact

Email: [dinhq@purdue.edu](mailto:dinhq@purdue.edu)
Email: [dupreys@purdue.edu](mailto:dupreys@purdue.edu)




# Tungstenkit: ML container made simple
[![Version](https://img.shields.io/pypi/v/tungstenkit?color=%2334D058&label=pypi%20package)](https://pypi.org/project/tungstenkit/)
[![License](https://img.shields.io/github/license/tungsten-ai/tungstenkit)](https://raw.githubusercontent.com/tungsten-ai/tungstenkit/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/tungstenkit?style=flat-square)](https://pypi.org/project/tungstenkit/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/tungstenkit.svg?color=%2334D058)](https://pypi.org/project/tungstenkit/)

[Introduction](#tungstenkit-ml-container-made-simple) | [Installation](#prerequisites) | [Documentation](#documentation) | [Community](#join-our-community)

**Tungstenkit** is ML containerization tool with a focus on developer productivity and versatility. 

Have you ever struggled to use models from github?
You may have repeated tedious steps like: cuda/dependency problems, file handling, and scripting for testing.

Standing on the shoulder of Docker, this project aims to make using ML models less painful by adding functionalities for typical use cases - REST API server, GUI, CLI, and Python script.

With Tungstenkit, sharing and consuming ML models can be quick and enjoyable.


## Features
- [Requires only a few lines of Python code](#requires-only-a-few-lines-of-python-code)
- [Build once, use everywhere](#build-once-use-everywhere):
    - [REST API server](#rest-api-server)
    - [GUI application](#gui-application)
    - [CLI application](#cli-application)
    - [Python function](#python-function)
- [Framework-agnostic and lightweight](#framework-agnostic-and-lightweight)
- [Pydantic input/output definitions with convenient file handling](#pydantic-inputoutput-definitions-with-convenient-file-handling)
- [Supports batched prediction](#supports-batched-prediction)
- Supports clustering with distributed machines (coming soon)

## Take the tour
### Requires only a few lines of python code
Building a Tungsten model is easy. All you have to do is write a simple ``tungsten_model.py`` like:

```python
from typing import List
import torch
from tungstenkit import BaseIO, Image, define_model


class Input(BaseIO):
    prompt: str


class Output(BaseIO):
    image: Image


@define_model(
    input=Input,
    output=Output,
    gpu=True,
    python_packages=["torch", "torchvision"],
    batch_size=4,
    gpu_mem_gb=16,
)
class TextToImageModel:
    def setup(self):
        weights = torch.load("./weights.pth")
        self.model = load_torch_model(weights)

    def predict(self, inputs: List[Input]) -> List[Output]:
        input_tensor = preprocess(inputs)
        output_tensor = self.model(input_tensor)
        outputs = postprocess(output_tensor)
        return outputs

```

Start a build process:

```console
$ tungsten build . -n text-to-image

✅ Successfully built tungsten model: 'text-to-image:e3a5de56'
```

Check the built image:
```
$ tungsten models

Repository        Tag       Create Time          Docker Image ID
----------------  --------  -------------------  ---------------
text-to-image     latest    2023-04-26 05:23:58  830eb82f0fcd
text-to-image     e3a5de56  2023-04-26 05:23:58  830eb82f0fcd
```

### Build once, use everywhere

#### REST API server

Start a server:

```console
$ tungsten serve text-to-image -p 3000

INFO:     Uvicorn running on http://0.0.0.0:3000 (Press CTRL+C to quit)
```

Send a prediction request with a JSON payload:

```console
$ curl -X 'POST' 'http://localhost:3000/predictions' \
  -H 'Accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[{"prompt": "a professional photograph of an astronaut riding a horse"}]'

{
    "prediction_id": "39c9eb6b"
}
```

Get the result:
```console
$ curl -X 'GET' 'http://localhost:3000/predictions/39c9eb6b' \
  -H 'Accept: application/json'

{
    "outputs": [{"image": "data:image/png;base64,..."}],
    "status": "success"
}
```


#### GUI application
If you need a more user-friendly way to make predictions, start a GUI app with the following command:

```console
$ tungsten demo text-to-image -p 8080

INFO:     Uvicorn running on http://localhost:8080 (Press CTRL+C to quit)
```

![tungsten-dashboard](https://github.com/tungsten-ai/assets/blob/main/common/local-model-demo.gif?raw=true "Demo GIF")

#### CLI application
Run a prediction in a terminal:
```console
$ tungsten predict text-to-image \
   -i prompt="a professional photograph of an astronaut riding a horse"

{
  "image": "./output.png"
}
```

#### Python function
If you want to run a model in your Python application, use the Python API:
```python
>>> from tungstenkit import models
>>> model = models.get("text-to-image")
>>> model.predict(
    {"prompt": "a professional photograph of an astronaut riding a horse"}
)
{"image": PosixPath("./output.png")}
```

### Framework-agnostic and lightweight
Tungstenkit doesn't restrict you to use specific ML libraries. Just use any library you want, and declare dependencies:

```python
# The latest cpu-only build of Tensorflow will be included
@define_model(gpu=False, python_packages=["tensorflow"])
class TensorflowModel:
    def predict(self, inputs):
        """Run a batch prediction"""
        # ...ops using tensorflow...
        return outputs
```

### Pydantic input/output definitions with convenient file handling
Let's look at the example below:
```python
from tungstenkit import BaseIO, Image, define_model


class Input(BaseIO):
    image: Image


class Output(BaseIO):
    image: Image


@define_model(input=Input, output=Output)
class StyleTransferModel:
    ...
```
As you see, input/output types are defined as subclasses of the ``BaseIO`` class. The ``BaseIO`` class is a simple wrapper of the [``BaseModel``](https://docs.pydantic.dev/latest/usage/models/) class of [Pydantic](https://docs.pydantic.dev/latest/), and Tungstenkit validates JSON requests utilizing functionalities Pydantic provides.

Also, you can see that the ``Image`` class is used. Tungstenkit provides four file classes for easing file handling - ``Image``, ``Audio``, ``Video``, and ``Binary``. They have useful methods for writing a model's ``predict`` method:

```python
class StyleTransferModel:
    def predict(self, inputs: List[Input]) -> List[Output]:
        # Preprocessing
        input_pil_images = [inp.image.to_pil_image() for inp in inputs]
        # Inference
        output_pil_images = do_inference(input_pil_images)
        # Postprocessing
        output_images = [Image.from_pil_image(pil_image) for pil_image in output_pil_images]
        outputs = [Output(image=image) for image in output_images]
        return outputs
```

### Supports batched prediction
Tungstenkit supports both server-side and client-side batching.

- **Server-side batching**  
    <!-- Explain more? Mention hashing? -->
    A server groups inputs across multiple requests and processes them together.
    You can configure the max batch size:
    ```python
    @define_model(input=Input, output=Output, gpu=True, batch_size=32)
    ```
    The max batch size can be changed when running a server:
    ```console
    $ tungsten serve mymodel -p 3000 --batch-size 16
    ```

- **Client-side batching**  
    Also, you can reduce traffic volume by putting multiple inputs in a single prediction request:
    ```console
    $ curl -X 'POST' 'http://localhost:3000/predictions' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '[{"field": "input1"}, {"field": "input2"}, {"field": "input3"}]'
    ```

## Prerequisites
- Python 3.7+
- [Docker](https://docs.docker.com/get-docker/)

## Installation
```shell
pip install tungstenkit
```

## Documentation
- [Getting Started](https://tungsten-ai.github.io/docs/getting_started/installation/)
- [Building Your Model](https://tungsten-ai.github.io/docs/building_your_model/model_definition/)
- [Running Models](https://tungsten-ai.github.io/docs/running_models/using_gpus/)
- [Pushing and Pulling Models](https://tungsten-ai.github.io/docs/pushing_and_pulling_models/pushing/)
- [CLI Reference](https://tungsten-ai.github.io/docs/cli_reference/)
- [REST API Reference](https://tungsten-ai.github.io/docs/rest_api_reference/)
- [Examples](https://tungsten-ai.github.io/docs/examples/image_blurring/)

## Join our community
If you have questions about anything related to Tungstenkit, you're always welcome to ask our community on [Discord](https://discord.gg/NESFeXzFuy).
