import schedule
import time
import datetime

def minute():
    currentTime = datetime.datetime.now().replace(microsecond=0)
    print(str(currentTime) + "This is printed every minute")

schedule.every(1).minute.do(minute)

while True:
    schedule.run_pending()
    time.sleep(1)
