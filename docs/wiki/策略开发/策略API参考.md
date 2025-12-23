
# 策略API参考

<cite>
**本文档中引用的文件**  
- [khQuantImport.py](file://khQuantImport.py)
- [MyTT.py](file://MyTT.py)
- [khQTTools.py](file://khQTTools.py)
</cite>

## 目录
1. [简介](#简介)
2. [核心数据获取函数](#核心数据获取函数)
3. [技术指标计算函数](#技术指标计算函数)
4. [交易指令生成函数](#交易指令生成函数)
5. [时间与交易日工具](#时间与交易日工具)
6. [策略上下文与便捷函数](#策略上下文与便捷函数)
7. [MA与khMA函数对比](#ma与khma函数对比)
8. [自定义指标扩展（MyTT）](#自定义指标扩展mytt)
9. [调用示例](#调用示例)
10. [错误码说明](#错误码说明)
11. [线程安全性与性能注意事项](#线程安全性与性能注意事项)

## 简介
`khQuantImport` 模块为量化策略开发提供了一站式导入接口，封装了数据获取、技术指标计算、交易信号生成等常用功能。开发者可通过 `from khQuantImport import *` 一行代码引入所有必要工具，简化策略编写流程。本参考文档详细说明了该模块中所有可用函数的参数、返回值及使用限制，并重点对比了标准移动平均 `MA` 与增强版 `khMA` 的实现差异。

**本文档中引用的文件**
- [khQuantImport.py](file://khQuantImport.py)

## 核心数据获取函数

### get_price / khPrice
获取指定股票的价格数据。

**参数**:
- `data`: 策略数据字典
- `stock_code`: 股票代码
- `field`: 价格字段，默认为 `'close'`，可选 `'open'`, `'high'`, `'low'`, `'volume'`

**返回值**: `float` - 价格值，若获取失败返回 `0.0`

**使用限制**:
- 支持处理 `pandas.Series`、数组及标量类型
- 自动处理 `None` 和空值情况
- 对非数值类型进行日志警告并返回 `0.0`

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L278-L351)

### StockDataParser.get_price
`get_price` 函数的底层实现类方法，提供更细粒度的股票数据访问。

**参数**:
- `stock_code`: 股票代码
- `field`: 价格字段

**返回值**: `float` - 价格值

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L107-L187)

## 技术指标计算函数

### MA (来自 MyTT)
标准移动平均线计算函数。

**参数**:
- `S`: 价格序列（如收盘价）
- `N`: 周期长度

**返回值**: `np.ndarray` - 等长于输入序列的移动平均值数组

**实现原理**:
- 使用 `pandas.Series(S).rolling(N).mean().values` 计算
- 基于滚动窗口的算术平均

**Section sources**
- [MyTT.py](file://MyTT.py#L157-L159)

### khMA
增强版移动平均线，支持多周期、多股票向量化计算。

**参数**:
- `stock_code`: 股票代码
- `period`: 周期长度
- `field`: 计算字段，默认为 `'close'`
- `fre_step`: 时间频率，如 `'1d'`, `'1m'`
- `end_time`: 结束时间，`None` 表示当前时间
- `fq`: 复权方式，`'pre'`（前复权）、`'post'`（后复权）、`'none'`（不复权）

**返回值**: `float` - 移动平均值

**异常**:
- `ValueError`: 不在交易时间内（日内频率）或数据不足

**使用场景**:
- 适用于复杂策略场景，支持分钟级、日线等多频率数据
- 可在回测和实盘中使用

**Section sources**
- [khQTTools.py](file://khQTTools.py#L279-L325)

## 交易指令生成函数

### order_target_value / khBuy / khSell
生成买入或卖出交易信号。

#### khBuy
生成买入信号。

**参数**:
- `data`: 策略数据字典
- `stock_code`: 股票代码
- `ratio`: 买入比例（≤1）或指定股数（>1）
- `volume`: 指定买入数量（可选）
- `reason`: 买入原因

**返回值**: `Dict` - 买入信号字典

**逻辑**:
- 若 `ratio > 1`，按指定股数下单，需为100的整数倍
- 若 `ratio ≤ 1`，按资金比例计算最大可买入量
- 自动调用 `calculate_max_buy_volume` 计算实际可买数量

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L465-L494)
- [khQTTools.py](file://khQTTools.py#L418-L520)

#### khSell
生成卖出信号。

**参数**:
- `data`: 策略数据字典
- `stock_code`: 股票代码
- `ratio`: 卖出比例
- `volume`: 指定卖出数量（可选）
- `reason`: 卖出原因

**返回值**: `Dict` - 卖出信号字典

**逻辑**:
- 计算可用持仓数量
- 按比例计算实际卖出股数（向下取整至100的倍数）

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L496-L520)
- [khQTTools.py](file://khQTTools.py#L418-L520)

### generate_signal
生成标准交易信号的核心函数。

**参数**:
- `data`: 包含账户、持仓信息的字典
- `stock_code`: 股票代码
- `price`: 交易价格
- `ratio`: 交易比例或股数
- `action`: `'buy'` 或 `'sell'`
- `reason`: 交易原因

**返回值**: `List[Dict]` - 信号列表（通常包含一个信号）

**Section sources**
- [khQTTools.py](file://khQTTools.py#L418-L520)

## 时间与交易日工具

### is_trade_time
判断当前是否为交易时间。

**返回值**: `bool`

**Section sources**
- [khQTTools.py](file://khQTTools.py#L77-L84)

### is_trade_day
判断指定日期是否为交易日。

**参数**:
- `date_str`: 日期字符串，支持 `'YYYY-MM-DD'` 或 `'YYYYMMDD'` 格式，`None` 表示当天

**返回值**: `bool`

**Section sources**
- [khQTTools.py](file://khQTTools.py#L86-L165)

### get_trade_days_count
计算两个日期之间的交易日天数。

**参数**:
- `start_date`: 起始日期 `'YYYY-MM-DD'`
- `end_date`: 结束日期 `'YYYY-MM-DD'`

**返回值**: `int`

**Section sources**
- [khQTTools.py](file://khQTTools.py#L167-L206)

## 策略上下文与便捷函数

### StrategyContext
策略上下文类，提供统一的数据访问接口。

**属性**:
- `time`: `TimeInfo` 对象
- `stocks`: `StockDataParser` 对象
- `positions`: `PositionParser` 对象
- `pool`: `StockPoolParser` 对象

**方法**:
- `buy_signal()`: 生成买入信号
- `sell_signal()`: 生成卖出信号

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L242-L276)

### khGet
通用数据获取函数，支持简洁键名访问。

**参数**:
- `data`: 策略数据字典
- `key`: 数据键，如 `'date'`, `'cash'`, `'positions'` 等

**返回值**: `Any` - 对应数据值

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L353-L420)

## MA与khMA函数对比

| 特性 | MA | khMA |
|------|----|------|
| **来源** | MyTT.py | khQTTools.py |
| **输入类型** | 价格序列 (`np.ndarray`) | 股票代码 (`str`) |
| **计算范围** | 单一股票、单一周期 | 支持多股票、多周期 |
| **频率支持** | 依赖输入数据 | 支持 `'1d'`, `'1m'`, `'5m'` 等 |
| **复权支持** | 无 | 支持 `'pre'`, `'post'`, `'none'` |
| **交易时间检查** | 无 | 有（日内频率） |
| **数据获取方式** | 直接传入序列 | 通过 `khHistory` 自动获取 |
| **适用场景** | 简单策略、批量计算 | 复杂策略、实盘交易 |

**结论**:
- `MA` 适用于对已有价格序列进行快速计算，适合向量化批量处理。
- `khMA` 为增强版本，更适合复杂策略开发，提供更完整的数据获取与风控检查，支持多频率、多股票场景。

**Section sources**
- [MyTT.py](file://MyTT.py#L157-L159)
- [khQTTools.py](file://khQTTools.py#L279-L325)

## 自定义指标扩展（MyTT）
`MyTT` 模块提供了丰富的技术指标实现，可通过 `from MyTT import *` 导入使用。

### RSI
相对强弱指数。

**参数**:
- `CLOSE`: 收盘价序列
- `N`: 周期，默认24

**返回值**: `float` - RSI值

**公式**: `SMA(MAX(DIF, 0), N) / SMA(ABS(DIF), N) * 100`

**Section sources**
- [MyTT.py](file://MyTT.py#L208-L210)

### MACD
指数平滑异同平均线。

**参数**:
- `CLOSE`: 收盘价序列
- `SHORT`: 短周期，默认12
- `LONG`: 长周期，默认26
- `M`: 信号线周期，默认9

**返回值**: `(DIF, DEA, MACD)` 三元组

**Section sources**
- [MyTT.py](file://MyTT.py#L190-L195)

### 其他指标
- `BOLL`: 布林带
- `KDJ`: 随机指标
- `CCI`: 顺势指标
- `ATR`: 平均真实波幅
- `SAR`: 抛物转向指标

**Section sources**
- [MyTT.py](file://MyTT.py#L190-L623)

## 调用示例

### 获取价格
```python
price = khPrice(data, 'sh.600030', 'close')
```

### 计算均线
```python
# 使用MA（需先获取价格序列）
close_prices = get_price_series('sh.600030', 20)
ma20 = MA(close_prices, 20)

# 使用khMA（直接计算）
ma20 = khMA('sh.600030', 20, 'close', '1d')
```

### 生成交易信号
```python
# 买入信号（按资金比例）
signal = khBuy(data, 'sh.600030', ratio=0.5, reason="突破20日均线")

# 卖出信号（按股数）
signal = khSell(data, 'sh.600030', volume=1000, reason="止盈")
```

### 使用策略上下文
```python
ctx = StrategyContext(data)
signal = ctx.buy_signal('sh.600030', ratio=1.0, reason="金叉买入")
```

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L465-L520)

## 错误码说明

| 错误类型 | 错误信息 | 原因 | 解决方案 |
|---------|--------|------|---------|
| `ValueError` | "不在交易时间内" | 调用 `khMA` 时非交易时间 | 仅在交易时段调用或使用日线数据 |
| `ValueError` | "数据量不足" | 历史