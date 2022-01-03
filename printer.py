import pandas as pd
import pdfkit
import collections
from dateutil.relativedelta import relativedelta
import get_service
from utils import strfdelta
from docopt import docopt
from core import Result
from functools import reduce

def print_csv(result: Result, csv_file_path, output_format):
    if output_format == 1:
        print_csv_human_readable(result, csv_file_path)
    elif output_format == 2:
        print_csv_processing_friendly(result, csv_file_path)
    else:
        print("Unsupported output format")
        exit(0)


def print_csv_processing_friendly(result: Result, csv_file_path):
    with open(csv_file_path, "w+") as file:
        print("Date", "Duration", sep=",", file=file)
        for date, value in collections.OrderedDict(
            sorted(result.by_date.items())
        ).items():
            print(date, str(round(float(strfdelta(value, "{M}")) / 60, 2)), sep=",", file=file)

        print("", sep=",", file=file)
        print("Task", "Duration", sep=",", file=file)
        for task, date in collections.OrderedDict(
            sorted(result.by_task.items())
        ).items():
            print(
                task,
                str(round(float(strfdelta(date, "{M}")) / 60, 2)),
                sep=",",
                file=file,
            )

def print_csv_human_readable(result: Result, csv_file_path):
    with open(csv_file_path, "w+") as file:
        print("Date", "Duration", sep=",", file=file)
        for date, value in collections.OrderedDict(
            sorted(result.by_date.items())
        ).items():
            print(date, strfdelta(value, "{H}h {M}m"), sep=",", file=file)

        print(
            "Sum",
            strfdelta(reduce(lambda a, b: a + b, result.by_date.values()), "{H}h"),
            sep=",",
            file=file,
        )

        print("", sep=",", file=file)
        print("Task", "Duration", sep=",", file=file)
        for task, date in collections.OrderedDict(
            sorted(result.by_task.items())
        ).items():
            print(
                task,
                strfdelta(date, "{H}h {M}m"),
                sep=",",
                file=file,
            )

        print(
            "Sum",
            strfdelta(reduce(lambda a, b: a + b, result.by_task.values()), "{H}h"),
            sep=",",
            file=file,
        )


def print_pdf_and_html(result: Result, pdf_file_path, html_file_path):
    dataFrameable = dict()
    for date, value in collections.OrderedDict(sorted(result.by_date.items())).items():
        dataFrameable[date] = (value,)

    df = pd.DataFrame.from_dict(dataFrameable, orient="index", columns=["Duration"])
    total_duration_iso = strfdelta(df["Duration"].sum(), "{H}h")

    df = df.applymap(lambda entry: strfdelta(entry, "{H}h {M}m"))
    df.loc["Sum"] = total_duration_iso

    df.to_html(html_file_path, header=True, index=True)
    pdfkit.from_file(html_file_path, pdf_file_path)
