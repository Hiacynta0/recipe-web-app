from datetime import datetime, date

today = datetime.today()
end_of_year = datetime(today.year, 12, 31)

days = end_of_year - today

print('Days: {}\nDays, hours, minutes...: {}'.format(days.days, days))