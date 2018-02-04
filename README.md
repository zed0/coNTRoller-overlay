# coNTRoller-overlay
Display 3DS controller inputs via NTR debugging information

## Getting started

```bash
git submodule update --init --recursive
pip install -r requirements.txt

#Find the local IP of your 3DS and replace it below
./coNTRoller-overlay.py 192.168.0.100
```

## Example output

![example](https://raw.githubusercontent.com/zed0/coNTRoller-overlay/master/example.png)

## Credits

- [zed0](https://github.com/zed0)
- [RhiannonMichelmore](https://github.com/RhiannonMichelmore) - Help locating memory offsets
- [imthe666st](https://github.com/imthe666st) - [PyNTR](https://github.com/imthe666st/PyNTR)
