# RAGAPP for text documents

## Description

This is a simple RAG(Retrieval-augmented generation) application developed for jk tech assesment ,which uses 
- Pinecone : for storing embedding vectors
- Openai api : for chat completion
- AWS : for handling system parameters(for larger application can be replaced by postgres or mongo)
- Fastapi : for restapi app development

## Prerequisites
Before setting up the project, ensure you have the following installed on your system:

    Python (version 3.10.12 recommended)
    Download and install from python.org.
    Ensure Python is added to your system PATH.

    pip (Python package manager)
    pip is included with Python 3.4 and later. You can check if it's installed by running:

`python -m pip --version`

If pip is not installed, install it using:

`python -m ensurepip --default-pip`



## Installation

1. Clone the repository: `git clone https://github.com/YashwanthMN1/ragapp.git`
2. Run shell script(windows): `sh setup.sh` 
3. Run shell script(linux):`source setup.sh`
4. check uvicorn `uvicorn --version`

## Usage
IMPORTANT: mention envirorment variables required in a `.env` file

1. Run the app: `uvicorn main:app`

2. Run using docker-compose :`docker-compose up --build`

## Features

- Feature 1: add document = add text document using swagger ui of fastapi(only .txt files are supported as of now).
- Feature 2: ask question = ask question with respect to document uploaded.
- Feature 3: list document ids =  get list of available document id ,currently we are not storing documetn name.
- Feature 4: select document = select document id which will be used for asking question.

