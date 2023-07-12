# Porobot - League of Legends Discord Bot 

![Python](https://img.shields.io/badge/Made%20With-Python%203.11-blue.svg?style=for-the-badge&logo=Python&logoColor=white)
![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?style=for-the-badge&logo=discord&logoColor=white)
![Riot Games](https://img.shields.io/badge/riotgames-D32936.svg?style=for-the-badge&logo=riotgames&logoColor=white)

![Version](https://img.shields.io/badge/Latest_Version-V1.0.0-blue?style=for-the-badge)

**Update** (12 July 2023): Invite Porobot to your discord server at [Porobot](https://echodb.streamlit.app/)

## About the project

Echodb is a tiny system for collecting and scheduling music data pipeline from [Spotify](https://engineering.atspotify.com/). In short, it allows you to:

* Collect playlist such as `Discovery Weekly`, `Release Radar` (or even custom events of your choosing).
* Store the data in a scalable database w/ [Postgresql](https://www.postgresql.org/) and [SQLAlchemy](https://www.sqlalchemy.org/).
* Leverage a wide range of tools to model and analyze the behavioral data.
* Generate reports and deploy online dashboard for easy management.


## Porobot Techstack 101

The repository structure follows the conceptual architecture of Echodb, which consists of four loosely-coupled sub-systems.

To briefly explain these six sub-systems:

* **[Orchestrator][orchestrator]** utilizes `Prefect` as a flexible and reliable workflow management system to orchestrate the data processing tasks in the data pipeline as well as generate custom logs for managing the whole cycle.
* **[Extractor][extractor]** employs `Pydantic` to validate the integrity and quality of the extracted Spotify data through customizable data quality checks and adherence to expected schema and format.
* **[Storage][storage]** relies on `PostgreSQL` as a robust and feature-rich database system for persistent storage of Spotify data, while leveraging `SQLAlchemy` as the ORM tool for simplified interaction with the database.
* **[Analytics][analytics]** employs `Plotly` for creating interactive and visually appealing data visualizations, `Pandas` for data transformation and analysis, and `Streamlit` for deploying intuitive and user-friendly dashboards to explore and analyze Spotify data.

## Instalation

Local hosting of Porobot is also possible

Create a `.env` file to store the application authentication token and guild ids

```sh
TOKEN = BOT_TOKEN
GUILD = DISCORD_SERVER_ID
STDOUT_CHANNEL_ID = OUTPUT_CHANEL_ID
VOICE_CHANNEL_ID = VOICE_CHANNEL_ID
RIOT = RIOT_TOKEN
```

Install dependencies:

```sh
$ pip install -r requirements.txt
```

[orchestrator]: https://www.prefect.io/
[extractor]: https://developer.spotify.com/documentation/web-api
[storage]: https://www.postgresql.org/
[analytics]: https://resonance.streamlit.app/

## Documentation

Since Porobot is built on the basis of `Hikari` library, it is essential to look for the library documentation for further implementation. 

- `Hikari`: https://www.hikari-py.dev/
- `Lightbulb`: https://hikari-lightbulb.readthedocs.io/en/latest/
- `RiotAPI`: https://developer.riotgames.com/

## Contributors

Nauqh - [Github](https://github.com/nauqh) - hodominhquan.self@gmail.com
