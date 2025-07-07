![Made with Python](https://forthebadge.com/images/badges/made-with-python.svg)
![Build with Love](http://ForTheBadge.com/images/badges/built-with-love.svg)

```ascii
███╗   ███╗ █████╗ ██████╗  ██████╗ 
████╗ ████║██╔══██╗██╔══██╗██╔═══██╗
██╔████╔██║███████║██████╔╝██║   ██║
██║╚██╔╝██║██╔══██║██╔═══╝ ██║   ██║
██║ ╚═╝ ██║██║  ██║██║     ╚██████╔╝
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝ 
       by HectorH06 (@HectorH06)          version 0.1
```

![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)
![MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)

### General Description
In order to get all kind of data from INEGI, created a dashboard that allows to get it through filters for state, class and up to five subclasses. An scraper was made so this was possible, but there's no need to run it since the data dict (indicadores.csv) is already loaded.

## General instructions

1. Install requirements with the following command :

   `pip install -r requirements.txt`

## Dashboard usage

1. Put your API token in a file named ".secrets", you can get one here: www.inegi.org.mx/app/desarrolladores/generatoken/Usuarios/token_Verify

2. Run:

    `streamlit run dashboard.py`

## Map dashboard usage

1. Run:

    `streamlit run mapsDashboard.py`

## Future Features

- Filter through zipcode
- Data fetching through zipcode