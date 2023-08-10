from PanchangCal import PanchangCal

def main():
   cal = PanchangCal('Panchang 1.0.ics')

   for year in cal.getValidYears():
      cal.run(year)

   cal.writeCal()

if __name__ == "__main__":
   main()