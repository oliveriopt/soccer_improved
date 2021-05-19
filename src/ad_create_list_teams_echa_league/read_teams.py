from src.utils.get_root_path import get_project_root
from src.define_paths import define_path

import pandas as pd
import src.cons_paths as cons_path

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

## TAKE ALL THE TEAMS FOR EVERY LEAGUE DURING ALL YEARS
## OUPUT IS THE FILE IN THE FOLDER teams FOR EACH LEAGUE

class ReadTeams:

    def __init__(self, league: str):
        self.path = str(get_project_root())
        self.path_dict = define_path(league=league)
        self.teams = None
        self.raw = None

    def __read_years(self, year_init: int, year_end: int):
        """
        Read file with the stats for each league
        :param year_init: initial year to read
        :param year_end: end year to read
        :return: raw data with all years per each league
        """
        li = []
        for filename in list(range(year_init, year_end)):
            df = pd.read_csv(self.path + self.path_dict.get("path_odds_stats") + cons_path.stats + str(
                filename) + cons_path.csv, index_col=None, header=0)
            li.append(df)

        self.raw = pd.concat(li, axis=0, ignore_index=True)

    def __select_teams(self):
        """
        Select the teams in the raw data
        :return:
        """
        hometeams = self.raw["HomeTeam"].tolist()
        awayteams = self.raw["AwayTeam"].tolist()
        teams = list(set(hometeams + awayteams))
        teams = [x for x in teams if str(x) != 'nan']
        teams.sort()

        df = pd.DataFrame(teams, columns=['teams'])
        return df

    def run(self):
        """
        Run the class TAKE ALL THE TEAMS FOR EVERY LEAGUE DURING ALL YEARS
        :return:
        """
        self.__read_years(2003, 2021)
        df = self.__select_teams()
        df.to_csv(self.path + self.path_dict.get("path_teams") + cons_path.teams + cons_path.csv)

