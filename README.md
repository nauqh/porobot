# Echodb - A tiny elt system

![Python](https://img.shields.io/badge/Made%20With-Python%203.11-blue.svg?style=for-the-badge&logo=Python&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white)

**Update** (30 June 2023): View the web application here at [Echodb](https://echodb.streamlit.app/)

## About the project

Echodb is a tiny system for collecting and scheduling music data pipeline from [Spotify](https://engineering.atspotify.com/). In short, it allows you to:

* Collect playlist such as `Discovery Weekly`, `Release Radar` (or even custom events of your choosing).
* Store the data in a scalable database w/ [Postgresql](https://www.postgresql.org/) and [SQLAlchemy](https://www.sqlalchemy.org/).
* Leverage a wide range of tools to model and analyze the behavioral data.
* Generate reports and deploy online dashboard for easy management.

---

## Echodb Datastack 101

![Pipeline](data/stack.png)

The repository structure follows the conceptual architecture of Echodb, which consists of four loosely-coupled sub-systems.

To briefly explain these six sub-systems:

* **[Orchestrator][orchestrator]** utilizes `Prefect` as a flexible and reliable workflow management system to orchestrate the data processing tasks in the data pipeline as well as generate custom logs for managing the whole cycle.
* **[Extractor][extractor]** employs `Pydantic` to validate the integrity and quality of the extracted Spotify data through customizable data quality checks and adherence to expected schema and format.
* **[Storage][storage]** relies on `PostgreSQL` as a robust and feature-rich database system for persistent storage of Spotify data, while leveraging `SQLAlchemy` as the ORM tool for simplified interaction with the database.
* **[Analytics][analytics]** employs `Plotly` for creating interactive and visually appealing data visualizations, `Pandas` for data transformation and analysis, and `Streamlit` for deploying intuitive and user-friendly dashboards to explore and analyze Spotify data.

[orchestrator]: https://www.prefect.io/
[extractor]: https://developer.spotify.com/documentation/web-api
[storage]: https://www.postgresql.org/
[analytics]: https://resonance.streamlit.app/