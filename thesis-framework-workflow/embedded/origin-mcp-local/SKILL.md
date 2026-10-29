---
name: origin-mcp-local
description: 通过本机 origin-mcp 服务连接 Origin，检查桥接、导入表格、绘图和导出可编辑 OPJU。适用于调用本地 Origin、配置 Origin MCP，以及与 EditaPlot 配合验证绘图。
---

# 本地 Origin MCP

触发词: "调用本地 Origin", "Origin MCP", "连接 Origin", "Origin 画图", "结合 EditaPlot"

## 本机安装

- 源码：`C:/Users/zwzhu/.local/share/origin-mcp/origin-mcp-main`
- 独立 Python：`C:/Users/zwzhu/.local/share/origin-mcp/.venv/Scripts/python.exe`
- Codex MCP 名称：`origin`，stdio 启动参数为 `-m origin_mcp`。
- 本机依赖要求 `mcp>=1.8,<2`。该源码使用 FastMCP，MCP 2.x 会使服务导入失败。
- 配套 EditaPlot：`C:/Users/zwzhu/.codex/skills/editaplot/SKILL.md`。

## 执行路径

1. 先读源码的 `docs/origin-bridge.md`。安装和配置依据 `docs/agentic/origin-mcp-bootstrap-codex.md`。
2. 区分三层证据：服务协议可连接、桥接可连接、Origin 真实绘图成功。列出工具成功不代表 Origin 可调用。
3. 用户正在安装或卸载 Origin 时，只准备 Python 和 MCP。安装完成后重新发现注册的版本，再启动应用。
4. `origin-mcp status` 检查桥接。`doctor --ping-origin` 会触发应用连接，只在需要实际作图或用户要求测试时运行。
5. 包含 `addon.py` 的嵌入式入口与 `origin_mcp.bridge` 外部入口。按官方说明选择，并保留 localhost 认证。不要打印握手 token，不要把 token 写进 skill、项目或全局 MCP 配置。
6. 真机测试用独立实例、自带 `examples/sample_data.csv` 和唯一输出目录。运行 `examples/smoke_bridge.py`，核对 PNG、OPJU 和 `smoke-report.json`，打开 PNG 检查。只重置自己创建的实例。
7. 与 EditaPlot 配合时先读其完整 SKILL.md 和 `references/origin-safety.md`，运行 doctor 与 origin-smoke。两套工具串行访问 Origin，各自报告验证结果。
8. 保存脚本、版本、日志及验证结果。论文正式图遵循项目绘图规范，不能用通用模板默认值替代。

## 已知状态

2026-10-25：Origin 2026（10.30）已安装，origin-mcp 0.1.4 的 stdio 握手返回25工具，官方真实桥接 smoke 通过导表、读取、绘图、PNG、OPJU、正常退出，报告位于 `C:/Users/zwzhu/.local/share/origin-mcp/output/smoke-origin2026-20261025/smoke-report.json`。
EditaPlot setup、doctor 和真实 Origin 2026 smoke 均通过。本机 CPython 3.12.14 运行时已实际完成论文 C2-D01、C2-D02、C2-D03 原生数据图及工程回开验收。论文任务优先读取 `C:/Users/zwzhu/.codex/skills/markov-thesis-origin-figures/SKILL.md`，不重复安装。桥接测试完成后已正常 shutdown，下次使用 MCP 时需按需启动桥接。

## PowerShell 诊断示例

打开 PowerShell，先进入源码目录，再检查服务。以下命令不启动绘图。

```powershell
cd "C:\Users\zwzhu\.local\share\origin-mcp\origin-mcp-main"
& "C:\Users\zwzhu\.local\share\origin-mcp\.venv\Scripts\python.exe" -m origin_mcp status
```

桥接未启动时返回非零退出码属于诊断结果，不代表 MCP 服务安装失败。Codex 新增 MCP 配置后若当前会话看不到工具，重连会话读取配置。
