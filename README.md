# Crawling MITRE ATT&CK Data

This project is designed to crawl and process data from the MITRE ATT&CK framework. It consists of two main scripts:
1. `main.py` - Crawls the MITRE ATT&CK website to extract tactics, techniques, procedures, and mitigations.
2. `data_generation.py` - Processes the extracted data and matches it with directories containing attack technique logs.

## Table of Contents

1. [Requirements](#requirements)
2. [Usage](#usage)
  - [Crawling Data](#crawling-data)
  - [Processing Data](#processing-data)
3. [File Structure](#file-structure)
4. [Output](#output)
5. [License](#license)

## Requirements

- Python 3.x
- `requests_html`
- `pandas`

In this project, we are using the `uv` package. You can install it using:
```bash
pip install uv
```
Initialize the environment using:
```bash
uv init
```
Create the environment using:
```bash
uv venv .venv
```
You can install the required Python packages using:
```sh
uv add requests_html pandas
```

## Usage

### Crawling Data

The `main.py` script crawls the MITRE ATT&CK website and extracts relevant data.
```sh
python codes/main.py
```
This will generate JSON files for each tactic containing the extracted data.

### Processing Data

The `data_generation.py` script processes the JSON data and matches it with directories containing attack technique logs.
```sh
python codes/data_generation.py
```
This will generate `data.csv` and `data.json` files containing the processed data.

#### Note:
For this project, you have to clone the following repository in the `attack_data_` folder:
```bash
git clone https://github.com/splunk/attack_data
```

## File Structure

- `codes/main.py`: Script to crawl MITRE ATT&CK data.
- `codes/data_generation.py`: Script to process the crawled data.
- `Reconnaissance/Reconnaissance.json`: Input JSON file for data processing.
- `attack_data_/attack_data/datasets/attack_techniques/`: Directory containing attack technique logs.

## Output

- JSON files for each tactic (generated by `main.py`).
- `data.csv` and `data.json` (generated by `data_generation.py`).

## License

This project is licensed under the MIT License. If you see any problem in the project, you can make a pull request or email me at aliasadifl@gmail.com. Feel free to ask me anything about this project.
