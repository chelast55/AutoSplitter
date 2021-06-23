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

# Configure Splits
Because this program works by virtually pressing your Split Key every time a "valid" blackscreen is detected, you somehow have to tell it, which blackscreens are considered "valid".
Internally, the program counts how many blackscreens it encountered so far and only presses the Split Key if the current black screen count is listed in [splits.txt](splits.txt).
Enter your valid blackscreen count values one per line into [splits.txt](splits.txt) like this:
```
1
3
5
```
This example would cause the program to split at the first, third and fifth blackscreen it encounters, but it will skip any other blackscreens.
