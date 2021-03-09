from src.utils.get_root_path import get_project_root

import src.cons_paths as cons_path
import src.cons_input_data as cons_input
import pandas as pd


class EncodingTeams:

    def __init__(self):
        self.path = str(get_project_root())
        self.stats = pd.DataFrame()
        self.teams = []

    def __read_csv(self, year: str) -> pd.DataFrame:
        df = pd.read_csv(self.path + cons_path.odds_stats + cons_path.stats + year + cons_path.csv, index_col=0)
        return df

    def __select_teams(self):
        teams_home = list(self.stats[cons_input.home_team])
        teams_away = list(self.stats[cons_input.home_team])
        self.teams = sorted(list(set(teams_home + teams_away)))

    def __write_teams(self):
        df = pd.DataFrame(self.teams, columns=['teams'])
        df.to_csv(self.path + cons_path.teams_path + cons_path.teams + cons_path.csv)

    def encode_teams(self):
        for year in list(range(2003, 2020)):
            df = self.__read_csv(year=str(year))
            self.stats = self.stats.append(df, ignore_index=False)
        self.stats = self.stats.reset_index(drop=True)
        self.__select_teams()
        self.__write_teams()



encode = EncodingTeams()
encode.encode_teams()
