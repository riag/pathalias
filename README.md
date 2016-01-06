# pathalias
Wox 启动器的插件, 用于快速打开文件夹。把常用的文件夹路径定义一个短名字，在Wox启动器里输入该短名字就可以打开该文件夹, 例子:

![screenshot: `pa open`](img/preview.png)

## 用法
* `pa open 文件夹短名字` 就能打开文件夹
* `pa editconfig` 使用默认的编辑器打开用户配置文件


## 配置
默认定义了几个文件夹路径, 见 `data.json`, 支持使用环境变量

```
"woxhome": "${WOX_HOME}",
"~": "$USERPROFILE",
"home": "$USERPROFILE",
"sys32": "${windir}\\System32",
"programfiles": "$ProgramFiles"
```

### 用户配置
配置文件 `config.json` 配置项如下

```

# 用户自定义的常用文件夹配置文件路径，格式如 `data.json`
"data_path": "",

# 打开文件夹的命令，如果为空，默认值为 `explorer %s`
"open_folder_cmd": ""

```
