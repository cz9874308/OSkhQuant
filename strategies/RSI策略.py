# coding: utf-8
"""
RSI 策略示例

本策略演示如何使用 RSI 指标实现超买超卖交易策略。
当 RSI 低于 30 时买入（超卖），高于 70 时卖出（超买）。

策略逻辑
--------
- 计算 14 日 RSI 指标
- RSI < 30（超卖区）且无持仓 → 半仓买入
- RSI > 70（超买区）且有持仓 → 全仓卖出
- 支持多只股票同时运行

使用的工具函数
-------------
- `RSI()`: 计算相对强弱指标（来自 MyTT 库）
- `khHistory()`: 获取历史行情数据
- `khGet()`: 获取策略数据
- `khPrice()`: 获取股票价格
- `khHas()`: 检查是否持有股票
- `generate_signal()`: 生成交易信号

注意事项
--------
- 需要至少 60 个交易日的历史数据
- 使用前复权价格计算 RSI
- 适用于震荡行情，趋势行情可能表现不佳
"""
# 策略说明：
# - 策略名称：RSI 策略
# - 功能：多只股票，比较当日 RSI(14) 与 30/70；RSI<30 买入，RSI>70 卖出
# - 指标来源：使用 MyTT 库的 RSI 函数（对收盘价序列计算RSI）
from khQuantImport import *  # 导入统一工具与指标

def init(stocks=None, data=None):  # 初始化（无需特殊处理）
    """策略初始化（本策略无需特殊初始化）"""
    pass  # 占位

def khHandlebar(data: Dict) -> List[Dict]:  # 主策略函数
    signals = []  # 信号列表
    dn = khGet(data, "date_num")  # 当前日期(数值格式)
    for sc in khGet(data, "stocks"):  # 遍历股票池
        hist = khHistory(sc, ["close"], 60, "1d", dn, fq="pre", force_download=False)  # 拉取60日收盘价
        r = RSI(hist[sc]["close"].values, 14)  # 计算RSI(14)
        rp, rn = float(r[-2]), float(r[-1])  # 前一日与当日RSI
        p = khPrice(data, sc, "open")  # 当日开盘价
        if (rp < 30 <= rn) and not khHas(data, sc):  # RSI上穿30且无持仓→买入
            signals.extend(generate_signal(data, sc, p, 0.5, "buy", f"{sc[:6]} RSI 上穿30，{rn:.2f}"))  # 0.5仓
        elif (rp > 70 >= rn) and khHas(data, sc):  # RSI下穿70且有持仓→卖出
            signals.extend(generate_signal(data, sc, p, 1.0, "sell", f"{sc[:6]} RSI 下穿70，{rn:.2f}"))  # 全部卖出
    return signals  # 返回信号

