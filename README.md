# ⚽💥 footcrawl


[![publish.yml](https://github.com/chonalchendo/footcrawl/actions/workflows/publish.yml/badge.svg)](https://github.com/chonalchendo/footcrawl/actions/workflows/publish.yml)
[![License](https://img.shields.io/github/license/chonalchendo/footcrawl)](https://github.com/chonalchendo/footcrawl/mlops-python-package/blob/main/LICENCE.txt)

**Asynchronous Python package to crawl football data from Transfermarkt.**

This project's main focus is to build a `Python` package similar to the one shown in the excellent `GitHub` repository [mlops-python-package](https://github.com/fmind/mlops-python-package/tree/main) by [Médéric Hurier (Fmind)](https://github.com/fmind).

However, this package is focused on data engineering/scraping rather than MLOps. Médéric highlights lots of coding best practices applicable to every stage of the data lifecycle, and I was excited to apply his methods to my own project. 

Although amazing for scraping projects, `scrapy` is not used here as I wanted to develop my understanding asynchronous programming by building my own version of `scrapy`. 


# 📁 Table of Contents

- [Install](#install)
- [Usage](#usage)
  - [User-Agent](#user-agent)
  - [Configuration](#configuration)
  - [Execution](#execution)
- [Tools](#tools)
- [Future Work](#future-work)

# 📥 Install

1. **Clone the repository**

```bash
git clone https://github.com/chonalchendo/footcrawl.git
```

2. **Install uv**

```bash
pip install uv
```

3. **Install the project**

```bash
cd footcrawl/
uv sync
```

# 🕹️ Usage

## 🕵 User-Agent

For the crawler to work, you must create a `.env` file and add your `User-Agent` as shown in the `.env.example` file.

```yaml
USER_AGENT = "PUT YOUR USER AGENT HERE"
```
You can get your `User-Agent` by simply googling, *"what is my user agent?"*

It should look similar to this: `Mozilla/5.0 Generic Browser Chrome/128.0.0.0`

## 🔧 Configuration

Project crawlers are managed using `YAML` files located in the `confs` directory. These can be updated to scrape data for different leagues, seasons, and to store outputs as different formats and file locations.

```yaml
crawler:
  KIND: AsyncClubsCrawler
  url: "https://transfermarkt.co.uk/{league}/startseite/wettbewerb/{league_id}/plus/?saison_id={season}"
  seasons: [2022, 2023, 2024]
  leagues: 
    - name: "premier-league"
      id: "GB1"
    - name: "la-liga"
      id: "ES1"
    - name: "bundesliga" 
      id: "L1"
    - name: "serie-a"
      id: "IT1"
    - name: "ligue-1"
      id: "FR1"
  output:
    KIND: AsyncJsonWriter
    path: data/transfermarkt/{season}/clubs.json
    overwrite: true
  http_client:
    headers: {
      "User-Agent": "",
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
      "Accept-Language": "en-US,en;q=0.9",
      "Accept-Encoding": "gzip, deflate, br" 
      }
```

The above is the `confs/clubs.yaml` file which specifies the following:
- The crawler
- The URL to crawl
- The seasons to crawl
- The leagues to crawl
- The output format type and location
- Client information e.g. request headers

## 🚀 Execution

1. **Running the project**

All information related to each crawler is contained in each configuration file in the `confs` directory. Each of these configs are parsed from the command line during runtime.

```bash
uv run footcrawl confs/clubs.yaml
```
The above command will run the `Transfermarkt` `clubs` crawler. 

2. **Output**

Results from the crawler are then output to the `data` directory where the data is organised by year and stored as `JSON` files.

```bash
data
└── transfermarkt
    ├── 2018
    │   └── clubs.json
    ├── 2019
    │   └── clubs.json
    ├── 2020
    │   └── clubs.json
    ├── 2021
    │   └── clubs.json
    ├── 2022
    │   └── clubs.json
    ├── 2023
    │   └── clubs.json
    └── 2024
        └── clubs.json
```


# 🛠️ Tools

### Language: Python
- The language of choice for web-scraping as it's easy to learn and use
- Alternatives include `TypeScript` and `Go`.

### Package Manager: uv
- Amazing `Python` package manager written in `Rust`
- Manages project `Python` verisons, code formatting, package building and publishing. 
- Alternatives include `Poetry` or `pip`

### Project Manager: just
- Used to house all frequently used CLI commands.

```bash
just default
```
- Run the above to see all project commands.
- Alternatives include `pyinvoke` and `MakeFile`.

### Configuration Manager: YAML
- Human readable configuration file used to abstract away project execution to avoid users having to dig through code to make changes.
- Not sure there are many alteratives (good ones anyway). 

### Containerisation: Docker
- Used in my `GitHub Actions` continous integration (CI) pipeline to build, test, and publish the project to `Docker Hub` and `GitHub Container Registry (GHCR)`.
- Alteratives include `Podman`.

### Asynchronous Client: aiohttp
- Asynchronous client used to make concurrent requests to fetch website content.
- Used to build my own scraping framework rather than using an out of the box scraping package like `scrapy`.
- Alternatives include `httpx` and `scrapy`.

### Code Validation: Pydantic
- Used to provide type validation to my project classes at runtime.
- There aren't really any alternatives.

### CI Pipeline: GitHub Actions
- Free serverless compute that automates the build, test, and publishing of the `footcrawl` package on every push into master. 
- Alternatives include `Jenkins`, `Azure Pipelines` - Just use `GitHub Actions` though for `GitHub` based projects. 

# 🔮 Future work
- Add more `Transfermarkt` data.
- Add more football data sources e.g. `Sofascore`, `Fbref`.
- Create more advanced middleware including exponential backoff, concurrency limiting, and rate limit handling.
