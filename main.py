import requests
import smtplib
import time
from datetime import datetime

MY_LAT = 50.349700
MY_LNG = 9.528860
MY_EMAIL = "christian1401.mueller@gmail.com"
MY_PW = "lxfjyessvvxxagmq"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if abs(iss_latitude-MY_LAT) < 5 and abs(iss_longitude-MY_LNG) < 5:
        return True


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

    hour_now = datetime.now().hour
    if hour_now >= sunset or hour_now <= sunrise:
        return True


while True:
    if is_iss_overhead and is_night:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PW)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="christian01.mueller@freenet.de",
                msg="Subject: ISS overhead\n\nLook out, the ISS is right above you!",
            )
    time.sleep(60)
