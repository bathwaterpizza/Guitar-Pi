# Guitar-Pi
A music rhythm game designed to run on the Raspberry Pi 3 embedded in a guitar with sensors, which act as a controller. Final project for my Programming I (INF1034) class at PUC-Rio.

This is a simple game written using pygame 2.5, with several optimizations to run smoothly on the RPi3, and a modular code structure which allows it to be easily further developed. Supports keyboard input (Z X C V) if you want to run it on PC, simply change GAME_USEKEYBOARDINPUT to True in the cfg file. Game window looks like this:

![python_nhUKFpYuxH](https://github.com/bathwaterpizza/Guitar-Pi/assets/8276713/d497403f-9944-4fa6-b0a1-28a24a843353)

For hardware, I use four TTP223 touch sensors, a HW-504 analog joystick which acts as the strum bar, and an Arduino Nano as an analog-to-digital converter, since the RPi has no analog inputs. All connected to the RPi's GPIO using jumper wires on a breadboard, which is zip-tied to a toy guitar, as shown below:

![20230629_083859](https://github.com/bathwaterpizza/Guitar-Pi/assets/8276713/f441ae5b-05f6-4b98-9e3f-44f4fb5df9dc)
