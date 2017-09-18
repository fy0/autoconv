# autoconv

自动音频转换工具

### 要求

Python 3.4+

依赖库 watchdog

```bash
pip3 install watchdog
python3 autoconv.py
```


### 预设用法

http://www.opus-codec.org/downloads/

下载 `opus-tools`，并将 `opusenc.exe` 丢在 `autoconv.py` 同目录

将音频文件(".wav", ".aiff", ".flac", ".ogg")放在 input 目录下或 input 的子目录

autoconv 会自动调用编码器将文件转换保存至 output 目录的对应路径。

子目录 48 96 192 384 500 代表 5 档不同的码率。

input 根目录的码率是192

举例：放入 `input/music.wav`，稍后将得到 `output/music.opus`


### 自定义

编辑 config.json 填写参数

在 types 中定义不同的子项，自动对应到 input/{配置名} 这一目录

```javascript
{
    "global": {
        "encoder": "opusenc.exe",
        "input_dir": "input",
        "output_dir": "output",
        "watch_ext": [".wav", ".aiff", ".flac", ".ogg"],
        "output_ext": ".opus"
    },
    "types": {
        "48": {
            "--bitrate": "48",
            "--vbr": ""
        },
        "96": {
            "--bitrate": "96",
            "--vbr": ""
        },
        "192": {
            "--bitrate": "192",
            "--vbr": ""
        },
        "384": {
            "--bitrate": "384",
            "--vbr": ""
        },
        "500": {
            "--bitrate": "500",
            "--vbr": ""
        },
        "": {
            "--bitrate": "192",
            "--vbr": ""            
        }
    }
}
```

看着改就行。
