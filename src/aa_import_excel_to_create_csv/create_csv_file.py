from src.utils.get_root_path import get_project_root

import pandas as pd


class ConvertExcel:

    def __init__(self, year):
        self.year = year
        self.excel_file = str(get_project_root()) + "/input/01_excel_raw/all-euro-data-" + str(year) + "-" + str(year +
                                                                                                                 1) +\
                          ".xlsx"
        self.sheets = None
        self.name_folders = {"E0": "EN_premiere_league",
                             "E1": "EN_championship",
                             "SC0": "SC_premiership",
                             "D1": "DE_bundesliga_1",
                             "SP1": "ES_la_liga",
                             "I1": "IT_serieA",
                             "F1": "FR_ligue1",
                             "B1": "BE_jupiler",
                             "N1": "NL_eredivise",
                             "P1": "PT_primeira_liga",
                             "T1": "TK_super_league",
                             "G1": "GR_super_league"
                             }

    def __read_sheets(self):
        """
        Read name of sheets
        :return:
        """
        all_sheets = pd.read_excel(self.excel_file, sheet_name=None, engine='openpyxl')
        self.sheets = all_sheets.keys()

    def __create_name_output(self, sheet_name: str):
        return str(get_project_root()) + "/input/" + self.name_folders.get(sheet_name) + "/01_raw/" + str(self.year) + \
               ".csv"

    def __read_excel(self):
        """
        Convert Sheet to csv
        :return:
        """
        for sheet_name in self.sheets:
            if sheet_name in list(self.name_folders.keys()):
                sheet = pd.read_excel(self.excel_file, sheet_name=sheet_name)
                path_output = self.__create_name_output(str(sheet_name))
                sheet.to_csv(path_output, index=False)

    def run(self):
        self.__read_sheets()
        self.__read_excel()


for year in list(range(2017, 2021)):
    convert = ConvertExcel(year=year)
    convert.run()
