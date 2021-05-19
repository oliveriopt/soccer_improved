from src.utils.get_root_path import get_project_root
from src.define_paths import define_path
from datetime import datetime, timedelta, date

import src.cons_input_data as cons_input
import src.cons_paths as cons_path
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class MakeCalculationPerRound:

    def __init__(self, league: str):
        self.path = str(get_project_root())
        self.path_dict = define_path(league=league)
        self.rating_initial = pd.DataFrame()
        self.rating_dynamic = pd.DataFrame()
        self.teams = pd.DataFrame()
        self.calendar_round = pd.DataFrame()
        self.rating = pd.DataFrame(columns=cons_input.columns_rating)
        self.list_rating = [["year", "team", "type_rating", "value_rating"]]

    def __read_file(self, year: int) -> None:
        """
        Read the file with the odds and stats
        :param year:
        :return:
        """
        self.stats = pd.read_csv(self.path + self.path_dict.get("path_odds_stats") +
                                 cons_path.stats + str(year) +
                                 cons_path.csv,
                                 sep=",",
                                 encoding='unicode_escape', index_col=0)
        self.stats['Date'] = pd.to_datetime(self.stats['Date'], format='%Y-%m-%d')
        self.teams = pd.read_csv(self.path + self.path_dict.get("path_teams") +
                                 cons_path.teams +
                                 cons_path.csv,
                                 sep=",",
                                 encoding='unicode_escape', index_col=0)
        self.teams = self.teams["teams"].tolist()
        self.rating_initial = pd.read_csv(self.path + self.path_dict.get("path_rating_macro") +
                                          cons_path.corrected_rating_macro + cons_path.csv,
                                          sep=",",
                                          encoding='unicode_escape', index_col=0)

    def __select_mondays(self, year: int) -> list:
        """
        Return a list with all mondays in the season
        :param year:
        :return:
        """

        self.stats = self.stats.sort_values(by="Date")
        first_day = self.stats.iloc[0]["Date"]
        last_day = self.stats["Date"].tolist()
        last_day = last_day[-1]
        self.list_mondays = pd.date_range(start=str(year), end=str(year + 2),
                                          freq='W-MON').strftime('%d-%m-%Y').tolist()
        self.list_mondays = [i for i in self.list_mondays if datetime.strptime(i, '%d-%m-%Y') >= first_day if
                             datetime.strptime(i, '%d-%m-%Y') <= last_day + timedelta(days=7)]

    def __write_file(self, year: int):
        """
        wrute file
        :param year:
        :return:
        """
        self.calendar_round.to_csv(self.path + self.path_dict.get("path_round") + cons_path.round +
                                   "_" + str(year) + cons_path.csv, index=False)
        del self.calendar_round

    def __create_round(self):
        """
        Calculate rating macro for all the team for each year
        :return:
        """
        calendar = self.stats[["Date", "HomeTeam", "AwayTeam", "idGame"]]
        self.calendar_round = pd.DataFrame()
        for team in self.teams:
            home = calendar.loc[calendar["HomeTeam"] == team]
            home["Round_as_Home"] = range(1, home.shape[0] + 1)
            away = calendar.loc[calendar["AwayTeam"] == team]
            away["Round_as_Away"] = range(1, away.shape[0] + 1)
            # print(away)
            total = home.append(away)
            total["team"] = team
            total = total.sort_values(by="Date")
            total = total.fillna(method='ffill')
            total = total.fillna(1.0)
            total["Round_as_Total"] = range(1, total.shape[0] + 1)
            total[["Round_as_Home", "Round_as_Away", "Round_as_Total"]] = total[
                ["Round_as_Home", "Round_as_Away", "Round_as_Total"
                 ]].astype(int)
            self.calendar_round = self.calendar_round.append(total).sort_values(by="Date")
        self.calendar_round = self.calendar_round[["Date", "idGame", "team", "Round_as_Home", "Round_as_Away",
                                                   "Round_as_Total"]]
        self.calendar_round["Date"] = pd.to_datetime(self.calendar_round['Date'], format='%d-%m-%Y')
        for index in range(len(self.list_mondays)):
            # print(self.list_mondays)
            if index == 0:
                self.calendar_round.loc[
                    self.calendar_round['Date'] <= datetime.strptime(self.list_mondays[index], "%d-%m-%Y"),
                    'Round_by_Week_Total'] = index + 1
            elif index + 1 == len(self.list_mondays):
                self.calendar_round.loc[
                    ((self.calendar_round['Date'] > datetime.strptime(self.list_mondays[index - 1], "%d-%m-%Y")) & (
                            self.calendar_round['Date'] <= datetime.strptime(self.list_mondays[index], "%d-%m-%Y"))),
                    'Round_by_Week_Total'] = index + 1

            elif (index >= 1) and ((index + 1) != len(self.list_mondays)):
                #    #print(self.calendar_round['Date'], self.list_mondays[index-1])
                self.calendar_round.loc[
                    ((self.calendar_round['Date'] > datetime.strptime(self.list_mondays[index - 1], "%d-%m-%Y")) & (
                            self.calendar_round['Date'] <=
                            datetime.strptime(self.list_mondays[index], "%d-%m-%Y"))),
                    'Round_by_Week_Total'] = index + 1
        self.calendar_round['Round_by_Week_Total'] = self.calendar_round['Round_by_Week_Total'].astype(int)

    def run(self):
        for year in list(range(2007, 2021)):
            self.__read_file(year=year)
            self.__select_mondays(year=year)
            self.__create_round()
            self.__write_file(year=year)


for league in cons_path.leagues[-1:]:
    if league != "GR_super_league":
        print(league)
        round = MakeCalculationPerRound(league=league)
        round.run()
