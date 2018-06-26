import os
import csv


def write_data(data_folder, filename, data):
    data_path = os.path.join(os.path.pardir, "data", data_folder)
    write_path = os.path.join(data_path, filename)
    csv.writer(data, write_path)
