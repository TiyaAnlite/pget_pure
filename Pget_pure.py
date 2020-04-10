import os
import re
import time
import json
import requests
from urllib.parse import unquote

Prefix = '!!pget2'
PluginName = 'Pget_pure'
chunk_size = 5
config_dir = os.path.join(PluginName, "whitelist.json")

helpmsg = '''------MCD pget pure插件------
!!pget2 [URL] -下载这个插件
--------------------------------'''


def download(link, server):
    server.replay(f"[{PluginName}]正在尝试连接")
    try:
        file = requests.get(link, stream=True)
    except requests.exceptions.ConnectTimeout:
        server.replay(f"[{PluginName}]错误：连接超时")
        return
    except requests.exceptions.ConnectionError:
        server.replay(f"[{PluginName}]错误：连接失败")
        return

    length = round(int(file.headers['Content-Length']), 1)
    if "Content-Disposition" in file.headers:
        filename = unquote(re.findall(r'filename= (.+)', file.headers["Content-Disposition"])[0])
    else:
        filename = os.path.basename(link)
    server.replay(f"[{PluginName}]正在下载 {filename} ({length}KB)")
    l_down_size = 0
    down_size = 0
    last_time = int(time.time())
    with open(f"{filename}.tmp", "wb") as fp:
        for chunk in file.iter_content(chunk_size=chunk_size):
            fp.write(chunk)
            down_size += len(chunk)
            u_time = int(time.time()) - last_time
            if u_time >= 1:
                server.replay(
                    f"[{PluginName}]{filename} : {down_size}/{length} ({round((down_size - l_down_size) / u_time / 1024, 2)}KB/s)")
                l_down_size += down_size
                down_size = 0
                last_time = int(time.time())
    os.rename(f"{filename}.tmp", filename)
    server.replay(f"[{PluginName}]{filename} 下载完成")


def check_player(config, player, server):
    flag = False
    for p in config["whitelist"]:
        if p == player:
            flag = True
    if not flag:
        server.replay(f"[{PluginName}]你在白名单中没有权限")
    return flag


def on_load(server, old_module):
    # check something...
    if not os.path.isfile(config_dir):
        server.replay(f"[{PluginName}]错误：没有找到白名单配置文件 {config_dir}")


def on_info(server, info):
    if info.is_player and info.content.startswith('!!pget2'):
        if os.path.isfile(config_dir):
            with open(config_dir) as handle:
                config = json.load(handle)
            if not config["use_whitelist"] or config["use_whitelist"] and check_player(config, info.player, server):
                args = info.content.split(' ')
                if len(args) == 1:
                    for line in helpmsg.splitlines():
                        server.replay(line)
                elif len(args) == 2:
                    download(args[1], server)
                else:
                    server.replay(f"[{PluginName}]输入的参数有误")
        else:
            server.replay(f"[{PluginName}]错误：没有找到白名单配置文件 {config_dir}")
