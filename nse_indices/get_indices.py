import requests
from rich.live import Live
from rich.table import Table
from rich import box
import time

all_indices_json = "https://www.nseindia.com/api/allIndices"


# res = requests.get(url=all_indices_json)
# print(res.json())
global last_indices_data
last_indices_data = {}
cookies = {
    "_ga": "GA1.1.261788827.1669819704",
    "nsit": "XcDuLqQ8zdAsyeLVt6CDyWyD",
    "nseappid": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTY2OTkyNzQ4MSwiZXhwIjoxNjY5OTMxMDgxfQ.ERyU8DmrnIn1B4wqksZiQOFCvakmWB17kTiz8LVrqvs",
    "AKA_A2": "A",
    "ak_bmsc": "D80D00EF692234D8D2937DDC355A8BC7~000000000000000000000000000000~YAAQKkw5F3MUxLmEAQAATkdvzxEXT3+wH4IJlrpOcTeBVpemekhv0BgCifk5RB/y2V8eimzqKmS7ZLEHG0NShlMQLMANgUJjLEarKcs2KubviHh0S+7E6xInmG1GwyA37ACNpGmLtncoFl0JJeZz37dFxVSJZv6Mf9jrIY9Nw+6ttcAmgzZm3Mr5iU6IZmC2M+1DNB04oURrQXzZf03zMM6oqLnd39LJ3nwnVgGCplUne/avrauucUYQfMKIsEBOW+g/H0DMhHohUU1t3zNSuPj3u9sGFb9hZ/qy1ppbNKUMJVG480uqVLPkK92SC4+YhMlLylnTHvUhGnM23MjG9BBKIYKcyuyCjgqAstTBixoRczYQUkVIMi5IUSPhmOWkju/Wph7EsuUKgghQZbJKMbE1RwW+jADlUFLaKniVCVkp5JM9N0jiedmdmsIMlrn5TNWSjPgzJ5R3y0D/g2wv3/tvoswCRfEQ4u3TMzWR1GHhJ1jrKZ1HGbZoNXWhLck=",
    "_ga_PJSKY6CFJH": "GS1.1.1669927403.4.1.1669927487.60.0.0",
    "bm_sv": "23DF9E9529D8ADBF4DC52D1E0894F369~YAAQKkw5F34UxLmEAQAADklvzxFF11UOIxyE1QkY8M78ssvDywewfG3zlhphNh7yXJzs8NXDRzpjLlSALGDdssZ1LYukVflen0IE6JM4rEfs/XEJijSasBcWiFP7B2K5k8Z+wMHKEA9/gTP+PKvzx13td9T5Hh6NsMS/KS9cxMISp7zBHltzD1aWclce6s7K7poHlnjDRQSE141AiQ6rzlOZQe3c7aikQLpBwvS9RrFQVLm1eIjR+tqTUKZt+632waM=~1",
}

