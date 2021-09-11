# AutoSplitter
For Speedrunning. Allows to split automatically when detecting blackscreen. Works in conjucntion with readily available split tools (LiveSplit, ...).

## How to install: Windows

- Download [Python 3.8](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
- Install Python 3.8. Make sure **"Add Python 3.8 to PATH"** IS ticked!
- Restart your computer
- Run [INSTALL.bat](INSTALL.bat)

### Configure Splits
Because this program works by virtually pressing your Split Key every time a "valid" blackscreen is detected, you somehow have to tell it, which blackscreens are considered "valid".
Internally, the program counts how many blackscreens it encountered so far and only presses the Split Key if the current black screen count is listed in [example.txt](splits_profiles/example.json).
But before you start creating your own splits file, you should give [the split profile archive](https://github.com/chelast55/AutoSplitter/tree/develop/splits_profiles) a visit. There is a certain possibility that someone already submitted a split file for the exact route you're planning to do.
if this is not the case, enter your valid blackscreen count values one per line into a text file in the following format:
```
# this is a comment
1
3
5 # you can also do inline comments
```
This example would cause the program to split at the first, third and fifth blackscreen it encounters, but it will skip any other blackscreens. This should resemble your exact route. Everything in a line after '#' is not read by the program, so you can use '#' to do comments.

## How to use

Make sure that the game you want to "auto split" is clearly visible on any of your screens. It doesn't matter if you play the game on that screen or if you use the preview window of your capture/streaming software (OBS, Game Capture HD, ...) for this purpose. After you start [main.py](main.py) you are greeted with a little window offering you the following options:
- **Select Splits Profile**: Select the split file for your route. You can't start the program if you didn't do this first.
- **Start**: Start the program. While started and not paused, it will monitor the area you selected and automatically press the **Split Key** you selected when detecting a blackscreen. This will change to **Stop** while the program is running.
- **Pause**: Pause the program (same as the **Pause Key**). While paused, the program doesn't check for blackscreens. You can, however, still press buttons. Changes to **Unpause** while paused.
- **Settings**:
  - First of all, you will notice an area that displays a preview of your screen(s). As the instruction on top says, use your mouse to drag a rectangle on the preview window. This rectangle should include the area you want the program to watch for blackscreens. You should choose this as big as possible, but it doesn't have to cover your whole screen. It is recommended that you select your area in a way that excludes random/not predictably occuring events (donation alerts, progress bars, facecam, ...).
  - **Restore Default Settings**: Does exactly what it says. This will **NOT** affect your key bindings. If you hit this button by accident and don't want to lose any of your previous settings, close the *Settings* menu without hitting *OK*.
  - Short note on any of the keys: Hold the key you want to set until the pop-up disappeard and the name of the key is successfully displayed next to the *Set* button.
  - **Split Key**: Press the key you use to split in your preferred splitting tool (LiveSplit, ...)
  - **Pause Key**: Set key to press once to pause and again to unpause the program. While paused, the program does not check for blackscreens.
  - **Reset Key**: Set key for resetting the program. Acts like restarting the program, but without closing and opening it again. It will however **NOT** read in the config again.
  - **Decrement Key**: Press the key you want to use to manually decrement the internal blackscreen counter. This is for occasions like an accidental death that would cause a blackscreen you haven't accounted for when configuring your splits. **Wait for blackscreen to fully disappear** before pressing!
  - **Increment Key**: Same as Decrement Key, but the blackscreen counter gets incremented instead. Well, there's currently no cases where that's useful or important ;)
  - **Automatic Blackscreen Threshold**: If you *really* don't care about what this "Blackscreen Threshold"-thing is, just click this button to enter *automatic mode*, select your preview area, wait for a blackscreen to occur, disable *automatic mode* again and you're good to go!
  - **Blackscreen Threshold**: The program detects blackscreens by taking a screenshot of the area you selected, converting it to greyscale and calculating the average grey value (value between 0 and 255, 0 is pure black and 255 pure white). What you recognize as black might not actually be black (i. e. grey value of 0), so this value should match the average grey value your selected area becomes when a "blackscreen" occurs. Don't set this too high, it could lead to the program detecting a blackscreen when in actuality the colors are only fairly dark at a certain moment in the game. If you need assistance for deciding on the perfect threshold value to fit your needs, the average grey value of the area you selected is displayed below the preview. The threshold you choose should at least be as high as this value and preferrably a bit higher. Again: If you don't care, just use the *automatic mode*, it is highly likely that this will work for you.
  - **After Split Delay**: The program checks the selected area multiple times per second for a blackscreen. You should set this delay long enough (in seconds) to cover at least the entire duration of a blackscreen to prevent it from splitting multiple times at a single blackscreen.
  - **Advanced Settings**: If you don't know, what you're doing, ignore this option. It is unlikely, you will break anything, but it is highly likely that everything works fine for you without touching anything here. If, however, you do want to know more about this, you will find what you're looking  for in [advanced.md](advanced.md).
- On the left side, you can see the current status of the program (stopped, running, paused).
- On the right side, while the program is running, you can see the current blackscreen count and the number of blackscreens required for the next split to happen (this follows the split file you selected, which is also displayed below).

## Contribution

### Splits File Submissions
TODO: figure this out somehow

### Source Code
If, for whatever reason, you ever felt the urge to contribute to the code side of this project, feel free to send pull requests. If you execute [update_docs.bat](update_docs.bat), an up-to-date version of the documentation should open in your default browser. Please remember to annotate everything you add to the code to allow the documentation to stay up-to-date.