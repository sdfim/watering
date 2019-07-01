import RPi.GPIO as GPIO
import sys


def off_relay(inputgpio):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(inputgpio,GPIO.OUT)

    state = GPIO.input(inputgpio)
    print("state = ", state)
    GPIO.output(inputgpio,GPIO.HIGH)
    GPIO.cleanup()

    if state == 1:
        GPIO.cleanup()


def on_relay(inputgpio):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(inputgpio,GPIO.OUT)
    GPIO.output(inputgpio,GPIO.LOW)



def status_relay(inputgpio):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(inputgpio,GPIO.OUT)
    state = GPIO.input(inputgpio)

    if state == 1:
        GPIO.cleanup()
    return state
