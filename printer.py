import pandas as pd
import pdfkit
import collections
from utils import strfdelta
from core import Result
from functools import reduce
from datetime import datetime

def print_csv(result: Result, csv_file_path, output_format):
    if output_format == 1:
        print_csv_human_readable(result, csv_file_path)
    elif output_format == 2:
        print_csv_processing_friendly(result, csv_file_path)
    else:
        print(f'Unsupported output format {output_format}')
        exit(0)


def print_csv_processing_friendly(result: Result, csv_file_path):
    def format_time(value: datetime):
        hours = float(value.strftime("%H"))
        if hours > 16:
            hours = hours - 24
        minutes = float(value.strftime("%M"))

        return str(round(hours + (minutes / 60), 2))
        
    with open(csv_file_path, "w+") as file:
        print("Date", "Duration","Start", "End", sep=",", file=file)
        for date, value in collections.OrderedDict(
            sorted(result.by_date.items())
        ).items():
            print(date,
                    str(float(strfdelta(value['duration'], "{M}")) / 60),
                    format_time(value['start']),
                    format_time(value['end']),
                    sep=",",
                    file=file)

        print("", sep=",", file=file)
        print("Task", "Duration","Start","End", sep=",", file=file)
        for task, date in collections.OrderedDict(
            sorted(result.by_task.items())
        ).items():
            print(
                f'"{task}"',
                str(round(float(strfdelta(date['duration'], "{M}")) / 60, 2)),
                str(round(float(date['start'].strftime("%H") ) / 60, 2)),
                str(round(float(date['end'].strftime("%H") ) / 60, 2)),
                sep=",",
                file=file,
            )

def print_csv_human_readable(result: Result, csv_file_path):
    with open(csv_file_path, "w+") as file:
        print("Date", "Duration", sep=",", file=file)
        for date, value in collections.OrderedDict(
            sorted(result.by_date.items())
        ).items():
            print(date, strfdelta(value['duration'], "{H}h {M}m"), sep=",", file=file)

        durations_by_date = map(lambda a : a['duration'] ,result.by_date.values())
        print(
            "Sum",
            strfdelta(reduce(lambda a, b: a + b, durations_by_date), "{H}h"),
            sep=",",
            file=file,
        )

        print("", sep=",", file=file)
        print("Task", "Duration", sep=",", file=file)
        for task, date in collections.OrderedDict(
            sorted(result.by_task.items())
        ).items():
            print(
                f'"{task}"',
                strfdelta(date['duration'], "{H}h {M}m"),
                sep=",",
                file=file,
            )

        durations_by_task = map(lambda a : a['duration'] ,result.by_task.values())
        print(
            "Sum",
            strfdelta(reduce(lambda a, b: a + b, durations_by_task), "{H}h"),
            sep=",",
            file=file,
        )


def print_pdf_and_html(result: Result, pdf_file_path, html_file_path):
    dataFrameable = dict()
    for date, value in collections.OrderedDict(sorted(result.by_date.items())).items():
        dataFrameable[date] = (value['duration'],)

    df = pd.DataFrame.from_dict(dataFrameable, orient="index", columns=["Duration"])
    total_duration_iso = strfdelta(df["Duration"].sum(), "{H}h")

    df = df.applymap(lambda entry: strfdelta(entry, "{H}h {M}m"))
    df.loc["Sum"] = total_duration_iso

    df.to_html(html_file_path, header=True, index=True)
    pdfkit.from_file(html_file_path, pdf_file_path)
