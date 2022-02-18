import requests
from datetime import datetime
import math
import time
import smtplib
from privates import *

# These come from privates.py
MY_LAT = MY_LAT
MY_LONG = MY_LONG

MY_EMAIL = MY_EMAIL
PASSWORD = PASSWORD
MY_MAIN_EMAIL = MY_MAIN_EMAIL
#

def is_night(sunrise_hour, sunset_hour, time_now):
    if int(time_now.hour) < sunrise_hour or int(time_now.hour) > sunset_hour:
        return True
    else:
        return False

def is_near(latitude,longitude,MY_LAT,MY_LONG):
    if math.isclose(latitude, MY_LAT, abs_tol=5):
        if math.isclose(longitude,MY_LONG,abs_tol=5):
            return True
        else:
            return False
    else:
        return False

while True:
    #TIME
    time_now = datetime.now()

    #ISS Info

    iss_response = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()
    iss_data = iss_response.json()
    iss_timestamp = datetime.fromtimestamp(iss_data["timestamp"])
    latitude = float(iss_data["iss_position"]["latitude"])
    longitude = float(iss_data["iss_position"]["longitude"])
    iss_position = (latitude, longitude)
    print(iss_position)

    parameteres = {
        "lat": MY_LAT,
        "long": MY_LONG,
        "formatted": 0
    }

    #sun position
    sunpos_response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameteres)
    sunpos_response.raise_for_status()
    sunpos_data = sunpos_response.json()
    sunrise_hour = int(sunpos_data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset_hour = int(sunpos_data["results"]["sunset"].split("T")[1].split(":")[0])


    if is_night(sunrise_hour, sunset_hour, time_now):
        print("It's Night!")
        if is_near(latitude,longitude,MY_LAT,MY_LONG):
            print("The ISS should be visible")
            connection = smtplib.SMTP("outlook.live.com")
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=my_main_email, msg=f"Subject:Look up!\n\nThe ISS should be visible above.")
            connection.close()
            print("Email sent, pausing for 10 hours.")
            time.sleep(600)
        else:
            print("The ISS isn't visible")
            time.sleep(60)

    else:
        print("It's day")
        time.sleep(60)



