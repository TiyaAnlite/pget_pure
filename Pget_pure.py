import os
import re
import time
import json
import requests
from urllib.parse import unquote

Prefix = '!!pget2'
PluginName = 'Pget_pure'
chunk_size = 8
config_dir = os.path.join("plugins", "config", "pget2_whitelist.json")

helpmsg = '''------MCDR pget pure------
!!pget2 [URL] -下载指定插件
--------------------------------'''


def download(link, server, info):
    server.reply(info, f"[{PluginName}] 正在尝试连接")
    try:
        file = requests.get(link, stream=True, timeout=(10, 27))

        length = round(int(file.headers['Content-Length']) / 1024, 2)
        if "Content-Disposition" in file.headers:
            filename = re.findall(r'filename=(.+)', file.headers["Content-Disposition"])
            if filename:
                print("!!!")
                filename = unquote(filename[0])
                if filename.startswith(" "):
                    filename = filename[1:]
            else:
                filename = os.path.basename(link)
        else:
            filename = os.path.basename(link)
        file_path = os.path.join('plugins', filename)
        server.reply(info, f"[{PluginName}] 正在下载 §b{filename} §6({length}KB)")
        start_time = int(time.time())
        down_size = 0
        with open(f"{file_path}.tmp", "wb") as fp:
            for chunk in file.iter_content(chunk_size=chunk_size):
                now_time = int(time.time())
                fp.write(chunk)
                down_size += len(chunk)
                u_time = now_time - start_time
                # 若下载时间过长，间隔5秒报告一次
                if u_time >= 5:
                    server.reply(
                        f"[{PluginName} Downloading §b{filename} §6{round(down_size / 1024, 2)}KB ({round(down_size / 1024 / u_time, 2)}KB/s)]")
                    start_time = int(time.time())
                    down_size = 0
    except requests.exceptions.ConnectTimeout:
        server.reply(info, f"[{PluginName}] §c错误：连接超时")
        return
    except requests.exceptions.ConnectionError:
        server.reply(info, f"[{PluginName}] §c错误：连接失败")
        return

    if os.path.isfile(file_path):
        server.reply(info, f"[{PluginName}] §c警告：发现旧文件已存在，将会被覆盖")
        os.remove(file_path)
    os.rename(f"{file_path}.tmp", file_path)
    server.reply(info, f"[{PluginName}] §b{filename} 下载完成")
    if info.is_player:
        msg = {
            "text": "§b在MCDR重载插件，请输入或§a点击这条消息§b来重载",
            "clickEvent": {
                "action": "run_command",
                "value": "!!MCDR reload plugin"
            },
            "hoverEvent": {
                "action": "show_text",
                "value": "点击重载"
            }
        }
        server.execute(f"tellraw {info.player} {json.dumps(msg)}")


def check_player(config, player, server, info):
    flag = False
    for p in config["whitelist"]:
        if p == player:
            flag = True
    if not flag:
        server.reply(info, f"[{PluginName}] §c你在白名单中没有权限")
    return flag


def on_load(server, old_module):
    # check something...
    server.add_help_message("!!pget2", "简易插件下载助手")
    if not os.path.isdir(os.path.join("plugins", "config")):
        os.mkdir(os.path.join("plugins", "config"))
        server.say(f"[{PluginName}]make config dir")
    if not os.path.isfile(config_dir):
        server.say(f"[{PluginName}] §f没有找到白名单配置文件，正在自动创建 §b{config_dir}")
        config = {"use_whitelist": False, "whitelist": []}
        with open(config_dir, "w") as fp:
            json.dump(config, fp, indent=4)


def on_info(server, info):
    if info.is_player and info.content.startswith('!!pget2'):
        if os.path.isfile(config_dir):
            with open(config_dir) as handle:
                config = json.load(handle)
            if not config["use_whitelist"] or config["use_whitelist"] and check_player(config, info.player, server,
                                                                                       info):
                args = info.content.split(' ')
                if len(args) == 1:
                    for line in helpmsg.splitlines():
                        server.reply(info, line)
                elif len(args) == 2:
                    download(args[1], server, info)
                else:
                    server.reply(info, f"[{PluginName}] §c输入的参数有误")
        else:
            server.reply(info, f"[{PluginName}] §c错误：没有找到白名单配置文件 {config_dir}")
