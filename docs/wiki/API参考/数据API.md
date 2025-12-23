
# 数据API

<cite>
**本文档引用的文件**   
- [khQTTools.py](file://khQTTools.py)
- [khQuantImport.py](file://khQuantImport.py)
- [strategies/双均线多股票_使用khMA函数.py](file://strategies/双均线多股票_使用khMA函数.py)
- [strategies/RSI策略.py](file://strategies/RSI策略.py)
- [README.md](file://README.md)
</cite>

## 目录
1. [引言](#引言)
2. [核心数据查询函数](#核心数据查询函数)
3. [技术指标计算函数](#技术指标计算函数)
4. [API与MiniQMT数据源交互](#api与miniqmt数据源交互)
5. [错误处理与性能建议](#错误处理与性能建议)
6. [策略脚本调用示例](#策略脚本调用示例)
7. [总结](#总结)

## 引言

本API文档旨在为用户提供一份详尽、清晰的指南，介绍`khQTTools.py`模块中提供的核心数据查询与处理函数。这些函数是构建量化策略的基石，它们封装了与MiniQMT数据源的复杂交互，使开发者能够专注于策略逻辑本身。文档将详细说明`get_price`、`get_history`（即`khHistory`）等数据查询函数的参数、返回值及使用场景，并深入解析`khMA`、`khMACD`、`khRSI`等技术指标计算函数的实现逻辑。同时，文档还将涵盖API的错误处理机制、性能优化建议，并通过实际的策略脚本示例，展示如何在回测与实盘模式下高效使用这些API。

**Section sources**
- [README.md](file://README.md#L1976-L2006)

## 核心数据查询函数

`khQTTools.py`模块提供了强大的数据查询功能，其核心是`khHistory`函数，它能够从MiniQMT数据源获取历史行情数据。此外，通过`khQuantImport.py`的统一导入，用户可以便捷地使用`khPrice`等辅助函数。

### khHistory函数详解

`khHistory`是获取历史K线数据的核心函数，它返回一个`pandas.DataFrame`，为技术指标计算和策略回测提供数据基础。

**函数签名**:
```python
def khHistory(symbol_list, fields, bar_count, fre_step, current_time=None, skip_paused=False, fq='pre', force_download=False) -> dict
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `symbol_list` | list 或 str | 是 | 股票代码列表或单个股票代码字符串。代码必须包含交易所后缀，如`'000001.SZ'`或`'600000.SH'`。 |
| `fields` | list | 是 | 要获取的数据字段列表。常用字段包括`'open'`（开盘价）、`'high'`（最高价）、`'low'`（最低价）、`'close'`（收盘价）、`'volume'`（成交量）、`'amount'`（成交额）。 |
| `bar_count` | int | 是 | 要获取的K线数量。例如，设置为`30`将获取最近的30根K线。 |
| `fre_step` | str | 是 | 时间频率（周期类型）。支持`'1d'`（日线）、`'1m'`（1分钟线）、`'5m'`（5分钟线）等。 |
| `current_time` | str | 否 | 数据获取的结束时间点。支持多种格式，如`'20241201'`（日线）、`'2024-12-01 14:30:00'`（分钟线）。如果为`None`，则使用当前时间。 |
| `skip_paused` | bool | 否 | 是否跳过停牌数据。`True`表示过滤掉成交量为0的K线，确保返回的K线是连续的交易日。 |
| `fq` | str | 否 | 复权方式。`'pre'`表示前复权，`'post'`表示后复权，`'none'`表示不复权。默认为`'pre'`。 |
| `force_download` | bool | 否 | 是否强制下载最新数据。`True`会从服务器强制更新数据，`False`则优先使用本地缓存以提高回测速度。 |

**返回值结构**:
- **类型**: `dict`
- **结构**: 返回一个字典，其键为股票代码（如`'000001.SZ'`），值为一个`pandas.DataFrame`。
- **DataFrame结构**: 包含`time`列和用户指定的`fields`列。`time`列是`datetime`对象，方便进行时间序列分析。

**使用场景**:
- **回测场景**: 在策略初始化或主逻辑中，拉取历史数据以计算技术指标（如均线、RSI）。
- **实盘场景**: 获取最新的历史数据，用于实时判断交易信号。

**Section sources**
- [khQTTools.py](file://khQTTools.py#L2400-L2745)

### khPrice函数详解

`khPrice`是一个便捷的辅助函数，用于快速获取某只股票在当前时间点的特定价格。

**函数签名**:
```python
def khPrice(data: Dict, stock_code: str, field: str = 'close') -> float
```

**参数说明**:
- `data`: 策略的上下文数据字典（即`context`），包含了当前的行情、账户和持仓信息。
- `stock_code`: 股票代码。
- `field`: 价格字段，默认为`'close'`，也可为`'open'`、`'high'`、`'low'`等。

**返回值**:
- **类型**: `float`
- **说明**: 返回指定股票和字段的价格。如果获取失败，则返回`0.0`。

**使用场景**:
- 在生成交易信号时，快速获取当前的开盘价或收盘价作为委托价格。

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L480-L520)

## 技术指标计算函数

`khQTTools.py`模块不仅提供数据查询，还直接封装了常用技术指标的计算逻辑，极大地简化了策略开发。

### khMA函数详解

`khMA`函数用于计算移动平均线（Moving Average），它内部调用了`khHistory`来获取数据并计算均值。

**函数签名**:
```python
def khMA(stock_code: str, period: int, field: str = 'close', fre_step: str = '1d', end_time: Optional[str] = None, fq: str = 'pre') -> float
```

**参数说明**:

| 参数 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `stock_code` | str | 是 | 股票代码。 |
| `period` | int | 是 | 均线的周期长度，如`5`表示5日均线。 |
| `field` | str | 否 | 用于计算均线的字段，默认为`'close'`（收盘价）。 |
| `fre_step` | str | 否 | 数据频率，默认为`'1d'`（日线）。 |
| `end_time` | str | 否 | 计算均线的截止时间。如果为`None`，则使用当前时间。 |
| `fq` | str | 否 | 复权方式，同`khHistory`。 |

**实现逻辑**:
1.  根据`end_time`和`fre_step`确定当前时间。
2.  调用`khHistory`函数，获取指定股票、周期长度、频率和复权方式的`period`条历史数据。
3.  计算`field`字段的算术平均值，并四舍五入到小数点后两位。
4.  如果数据量不足`period`条，会抛出`ValueError`异常。

**返回值**:
- **类型**: `float`
- **说明**: 返回计算出的移动平均值。

**使用场景**:
- 实现双均线策略，比较短期均线和长期均线的金叉/死叉。

**Section sources**
- [khQTTools.py](file://khQTTools.py#L700-L799)

### khMACD与khRSI函数

虽然`khQTTools.py`中未直接定义`khMACD`和`khRSI`函数，但通过`khQuantImport.py`模块，用户可以无缝使用`MyTT`库中的`MACD`和`RSI`函数。

**实现逻辑**:
- 这些函数本身不直接与MiniQMT交互，而是接收一个价格序列（通常是`pandas.Series`）作为输入。
- `khHistory`函数负责从MiniQMT获取原始价格数据，并将其转换为`Series`。
- 然后，将此`Series`传递给`MyTT`中的`MACD`或`RSI`函数进行计算。

**使用场景**:
- `RSI`：判断股票的超买超卖状态。
- `MACD`：识别趋势的强度和方向。

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L10-L20)
- [strategies/RSI策略.py](file://strategies/RSI策略.py#L1-L26)

## API与MiniQMT数据源交互

`khQTTools`中的所有数据查询函数都依赖于`xtquant`库，该库是MiniQMT提供的官方Python接口。这种设计确保了数据的权威性和实时性。

### 交互流程
1.  **数据请求**: 当调用`khHistory`时，`khQTTools`内部会调用`xtdata.get_market_data_ex`等函数。
2.  **数据源**: `xtdata`会优先从本地缓存（`userdata_mini\datadir`目录下的`.dat`文件）读取数据，这保证了回测的高速度。
3.  **数据补充**: 如果本地数据不足，且`force_download=True`，则会通过`xtdata.download_history_data`从MiniQMT服务器下载缺失的数据。
4.  **数据返回**: 获取到的数据被封装成`pandas.DataFrame`并返回给用户。

### 回测与实盘模式
- **回测模式**: 策略在历史数据上运行。`khHistory`函数通过`current_time`参数精确控制数据的截止点，确保回测逻辑的正确性