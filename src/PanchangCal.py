# imports
from icalendar import Calendar, Event
import json
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
        self.cal.add('prodid', '-//Panchang Calendar//panchang-cal.vercel.app///')
        self.cal.add('version', '1.0')
        self.eventGuid = 0
        self.allEvents = []
    
    def pingYear(self, year):
        url = "http://www.mypanchang.com/calformat.php"
        params = {
            "cityname": "Toronto-ON-Canada",
            "yr": str(year),
            "mn": "1",
            "monthtype": "0"
        }
        response = requests.get(url, params=params)

        if "File not found" not in response.text:
            return True
        else:
            return False
        
    def getValidYears(self):
        currentYear = 2017
        validYears = []

        while True:
            if self.pingYear(currentYear):
                validYears.append(currentYear)
            else:
                break
            currentYear += 1

        return validYears

    def isGoodEvent(self, name):
        mappings = {
            "Rahu Kalam": False,
            "Yama Gandam": False,
            "Gulika Kalam": False,
            "Abhijit Muhurta": True,
            "Durmuhurtham": False,
            "Varjyam": False,
            "Amrit Kalam": True
        }

        return mappings[name]

    def addEvent(self, name, description, startTime, endTime):
        event = Event()
        startTime = self.adjustTime(startTime)
        endTime = self.adjustTime(endTime)

        try:
            startDateTime = datetime(
                startTime["year"],
                startTime["month"],
                startTime["day"],
                startTime["hour"],
                startTime["minute"],
                startTime["second"]
            )

            endDateTime = datetime(
                endTime["year"],
                endTime["month"],
                endTime["day"],
                endTime["hour"],
                endTime["minute"],
                endTime["second"]
            )

            eventObj = {
                "id": self.eventGuid,
                "title": name,
                "start": startDateTime.isoformat(),
                "end": endDateTime.isoformat(),
                "color": "darkgreen" if self.isGoodEvent(name) else "darkred"
            }
            self.allEvents.append(eventObj)

            self.eventGuid += 1

            event.add('summary', name)
            event.add('description', description)
            event.add('dtstart', startDateTime)
            event.add('dtend', endDateTime)
            self.cal.add_component(event)
        except Exception as e:
            print(e)

    def writeCal(self):
        directory = Path.cwd() / 'client' / 'public' / 'ics'
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

    def run(self, year):
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
                            start_time, end_time = value.split('-')
                            startHour, startMinute, startSecond = map(int, start_time.split(':'))
                            endHour, endMinute, endSecond = map(int, end_time.split(':'))

                            self.addEvent(mappings[prop], prop, {
                                    "year": year, 
                                    "month": i, 
                                    "day": day, 
                                    "hour": startHour, 
                                    "minute": startMinute, 
                                    "second": startSecond
                                }, {
                                    "year": year, 
                                    "month": i, 
                                    "day": day, 
                                    "hour": endHour, 
                                    "minute": endMinute, 
                                    "second": endSecond
                                }
                            )
        with open('./client/src/assets/Events.json', 'w') as convert_file:
            convert_file.write(json.dumps(self.allEvents))

    def isLeapYear(self, year):
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def adjustTime(self, time):
        days_in_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if self.isLeapYear(time['year']):
            days_in_month[2] = 29

        while time['second'] >= 60:
            time['second'] -= 60
            time['minute'] += 1
        
        while time['minute'] >= 60:
            time['minute'] -= 60
            time['hour'] += 1
        
        while time['hour'] >= 24:
            time['hour'] -= 24
            time['day'] += 1
            
            if time['day'] > days_in_month[time['month']]:
                time['day'] = 1
                time['month'] += 1

                if time['month'] > 12:
                    time['month'] = 1
                    time['year'] += 1

        return time