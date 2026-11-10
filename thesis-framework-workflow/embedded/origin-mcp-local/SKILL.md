---
name: origin-mcp-local
description: 探测当前主机可用的 Origin MCP，或使用包内 EditaPlot 隔离自动化路线。
---

# Origin 桥接与可迁移入口

触发词: “连接 Origin”, “Origin MCP”, “Origin 桥接”。

不假定服务已安装，不沿用其他电脑的配置或路径。先枚举当前会话可调用的 Origin 工具，按其文档执行只读状态探测。没有桥接时，使用本包 [EditaPlot](../editaplot/SKILL.md) 与 [独立使用说明](../../references/portability.md)，不要求获得原作者机器的文件或历史会话。

MCP 不是完成制图的必要依赖。Origin 原生输出需要本机 Windows 和 Origin，软件兼容范围以实际握手、输出和回开检查为准。不自动修改 DCOM、注册表或全局依赖，不重置或关闭用户已有实例。需要配置新服务时先取得当前主机实际可用的安装目录，按用户授权范围操作。
