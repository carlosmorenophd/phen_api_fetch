import flet as ft
from time import sleep
from api.data_warehouse import DataWarehouseApi
import numpy


def main(page: ft.Page):
    api = DataWarehouseApi(base_url="http://127.0.0.1:8000")
    page.title = "Get Dataset from data warehouse phenotypic"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    pb = ft.ProgressBar(width=400)
    pb.value = 0
    raw_result = []

    def search_click(e):
        pb.value = 0
        result = api.get_list_attributes()
        progress_count = 1

        for genotype in result["genotype"]:
            pb.value = progress_count / len(result["genotype"])
            for location in result["location"]:
                for repetition in result["repetition"]:
                    for cycle in result["cycle"]:
                        raw_row = []
                        raw_row.append(genotype["name"])
                        raw_row.append(location["name"])
                        raw_row.append(repetition["name"])
                        raw_row.append(cycle["name"])
                        for trait in result["trait"]:
                            value = api.get_raw(genotype=genotype["id"], location=location["id"],
                                                repetition=repetition["id"], trait=trait["id"], cycle=cycle["name"])
                            raw_row.append(value)
                        raw_result.append(raw_row)
            progress_count = progress_count + 1
            page.update()
        n_file = numpy.asarray(raw_result)
        numpy.savetxt("test.csv", n_file, fmt='%s', delimiter=",")
    page.add(
        ft.Text("Linear progress indicator", style="headlineSmall"),
        ft.IconButton(ft.icons.SEARCH, on_click=search_click),
        ft.Column([ft.Text("Doing something..."), pb]),
    )


ft.app(target=main)
