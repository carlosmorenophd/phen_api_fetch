import requests


class DataWarehouseApi:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_list_attributes(self):
        targets = ["genotype", "trait", "repetition", "location", "cycle"]
        variable_target = {}
        for target in targets:
            response = requests.get(
                url="{}/special_query/ids/{}".format(self.base_url, target)
            )
            # print(response.json())
            if response.ok:
                variable_target[target] = response.json()
        return variable_target

    def get_raw(self, genotype: int, location: int, repetition: int, trait: int, cycle: str) -> str:
        response = requests.post(
            url="{}/raw_collections/search/".format(self.base_url),
            params={"page": 1, "size": 10},
            json={
                "occurrence": 0,
                "cycle": cycle,
                "gen_number": 0,
                "repetition": repetition,
                "sub_block": 0,
                "plot": 0,
                "value_data": "",
                "trail_id": 0,
                "trait_id": trait,
                "genotype_id": genotype,
                "location_id": location,
                "unit_id": 0
            },
        )
        if response.ok:
            result = response.json()["items"]
            if len(result) == 1:
                if result[0]["value_data"] == None or result[0]["value_data"] == "-":
                    return ""
                return result[0]["value_data"].strip()
            elif len(result) == 0:
                return ""
        raise ValueError("Error on fetch to raw values")
    
    
