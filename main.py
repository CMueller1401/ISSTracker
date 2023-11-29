import requests
import smtplib
import time
from datetime import datetime
import os

MY_LAT = float(os.environ["LATITUDE"])
MY_LNG = float(os.environ["LONGITUDE"])
MY_EMAIL = os.environ["FROM_MAIL"]
MY_PW = os.environ["MAIL_PW"]


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    print(iss_latitude, ";", iss_longitude)
    if abs(iss_latitude-MY_LAT) < 5 and abs(iss_longitude-MY_LNG) < 5:
        return True
    else:
        return False


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    print(sunrise)
    print(sunset)

    hour_now = datetime.now().hour
    if hour_now >= sunset or hour_now <= sunrise:
        return True
    else:
        return False


while True:
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PW)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=os.environ["TO_MAIL"],
                msg="Subject: ISS overhead\n\nLook out, the ISS is right above you!",
            )
    time.sleep(60)
