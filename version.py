# coding: utf-8
"""
版本信息管理模块

本模块负责管理看海量化回测平台的版本信息，提供统一的版本号查询接口。

核心功能
--------
- 存储应用的版本号、构建日期、更新通道等信息
- 提供便捷的版本信息查询函数

使用方式
--------
>>> from version import get_version, get_version_info
>>> print(get_version())  # 输出: "2.1.4"
>>> info = get_version_info()
>>> print(info["app_name"])  # 输出: "看海量化回测平台"
"""

# 版本信息字典
# 包含应用的核心版本元数据，用于更新检查和界面显示
VERSION_INFO = {
    "version": "2.1.4",           # 语义化版本号 (主版本.次版本.修订号)
    "build_date": "2025-12-04",   # 构建日期，格式 YYYY-MM-DD
    "channel": "stable",          # 更新通道: stable(稳定版) / beta(测试版)
    "app_name": "看海量化回测平台"  # 应用显示名称
}


def get_version() -> str:
    """获取当前版本号
    
    Returns:
        str: 版本号字符串，如 "2.1.4"
    
    Example:
        >>> version = get_version()
        >>> print(f"当前版本: v{version}")
        当前版本: v2.1.4
    """
    return VERSION_INFO["version"]


def get_version_info() -> dict:
    """获取完整版本信息
    
    返回版本信息的副本，防止外部代码意外修改原始数据。
    
    Returns:
        dict: 包含 version, build_date, channel, app_name 的字典
    
    Example:
        >>> info = get_version_info()
        >>> print(info)
        {'version': '2.1.4', 'build_date': '2025-12-04', ...}
    """
    return VERSION_INFO.copy()


def get_channel() -> str:
    """获取当前更新通道
    
    更新通道决定了软件接收哪个版本线的更新：
    - stable: 稳定版，经过充分测试
    - beta: 测试版，包含最新功能但可能不稳定
    
    Returns:
        str: 更新通道名称
    """
    return VERSION_INFO["channel"]