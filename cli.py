import core
from get_service import service
from printer import print_csv, print_pdf_and_html
from slugify import slugify
from utils import safe_input
import os

calendars_result = service.calendarList().list().execute()
calendars = calendars_result.get("items", [])
for index, cal in enumerate(calendars):
    print(f'{index}) {cal["summary"]}')

index = safe_input("Chose calendar index:")

if index < 0 or index >= len(calendars):
    print("Illegal index")
    exit(0)

picked_cal = calendars[index]
picked_cal_id = calendars[index]["id"]
picked_cal_name = picked_cal["summary"]
print(f'picked {picked_cal["summary"]}')

print("Chose how would you like to specify range:")
print("1) last month")
print("2) last x months")
print("3) x month")
print("4) from x month to y month")
print("5) from x month to y month in year z")


option = safe_input("Choose option: ")
if option == 1:
    from_date, to_date = core.last_months(picked_cal_id, 1)
elif option == 2:
    last_months = safe_input("Start from months ago: ")
    from_date, to_date = core.last_months(picked_cal_id, last_months)
elif option == 3:
    month = safe_input("Month: ")
    from_date, to_date = core.from_to(picked_cal_id, month, month)
elif option == 4:
    month_from = safe_input("From month: ")
    month_to = safe_input("To month: ")
    from_date, to_date = core.from_to(picked_cal_id, month_from, month_to)
elif option == 5:
    month_from = safe_input("From month: ")
    month_to = safe_input("To month: ")
    year = safe_input("Year: ")
    from_date, to_date = core.from_to(picked_cal_id, month_from, month_to, year)

print("From", from_date)
print("To", to_date)

if from_date.year == from_date.year and from_date.month == to_date.month:
    file_name = from_date.strftime("%b-%Y")
else:
    file_name = f'{from_date.strftime("%b-%Y")}_to_{to_date.strftime("%b-%Y")}'

calendar_name = slugify(picked_cal_name)

csv_file_path = f"out/{calendar_name}/csv/{file_name}.csv"
html_file_path = f"out/{calendar_name}/html/{file_name}.html"
pdf_file_path = f"out/{calendar_name}/pdf/{file_name}.pdf"

os.makedirs("out", exist_ok=True)
os.makedirs(f"out/{calendar_name}", exist_ok=True)
os.makedirs(f"out/{calendar_name}/csv", exist_ok=True)
os.makedirs(f"out/{calendar_name}/html", exist_ok=True)
os.makedirs(f"out/{calendar_name}/pdf", exist_ok=True)

working_schedule = core.execute(picked_cal_id, from_date, to_date)

print_csv(working_schedule, csv_file_path)
print_pdf_and_html(working_schedule, pdf_file_path, html_file_path)
print(f"Saved to: \n{csv_file_path} \n{pdf_file_path} \n{html_file_path}")
