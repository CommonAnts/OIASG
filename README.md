# OIASG
An OIer's Adventure-Strategy Game Engine

OIASG is an light,simple and naive game engine for adventure-strategy games with events(and can be used for plots),tech trees and exams.

The engine users works with python and APIs in a subnamespace of the game.

It also has a default GUI and basic OI strategy systems for the certain game project:"OI Diary"(a temporary call).

## about development

OIASG is based on python 3 and [pyglet](http://pyglet.org/).

We use modified(mainly debugging) pyglet 1.3.1 for windows.You can get the modifications form `/pyglet`.

**The game is chiefly for Windows 10,so it may not work well on other platforms(but this is not normal).**

**Note that pyglet uses AVBin to decode medias.**

## How to run OIASG

1. install Python 3(>=3.6.3)

2. install pyglet for python3(>=1.4.0a1)

3. if you are using Windows OS(especially Windows 10),cover pyglet library directory(usually at `C:\Users\<Your User Name>\AppData\Local\Programs\Python\Python36\Lib\site-packages\pyglet`) with `/pyglet`.

4. install FFmpeg(>=3.4.2,"shared" version(including libs))

5. clone files from `/oiasg`.

6. run `/oiasg/main.py` to start.
