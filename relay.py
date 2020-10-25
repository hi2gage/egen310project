import RPi.GPIO as GPIO
import time

channel = 4

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
# GPIO.output(channel, GPIO.HIGH)


def motor_on(pin):
    print("turned on")
    GPIO.output(pin, GPIO.LOW)  # Turn motor on


def motor_off(pin):
    print("turned off")
    GPIO.output(pin, GPIO.HIGH)  # Turn motor off


if __name__ == '__main__':
    try:
        motor_on(channel)
        time.sleep(3)
        motor_off(channel)
        time.sleep(1)

        motor_on(channel)
        time.sleep(3)
        motor_off(channel)
        time.sleep(1)

        GPIO.cleanup()
    except KeyboardInterrupt:
        GPIO.cleanup()


