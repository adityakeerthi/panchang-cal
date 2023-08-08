# imports
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import os
import requests
from bs4 import BeautifulSoup
import re

class PanchangCal:
    def __init__(self, calName):
        self.calName = calName
        self.cal = Calendar()
        self.cal.add('prodid', '-//My calendar product//example.com//')
        self.cal.add('version', '2.0')
    
    def addEvent(self, name, description, startTime, endTime):
        event = Event()
        try:
            event.add('summary', name)
            event.add('description', description)
            event.add('dtstart', datetime(startTime["year"], startTime["month"], startTime["day"], startTime["hour"], startTime["minute"], startTime["second"]))
            event.add('dtend', datetime(endTime["year"], endTime["month"], endTime["day"], endTime["hour"], endTime["minute"], endTime["second"]))
            self.cal.add_component(event)
        except Exception as e:
            print(e)
        


    def writeCal(self):
        directory = Path.cwd() / 'calendar'
        try:
            directory.mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            print("Folder already exists")
        else:
            print("Folder was created")
        f = open(os.path.join(directory, self.calName), 'wb')
        f.write(self.cal.to_ical())
        f.close()

    def parseDay(self, rawHTML):
        strings = rawHTML.split("<br/>")

        cleaned_strings = []

        for string in strings:
            clean_string = re.sub(r'<.*?>', '', string).strip()
            cleaned_strings.append(clean_string)

        data_dict = {}
        key_counter = {}

        for item in cleaned_strings:
            if ':' in item:
                key, value = item.split(':', 1)
                key = key.strip()
                
                if key in data_dict:
                    if key not in key_counter:
                        key_counter[key] = 1
                    else:
                        key_counter[key] += 1
                    new_key = f"{key}_{key_counter[key]}"
                    data_dict[new_key] = value.strip()
                else:
                    data_dict[key] = value.strip()

        return(data_dict)

    def getMonthData(self, year, month):
        url = "http://www.mypanchang.com/calformat.php"
        params = {
            "cityname": "Toronto-ON-Canada",
            "yr": str(year),
            "mn": str(month),
            "monthtype": "0"
        }

        response = requests.get(url, params=params)

        script_tag = ""

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            script_tags = soup.find_all("script")

            for script in script_tags:
                script_content = script.string
                if script_content:
                    script_tag += script_content
        else:
            print("Request failed with status code:", response.status_code)
        
        matches = re.findall(r'"(.*?)"', script_tag)
        days = []
        month = {}
        dateInMonth = 1
        for match in matches:
            if (match != "" and match[0] == "<"):
                month[dateInMonth] = self.parseDay(match)
                days.append(self.parseDay(match))
                dateInMonth += 1

        return month

    def loop(self, year):
        params = [
            "RK", "YM", "GK", "AJ", "DM", "DM_1", "V", "V_1", "AK"
        ]
        mappings = {
            "RK": "Rahu Kalam",
            "YM": "Yama Gandam",
            "GK": "Gulika Kalam",
            "AJ": "Abhijit Muhurta",
            "DM": "Durmuhurtham",
            "DM_1": "Durmuhurtham",
            "V": "Varjyam",
            "V_1": "Varjyam",
            "AK": "Amrit Kalam"
        }
        for i in range(1, 13):
            monthData = self.getMonthData(year, i)

            for day in monthData:
                description = monthData[day]
                for prop in description:
                    if prop in params:
                        value = description[prop]
                        if value != "none":
                            print(value)
                            start_time, end_time = value.split('-')
                            startHour, startMinute, startSecond = map(int, start_time.split(':'))
                            endHour, endMinute, endSecond = map(int, end_time.split(':'))

                            self.addEvent(mappings[prop], prop, {"year": year, "month": i, "day": day, "hour": startHour, "minute": startMinute, "second": startSecond}, {"year": 2023, "month": i, "day": day, "hour": endHour, "minute": endMinute, "second": endSecond})