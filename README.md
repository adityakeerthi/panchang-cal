# PanchangCal
Generating a calendar of all the notable events with respect to [Panchangam](https://en.wikipedia.org/wiki/Panchangam). 

## Why
Current Panchang needs to be read by astrologers who have a deep understanding of Hindu astrology. This software offers an easier method of consultation by scraping known times ([mypanchang](https://mypanchang.com/)) and displaying them in a calendar (Google Calendar, iCal, etc). I also think it helps people who have very limited knowledge when it comes to Hindu astrology (like me) to determine auspicious and inauspicious times.

## Todo
- [x] Scrape [mypanchang](https://mypanchang.com/) and parse data
- [x] Handle invalid times (e.g. 25:05:23)
- [ ] Generate a web-client for custom configurations 
- [ ] Color-code the almanac to indicate good/bad times
- [ ] Visualize calendar instead of using Google or Apple client

## Stack
- Python