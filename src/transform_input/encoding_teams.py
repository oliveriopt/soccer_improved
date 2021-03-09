import pandas as pd
from src.utils.get_root_path import get_project_root


class EncodingTeams:

    def __init__(self):
        self.path = get_project_root()

    def __read_csv(self, year: str) -> pd.DataFrame:
        df = pd.read_csv(str(self.path) + "/input/england-master/" + year + "/eng.1.csv")
        return df

    def read_year(self):
        for year in list(range(1992, 2021)):
            data = self.__read_csv(year=str(year))
            print(data)


encode = EncodingTeams()
encode.read_year()
