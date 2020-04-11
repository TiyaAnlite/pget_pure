# pget_pure
***本插件遵循 GNU-3.0 通用公共许可证***

支持[MCDReforged](https://github.com/Fallen-Breath/MCDReforged)的一款插件下载助手

无需借助外部指令，显示更加友好的pget插件，支持独立白名单配置

------

## 指令：

!!pget2 [URL] 下载指定插件

## 配置文件：

***位于`plugins/config/pget2_whitelist.json`***

| 属性          | 释义                           |
| ------------- | ------------------------------ |
| use_whitelist | 开关独立白名单功能(true/false) |
| whitelist     | 存放白名单中的玩家名           |

## 注意事项：

插件不会为你检查链接内的文件是否为合法的Python文件或者MCDR插件

部分特殊的链接(无文件名后缀或者headers中没有Content-Disposition)的文件名可能会无法正常解析，在此情景下建议手动修改至正确文件名