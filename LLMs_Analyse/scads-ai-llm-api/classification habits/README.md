# Classification example

This is an example that intends to show you how to:

- classify sentences into two categories
- use `guided_choice` to steer the answer generation

## Installation

Do the following steps in your bash shell:

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

## Usage

1. Create a file `.scadsai-api-key` in your home directory and put your API key in the file. You have to obtain the API Key from the llm.scads.ai team. You can find instructions on https://llm.scads.ai/.
2. Then simply start the script `main.py` from your bash shell:

```bash
source myenv/bin/activate
./main.py
```

3. Modify `main.py` as needed for different texts/categories
