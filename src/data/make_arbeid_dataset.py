import requests
import os


def make_nav_work_dataset_for_year(year: str, file_path: str) -> str:
    endpoint = "https://hotell.difi.no/download/nav/ledige-stillinger/{0}".format(year)
    data_path = os.path.join(os.path.pardir, "data", "raw")
    write_path = os.path.join(data_path, file_path)

    result = requests.api.get(endpoint)
    if result.status_code == 200:
        with open(write_path, "wb") as handle:
            for block in result.iter_content(1024):
                handle.write(block)
        return write_path
    if result.status_code == 404:
        raise FileNotFoundError("ERROR: HTTP 404 | Could not find a endpoint corresponding to the given year")
    else:
        raise E


if __name__ == "__main__":
    make_nav_work_dataset_for_year(2017, "nav_work_dataset.csv")
