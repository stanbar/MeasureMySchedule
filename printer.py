import pandas as pd
import pdfkit
from dateutil.relativedelta import relativedelta
import get_service
from utils import strfdelta
from docopt import docopt


def print_csv(working_schedule, csv_file_path):
    with open(csv_file_path, "w+") as file:
        print("Data", "Czas pracy", sep=',', file=file)
        for date in working_schedule:
            print(date, working_schedule[date], sep=',', file=file)


def print_pdf_and_html(working_schedule, pdf_file_path, html_file_path):
    dataFrameable = dict()
    for key, value in working_schedule.items():
        dataFrameable[key] = (value,)

    df = pd.DataFrame.from_dict(
        dataFrameable, orient='index', columns=['Czas pracy'])
    total_duration_iso = strfdelta(df["Czas pracy"].sum(), "{H}h")

    df = df.applymap(lambda entry: strfdelta(entry, "{H}h {M}m"))
    df.loc['Suma'] = total_duration_iso

    df.to_html(html_file_path, header=True, index=True)
    pdfkit.from_file(html_file_path, pdf_file_path)
