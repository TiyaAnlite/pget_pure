# pget_pure
[![Latest release](https://img.shields.io/github/release/MCDReforged-Plugins/pget_pure.svg)](https://github.com/MCDReforged-Plugins/pget_pure/releases/latest)

![License](https://img.shields.io/github/license/MCDReforged-Plugins/pget_pure.svg)

支持[MCDReforged](https://github.com/Fallen-Breath/MCDReforged)的一款插件下载助手

无需借助外部指令，显示更加友好的pget插件，支持独立白名单配置

------

## 指令：

!!pget2 [URL] 下载指定插件

## 权限

默认玩家需要至少权限等级为2(Helper)才能访问该命令
> 你可以在`Pget_pure.py:16`处修改`MinimumPermissionLevel`最低玩家所需权限

开启白名单时以白名单为准(默认关闭)

## 配置文件：

***位于`plugins/config/pget2_whitelist.json`***

| 属性          | 释义                           |
| ------------- | ------------------------------ |
| use_whitelist | 开关独立白名单功能(true/false) |
| whitelist     | 存放白名单中的玩家名           |

## 注意事项：

插件不会为你检查链接内的文件是否为合法的Python文件或者MCDR插件

部分特殊的链接(无文件名后缀或者headers中没有Content-Disposition)的文件名可能会无法正常解析，在此情景下建议手动修改至正确文件名
