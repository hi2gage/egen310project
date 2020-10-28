import water
import RPi.GPIO as GPIO
import time
import smbus
import statistics as stat
import datetime


GPIO.setmode(GPIO.BOARD)
address = 0x48
cmd = 0x40
bus = smbus.SMBus(1)


def pump_on(pin):
    print("turned on")
    GPIO.output(pin, GPIO.LOW)  # Turn motor on


def pump_off(pin):
    print("turned off")
    GPIO.output(pin, GPIO.HIGH)  # Turn motor off


def analog_read(chn):   # read ADC value,chn:0,1,2,3
    value = bus.read_byte_data(address, cmd+chn)
    return value


def read_sensor(trans_pin, sensor_pin):
    # Setting up GPIOs
    data = []
    GPIO.setup(trans_pin, GPIO.OUT)
    GPIO.setup(sensor_pin, GPIO.IN)

    # Data Collection is started
    print("Data Collection is starting")

    # Collects data and averages it
    GPIO.output(trans_pin, GPIO.HIGH)
    time.sleep(1)
    analog_read(0)
    analog_read(0)
    for point in range(0, 50):
        data.append(analog_read(0))
        # time.sleep(0.01)

    print("average = " + str(stat.mean(data)))
    GPIO.output(trans_pin, GPIO.LOW)
    GPIO.output(trans_pin, GPIO.LOW)
    return stat.mean(data)


def is_it_time_yet():
    current_time = datetime.datetime.now()
    year, month, day, hour, min, sec = map(int, time.strftime("%Y %m %d %H %M %S").split())
    # print(str(hour) + " " + str(min))
    return hour == 8 or hour == 20 and min == 7 and sec < 30


def main():
    try:
        pump_pin = 7
        sensor_pin = 33
        trans_pin = 37

        GPIO.setup(pump_pin, GPIO.OUT)
        GPIO.output(pump_pin, GPIO.HIGH)

        while True:
            if is_it_time_yet():
                print("hey")
                data = read_sensor(trans_pin, sensor_pin)

                if data > 100:
                    pump_on(pump_pin)
                    time.sleep(3)
                    pump_off(pump_pin)
                    time.sleep(1)
                time.sleep(60)

    except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup()  # cleanup all GPI


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # the input arguments will determine at what hour the plant will be watered
    main()
