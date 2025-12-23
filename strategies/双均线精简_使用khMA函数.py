# coding: utf-8
"""
双均线策略示例（使用 khMA 函数）

本策略演示如何使用 khMA 函数实现经典的双均线交易策略。
当短期均线上穿长期均线时买入，下穿时卖出。

策略逻辑
--------
- 计算 5 日均线（短期）和 20 日均线（长期）
- 金叉（5日线上穿20日线）且无持仓 → 全仓买入
- 死叉（5日线下穿20日线）且有持仓 → 全仓卖出

使用的工具函数
-------------
- `khMA()`: 计算移动平均线
- `khGet()`: 获取策略数据（日期、股票代码等）
- `khPrice()`: 获取股票价格
- `khHas()`: 检查是否持有股票
- `generate_signal()`: 生成交易信号

注意事项
--------
- 本策略仅适用于单只股票
- 使用开盘价进行交易
- 需要至少 20 个交易日的历史数据
"""
# 策略说明：
# - 策略名称：双均线精简（使用 khMA）
# - 功能：单只股票，比较当日 khMA5 与 khMA20；khMA5>khMA20 买入，khMA5<khMA20 卖出
# - 指标来源：使用 khQTTools 中的 khMA（内部封装的行情获取 + 移动平均）
from khQuantImport import *  # 导入所有量化工具

def init(stocks=None, data=None):  # 策略初始化函数
    """策略初始化"""

def khHandlebar(data: Dict) -> List[Dict]:  # 主策略函数
    """策略主逻辑，在每个K线或Tick数据到来时执行"""
    signals = []  # 初始化信号列表
    stock_code = khGet(data, "first_stock")  # 获取第一只股票代码
    current_price = khPrice(data, stock_code, "open")  # 获取当前开盘价
    current_date_str = khGet(data, "date_num")  # 获取当前日期数字格式
  
    ma_short = khMA(stock_code, 5, end_time=current_date_str)  # 计算5日均线
    ma_long = khMA(stock_code, 20, end_time=current_date_str)  # 计算20日均线
      
    has_position = khHas(data, stock_code)  # 检查是否持有该股票
  
    if ma_short > ma_long and not has_position:  # 金叉且无持仓
        signals = generate_signal(data, stock_code, current_price, 1.0, 'buy', f"5日线({ma_short:.2f}) 上穿 20日线({ma_long:.2f})，全仓买入")  # 生成买入信号

    elif ma_short < ma_long and has_position:  # 死叉且有持仓
        signals = generate_signal(data, stock_code, current_price, 1.0, 'sell', f"5日线({ma_short:.2f}) 下穿 20日线({ma_long:.2f})，全仓卖出")  # 生成卖出信号

    return signals  # 返回交易信号

# khPreMarket 和 khPostMarket 函数省略，本次策略未使用