headers = {
    "authority": "www.nseindia.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ga=GA1.1.261788827.1669819704; nsit=XcDuLqQ8zdAsyeLVt6CDyWyD; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTY2OTkyNzQ4MSwiZXhwIjoxNjY5OTMxMDgxfQ.ERyU8DmrnIn1B4wqksZiQOFCvakmWB17kTiz8LVrqvs; AKA_A2=A; ak_bmsc=D80D00EF692234D8D2937DDC355A8BC7~000000000000000000000000000000~YAAQKkw5F3MUxLmEAQAATkdvzxEXT3+wH4IJlrpOcTeBVpemekhv0BgCifk5RB/y2V8eimzqKmS7ZLEHG0NShlMQLMANgUJjLEarKcs2KubviHh0S+7E6xInmG1GwyA37ACNpGmLtncoFl0JJeZz37dFxVSJZv6Mf9jrIY9Nw+6ttcAmgzZm3Mr5iU6IZmC2M+1DNB04oURrQXzZf03zMM6oqLnd39LJ3nwnVgGCplUne/avrauucUYQfMKIsEBOW+g/H0DMhHohUU1t3zNSuPj3u9sGFb9hZ/qy1ppbNKUMJVG480uqVLPkK92SC4+YhMlLylnTHvUhGnM23MjG9BBKIYKcyuyCjgqAstTBixoRczYQUkVIMi5IUSPhmOWkju/Wph7EsuUKgghQZbJKMbE1RwW+jADlUFLaKniVCVkp5JM9N0jiedmdmsIMlrn5TNWSjPgzJ5R3y0D/g2wv3/tvoswCRfEQ4u3TMzWR1GHhJ1jrKZ1HGbZoNXWhLck=; _ga_PJSKY6CFJH=GS1.1.1669927403.4.1.1669927487.60.0.0; bm_sv=23DF9E9529D8ADBF4DC52D1E0894F369~YAAQKkw5F34UxLmEAQAADklvzxFF11UOIxyE1QkY8M78ssvDywewfG3zlhphNh7yXJzs8NXDRzpjLlSALGDdssZ1LYukVflen0IE6JM4rEfs/XEJijSasBcWiFP7B2K5k8Z+wMHKEA9/gTP+PKvzx13td9T5Hh6NsMS/KS9cxMISp7zBHltzD1aWclce6s7K7poHlnjDRQSE141AiQ6rzlOZQe3c7aikQLpBwvS9RrFQVLm1eIjR+tqTUKZt+632waM=~1',
    "referer": "https://www.nseindia.com/market-data/live-market-indices",
    "sec-ch-ua": '"Chromium";v="106", "Not.A/Brand";v="24", "Opera GX";v="92"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 OPR/92.0.0.0",
}


def check_market_open():
    """checks if NSE market is open from response JSON ["marketState"][0]["marketStatus"]

    Returns:
        Boolean: Returns True if open else False
    """
    try:
        response = requests.get(
            "https://www.nseindia.com/api/marketStatus", headers=headers
        )
        if response.json()["marketState"][0]["marketStatus"] == "Open":
            return True
        else:
            return False
    except Exception as err:
        print("error occured: ", err)
        return check_market_open()


def fetch_nse_indices_json(last_indices_data):
    if check_market_open() == False and len(last_indices_data):
        data = last_indices_data
    else:
        try:
            response = requests.get(
                "https://www.nseindia.com/api/allIndices", headers=headers
            )
            # print(response.json())
            data = response.json()
            last_indices_data = data
            return data
        except Exception as err:
            print("error occured: ", err)
            return fetch_nse_indices_json(last_indices_data)


def reformat_nse_indices_json(last_indices_data):
    # if check_market_open() == False and len(last_indices_data):
    #     data = last_indices_data
    # else:
    #     response = requests.get(
    #         "https://www.nseindia.com/api/allIndices", headers=headers
    #     )
    #     # print(response.json())

    #     data = response.json()
    #     last_indices_data = data
    #
    data = fetch_nse_indices_json(last_indices_data)
    print(data)
    indices = []
    price = []
    result = []
    for d in data["data"]:
        # print(d["index"], d["last"])
        # indices.append(d["index"])
        # price.append(d["last"])
        if any(ele in d["index"] for ele in ["TR", "YR"]) == False:
            result.append(
                {"index": d["index"], "value": d["last"], "change": d["variation"]}
            )
    return result


fetch_nse_indices_json(last_indices_data)

table = Table()
table.add_column("Index")
table.add_column("Value")
# table.add_column("Level")


def generate_table():
    # Make a new table.
    table = Table(box=box.ROUNDED)
    table.add_column("Index")
    table.add_column("Value")
    table.add_column("Status")

    res = reformat_nse_indices_json(last_indices_data)
    for row in res:
        # value = random.random() * 100
        # table.add_row(
        #     f"{row}", f"{value:3.2f}", "[red]ERROR" if value < 50 else "[green]SUCCESS"
        # )
        table.add_row(
            f"{row['index']}",
            f"{row['value']}",
            "[red]ERROR" if row["value"] < 50000 else "[green]SUCCESS",
        )
    return table


# with Live(table, refresh_per_second=30):  # update 4 times a second to feel fluid
#     for row in range(12):
#         time.sleep(0.4)  # arbitrary delay
#         # update the renderable internally
#         table.add_row(f"{row}", f"description {row}", "[red]ERROR")
with Live(generate_table(), refresh_per_second=4) as live:
    while True:
        time.sleep(30)
        live.update(generate_table())
