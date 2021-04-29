from src.utils.get_root_path import get_project_root

import src.cons_paths as cons_path
import src.cons_input_data as cons_input
import pandas as pd
import csv

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class CorrectionRating:

    def __init__(self):
        self.path = str(get_project_root())
        self.rating_macro = pd.DataFrame
        self.type_rating = []
        self.teams = []
        self.years = []
        self.output = pd.DataFrame()

    def __define_unique_values(self):
        """
        Define unique values of the rating macro
        :return:
        """
        self.type_rating = list(set(self.rating_macro[cons_input.columns_rating[2]].tolist()))
        self.teams = list(set(self.rating_macro[cons_input.columns_rating[1]].tolist()))
        self.years = list(set(self.rating_macro[cons_input.columns_rating[0]].tolist()))

    def __take_minima(self, df: pd.DataFrame) -> int:
        """
        Take second minima value of the column
        :param df:
        :return:
        """
        minima = list(set(df[cons_input.columns_rating[3]].tolist()))
        minima.sort()
        if minima[0] == 0:
            return minima[1]
        else:
            return minima[0]

    def __transformation_data(self) -> pd.DataFrame:
        self.__define_unique_values()
        for year in self.years:
            df1 = self.rating_macro.loc[self.rating_macro[cons_input.columns_rating[0]] == year]
            for type_rat in self.type_rating:
                df2 = df1.loc[df1[cons_input.columns_rating[2]] == type_rat]
                mini = self.__take_minima(df2)
                df2.loc[df2[cons_input.columns_rating[3]] == 0, cons_input.columns_rating[3]] = mini
                self.output = self.output.append(df2, ignore_index=True)

    def __read_file(self):
        self.rating_macro = pd.read_csv(
            self.path + cons_path.path_rating_macro + cons_path.rating_macro + cons_path.csv, sep=",",
            encoding='unicode_escape')

    def __write_file(self):
        self.output.to_csv(self.path + cons_path.path_rating_macro + cons_path.corrected_rating_macro + cons_path.csv, \
                                     index=False)

    def run(self):
        self.__read_file()
        self.__transformation_data()
        self.__write_file()


correction = CorrectionRating()
correction.run()
