import requests
import pathlib


API_URL_BASE = "https://hotell.difi.no/download/nav/ledige-stillinger/"


def make_data_set_for_year(year: int, file_path: str) -> str:
    """Attempts to download a NAV work ad data set for a given year"""
    path = pathlib.Path(file_path).absolute()

    result = requests.api.get(API_URL_BASE + str(year))
    if result.status_code == 200:
        with open(path, "wb") as handle:
            for block in result.iter_content(1024):
                handle.write(block)
        return path.as_uri()
    if result.status_code == 404:
        raise FileNotFoundError("ERROR: HTTP 404 | Could not find a endpoint corresponding to the given year")
    else:
        raise IOError("ERROR: HTTP {0} | Could not connect to API endpoint".format(result.status_code))


def make_complete_data_set(dir: str):
    """Downloads all the available work ad data files"""
    path = pathlib.Path(dir)

    print("Downloading...")
    for year in range (2002, 2018):
        print("Downloading work ad data set for year: {0}".format(year))
        make_data_set_for_year(year, path.joinpath("work_ad_dataset-{0}.csv".format(year)).absolute())
    print("Completed download successfully")


if __name__ == "__main__":
    make_data_set_for_year(2017, "test.csv")