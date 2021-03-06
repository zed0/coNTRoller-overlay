# coNTRoller-overlay
Display 3DS controller inputs via NTR debugging information

## Getting started

Clone the repository via git (as the .zip doesn't include submodules) then navigate to the root of the repository and run:
```bash
git submodule update --init --recursive
pip install -r requirements.txt

#Find the local IP of your 3DS and replace it below
python coNTRoller-overlay.py 192.168.0.100
```

## Example output

![example](https://raw.githubusercontent.com/zed0/coNTRoller-overlay/master/example.png)

## Building a standalone executable

Once the software is working a standalone executable with assets bundled can be built using the following:
```bash
pip install pyinstaller
pyinstaller coNTRoller-overlay.spec
```

This will place a standalone executable in the `dist` directory.

## Todo list

- Display where the touchscreen is being touched
- Display extra buttons on the New 3DS
- Theming?

## Credits

- [zed0](https://github.com/zed0)
- [RhiannonMichelmore](https://github.com/RhiannonMichelmore) - Help locating memory offsets
- [imthe666st](https://github.com/imthe666st) - [PyNTR](https://github.com/imthe666st/PyNTR)
