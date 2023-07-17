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

    def get_stats(self, summoner_name):
        puuid = get_puuid(summoner_name, self.region, self.api_key)
        df = self.db.get_stats(puuid=puuid)
        return df

    # Get list of champions sort by a criteria
    def best_champion_by(self, df, criteria) -> pd.DataFrame:
        # Calculate average damage of each champions
        champ_damages = df[['championName',
        criteria]].groupby('championName').mean()
        return champ_damages.sort_values(by=criteria,ascending=False)


    #Get stats ratio
    def get_ratio(self,df, stat_a, stat_b):
        nominator = df[stat_a].sum()
        total = df[stat_b].sum() + nominator
        return (nominator / total, total)


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
        df = an.get_stats(summoner_name)
        damage_df = an.best_champion_by(df,'totalDamageDealtToChampions')
        participation_df = an.best_champion_by(df,'challenges.killParticipation')

        print(f"Player: {summoner_name}\n")

        print(f"Average damage dealt:{round(damage_df.mean().item())}")

        print(f"Kda:{df['challenges.kda'].mean():.2f}")

        dodged_ratio, total_skillshot = an.get_ratio(df,
        'challenges.skillshotsDodged','challenges.skillshotsHit')

        print(f"Dodge ratio: {dodged_ratio*100:.2f}% ({total_skillshot})\n")

        print(f"Highest participation:\n",participation_df.head(3))
        print("\n")
