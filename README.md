# Guitar-Pi
A music rhythm game made to run on the Raspberry Pi 3 embedded in a guitar with sensors, which act as a controller. Final project for my Programming I (INF1034) course at PUC-Rio, in collaboration with design student Renato Coutinho, and his final project for Physical and logical interfaces (DSG1412).

This is a simple game written using Pygame 2.5, with several optimizations to run smoothly on the RPi3, and a modular code structure which allows it to be easily further developed. Supports keyboard input (Z X C V) if you want to run it on PC, simply change GAME_USEKEYBOARDINPUT to True in the cfg file. Our game window looks like this:

![python_nhUKFpYuxH](https://github.com/bathwaterpizza/Guitar-Pi/assets/8276713/d497403f-9944-4fa6-b0a1-28a24a843353)


For hardware, we use four TTP223 touch sensors, a HW-504 analog joystick which acts as the strum bar, and an Arduino Nano as an analog-to-digital converter, since the RPi has no analog inputs. All connected to the RPi's GPIO using jumper wires on a breadboard, which is zip-tied to a toy guitar, as shown below:

![20230629_083859](https://github.com/bathwaterpizza/Guitar-Pi/assets/8276713/f441ae5b-05f6-4b98-9e3f-44f4fb5df9dc)


Initial concept drawn on ICAD's whiteboard by game designer Renato:

![renato](https://github.com/bathwaterpizza/Guitar-Pi/assets/8276713/3620133a-545a-40a5-89ea-08e8b1264404)


Playtest by developer Miguel at ICAD laboratory:

https://github.com/bathwaterpizza/Guitar-Pi/assets/8276713/6c61e8f3-2630-41b3-8ae2-56d5df0c5754
