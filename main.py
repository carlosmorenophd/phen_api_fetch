import flet as ft
from api.data_warehouse import DataWarehouseApi
import numpy
import json
from analysis.principalComponentAnalysis import calculate_with_dataset


def main(page: ft.Page):
    page.title = "Phenotypic tools dataset"

    def calculate_pca():
        calculate_with_dataset()

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Phenotypic tools dataset"),
                              bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton(
                        "PCA", on_click=lambda _: page.go("/pca")),
                ],
            )
        )
        if page.route == "/pca":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Principal Component Analysis"),
                                  bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton(
                            "Calculate", on_click=calculate_pca),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    # base_url = "http://127.0.0.1:8000"
    # valid_trait = 1
    # percentage_column = .90
    # percentage_row = .20
    # path_to_save = "/home/yeiden/Downloads/"
    # api = DataWarehouseApi(base_url=base_url)
    # page.title = "Get Dataset from data warehouse phenotypic"
    # page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # pb = ft.ProgressBar(width=400)
    # pb.value = 0
    # raw_result = []
    # raw_result_valid = []

    # def search_click(e):
    #     pb.value = 0
    #     result = api.get_list_attributes()
    #     progress_count = 1

    #     for genotype in result["genotype"]:
    #         pb.value = progress_count / len(result["genotype"])
    #         for location in result["location"]:
    #             for repetition in result["repetition"]:
    #                 for cycle in result["cycle"]:
    #                     raw_row = []
    #                     raw_row.append(genotype["name"])
    #                     raw_row.append(location["name"])
    #                     raw_row.append(repetition["name"])
    #                     raw_row.append(cycle["name"])
    #                     is_valid = True
    #                     for trait in result["trait"]:
    #                         value = api.get_raw(genotype=genotype["id"], location=location["id"],
    #                                             repetition=repetition["id"], trait=trait["id"], cycle=cycle["name"])
    #                         raw_row.append(value)
    #                         if valid_trait == trait["id"] and value == "":
    #                             is_valid = False
    #                     raw_result.append(raw_row)
    #                     if is_valid:
    #                         raw_result_valid.append(raw_row)
    #         progress_count = progress_count + 1
    #         page.update()
    #         break
    #     numpy.savetxt("{}test.{}".format(path_to_save, "csv"),
    #                   numpy.asarray(raw_result), fmt='%s', delimiter=",")
    #     numpy.savetxt("{}test_valid.{}".format(path_to_save, "csv"), numpy.asarray(
    #         raw_result_valid), fmt='%s', delimiter=",")
    #     with open("{}json_data.{}".format(path_to_save, "json"), "w") as file:
    #         json.dump(result, file)

    # def filter_click(e):
    #     list_valid_row = []
    #     arr = numpy.loadtxt("{}test_valid.{}".format(path_to_save, "csv"),
    #                         delimiter=",", dtype=str)
    #     result = {}
    #     with open("{}json_data.{}".format(path_to_save, "json")) as file:
    #         # Load its content and make a new dictionary
    #         result = json.load(file)
    #     for row in arr:
    #         empty = numpy.count_nonzero(row == '')
    #         percentage = len(result["trait"]) - empty / len(result["trait"])
    #         if percentage > percentage_row:
    #             list_valid_row.append(row)
    #     print(list_valid_row)

    # page.add(
    #     ft.Column(
    #         [
    #             ft.Text(
    #                 "Aplicacion para acciones relacionadas a los datasets", style="headlineSmall"),
    #         ]
    #     ),
    #     # ft.Text("Linear progress indicator", style="headlineSmall"),
    #     # ft.IconButton(ft.icons.SEARCH, on_click=search_click),
    #     # ft.Column([ft.Text("Doing something..."), pb]),
    #     # ft.Text("Convert validate file", style="headlineSmall"),
    #     # ft.IconButton(ft.icons.FILTER_LIST_ALT, on_click=filter_click),
    # )


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
