from src.utils.get_root_path import get_project_root
from src.define_paths import define_path

import src.cons_paths as cons_path
import src.cons_calculations as cons_calc
import src.cons_input_data as cons_input
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class CalculateRatingFixoInitialEpoca:

    def __init__(self, league: str):
        self.path = str(get_project_root())
        self.path_dict = define_path(league=league)
        self.rating_macro = pd.DataFrame
        self.type_rating = []
        self.teams = []
        self.years = []
        self.output = pd.DataFrame(columns=cons_calc.columns_rating_fixo_initial)
        self.init_year = None

    def __define_unique_values(self):
        """
        Define unique values of the rating macro
        :return:
        """
        self.type_rating = list(set(self.rating_macro[cons_input.columns_rating[2]].tolist()))
        self.teams = list(set(self.rating_macro[cons_input.columns_rating[1]].tolist()))
        self.years = list(set(self.rating_macro[cons_input.columns_rating[0]].tolist()))
        self.years.sort()
        self.init_year = self.years[4]

    def __transformation_data(self) -> None:
        self.__define_unique_values()
        for type_rating in self.type_rating[:]:
            df = self.rating_macro.loc[self.rating_macro[cons_input.columns_rating[2]] == type_rating]
            for team in self.teams[:]:
                df1 = df.loc[df[cons_input.columns_rating[1]] == team].sort_values(by=cons_input.columns_rating[
                    0]).drop_duplicates()
                for year in range(self.init_year, self.years[-1] + 1)[:]:
                    df2 = df1.loc[
                        (df1[cons_input.columns_rating[0]] >= (year - cons_calc.delay_year_rating_fixo)) & (df1[
                                                                                                                cons_input.columns_rating[
                                                                                                                    0]] < year)]
                    value_rating = sum([x * y for x, y in
                                        zip(cons_calc.weight_rating_fixo_initial, df2[cons_input.columns_rating[3]])])
                    self.output.loc[len(self.output)] = [year, team, type_rating, round(value_rating, 1)]

    def __read_file(self):
        self.rating_macro = pd.read_csv(
            self.path + self.path_dict.get("path_rating_macro") + cons_path.corrected_rating_macro + cons_path.csv,
            sep=",",
            encoding='unicode_escape')

    def __write_file(self):
        self.output.to_csv(
            self.path + self.path_dict.get("path_rating_macro") + cons_path.rating_fixo_macro + cons_path.csv, \
            index=False)

    def run(self):
        self.__read_file()
        self.__transformation_data()
        print(self.output)
        self.__write_file()
