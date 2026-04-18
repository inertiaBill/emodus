# eModus

Modus: Latin for "way" or "method."

eModus is a way to build event descriptions when planning events.
This has its roots with the Waterloo Cycling Club and planning
club events but could be used in a more general way.

Base configuration details are in `ride_attributes.yml`. The
responses to the prompts of gen.py combined with
ride_attributes.yml are synthesized into a complete ride
description.

## Prerequites

- Some computer that can run Python
    - Easiest is Linux, macOS, or Windows box
    - There are programs available for running Python programs on mobile devices (but these have not been tested)
- Python version 3.12 (later is expected to work but not tested).
- Python venv.
- To tell Emodus about known start locations,
    - Add them to a ile named secrets.yml in same directory as gen.py
    - Use the same format as the "locations" section of ride_attributes.yml

## Setup

It is recommended that you use a Python virtual environment:

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

## How to Create a New Topic in the Waterloo Cycling Club Discourse Forum

Follow these steps to use the eModus tool to automate your topic creation.

### 1. Preparation
* **Collect URLs:** Have the links for your routes ready to paste.
* **Open Terminal:** Open your Command Prompt (Windows) or Terminal (macOS or Linux).

### 2. Launch the Tool

Navigate to your eModus folder and start the application:

1.  **Enter the folder:** Use the `cd` command to move into the directory where you downloaded the files.
2.  **Activate the environment:** Run the activation command from the "Setup" guide (this ensures the tool has the right permissions to run).
3.  **Start the script:** Type the following and press **Enter**:
    ```bash
    python gen.py
    ```
### 3. Complete the Form

* **Follow Prompts:** The terminal will ask you for specific information. Type or paste your details as requested.
* **Automated Browser:** Once the info is entered, **gen.py** will automatically open your web browser and fill in the fields for you. 
* **Select Discipline:** Look for the "Tag" section in the browser and manually select the correct **Ride Discipline**.

### 4. Review and Submit
* **Check Your Work:** Briefly review the information the script populated in the browser to ensure everything looks correct.
* **Publish:** Click the **Create topic** button at the bottom of the page to finish.

Note to Developers: if you would like to enable debug logging set debugging:
- Linux: `DEBUG=1 python gen.py`
