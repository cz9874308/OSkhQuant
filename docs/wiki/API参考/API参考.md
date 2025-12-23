
# API参考

<cite>
**本文档引用的文件**   
- [khQuantImport.py](file://khQuantImport.py)
- [khQTTools.py](file://khQTTools.py)
- [khTrade.py](file://khTrade.py)
- [khFrame.py](file://khFrame.py)
</cite>

## 目录
1. [khQuantImport.py 导出接口](#khquantimportpy-导出接口)
2. [khQTTools.py 数据查询与技术指标](#khqttoolspy-数据查询与技术指标)
3. [khTrade.py 交易接口](#khtradepy-交易接口)
4. [khFrame.py 框架核心方法](#khframepy-框架核心方法)

## khQuantImport.py 导出接口

`khQuantImport.py` 模块提供了一站式导入功能，通过 `from khQuantImport import *` 即可导入策略开发所需的所有常用模块和工具。该模块主要导出以下几类接口：

### 时间信息类 (TimeInfo)
一个标准化的时间信息类，用于从策略数据中解析时间信息。

**属性:**
- `date_str`: 返回标准日期格式，如 "2024-06-03"。
- `date_num`: 返回数字日期格式，如 "20240603"。
- `time_str`: 返回时间格式，如 "09:30:00"。
- `datetime_str`: 返回完整日期时间格式，如 "2024-06-03 09:30:00"。
- `datetime_num`: 返回数字日期时间格式，如 "20240603093000"。
- `datetime_obj`: 返回 Python 的 `datetime` 对象。
- `timestamp`: 返回时间戳。

**示例:**
```python
time_info = TimeInfo(data)
print(time_info.date_str)  # 输出: 2024-06-03
```

### 股票数据解析类 (StockDataParser)
用于解析和获取股票数据。

**方法:**
- `get(stock_code: str) -> Dict`: 获取指定股票的完整数据。
- `get_price(stock_code: str, field: str = "close") -> float`: 获取指定股票的价格，`field` 可为 'open', 'high', 'low', 'close', 'volume'。若数据无效，返回 0.0。
- `get_close(stock_code: str) -> float`: 获取收盘价。
- `get_open(stock_code: str) -> float`: 获取开盘价。
- `get_high(stock_code: str) -> float`: 获取最高价。
- `get_low(stock_code: str) -> float`: 获取最低价。
- `get_volume(stock_code: str) -> float`: 获取成交量。

**示例:**
```python
parser = StockDataParser(data)
price = parser.get_price("000001.SZ", "close")
```

### 持仓数据解析类 (PositionParser)
用于解析和获取持仓数据。

**方法:**
- `has(stock_code: str) -> bool`: 检查是否持有某股票。
- `get_volume(stock_code: str) -> float`: 获取持仓数量。
- `get_cost(stock_code: str) -> float`: 获取持仓成本价。
- `get_all() -> Dict`: 获取所有持仓。

**示例:**
```python
positions = PositionParser(data)
if positions.has("000001.SZ"):
    volume = positions.get_volume("000001.SZ")
```

### 股票池解析类 (StockPoolParser)
用于解析和获取股票池信息。

**方法:**
- `get_all() -> List[str]`: 获取所有股票代码。
- `size() -> int`: 获取股票池大小。
- `contains(stock_code: str) -> bool`: 检查是否包含某股票。
- `first() -> Optional[str]`: 获取第一个股票代码。

**示例:**
```python
pool = StockPoolParser(data)
all_stocks = pool.get_all()
```

### 策略上下文类 (StrategyContext)
提供便捷的数据访问和信号生成方法。

**属性:**
- `data`: 原始数据字典。
- `time`: `TimeInfo` 实例。
- `stocks`: `StockDataParser` 实例。
- `positions`: `PositionParser` 实例。
- `pool`: `StockPoolParser` 实例。

**方法:**
- `buy_signal(stock_code: str, ratio: float = 1.0, volume: Optional[int] = None, reason: str = "") -> Dict`: 生成买入信号。
- `sell_signal(stock_code: str, ratio: float = 1.0, volume: Optional[int] = None, reason: str = "") -> Dict`: 生成卖出信号。

**示例:**
```python
context = StrategyContext(data)
signal = context.buy_signal("000001.SZ", ratio=0.5, reason="金叉买入")
```

### 便捷函数
提供一系列简化操作的函数。

- `parse_context(data: Dict) -> StrategyContext`: 解析策略数据为 `StrategyContext` 对象。
- `khGet(data: Dict, key: str) -> Any`: 通用数据获取函数，支持多种键值，如 'date_str', 'time_str', 'cash', 'stocks', 'positions' 等。
- `khPrice(data: Dict, stock_code: str, field: str = 'close') -> float`: 获取股票价格的便捷函数。
- `khHas(data: Dict, stock_code: str) -> bool`: 检查是否持有某股票的便捷函数。
- `khBuy(data: Dict, stock_code: str, ratio: float = 1.0, volume: Optional[int] = None, reason: str = "") -> Dict`: 生成买入信号的便捷函数。
- `khSell(data: Dict, stock_code: str, ratio: float = 1.0, volume: Optional[int] = None, reason: str = "") -> Dict`: 生成卖出信号的便捷函数。
- `get_default_risk_params() -> Dict`: 获取默认的风控参数。

**示例:**
```python
current_price = khPrice(data, "000001.SZ")
if khHas(data, "000001.SZ"):
    signal = khSell(data, "000001.SZ", ratio=1.0)
```

**Section sources**
- [khQuantImport.py](file://khQuantImport.py#L1-L520)

## khQTTools.py 数据查询与技术指标

`khQTTools.py` 模块提供了数据查询、技术指标计算和交易工具函数。

### 数据查询函数 (khHistory)
获取股票历史数据（不包含当前时间点）。

**签名:**
```python
def khHistory(
    symbol_list, 
    fields, 
    bar_count, 
    fre_step, 
    current_time=None, 
    skip_paused=False, 
    fq='pre', 
    force_download=False
) -> dict
```

**参数:**
- `symbol_list`: 股票代码列表或单个字符串。
- `fields`: 数据字段列表，如 ['open', 'high', 'low', 'close', 'volume']。
- `bar_count`: 获取的K线数量。
- `fre_step`: 时间频率，如 '1d', '1m', '5m'。
- `current_time`: 当前时间，支持多种格式（如 'YYYYMMDD', 'YYYY-MM-DD HH:MM:SS'），默认为当前时间。
- `skip_paused`: 是否跳过停牌数据。
- `fq`: 复权方式，'pre'(前复权), 'post'(后复权), 'none'(不复权)。
- `force_download`: 是否强制下载最新数据。

**返回值:**
- `dict`: {股票代码: DataFrame}，DataFrame包含time列和指定的数据字段。

**异常:**
- `ValueError`: 当 `symbol_list` 或 `fields` 为空，或 `bar_count` 小于等于0时抛出。

**示例:**
```python
# 获取000001.SZ过去60天的日线收盘价
hist = khHistory("000001.SZ", ["close"], 60, "1d", fq="pre")
closes = hist["000001.SZ"]["close"].values
```

### 技术指标计算函数 (khMA)
计算移动平均线。

**签名:**
```python
def khMA(
    stock_code: str, 
    period: int, 
    field: str = 'close', 
    fre_step: str = '1d', 
    end_time: Optional[str] = None, 
    fq: str = 'pre'
) -> float
```

**参数:**
- `stock_code`: 股票代码。
- `period`: 周期长度。
- `field`: 计算字段，默认为'close'。
- `fre_step`: 时间频率，如 '1d', '1m'。
- `end_time`: 结束时间，如果为None则使用当前时间。
- `fq`: 复权方式。

**返回值:**
- `float`: 移动平均值。

**异常:**
- `ValueError`: 如果在日内频率下不在交易时间内，或数据量不足时抛出。

**示例:**
```python
# 计算000001.SZ的5日均线
ma5 = khMA("000001.SZ", 5, end_time="20240603")
```

### 时间工具函数
- `is_trade_time() -> bool`: 判断当前是否为交易时间。
- `is_trade_day(date_str: str = None) -> bool`: 判断指定日期是否为交易日（工作日且非法定节假日）。
- `get_trade_days_count(start_date: str, end_date: str) -> int`: 计算指定日期范围内的交易日天数。

**示例:**
```python
if is_trade_time():
    print("当前是交易时间")
days = get_trade_days_count("2024-01-01", "2024-01-31")
```

**Section sources**
- [khQTTools.py](file://khQTTools.py#L0-L799)

## khTrade.py 交易接口

`khTrade.py` 模块中的 `KhTradeManager` 类负责处理交易逻辑，包括下单、撤单和计算交易成本。

### 交易管理器 (KhTradeManager)
**初始化:**
```python
def __init__(self, config, callback=None)
```
- `config`: 配置对象。
- `callback`: 回调对象，用于接收交易回报。

### 下单接口 (place_order)
根据运行模式执行下单。

**签名:**
```python
def place_order(self, signal: Dict)
```

**调用方式:**
- **实盘模式 (`live`)**: 调用 `_place_order_live(signal)`，需连接实