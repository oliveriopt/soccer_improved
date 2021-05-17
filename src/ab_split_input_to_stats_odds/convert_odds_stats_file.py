from src import cons_input_data
from src.utils.get_root_path import get_project_root
from src.utils.create_directory_file import create_directory
from src.define_paths import define_path

import src.cons_paths as cons_path
import pandas as pd


class SplitOddsStatsFile:

    def __init__(self, league: str):
        self.path = str(get_project_root())
        self.path_dict = define_path(league=league)
        self.dict_stats = cons_input_data.stats
        self.dict_odds = cons_input_data.odds
        self.stats = pd.DataFrame
        self.odds = pd.DataFrame

    def __read_input(self, year: int) -> pd.DataFrame:
        """
        Read file and convert into dataframe
        :param year:
        :return:
        """
        df = pd.read_csv(self.path + self.path_dict.get("path_raw") + str(year) + cons_path.csv, sep=",",
                         encoding='unicode_escape')
        print(df)
        return df

    def __write_stats_odds(self, year) -> None:
        """
        Write stats and odds file into the project
        :param year: year
        :return:
        """

        create_directory(self.path + self.path_dict.get("path_odds_stats"))
        self.stats.to_csv(self.path + self.path_dict.get("path_odds_stats") + cons_path.stats + str(year) +
                          cons_path.csv)
        self.odds.to_csv(self.path + self.path_dict.get("path_odds_stats") + cons_path.odds + str(year) + cons_path.csv)

    def __read_select_columns(self, year: int):
        """
        Read select columns from dict and create stats and odds files
        :param year: year
        :return:
        """
        df = self.__read_input(year=year)

        self.stats = df[list(set(cons_input_data.stats.keys()) & set(df.columns.values.tolist()))]
        self.odds = df[list(set(cons_input_data.odds.keys()) & set(df.columns.values.tolist())) + [
            cons_input_data.home_team, cons_input_data.away_team]]
        self.stats["idGame"] = self.stats["HomeTeam"].astype(str).str[:] + "_" + self.stats["AwayTeam"].astype(
            str).str[:] + "_" + str(year)
        self.odds["idGame"] = self.odds["HomeTeam"].astype(str).str[:] + "_" + self.odds["AwayTeam"].astype(
            str).str[:] + "_" + str(year)

    def run_split(self, init_year: int, end_year: int):
        """
        SPLIT FILES FROM 01_RAW FOR STATS AND ODDS FILE
        :return:
        """
        for year in list(range(init_year, end_year)):
            self.__read_select_columns(year=year)
            self.__write_stats_odds(year=year)
