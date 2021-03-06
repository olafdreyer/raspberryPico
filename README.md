# MicroPython Code for the Raspberry Pico

## Introduction
This is a collection of some MicroPython code for the Raspberry Pico. 

## display1602.py 
This provides the basic class LCD that controls a 16x2 LCD display run by a HD44780. It is a slight modification from an equivalent program for the Raspberry Pi. That program can be found here:

https://github.com/brantje/rpi-16x2-lcd

The pins for the LCD display are as follows:

<p align="center">
  <img src="./img/lcdPinout.png" alt="PinOut for the 16x2 display" width="500">
</p>

The program 

**temperature.py**

is an example program that uses the LCD class and the on-board thermometer of the Pico to display the temperature. 

Depending on the wiring some constants in the LCD class need to be adjusted. I have used the following wiring:

<p align="center">
  <img src="./img/lcdWiring.png" alt="Wiring for the 16x2 display" width="800">
</p>


