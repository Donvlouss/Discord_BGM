# BGM kun
A bot which can play music and image when someone entered a voice channel.

## Installation
```
pip install discord youtube_dl
```
Install [FFmpeg](https://www.ffmpeg.org/)

## Confiuraion
1. Input **GUILD ID**, **CHANNEL ID**, **Path of FFmpeg** and **BOT TOKEN** in bgm_bot.<br />
  **Guild ID** and **Channel ID** is the text channel. <br />Bot will log someone enter a voice channel and show a image if has.
2. Run bgm_bot, then the config file will be generated.


# Usage
## Add user
1. You can directly edit config.json.<br />Data format is below.<br />
Add a new user, then add a new block.
```
" < Client ID > " :{ 
        "bgm" : "< File name or Youtube Link : str>,"
        "time": " <sec: int> ", # suggest 10 sec
        "img" : " < File Name: str > "
    }
```
2. Use command in discrod.<br />
```
    !add_user USER_ID BGM TIME
``` 
3. When any changes to config, run this command in discord to update.
```
!update_context
```

Currently, image could be added by editing config only.<br /><br />


