import pandas as pd
import pdfkit
import collections
from dateutil.relativedelta import relativedelta
import get_service
from utils import strfdelta
from docopt import docopt
from core import Result
from functools import reduce


def print_csv(result: Result, csv_file_path):
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
        for task in result.by_task:
            print(
                task,
                strfdelta(result.by_task[task], "{H}h {M}m"),
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
