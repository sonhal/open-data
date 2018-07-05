import numpy as np
import pandas as pd
import scipy.stats as sci
import re
import pathlib


def save_dataframe(df: pd.DataFrame, file_path: str):
    path = pathlib.Path(file_path)
    df.to_pickle(path.absolute())
    return path.absolute()


def load_dataframe(file_path: str):
    path = pathlib.Path(file_path)
    df = pd.read_pickle(path.absolute())
    return df


def get_work_ad_data_frame(work_ad_dir: str):
    path = pathlib.Path(work_ad_dir)
    if path.exists():

        main_df = pd.DataFrame()
        df_list = list()
        for file in path.iterdir():
            print(file.absolute())
            year_df = pd.read_csv(file.absolute(), na_values="*", sep=";", error_bad_lines=False, index_col="stillingsnummer")
            df_list.append(year_df)
        return pd.concat(df_list, axis=0, sort=True)
    else:
        raise FileNotFoundError("Could not find the specified path")


def clean_yrke_grovgruppe(grov_gruppe: str) -> str:
    matcher = {'Ingen yrkesbakgrunn eller uoppgitt (2001-2011)': 'Ingen yrkesbakgrunn eller uoppgitt',
               'Kontorarbeid (2001-2011)': 'Kontorarbeid', 'Meglere og konsulenter (2001-2011)': 'Meglere og konsulenter',
               'Bygg og anlegg (2001-2011)': 'Bygg og anlegg', 'Butikk- og salgsarbeid (2001-2011)': 'Butikk- og salgsarbeid',
               'Ledere (2001-2011)': 'Ledere', 'Industriarbeid (2001-2011)': 'Industriarbeid',
               'Ingeniør- og ikt-fag (2001-2011)': 'Ingeniør- og ikt-fag',
               'Serviceyrker og annet arbeid (2001-2011)': 'Serviceyrker og annet arbeid',
               'Reiseliv og transport (2001-2011)': 'Reiseliv og transport', 'Undervisning (2001-2011)': 'Undervisning',
               'Barne- og ungdomsarbeid (2001-2011)': 'Barne- og ungdomsarbeid',
               'Helse, pleie og omsorg (2001-2011)': 'Helse, pleie og omsorg',
               'Akademiske yrker (2001-2011)': 'Akademiske yrker',
               'Jordbruk, skogbruk og fiske (2001-2011)': 'Jordbruk, skogbruk og fiske', 'Undervisning': 'Undervisning',
               'Reiseliv og transport': 'Reiseliv og transport', 'Ledere': 'Ledere', 'Helse, pleie og omsorg': 'Helse, pleie og omsorg',
               'Serviceyrker og annet arbeid': 'Serviceyrker og annet arbeid', 'Barne- og ungdomsarbeid': 'Barne- og ungdomsarbeid',
               'Akademiske yrker': 'Akademiske yrker', 'Butikk- og salgsarbeid': 'Butikk- og salgsarbeid', 'Bygg og anlegg': 'Bygg og anlegg',
               'Ingeniør- og ikt-fag': 'Ingeniør- og ikt-fag', 'Industriarbeid': 'Industriarbeid', 'Kontorarbeid': 'Kontorarbeid',
               'Meglere og konsulenter': 'Meglere og konsulenter', 'Ingen yrkesbakgrunn eller uoppgitt': 'Ingen yrkesbakgrunn eller uoppgitt',
               'Jordbruk, skogbruk og fiske': 'Jordbruk, skogbruk og fiske'}
    return matcher[grov_gruppe]


def clean_work_ad_data_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """Data cleaning pipeline for NAV work ad dataset"""

    return (df
            .assign(yrke_grovgruppe=lambda x: x.yrke_grovgruppe.map(clean_yrke_grovgruppe))
            .assign(registrert_dato=lambda x: pd.to_datetime(x.registrert_dato, format='%d.%m.%Y', errors="coerce"))
            .assign(sistepubl_dato=lambda x: pd.to_datetime(x.sistepubl_dato, format='%d.%m.%Y'))
            )
