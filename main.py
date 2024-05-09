import time
import argparse
from browser import Browser

parser = argparse.ArgumentParser(description='Letswork timesheet autofill system')

parser.add_argument('-sd', '--start-date', type=str, help='Start date in format dd-mm-yyyy')
parser.add_argument('-ed', '--end-date', type=str, help='End date in format dd-mm-yyyy')
parser.add_argument('-st', '--start-time', type=str, help='Start time in format HH:MM')
parser.add_argument('-et', '--end-time', type=str, help='End time in format HH:MM')
parser.add_argument('-p', '--project-name', type=str, help='Fill Project name')
parser.add_argument('-t', '--today', help='Fill today timesheet', action='store_true', default=False)

args = parser.parse_args()
if __name__ == '__main__':

    if args.today:
        args.start_date=None
        args.end_date=None
        
    browser = Browser(args.start_date, args.end_date,args.start_time, args.end_time,args.project_name,args.today)
    
    browser.setup()
    browser.login()

    for day in browser.days_list:
        browser.fill_missing_days(day)
        print(f"Day {day} filled successfully")

    time.sleep(1)
    browser.close()
