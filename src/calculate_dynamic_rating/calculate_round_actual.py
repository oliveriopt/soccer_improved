from src.utils.get_root_path import get_project_root

import src.define_paths as cons_path
import src.cons_input_data as cons_input
import pandas as pd
import csv

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class CreateDynamicsPoints:

    def __init__(self):
        self.path = str(get_project_root())
        self.stats = pd.DataFrame()
        self.teams = pd.DataFrame()
        self.data_team_total = pd.DataFrame()
        self.data_team_home = pd.DataFrame()
        self.data_team_away = pd.DataFrame()
        self.rating = pd.DataFrame(columns=cons_input.columns_rating)
        self.list_rating = [["year", "team", "type_rating", "value_rating"]]

    def __read_file(self, year: int) -> pd.DataFrame:
        self.stats = pd.read_csv(self.path + cons_path.path_odds_stats + cons_path.stats + str(year) + cons_path.csv,
                                 sep=",",
                                 encoding='unicode_escape', index_col=0)
        self.stats['Date'] = pd.to_datetime(self.stats['Date'].astype(str), format='%d/%m/%Y')

    # print(self.stats)

    def __write_file(self):
        self.output.to_csv(self.path + cons_path.path_rating_macro + cons_path.corrected_rating_macro + cons_path.csv, \
                           index=False)

    def __create_rating(self, year: int):
        """
        Calculate rating macro for all the team for each year
        :return:
        """
        for index, row in self.teams.iterrows():
            self.__select_data_team(team=row[cons_path.teams], year=year)
            # self.calculate_rating(team=row[cons_path.teams], year=year)
        # print(self.list_rating)

    def __read_teams(self):
        """
        Read teams file and convert into dataframe
        :param year:
        :return:
        """
        self.teams = pd.read_csv(self.path + cons_path.path_teams + cons_path.teams + cons_path.csv, sep=",",
                                 encoding='unicode_escape', index_col=0)

    def run(self):
        for year in list(range(2003, 2005)):
            self.__read_file(year)
            self.__create_rating(year=year)
        print(self.data_team_home)
        # self.__transformation_data()
        # self.__write_file()


dynamic = CreateDynamicsPoints()
dynamic.run()
