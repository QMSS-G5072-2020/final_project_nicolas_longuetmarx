# legis_easy_download 

![](https://github.com/ n-longuetmarx/legis_easy_download/workflows/build/badge.svg) [![codecov](https://codecov.io/gh/ n-longuetmarx/legis_easy_download/branch/main/graph/badge.svg)](https://codecov.io/gh/ n-longuetmarx/legis_easy_download) ![Release](https://github.com/ n-longuetmarx/legis_easy_download/workflows/Release/badge.svg) [![Documentation Status](https://readthedocs.org/projects/legis_easy_download/badge/?version=latest)](https://legis_easy_download.readthedocs.io/en/latest/?badge=latest)

Python packages that eases to use Legiscan API to download and classify legislation data. 
You should first obtin an API key from https://legiscan.com/. 

## Installation

```bash
$ pip install -i https://test.pypi.org/simple/ legis_easy_download
```

## Features

There are several features in this package: 
- Display the list of sessions available for one state: get_session_list(state)
- Display the list of bills available for one state (or one specific session in one state): get_bills_list(session)
- Import all the law text from one (or several) sessions: import_text(bill)
- An aggregate command that allows to start either with a state (or a state session) and get the classification of laws by categories: (overall_request(state, year, download, path)

## Dependencies
- numpy 
- pandas
- requests
- json
- codecs
- matplotlib
- nltk 
- base64
- bs4
- re
- pytest

## Usage

Examples of each commands are provided below: 

##### get the list of sessions available for NY State: 
get_session_list('NY')

#### get the list of bills available for session 27 (NY State)
get_bill_list('27')

#### get the classification of bills from NY session in 2009: 
overall_request('NY', year=2009)

#### download all bills of NY 2009 session and get classification: 
overall_request('NY', download=True, year=2009,  path="NY")


## Documentation

The official documentation is hosted on Read the Docs: https://legis_easy_download.readthedocs.io/en/latest/

## Contributors

We welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/ n-longuetmarx/legis_easy_download/graphs/contributors).

### Credits

This package was created with Cookiecutter and the UBC-MDS/cookiecutter-ubc-mds project template, modified from the [pyOpenSci/cookiecutter-pyopensci](https://github.com/pyOpenSci/cookiecutter-pyopensci) project template and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage).
