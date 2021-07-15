**NOTE:** If you're just looking for instructions on how to use this program, take a look at [README.md](README.md). If you do, however, want more in-depth information about this program and its advanced features, this is the right place.

## Advanced Settings
These are accessible by ticking the "Show Advanced Settings" box in the Settings menu.
- Settings:
    - **Max Capture Rate**: Maximum amount of screenshots for evaluation (looking for blackscreens) taken per second. If you experience issues with this program causing lag or have any other reason to limit the capture rate, feel free to do so. However, **don't forget that this is a maximum**, so there's no guarantee that this capture rate will actually be reached or even is realistically reachable (actual capture rate will likely be between 20-30 times per second).
    - **After Key Press Delay**: Delay after successful key press that has to pass to trigger the same key again (even when holding it down). This exists to prevent multiple registartions within the same key press and will most likely be helpful in stressful (in-run) situations.  If you should (for some reason) feel the urge to mash any of the hotkeys, feel free to lower this setting down to 0.
    - **Automatic Threshold Overhead**: This value is added onto the current average gray value while *automatic threshold detection* is active. This is done reduce impact of small fluctuations. There might, however, be no cases where it's useful or important to change this value since it's highly likely, that you will set the *blackscreen threshold* manually anyway if you care enough to read this.
    
## Structure of config.cfg
The config.cfg file is generated automatically in the main directory of the program as soon as you press *OK* in the *Settings* menu.
Its structure follows the order the settings appear in the *Settings* menu:
```
[float, float, float, float]:   corner coordinates of evaluated area
str:    string representation of split key
str:    string representation of pause key
str:    string representation of reset key
str:    string representation of decrement key
str:    string representation of increment key
float:  blackscreen threshold
float:  after split delay (s)
int:    max capture rate (1/s)
float:  after key press delay (s)
float:  automatic threshold overhead (s)
str:    file path to splits file
<empty line at end of file>
```
Additional notes on the structure:
- The corner coordinates are layed out as follows: (*x1*, *y1*, *x2*, *y2*) with the first two values / the first coordinate always being the top left of the rectangle and the second being the lower right.
- string representations of keys are either "'*x*'" (with *x* being alphanumeric character) for alphanumeric keys, "<Key.*X*: <*n*>>" (with *X* being a unique identifier of a function key and *n* being the numeric index of the same key) for function keys (e. g. CTRL, ALT, DELETE, ...) or "<*n*>" (with *n* being the numeric index of a key) for non-standard keys that send unique scan codes (e. g. extra keys on IBM 122-key terminal keyboards that are NOT F13-F24). The string representation of a key funktion that wasn't mapped yet is "None".
- the value for any of the settings of type float are actually of type int, at least when obtained via the *Settings* menu. It does, however, work with any *float* value.
- the upper shpould also hold true for *Max Capture Rate*, but it is recommended to stick with integer values 
- file path should (obviously) be either a valid path to a valid splits file following the layout described in [README.md](README.md) or an empty line. In the second case, not having a blank line at the end will keep the program from starting.
- **DON'T** try to change anything about the structure of config.cfg (no, comments are not supported) and expect it to still work. If you do anyway and mess up the program by that, just delete your current config.cfg before you try to start the program again. 