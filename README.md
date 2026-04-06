# eModus

Modus: Latin for "way" or "method."

eModus is a way to build event descriptions when planning events
This has its roots with the Waterloo Cycling Club and planning
club events but could be used in a more general way

Base configuration details are in `ride_attributes.yml`. The
responses to the prompts of gen.py combined with
ride_attributes.yml are pushed into 

## Prerequites

- Python version 3.12 (later is expected to work but not tested)
- Python venv

## Setup

It is recommended that you use a Python virtual environment

- Open command prompt for your system
- Create virtual environment
    - Linux/macOS: `python3 -m venv ~/pyenv/emodus312`
    - Window:  `python3 -m venv emodus312`
- Active virtual environment:
    - Linux/macOS: `source ~/pyenv/emodus312/bin/activate`
    - Window: `.\emodus312\Scripts\activate.bat`
- `python3 -m pip install PyYAML==6.0.3`
- `python3 -m pip install pytest`
    - Only needed if you plan to do development and run pytest unit test

## Get eModus

Download the following files from GitHub:
- Open the following in your web browser:
    - https://github.com/inertiaBill/emodus/tree/main/src/emodus
- Download the following files:
    - gen.py
    - ride_attributes.yml
    - ride_template.md

## Running

- Move to the folder where you downloaded the eModus files
- Activate virtual environment as in "Setup" section above.
- `python gen.py`

Note: if you would like to enable debug logging set debugging:
- Linux: `DEBUG=1 python gen.py`
