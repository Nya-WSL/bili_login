通过B站web端扫码登录接口获取Cookie信息

### Data

- SESSDATA
- bili_jct
- DedeUserID
- DedeUserID__ckMd5
- sid
- buvid3

### Build

```
# need python >= 3.8, dev on python 3.13.5

# use nuitka

uv sync
uv run build.py

# use pyinstaller

uv add pyinstaller
uv run pyinstaller -F main.py --icon logo.ico --windows
```