# 📔 Glider logbook

Simple streamlit application to display various statistics on glider flights.
This application use a csv file containing the flight data extracted from the Givav Smart'Glide website using the cli [givav-scrape](#extracting-flights-data-from-givav-smart-glide-website)

## Requirements

* Python 3.11

## How to run this app locally with python 3

We suggest you to create a virtual environment for running this app with Python 3. Clone this repository and open your terminal/command prompt in a folder.

```bash
git clone https://github.com/tfraudet/glider-logbook.git
cd ./glider-logbook
python3 -m venv .venv
```

On Unix systems

```bash
source .venv/bin/activate
```

On Window systems

```bash
.venv\scripts\activate
```

Install all required packages by running:

```bash
pip3 install -r requirements.txt
```

Then run the app locally:

```bash
streamlit run logbook.py
```

## Extracting flights data from Givav Smart Glide website

To run the givav scraping script, you have to install the ```givav``` package from the source:

```bash
pip install --editable .
```

Afterwards, the  ```givav-scrape``` command should be available:

```bash
# To extract the Givav logbook to a specific file use -o option. If no output file is specified, the result is send to stdout.
givav-scrape -o my-extract.csv

# You can also pass userid and password as arguments
givav-scrape --user my-userid --password my-password --output my-extract.csv

# To get the help
givav-scrape --help

# To get the version
givav-scrape --version
```

Eventually, you can run the script directly from the source code.

```bash
python ./givav/scrape.py --help
```
