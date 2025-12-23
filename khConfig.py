# coding: utf-8
"""
配置管理模块

本模块负责加载、解析和管理看海量化平台的配置文件（.kh 文件）。
配置文件使用 JSON 格式，包含系统、账户、回测、数据、风控等多个配置块。

核心功能
--------
- 从 .kh 文件加载配置
- 提供配置项的便捷访问接口
- 支持配置的动态更新和保存

配置文件结构
-----------
一个典型的 .kh 配置文件结构如下：

```json
{
    "run_mode": "backtest",
    "system": {
        "userdata_path": "path/to/userdata_mini",
        "session_id": 12345
    },
    "account": {
        "account_id": "test_account"
    },
    "backtest": {
        "start_time": "20240101",
        "end_time": "20241231",
        "init_capital": 1000000
    },
    "data": {
        "kline_period": "1d",
        "stock_list": ["000001.SZ", "600519.SH"]
    },
    "risk": {
        "position_limit": 0.95,
        "order_limit": 100,
        "loss_limit": 0.1
    }
}
```

使用方式
--------
>>> from khConfig import KhConfig
>>> config = KhConfig("my_strategy.kh")
>>> print(config.stock_pool)  # 获取股票池
>>> print(config.init_capital)  # 获取初始资金
"""
import json
from typing import Dict, List, Optional, Any
import time


class KhConfig:
    """配置管理类
    
    负责加载和管理 .kh 配置文件，为策略框架提供统一的配置访问接口。
    
    配置对象就像一个"配置中心"，策略运行所需的所有参数都可以从这里获取。
    
    Attributes:
        config_path (str): 配置文件路径
        config_dict (dict): 原始配置字典
        run_mode (str): 运行模式，"backtest"(回测) 或 "live"(实盘)
        userdata_path (str): MiniQMT 用户数据目录路径
        session_id (int): 会话标识符
        check_interval (int): 检查间隔（秒）
        account_id (str): 账户标识
        account_type (str): 账户类型
        backtest_start (str): 回测开始日期，格式 YYYYMMDD
        backtest_end (str): 回测结束日期，格式 YYYYMMDD
        init_capital (float): 初始资金
        kline_period (str): K线周期，如 "1d", "1m", "5m"
        stock_pool (List[str]): 股票代码列表
        position_limit (float): 持仓比例上限
        order_limit (int): 单日委托上限
        loss_limit (float): 止损比例
    
    Example:
        >>> config = KhConfig("demo.kh")
        >>> print(f"回测区间: {config.backtest_start} - {config.backtest_end}")
        >>> print(f"股票池: {config.stock_pool}")
    """
    
    def __init__(self, config_path: str):
        """初始化配置管理器
        
        加载指定路径的配置文件，并解析各配置块。
        
        Args:
            config_path: 配置文件路径（.kh 或 .json 文件）
        
        Raises:
            FileNotFoundError: 配置文件不存在
            json.JSONDecodeError: 配置文件格式错误
        """
        self.config_path = config_path  # 保存配置文件路径
        
        # 加载配置文件
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config_dict = json.load(f)
        
        # ========== 系统配置 ==========
        # run_mode 可能在根级别或 system 块中
        self.run_mode = self.config_dict.get("run_mode") or \
                       self.config_dict.get("system", {}).get("run_mode", "backtest")
        self.userdata_path = self.config_dict.get("system", {}).get("userdata_path", "")
        self.session_id = self.config_dict.get("system", {}).get("session_id", int(time.time()))
        self.check_interval = self.config_dict.get("system", {}).get("check_interval", 3)
        
        # ========== 账户配置 ==========
        account_config = self.config_dict.get("account", {})
        self.account_id = account_config.get("account_id", "test_account")
        self.account_type = account_config.get("account_type", "SECURITY_ACCOUNT")
        
        # ========== 回测配置 ==========
        backtest_config = self.config_dict.get("backtest", {})
        self.backtest_start = backtest_config.get("start_time", "20240101")
        self.backtest_end = backtest_config.get("end_time", "20241231")
        self.init_capital = backtest_config.get("init_capital", 1000000)  # 默认100万
        
        # ========== 数据配置 ==========
        data_config = self.config_dict.get("data", {})
        self.kline_period = data_config.get("kline_period", "1d")
        # 兼容性处理：优先使用 stock_list，其次使用 stock_pool
        self.stock_pool = data_config.get("stock_list", data_config.get("stock_pool", []))
        
        # ========== 风控配置 ==========
        risk_config = self.config_dict.get("risk", {})
        self.position_limit = risk_config.get("position_limit", 0.95)  # 默认95%仓位上限
        self.order_limit = risk_config.get("order_limit", 100)         # 默认单日100次
        self.loss_limit = risk_config.get("loss_limit", 0.1)           # 默认10%止损
        
    @property
    def initial_cash(self) -> float:
        """获取初始资金
        
        此属性确保与回测配置中的 init_capital 保持一致，
        提供统一的资金访问接口。
        
        Returns:
            float: 初始资金金额
        """
        return self.init_capital

    def get_stock_list(self) -> List[str]:
        """获取股票列表
        
        从配置中读取股票池，支持 stock_list 和 stock_pool 两种字段名。
        
        Returns:
            List[str]: 股票代码列表，如 ["000001.SZ", "600519.SH"]
        """
        data_config = self.config_dict.get("data", {})
        # 优先从 stock_list 读取，兼容旧版 stock_pool
        return data_config.get("stock_list", data_config.get("stock_pool", []))
    
    def update_stock_list(self, stock_list: List[str]) -> None:
        """更新股票列表
        
        将新的股票列表写入配置，同时更新内存和配置字典。
        
        Args:
            stock_list: 新的股票代码列表
        
        Example:
            >>> config.update_stock_list(["000001.SZ", "000002.SZ"])
        """
        if "data" not in self.config_dict:
            self.config_dict["data"] = {}
        
        # 统一使用 stock_list 字段
        self.config_dict["data"]["stock_list"] = stock_list
        self.stock_pool = stock_list  # 同步更新内存
        
        # 清理旧字段
        if "stock_list_file" in self.config_dict["data"]:
            del self.config_dict["data"]["stock_list_file"]

    def _load_config(self) -> Dict:
        """重新加载配置文件
        
        从磁盘重新读取配置文件内容。
        
        Returns:
            Dict: 配置字典
        
        Raises:
            Exception: 加载失败时抛出异常
        """
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"加载配置文件失败: {str(e)}")
            
    def save_config(self) -> None:
        """保存配置到文件
        
        将当前配置字典序列化为 JSON 并写入文件。
        
        Raises:
            Exception: 保存失败时抛出异常
        
        Example:
            >>> config.update_config("run_mode", "backtest")
            >>> config.save_config()  # 变更已自动保存
        """
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config_dict, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"保存配置文件失败: {str(e)}")
            
    def update_config(self, key: str, value: Any) -> None:
        """更新配置并保存
        
        修改指定配置项的值，并自动保存到文件。
        
        Args:
            key: 配置键名（顶层键）
            value: 新的配置值
        
        Example:
            >>> config.update_config("run_mode", "live")
        
        Note:
            此方法直接操作顶层配置，如需修改嵌套配置，
            可直接操作 config_dict 后调用 save_config()
        """
        self.config_dict[key] = value
        self.save_config()
 