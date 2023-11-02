
class MeanRawCountryInstitute ():
    def __init__(self, country: str, institute: str, index_country: int, index_institute: int, index_data: int) -> None:
        self.country = country
        self.institute = institute
        self.index_country = index_country
        self.index_institute = index_institute
        self.index_data = index_data
        self.clean()

    def clean(self):
        self.mean = 0
        self.mean_country = 0
        self.count_country = 0
        self.mean_institution = 0
        self.count_institution = 0
        self.count_all = 0
        self.mean_all = 0

    def add_item(self, row_child):
        self.add_mean(new_data=float(row_child[self.index_data]))
        if row_child[self.index_country] == self.country:
            self.add_mean_country(new_data=float(row_child[self.index_data]))
            if row_child[self.index_institute] == self.institute:
                self.add_mean_institute(
                    new_data=float(row_child[self.index_data]))

    def add_mean_country(self, new_data: float):
        self.mean_country = self.mean_country + new_data
        self.count_country = self.count_country + 1

    def add_mean_institute(self, new_data: float):
        self.mean_institution = self.mean_institution + new_data
        self.count_institution = self.count_institution + 1

    def add_mean(self, new_data: float):
        self.mean_all = self.mean_all + new_data
        self.count_all = self.count_all + 1

    def get_mean(self) -> float:
        if self.mean_institution != 0:
            return self.mean_institution / self.count_institution
        elif self.mean_country != 0:
            return self.mean_institution / self.count_institution
        else:
            return self.mean_all / self.count_all

    def get_tag(self, data_parent: float, scale: float = 0.5) -> str:
        mean = self.get_mean()
        if data_parent >= mean and data_parent <= (mean + scale):
            return "bueno"
        elif data_parent >= (mean + scale) and data_parent <= (mean + (scale * 2)):
            return "excelente"
        elif data_parent >= mean + (scale * 2):
            return "sobresaliente"
        else:
            return "malo"
