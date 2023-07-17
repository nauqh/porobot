import sqlite3
import json
import pandas as pd
from datetime import datetime as dt

from riot import *
from db import *


class Analysis():
    __slots__ = ("db", "api_key", "region", "mass_region")

    def __init__(self, db: Database, api_key,
    region, mass_region) -> None:
        self.db = db
        self.api_key = api_key
        self.region = region
        self.mass_region = mass_region


    # Get damage dealt of a summoner by champions
    def champion_damage(self, summoner_name):
        puuid = get_puuid(summoner_name, self.region, self.api_key)

        df = self.db.get_stats(puuid=puuid)

        # Calculate average damage of each champions
        champ_damages = df[['championName',
        'totalDamageDealtToChampions']].groupby('championName').mean()

        return champ_damages.sort_values(by='totalDamageDealtToChampions',ascending=False)



if __name__ == "__main__":
    members = {"Cozy Bearrrrr": 'Cozy Bearrrrr',
               "ancomsuon": 'UnbeatableVN',
               "urbestbae": '3 Giờ Rửa Chim',
               "iu vk thungan": 'Lushen2711',
               "Obi-Wan": 'Sứ Giả Lọk Khe',
               "Wavepin": 'Wavepin'}

    db = init_database()
    an = Analysis(db, "RGAPI-a384a673-d288-42ec-a860-55a1602dba94", "vn2", "sea")
    for summoner_name in members.values():
        df = an.champion_damage(summoner_name)
        print(f"Player: {summoner_name}")
        print(f"avg:{df['totalDamageDealtToChampions'].mean()}\n")
        print(df.head(3))
        print("\n")
