import requests
import os


API_URL_BASE = "https://hotell.difi.no/download/nav/ledige-stillinger/"


def make_data_set_for_year(year: str, file_path: str) -> str:

    data_path = os.path.join(os.path.pardir, "data", "raw")
    write_path = os.path.join(data_path, file_path)

    result = requests.api.get(API_URL_BASE + str(year))
    if result.status_code == 200:
        with open(write_path, "wb") as handle:
            for block in result.iter_content(1024):
                handle.write(block)
        return write_path
    if result.status_code == 404:
        raise FileNotFoundError("ERROR: HTTP 404 | Could not find a endpoint corresponding to the given year")
    else:
        raise IOError("ERROR: {0} | Could not connect to API endpoint".format(result.status_code))



