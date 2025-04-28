"""
颜色管理模块 - 管理所有科研绘图相关的颜色配置
"""
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple, Union, Optional

# 基础颜色字典
class ColorManager:
    def __init__(self):
        # 基础颜色定义
        self.base_colors = {
            # 基础颜色组
            'primary': '#1f77b4',    # 蓝色
            'secondary': '#ff7f0e',  # 橙色
            'tertiary': '#2ca02c',   # 绿色
            
            # 状态颜色
            'success': '#2ecc71',
            'warning': '#f39c12',
            'error': '#e74c3c',
            'info': '#3498db',
            
            # 背景色
            'background': '#ffffff',
            'background_alt': '#f8f9fa',
            
            # 前景色
            'foreground': '#333333',
            'foreground_alt': '#666666',
            
            # 强调色
            'accent': '#9b59b6',
            'accent_alt': '#8e44ad',
        }
        
        # 预设调色板组 - 用于多系列数据
        self.palettes = {
            'default': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'],
            'pastel': ['#a1c9f4', '#ffb482', '#8de5a1', '#ff9f9b', '#d0bbff', '#debb9b', '#fab0e4', '#cfcfcf', '#fffea3', '#b9f2f0'],
            'vibrant': ['#0077bb', '#cc3311', '#009988', '#ee7733', '#33bbee', '#ee3377', '#bbbbbb'],
            'muted': ['#4878d0', '#ee854a', '#6acc64', '#d65f5f', '#956cb4', '#8c613c', '#dc7ec0', '#797979', '#d5bb67', '#82c6e2'],
            'scientific': ['#0C5DA5', '#00B945', '#FF9500', '#FF2C00', '#845B97', '#474747', '#9e9e9e'],
            'qualitative': ['#4477AA', '#66CCEE', '#228833', '#CCBB44', '#EE6677', '#AA3377', '#BBBBBB'],
        }
        
        # 渐变色预设
        self.gradients = {
            'blues': ['#deebf7', '#9ecae1', '#3182bd'],
            'reds': ['#fee0d2', '#fc9272', '#de2d26'],
            'greens': ['#e5f5e0', '#a1d99b', '#31a354'],
            'purples': ['#efedf5', '#bcbddc', '#756bb1'],
            'greys': ['#f7f7f7', '#cccccc', '#636363'],
            'heat': ['#ffffcc', '#fd8d3c', '#800026'],
            'cool': ['#f7fcfd', '#66c2a4', '#00441b'],
            'diverging': ['#2166ac', '#f7f7f7', '#b2182b'],
        }
        
        # 语义颜色角色
        self.roles = {
            'main_item': self.base_colors['primary'],
            'comparison_item': self.base_colors['secondary'],
            'highlight': self.base_colors['accent'],
            'background': self.base_colors['background'],
            'grid': '#eeeeee',
            'text': self.base_colors['foreground'],
            'annotation': self.base_colors['foreground_alt'],
        }
    
    def get_color(self, name: str) -> str:
        """获取单个颜色"""
        if name in self.base_colors:
            return self.base_colors[name]
        elif name in self.roles:
            return self.roles[name]
        else:
            raise ValueError(f"颜色 '{name}' 未找到")
    
    def get_palette(self, name: str = 'default', n: Optional[int] = None) -> List[str]:
        """获取调色板颜色列表"""
        if name not in self.palettes:
            raise ValueError(f"调色板 '{name}' 未找到")
        
        palette = self.palettes[name]
        
        # 如果指定了颜色数量，循环使用调色板颜色
        if n is not None:
            return [palette[i % len(palette)] for i in range(n)]
        
        return palette
    
    def get_gradient(self, name: str, n: int = 3) -> List[str]:
        """获取渐变色列表"""
        if name not in self.gradients:
            raise ValueError(f"渐变色 '{name}' 未找到")
        
        gradient = self.gradients[name]
        
        # 创建颜色映射
        cmap = mcolors.LinearSegmentedColormap.from_list('custom_gradient', gradient)
        
        # 返回n个颜色
        return [mcolors.to_hex(cmap(i/(n-1))) for i in range(n)]
    
    def create_custom_palette(self, name: str, colors: List[str]) -> None:
        """创建自定义调色板"""
        self.palettes[name] = colors
    
    def create_custom_gradient(self, name: str, colors: List[str]) -> None:
        """创建自定义渐变色"""
        self.gradients[name] = colors
    
    def update_role(self, role_name: str, color: str) -> None:
        """更新颜色角色"""
        self.roles[role_name] = color
    
    def add_base_color(self, name: str, color: str) -> None:
        """添加新的基础颜色"""
        self.base_colors[name] = color
    
    def get_colormap(self, name: str) -> mcolors.LinearSegmentedColormap:
        """获取matplotlib兼容的colormap"""
        if name in self.gradients:
            return mcolors.LinearSegmentedColormap.from_list(name, self.gradients[name])
        
        # 尝试使用matplotlib内置colormap
        try:
            return plt.cm.get_cmap(name)
        except:
            raise ValueError(f"Colormap '{name}' 未找到")

    def show_palette(self, name: str = 'default') -> None:
        """展示调色板颜色"""
        if name not in self.palettes:
            raise ValueError(f"调色板 '{name}' 未找到")
        
        colors = self.palettes[name]
        fig, ax = plt.subplots(figsize=(10, 1))
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
        
        ax.set_xlim(0, len(colors))
        ax.set_ylim(0, 1)
        ax.set_xticks([i + 0.5 for i in range(len(colors))])
        ax.set_xticklabels([f"{i}: {color}" for i, color in enumerate(colors)])
        ax.set_yticks([])
        ax.set_title(f"调色板: {name}")
        plt.show()

    def show_all_palettes(self) -> None:
        """展示所有调色板"""
        fig, axes = plt.subplots(len(self.palettes), 1, figsize=(10, len(self.palettes)))
        
        for i, (name, colors) in enumerate(self.palettes.items()):
            ax = axes[i]
            for j, color in enumerate(colors):
                ax.add_patch(plt.Rectangle((j, 0), 1, 1, color=color))
            
            ax.set_xlim(0, max(len(palette) for palette in self.palettes.values()))
            ax.set_ylim(0, 1)
            ax.set_yticks([])
            ax.set_title(name)
        
        plt.tight_layout()
        plt.show()

    def show_gradient(self, name: str, n: int = 10) -> None:
        """展示渐变色"""
        if name not in self.gradients:
            raise ValueError(f"渐变色 '{name}' 未找到")
        
        colors = self.get_gradient(name, n)
        fig, ax = plt.subplots(figsize=(10, 1))
        for i, color in enumerate(colors):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
        
        ax.set_xlim(0, len(colors))
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title(f"渐变色: {name}")
        plt.show()

# 创建全局颜色管理器实例
colors = ColorManager()