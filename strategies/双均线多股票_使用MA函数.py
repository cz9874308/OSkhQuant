# coding: utf-8  # 源文件编码
"""
双均线多股票策略（使用 MyTT.MA）

本策略演示如何对股票池内的多只股票应用双均线策略。
与 khMA 版本不同，本策略使用 MyTT.MA 函数手动计算均线。

策略逻辑
--------
- 对股票池内每只股票计算 MA5 和 MA20
- MA5 > MA20（金叉）且无持仓 → 半仓买入
- MA5 < MA20（死叉）且有持仓 → 全仓卖出

与 khMA 版本的区别
-----------------
- **khMA**: 内置行情获取 + 移动平均计算，更加方便
- **MyTT.MA**: 需要先手动拉取历史行情，再计算均线，更灵活

使用的工具函数
-------------
- `MA()`: 计算移动平均线（来自 MyTT 库）
- `khHistory()`: 获取历史行情数据
- `khGet()`: 获取策略数据
- `khPrice()`: 获取股票价格
- `khHas()`: 检查是否持有股票
- `generate_signal()`: 生成交易信号

注意事项
--------
- 支持多只股票同时运行
- 需要至少 60 个交易日的历史数据
- 使用前复权价格计算均线
"""
# 策略说明：
# - 策略名称：双均线多股票（使用 MyTT.MA）
# - 功能：对股票池内每只股票，比较当日 MA5 与 MA20；MA5>MA20 买入，MA5<MA20 卖出
# - 指标来源：使用 MyTT 库的 MA 函数（对收盘价序列计算均线）
# - 与使用 MyTT.MA 的版本区别：khMA 中内置了行情获取 + 移动平均，更加方便，MyTT.MA 需要在策略文档中先拉取历史行情再计算
from khQuantImport import *  # 统一导入工具与指标

def init(stocks=None, data=None):  # 策略初始化（无需特殊处理）
    """本策略不需初始化"""
    pass  # 占位


def khHandlebar(data: Dict) -> List[Dict]:  # 主策略函数
    """多股票双均线（MyTT.MA）策略：MA5 上穿 MA20 买入，反向卖出"""
    signals = []  # 信号列表
    stock_list = khGet(data, "stocks")  # 股票池
    dn = khGet(data, "date_num")  # 当前日期(数值格式)

    for sc in stock_list:  # 遍历股票
        hist = khHistory(sc, ["close"], 60, "1d", dn, fq="pre", force_download=False)  # 拉取60日收盘价
        closes = hist[sc]["close"].values  # 收盘序列
        ma5_now = float(MA(closes, 5)[-1])  # 当日MA5
        ma20_now = float(MA(closes, 20)[-1])  # 当日MA20

        price = khPrice(data, sc, "open")  # 当日开盘价
        has_pos = khHas(data, sc)  # 是否持仓

        if ma5_now > ma20_now and not has_pos:  # 金叉且无持仓→买入
            signals.extend(generate_signal(data, sc, price, 0.5, "buy", f"{sc[:6]} 金叉买入"))  # 0.5仓
        elif ma5_now < ma20_now and has_pos:  # 死叉且有持仓→卖出
            signals.extend(generate_signal(data, sc, price, 1.0, "sell", f"{sc[:6]} 死叉卖出"))  # 全部卖出

    return signals  # 返回信号

