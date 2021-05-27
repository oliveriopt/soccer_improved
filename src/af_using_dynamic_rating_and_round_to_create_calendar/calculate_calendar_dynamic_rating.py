# TODO:
# a) Take rating_fixo_macro  file with the year
# b) Make order by date to rating_dynamic_year file
# c) Make join with the "round" file  using "team" and "idGame"
# d) Change the feature "type_rating" from the last file and the file rating_fixo_macro, using "static_type_rating" and
#    "dynamic_type_rating".
# e) Make join with the big file and the file with tyoe_rating using "team" and "idGame" features. With this file we
#    build the CALENDAR DATA
# f) Run the FORMULA for RATING DYNAMIC using the equation. MAKE ATENTION WITH HOME; AWAY AND TOTAL
# g)
#
#

from src.utils.get_root_path import get_project_root
from src.define_paths import define_path

import src.cons_paths as cons_path
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class JoinData:

    def __init__(self, league: str):
        self.path = str(get_project_root())
        self.path_dict = define_path(league=league)
        self.rating_fixo_macro = pd.DataFrame()
        self.rating_dynamic = pd.DataFrame()
        self.round = pd.DataFrame()

    def __read_files(self, year: int) -> None:
        """
        Read the file with the rating fixo macro and rating_dynamic
        :param year:
        :return:
        """
        self.rating_fixo_macro = pd.read_csv(self.path + self.path_dict.get("path_rating_macro") +
                                             cons_path.rating_fixo_macro + cons_path.csv, sep=",",
                                             encoding='unicode_escape')
        self.rating_dynamic = pd.read_csv(self.path + self.path_dict.get("path_rating_dynamic") +
                                          cons_path.rating_dynamic + "_" + str(year) + cons_path.csv, sep=",",
                                          encoding='unicode_escape')
        self.rating_dynamic['date'] = pd.to_datetime(self.rating_dynamic['date'], format='%Y-%m-%d')
        self.round = pd.read_csv(self.path + self.path_dict.get("path_round") +
                                 cons_path.round + "_" + str(year) + cons_path.csv, sep=",",
                                 encoding='unicode_escape')
        self.round['Date'] = pd.to_datetime(self.round['Date'], format='%Y-%m-%d')
        self.round = self.round.rename(columns={"Date": "date", "idGame": "game_id"})
        self.teams = pd.read_csv(self.path + self.path_dict.get("path_teams") +
                                 cons_path.teams +
                                 cons_path.csv,
                                 sep=",",
                                 encoding='unicode_escape', index_col=0)
        self.teams = self.teams["teams"].tolist()
        self.calendar = pd.DataFrame()

    def __join_file(self):
        """
        Join file of calendar
        :return:
        """
        self.rating_fixo_macro['type_rating'] = self.rating_fixo_macro['type_rating'].map(lambda x: x.lstrip('static_'))
        result = pd.merge(self.rating_dynamic, self.round, how="inner", on=["game_id", "team", "date"])
        result['type_rating'] = result['type_rating'].map(lambda x: x.lstrip('dynamic_'))
        self.calendar = pd.merge(result, self.rating_fixo_macro, how="inner", on=["type_rating", "team", "year"])
        self.calendar = self.calendar.rename(columns={"value_rating": "Rating_Initial"})
        self.calendar = self.calendar.sort_values(by=["date", "team", "type_rating"]).reset_index(drop=True)

    def __write_file(self, year: int):
        """
        wrute file
        :param year:
        :return:
        """
        self.calendar.to_csv(self.path + self.path_dict.get("path_calendar") + cons_path.calendar +
                             "_" + str(year) + cons_path.csv, index=False)
        del self.calendar

    def run(self):
        """

        :return:
        """
        for year in list(range(2007, 2021)):
            self.__read_files(year=year)
            self.__join_file()
            self.__write_file(year=year)


for league in cons_path.leagues:
    if league != "GR_super_league":
        print(league)
        join_data = JoinData(league=league)
        join_data.run()
