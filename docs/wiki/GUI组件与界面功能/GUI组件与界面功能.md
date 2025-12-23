# GUI组件与界面功能

<cite>
**本文档引用的文件**   
- [GUI.py](file://GUI.py)
- [GUIDataViewer.py](file://GUIDataViewer.py)
- [GUIScheduler.py](file://GUIScheduler.py)
- [GUIplotLoadData.py](file://GUIplotLoadData.py)
- [SettingsDialog.py](file://SettingsDialog.py)
- [backtest_result_window.py](file://backtest_result_window.py)
- [khFrame.py](file://khFrame.py)
</cite>

## 目录
1. [主界面 (GUI.py)](#主界面-guipy)
2. [数据查看器 (GUIDataViewer.py)](#数据查看器-guidataviewerpy)
3. [调度器 (GUIScheduler.py)](#调度器-guischedulerpy)
4. [数据加载界面 (GUIplotLoadData.py)](#数据加载界面-guiplotloaddatapy)
5. [设置对话框 (SettingsDialog.py)](#设置对话框-settingsdialogpy)
6. [回测结果窗口 (backtest_result_window.py)](#回测结果窗口-backtest_result_windowpy)
7. [底层逻辑模块 (khFrame.py)](#底层逻辑模块-khframepy)

## 主界面 (GUI.py)

主界面是系统的控制中心，集成了策略配置、运行控制和状态监控等功能。其布局采用三栏式设计，左侧为配置区，中间为运行驱动区，右侧为信息反馈区。

**Section sources**
- [GUI.py](file://GUI.py#L0-L3887)

## 数据查看器 (GUIDataViewer.py)

数据查看器用于展示从miniQMT客户端下载的本地存储行情数据。用户可以通过树形结构浏览不同日期和股票的数据文件，并在表格中查看详细数据。

**Section sources**
- [GUIDataViewer.py](file://GUIDataViewer.py#L0-L4260)

## 调度器 (GUIScheduler.py)

调度器用于配置和管理定时任务，如定期补充历史数据。用户可以设置任务的执行时间、周期类型和股票池，实现数据的自动化更新。

**Section sources**
- [GUIScheduler.py](file://GUIScheduler.py#L0-L1855)

## 数据加载界面 (GUIplotLoadData.py)

数据加载界面提供了一个可视化工具，用于加载和分析本地存储的CSV格式行情数据。用户可以选择数据文件夹，浏览不同股票的数据，并通过图表直观地查看价格走势。

**Section sources**
- [GUIplotLoadData.py](file://GUIplotLoadData.py#L0-L1122)

## 设置对话框 (SettingsDialog.py)

设置对话框允许用户配置系统参数，包括无风险收益率、延迟显示日志、账户信息等。此外，用户还可以在此更新股票列表和设置miniQMT客户端路径。

**Section sources**
- [SettingsDialog.py](file://SettingsDialog.py#L0-L649)

## 回测结果窗口 (backtest_result_window.py)

回测结果窗口展示了策略回测的详细结果，包括资金曲线、交易记录、每日收益等。用户可以通过多个标签页查看不同的绩效指标和图表，全面评估策略表现。

**Section sources**
- [backtest_result_window.py](file://backtest_result_window.py#L0-L3183)

## 底层逻辑模块 (khFrame.py)

底层逻辑模块（khFrame.py）是系统的核心，负责策略的执行、数据的处理和交易的管理。它与GUI组件通过回调函数进行通信，确保用户界面的实时更新。

**Section sources**
- [khFrame.py](file://khFrame.py#L0-L2679)