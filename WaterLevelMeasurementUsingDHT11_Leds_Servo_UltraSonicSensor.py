# Water level measurement project using python. An ultrasonic sensor is placed over the water, when it reads that
# water level is below 30%, a red led lights up and servo is set to max indicating that a water valve will open to
# pour big quantity of water. When it reads that water level is over 30% and below 60%, a yellow led lights up
# and servo is set to mid indicating that a water valve will open to pour some water but not a great quantity.
# When it reads that water level is over 60%, a green led lights up and servo is set to detach indicating that
# the water valve will stop pouring water, until it reads another reading. Also there's a function
# "measure_temperature_humidity()" that uses the DHT sensor to read temperature and humidity and put them in a csv
# file along with the time of the reading and the water percentage.

from gpiozero import DistanceSensor, LED, Servo
import Adafruit_DHT
import time
import csv

red_led = LED(27)
yellow_led = LED(22)
green_led = LED(4)

distance_sensor = DistanceSensor(echo=24, trigger=23)
servo = Servo(25)

csv_filename = "water_level.csv"
csv_columns = ["Time", "Percentage", "Temp"]


def measure_temperature_humidity():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 26)
    return humidity, temperature


def calculate_percentage(distance):
    min_distance = 7
    max_distance = 2

    percentage = 100 - ((distance - max_distance) /
                        (min_distance - max_distance)) * 100
    percentage = max(0, min(100, percentage))
    return percentage


try:
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
        csv_writer.writeheader()

        while True:
            distance = distance_sensor.distance * 100
            humidity, temperature = measure_temperature_humidity()
            percentage = calculate_percentage(distance)

            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            csv_writer.writerow(
                {"Time": current_time, "Percentage": percentage, "Temp": temperature})

            if percentage < 30:
                red_led.on()
                yellow_led.off()
                green_led.off()
                servo.max()
            elif 30 < percentage < 60:
                red_led.off()
                yellow_led.on()
                green_led.off()
                servo.mid()
            else:
                red_led.off()
                yellow_led.off()
                green_led.on()
                servo.detach()

            time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
