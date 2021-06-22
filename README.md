# AutoSplitter
For Speedrunning, allows to split automatically when detecting blackscreen

# How to install: Windows

- Download python 3.8 (https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe)
- Install Python 3.8. Make sure **"Add Python 3.8 to PATH"** IS ticked!
- Open Windows Command Line (Windows+R or Start Menu, enter "cmd")
- Enter "py -help". If this does nothing, try restarting
- Install necessary packages by executing the following lines one after another:
```
python -m pip install –-upgrade pip
py -m pip install -U setuptools wheel
py -m pip install -U numpy opencv-python pynput pillow python-time
```
- Start autosplit.py
- You can stop with CTRL+C while console is active
