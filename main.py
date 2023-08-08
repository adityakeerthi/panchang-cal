from PanchangCal import PanchangCal

def main():
   cal = PanchangCal('Panchang.ics')
   cal.loop(2023)
   cal.writeCal()

if __name__ == "__main__":
   main()