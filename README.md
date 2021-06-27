# AutoSplitter
For Speedrunning, allows to split automatically when detecting blackscreen

## How to install: Windows

- Download python 3.8 (https://www.python.org/ftp/python/3.8.0/python-3.8.0-amd64.exe)
- Install Python 3.8. Make sure **"Add Python 3.8 to PATH"** IS ticked!
- Open Windows Command Line (Windows+R or Start Menu, enter "cmd")
- Enter "py -help". If this does nothing, try restarting
- Install necessary packages by executing the following lines **one after another**:
```
python -m pip install –-upgrade pip
py -m pip install -U setuptools wheel
py -m pip install -U numpy opencv-python pynput pillow python-time
```

### Configure Splits
Because this program works by virtually pressing your Split Key every time a "valid" blackscreen is detected, you somehow have to tell it, which blackscreens are considered "valid".
Internally, the program counts how many blackscreens it encountered so far and only presses the Split Key if the current black screen count is listed in [splits.txt](splits.txt).
Enter your valid blackscreen count values one per line into [splits.txt](splits.txt) like this:
```
# this is a comment
1
3
5 # you can also do inline comments
```
This example would cause the program to split at the first, third and fifth blackscreen it encounters, but it will skip any other blackscreens. This should resemble your exact route. Everything in a line after '#' is not read by the program, so you can use '#' to do comments.

## How to use

Make sure that the game you want to "auto split" is clearly visible on you **primary screen** (known issue for Windows, not tested on other OS yet). It doesn't matter of you play the game on that screen or if you use the preview window of your capture/streaming software (OBS, Game Capture HD, ...) for this purpose.

- Start [autosplit.py](autosplit.py)
- On first start you are asked to give certain inputs to configure the program
  - **Split Key**: Press the key you use to split in your preferred splitting tool (LiveSplit, ...)
  - **Decrement Key**: Press the key you want to use to manually decrement the internal blackscreen counter. This is for occasions like an accidental death that would cause a blackscreen you haven't accounted for when configuring your splits in [splits.txt](splits.txt). **Wait for blackscreen to fully disappear** before pressing!
  - **Increment Key**: Same as Dekrement Key, but the blackscreen counter gets incremented instead. Well, there's currently no cases where that's useful or important ;)
  - **Reset Key**: Set key for resetting the program. Acts like restarting the program, but without closing and opening it again. It will however **NOT** read in the config again.
  - **Pause Key**: Set key to press once to pause and again to unpause the program. While paused, the program does not look for blackscreens.
  - **Video Preview Coordinates**: Select the area you want to monitor for blackscreen by clicking 2 points on your screen. These points act as corners of a rectangle and the rectangle they form is monitored. 
  - **Blackscreen Threshold**: The program detects blackscreens by taking a screenshots of the area you selected, converting it to greyscale and calculating the average grey value (value between 0 and 255, 0 is pure black and 255 pure white). What you recognize as black mightt nott actually be black (i. e. grey value of 0), so this value should match the average grey value your selected area becomes when a "blackscreen" occurs. Don't set this too high, it could lead to the program detecting a blackscreen when in actuality the colors are only fairly dark at a certain moment in the game. For now, you can remove the "# " efore the second to last "print"-statement in [autosplit.py](autosplit.py) to monitor the average grey value in your selected area. There will likely be a better way in a future version of this program.
  - **After Split Delay**: The program checks the selected area multiple times per second for a blackscreen. You should set this delay long enough (in seconds) to cover at least the entire duration of a blackscreen to prevent it from splitting multiple times at a single blackscreen.
- At the end of the setup, you can enter "yes" if you don't want to redo this setup process the next time you start the program (your inputs are saved in [config.cfg](config.cfg), if you disabled the setup, but want to redo it anyway, change the first line of [config.cfg](config.cfg) from "False" to "True")
- You can stop the program with CTRL+C while the console window is active or by just closing the window

## The Archive
This is supposed to become a place where split files of various speedrun routes could be stored