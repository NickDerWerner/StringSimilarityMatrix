# Project: Similarity Calculation for [Specify what it's for here]

This project implements various algorithms to calculate semantic and lexical similarity between texts/models, divided into Model to Model (M2M) and Model to Text (M2T) approaches.


## Installation

1.  **Clone the repository:**
    ```bash
    git https://github.com/NickDerWerner/StringSimilarityMatrix.git
    cd StringMatchingSimilarity
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # For Linux/macOS
    # .\.venv\Scripts\activate   # For Windows CMD
    # .\.venv\Scripts\Activate.ps1 # For Windows PowerShell
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The M2T folder consists of files to analyse Model to Text similarity, given an initial project descriiption and the task description of a BPMN modell. A similarity matrix is created.
The different files use different strategies to determine the text similarity between the Tasks of the BPMN and Sentences of the Description.

The files in M2M do the same for a Model to Model comparison, where one Model was created by hand and the other one with a LLM powerd BPMN converter

**Example for M2M Semantic Similarity:**
```bash
python M2M/SematnicSimilarity.py --parameter1 value1 --parameter2 value2