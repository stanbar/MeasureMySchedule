import core
from get_service import service
from printer import print_csv, print_pdf_and_html
from slugify import slugify
from utils import safe_input, safe_input_many, safe_input_str
from datetime import datetime
import sys
import os

arguments = sys.argv
arguments.pop(0)
print(arguments)

def input_calendars():
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get("items", [])
    for index, cal in enumerate(calendars):
        print(f'{index}) {cal["summary"]}')

    indexes = [int(arguments.pop(0))] if len(arguments) > 0 else safe_input_many("Chose calendar index[s] separate by comma (,):")


    picked_cal_names, picked_cal_ids = [], []
    for index in indexes:
        if index < 0 or index >= len(calendars):
            print("Illegal index")
            exit(0)

        picked_cal = calendars[index]
        picked_cal_id = calendars[index]["id"]
        picked_cal_ids.append(picked_cal_id)
        picked_cal_name = picked_cal["summary"]
        picked_cal_names.append(picked_cal_name)

    return picked_cal_names, picked_cal_ids


def input_range_option():
    print("Chose how would you like to specify range:")
    print("1) last month")
    print("2) last x months")
    print("3) x month")
    print("4) from x month to y month")
    print("5) from x month to y month in year z")
    print("6) last x days")
    print("7) last week")
    print("8) last x weeks")

    from_date = datetime.now()
    to_date = datetime.now()
    option = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("Choose option: ")

    if option == 1:
        from_date, to_date = core.last_months(1)
    elif option == 2:
        last_months = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("Start from months ago: ")
        from_date, to_date = core.last_months(last_months)
    elif option == 3:
        month = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("Month: ")
        from_date, to_date = core.from_to(month, month)
    elif option == 4:
        month_from = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("From month: ")
        month_to = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("To month: ")
        from_date, to_date = core.from_to(month_from, month_to)
    elif option == 5:
        month_from = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("From month: ")
        month_to = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("To month: ")
        year = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("Year: ")
        from_date, to_date = core.from_to(month_from, month_to, year)
    elif option == 6:
        last_days =  int(arguments.pop(0)) if len(arguments) > 0 else safe_input("Last days: ")
        from_date, to_date = core.last_days(last_days)
    elif option == 7:
        from_date, to_date = core.last_week()
    elif option == 8:
        weeks = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("Last weeks: ")
        from_date, to_date = core.last_weeks(weeks)

    return from_date, to_date

def input_filter():
    return arguments.pop(0) if len(arguments) > 0 else safe_input_str("Filter phrase: ")

def input_format():
    print("Chose how would you like to print results:")
    print("1) human readable (%H h %m min)")
    print("2) processing friendly (%m)")

    output_format = int(arguments.pop(0)) if len(arguments) > 0 else safe_input("Choose option: ")

    if output_format == 1:
        pass
    elif output_format == 2:
        pass
    else:
        print("Illegal option")
        exit(0)

    return output_format


def compute_file_name(from_date, to_date):
    if from_date.year == from_date.year and from_date.month == to_date.month:
        file_name = from_date.strftime("%b-%Y")
    else:
        file_name = f'{from_date.strftime("%b-%Y")}_to_{to_date.strftime("%b-%Y")}'

    return file_name

def compute_directory_name(picked_cal_names):
    return "+".join(
        [slugify(picked_cal_name) for picked_cal_name in picked_cal_names]
    )

def compute_file_paths():
    csv_file_path = f"out/{directory_name}/csv/{file_name}.csv"
    html_file_path = f"out/{directory_name}/html/{file_name}.html"
    pdf_file_path = f"out/{directory_name}/pdf/{file_name}.pdf"
    return csv_file_path, html_file_path, pdf_file_path

def compute_file_paths_latest():
    csv_file_path = f"out/{directory_name}/csv/latest.csv"
    html_file_path = f"out/{directory_name}/html/latest.html"
    pdf_file_path = f"out/{directory_name}/pdf/latest.pdf"
    return csv_file_path, html_file_path, pdf_file_path

def create_directories(directory_name):
    os.makedirs("out", exist_ok=True)
    os.makedirs(f"out/{directory_name}", exist_ok=True)
    os.makedirs(f"out/{directory_name}/csv", exist_ok=True)
    os.makedirs(f"out/{directory_name}/html", exist_ok=True)
    os.makedirs(f"out/{directory_name}/pdf", exist_ok=True)

picked_cal_names, picked_cal_ids = input_calendars()
from_date, to_date = input_range_option()
filter = input_filter()
output_format = input_format()
file_name = compute_file_name(from_date, to_date)
directory_name = compute_directory_name(picked_cal_names)
csv_file_path, html_file_path, pdf_file_path = compute_file_paths()
csv_file_path_latest, html_file_path_latest, pdf_file_path_latest = compute_file_paths_latest()
create_directories(directory_name)
result = core.execute(picked_cal_ids, from_date, to_date, filter)
print_csv(result, csv_file_path, output_format)
print_csv(result, csv_file_path_latest, output_format)
print_pdf_and_html(result, pdf_file_path, html_file_path)

print("From", from_date)
print("To", to_date)
print(f"Saved to: \n{csv_file_path_latest} \n{csv_file_path} \n{pdf_file_path} \n{html_file_path}")
