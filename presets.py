"""
预设组合模块 - 提供常用的图表预设和复合图表样式
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from typing import Dict, List, Tuple, Union, Optional, Any, Callable
from .colors import colors
from .themes import themes
from .elements import elements

class Preset:
    """图表预设类"""
    def __init__(self, name: str, setup_func: Callable):
        self.name = name
        self.setup_func = setup_func
    
    def apply(self, *args, **kwargs):
        """应用预设"""
        return self.setup_func(*args, **kwargs)

class PresetManager:
    """预设管理器类"""
    def __init__(self):
        # 存储图表预设
        self.presets = {}
        
        # 初始化内置预设
        self._init_default_presets()
    
    def _init_default_presets(self):
        """初始化默认预设"""
        # 基础线图预设
        self.add_preset('line_basic', self._setup_line_basic)
        
        # 科研论文线图预设
        self.add_preset('line_academic', self._setup_line_academic)
        
        # 对比柱状图预设
        self.add_preset('bar_comparison', self._setup_bar_comparison)
        
        # 堆叠柱状图预设
        self.add_preset('bar_stacked', self._setup_bar_stacked)
        
        # 散点图预设
        self.add_preset('scatter_basic', self._setup_scatter_basic)
        
        # 箱线图预设
        self.add_preset('boxplot_basic', self._setup_boxplot_basic)
        
        # 热图预设
        self.add_preset('heatmap_basic', self._setup_heatmap_basic)
        
        # 饼图预设
        self.add_preset('pie_basic', self._setup_pie_basic)
        
        # 子图布局预设
        self.add_preset('multi_panel_2x2', self._setup_multi_panel_2x2)
        
        # 双Y轴图预设
        self.add_preset('dual_axis', self._setup_dual_axis)
        
        # 带趋势线的散点图预设
        self.add_preset('scatter_with_trend', self._setup_scatter_with_trend)
        
        # 简洁风格预设
        self.add_preset('minimal_style', self._setup_minimal_style)
    
    def add_preset(self, name: str, setup_func: Callable) -> None:
        """添加新预设"""
        self.presets[name] = Preset(name, setup_func)
    
    def get_preset(self, name: str) -> Preset:
        """获取预设"""
        if name not in self.presets:
            raise ValueError(f"预设 '{name}' 未找到")
        return self.presets[name]
    
    def apply_preset(self, name: str, *args, **kwargs):
        """应用预设"""
        preset = self.get_preset(name)
        return preset.apply(*args, **kwargs)
    
    def list_presets(self) -> List[str]:
        """列出所有可用预设"""
        return list(self.presets.keys())
    
    # 以下是各种预设的实现
    
    def _setup_line_basic(self, fig=None, ax=None, title=None, xlabel=None, ylabel=None, 
                          grid_style='default', legend_style='default'):
        """基础线图预设"""
        # 创建图表（如果未提供）
        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
        
        # 应用网格样式
        elements.set_grid(ax, style=grid_style)
        
        # 设置标签
        elements.set_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel, style='default')
        
        # 设置图例
        if legend_style:
            elements.set_legend(ax, style=legend_style)
        
        # 设置轴线样式
        elements.style_axis(ax, spine_top=False, spine_right=False)
        
        return fig, ax
    
    def _setup_line_academic(self, fig=None, ax=None, title=None, xlabel=None, ylabel=None):
        """科研论文线图预设"""
        # 应用学术主题
        themes.apply_theme('academic')
        
        # 创建图表（如果未提供）
        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(6, 4.5))
        
        # 设置网格（仅Y轴）
        ax.grid(True, axis='y', linestyle='--', alpha=0.7, zorder=0)
        
        # 设置标签
        elements.set_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel, style='bold')
        
        # 设置图例
        elements.set_legend(ax, style='default', framealpha=0.9)
        
        # 让所有轴线可见
        elements.style_axis(ax, spine_top=True, spine_right=True)
        
        return fig, ax
    
    def _setup_bar_comparison(self, fig=None, ax=None, title=None, xlabel=None, ylabel=None, 
                             bar_width=0.8, grid_style='default'):
        """对比柱状图预设"""
        # 创建图表（如果未提供）
        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
        
        # 应用网格样式（仅Y轴）
        if grid_style:
            elements.set_grid(ax, style=grid_style, axis='y')
            ax.set_axisbelow(True)  # 确保网格线在数据下方
        
        # 设置标签
        elements.set_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel, style='default')
        
        # 设置轴线样式
        elements.style_axis(ax, spine_top=False, spine_right=False)
        
        # 设置图例
        elements.set_legend(ax, style='default')
        
        return fig, ax, bar_width
    
    def _setup_bar_stacked(self, fig=None, ax=None, title=None, xlabel=None, ylabel=None):
        """堆叠柱状图预设"""
        # 创建图表（如果未提供）
        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
        
        # 应用网格样式（仅Y轴）
        elements.set_grid(ax, style='subtle', axis='y')
        ax.set_axisbelow(True)  # 确保网格线在数据下方
        
        # 设置标签
        elements.set_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel, style='default')
        
        # 设置轴线样式
        elements.style_axis(ax, spine_top=False, spine_right=False)
        
        # 设置图例
        elements.set_legend(ax, style='outside')
        
        return fig, ax
    
    def _setup_scatter_basic(self, fig=None, ax=None, title=None, xlabel=None, ylabel=None,
                            marker='o', alpha=0.7, s=50):
        """散点图预设"""
        # 创建图表（如果未提供）
        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
        
        # 应用网格样式
        elements.set_grid(ax, style='dashed')
        
        # 设置标签
        elements.set_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel, style='default')
        
        # 设置轴线样式
        elements.style_axis(ax, spine_top=False, spine_right=False)
        
        # 配置散点属性
        scatter_params = {
            'marker': marker,
            'alpha': alpha,
            's': s,
        }
        
        return fig, ax, scatter_params
    
    def _setup_boxplot_basic(self, fig=None, ax=None, title=None, xlabel=None, ylabel=None,
                            grid_style='dashed', box_width=0.6):
        """箱线图预设"""
        # 创建图表（如果未提供）
        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
        
        # 应用网格样式（仅Y轴）
        if grid_style:
            ax.grid(True, axis='y', **elements.grid_styles[grid_style])
            ax.set_axisbelow(True)  # 确保网格线在数据下方
        
        # 设置标签
        elements.set_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel, style='default')
        
        # 设置轴线样式
        elements.style_axis(ax, spine_top=False, spine_right=False)
        
        # 箱线图参数
        boxplot_params = {
            'boxprops': {'facecolor': 'lightblue', 'alpha': 0.8},
            'medianprops': {'color': 'red'},
            'whiskerprops': {'linestyle': '--'},
            'capprops': {'linestyle': '-'},
            'widths': box_width,
            'showfliers': True,
            'flierprops': {'marker': 'o', 'markerfacecolor': 'red', 'markersize': 4, 'alpha': 0.7},
        }
        
        return fig, ax, boxplot_params
    
    def _setup_heatmap_basic(self, fig=None, ax=None, title=None, xlabel=None, ylabel=None,
                            cmap='Blues', annot=True):
        """热图预设"""
        # 创建图表（如果未提供）
        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))
        
        # 设置标签
        elements.set_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel, style='default')
        
        # 热图参数
        heatmap_params = {
            'cmap': cmap,
            'annot': annot,
            'fmt': '.2f',
            'linewidths': 0.5,
            'cbar_kws': {'shrink': 0.8},
        }
        
        return fig, ax, heatmap_params
    
    def _setup_pie_basic(self, fig=None, ax=None, title=None, explode=None, 
                        autopct='%1.1f%%', startangle=90, shadow=False):
        """饼图预设"""
        # 创建图表（如果未提供）
        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(8, 8))
        
        # 设置标题
        if title:
            ax.set_title(title, fontsize=14, weight='bold')
        
        # 确保图形是圆形的
        ax.axis('equal')
        
        # 饼图参数
        pie_params = {
            'explode': explode,
            'autopct': autopct,
            'startangle': startangle,
            'shadow': shadow,
            'colors': colors.get_palette('pastel'),
            'wedgeprops': {'edgecolor': 'w', 'linewidth': 1},
            'textprops': {'fontsize': 10},
        }
        
        return fig, ax, pie_params
    
    def _setup_multi_panel_2x2(self, figsize=(10, 8), sharex=False, sharey=False, 
                             title=None, tight_layout=True, add_labels=True):
        """2x2子图布局预设"""
        # 创建图表
        fig, axes = plt.subplots(2, 2, figsize=figsize, sharex=sharex, sharey=sharey)
        axes = axes.flatten()  # 扁平化轴数组以便于访问
        
        # 设置整体标题
        if title:
            fig.suptitle(title, fontsize=16, weight='bold', y=0.98)
        
        # 为每个子图设置基本样式
        for ax in axes:
            elements.set_grid(ax, style='subtle')
            elements.style_axis(ax, spine_top=False, spine_right=False)
        
        # 添加子图标签
        if add_labels:
            elements.add_subplot_labels(fig, axes)
        
        # 应用紧凑布局
        if tight_layout:
            fig.tight_layout()
            if title:
                # 为标题留出空间
                plt.subplots_adjust(top=0.9)
        
        return fig, axes
    
    def _setup_dual_axis(self, fig=None, ax=None, ax1=None, title=None, xlabel=None, 
                        y1label=None, y2label=None, color1=None, color2=None):
        """双Y轴图预设"""
        # 处理 ax 和 ax1 参数
        if ax is not None and ax1 is None:
            ax1 = ax
        
        # 创建主图表（如果未提供）
        if fig is None and ax1 is None:
            fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # 创建次坐标轴
        ax2 = ax1.twinx()
        
        # 设置标签
        if title:
            ax1.set_title(title, fontsize=14, weight='bold')
        if xlabel:
            ax1.set_xlabel(xlabel, fontsize=12)
        if y1label:
            ax1.set_ylabel(y1label, fontsize=12, color=color1 if color1 else colors.get_color('primary'))
        if y2label:
            ax2.set_ylabel(y2label, fontsize=12, color=color2 if color2 else colors.get_color('secondary'))
        
        # 设置刻度颜色
        if color1:
            ax1.tick_params(axis='y', colors=color1)
        if color2:
            ax2.tick_params(axis='y', colors=color2)
        
        # 设置网格（来自第一个Y轴）
        elements.set_grid(ax1, style='subtle')
        
        # 设置轴线样式
        elements.style_axis(ax1, spine_top=False, spine_right=False)
        # elements.style_axis(ax2, spine_top=False, spine_left=False)
        
        return fig, ax1, ax2
    
    def _setup_scatter_with_trend(self, fig=None, ax=None, title=None, xlabel=None, ylabel=None,
                                 marker='o', alpha=0.7, s=50, add_trend=True, 
                                 trend_order=1, trend_color='red'):
        """带趋势线的散点图预设"""
        # 获取基本散点图预设
        fig, ax, scatter_params = self._setup_scatter_basic(
            fig=fig, ax=ax, title=title, xlabel=xlabel, ylabel=ylabel,
            marker=marker, alpha=alpha, s=s
        )
        
        # 趋势线参数
        trend_params = {
            'add': add_trend,
            'order': trend_order,
            'color': trend_color,
            'linestyle': '--',
            'linewidth': 2,
        }
        
        return fig, ax, scatter_params, trend_params
    
    def _setup_minimal_style(self, fig=None, ax=None, title=None, xlabel=None, ylabel=None):
        """简洁风格预设"""
        # 创建图表（如果未提供）
        if fig is None and ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
        
        # 设置标签
        elements.set_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel, style='default')
        
        # 隐藏所有轴线
        elements.style_axis(ax, spines=False)
        
        # 简化刻度
        elements.clean_ticks(ax, x=True, y=True)
        
        # 关闭网格
        elements.set_grid(ax, style='none')
        
        # 设置图例
        elements.set_legend(ax, style='minimal')
        
        return fig, ax
    
    def create_composite_figure(self, layout_type='grid', 
                               num_plots=4, figsize=(12, 10),
                               title=None, subtitle=None,
                               tight_layout=True, add_labels=True):
        """创建复合图表布局"""

        if layout_type == 'grid':
            # 确定行列数
            ncols = int(np.ceil(np.sqrt(num_plots)))
            nrows = int(np.ceil(num_plots / ncols))
            
            # 创建网格布局
            fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
            axes = axes.flatten() if num_plots > 1 else [axes]
            
            # 隐藏多余的子图
            for i in range(num_plots, len(axes)):
                axes[i].set_visible(False)
        
        elif layout_type == 'row':
            # 所有子图在一行
            fig, axes = plt.subplots(1, num_plots, figsize=figsize)
            if num_plots == 1:
                axes = [axes]
        
        elif layout_type == 'column':
            # 所有子图在一列
            fig, axes = plt.subplots(num_plots, 1, figsize=figsize)
            if num_plots == 1:
                axes = [axes]
        
        elif layout_type == 'irregular':
            # 创建不规则布局（示例：2x2布局，左上格子占据2格）
            from matplotlib.gridspec import GridSpec
            fig = plt.figure(figsize=figsize)
            gs = GridSpec(2, 2, figure=fig)
            
            # 创建轴列表
            axes = []
            
            # 左上方大格子
            axes.append(fig.add_subplot(gs[0, 0]))
            
            # 其他格子
            axes.append(fig.add_subplot(gs[0, 1]))
            axes.append(fig.add_subplot(gs[1, 0]))
            axes.append(fig.add_subplot(gs[1, 1]))
            
            # 限制轴数量
            axes = axes[:num_plots]
        
        else:
            raise ValueError(f"不支持的布局类型 '{layout_type}'")
        
        # 设置整体标题
        if title:
            fig.suptitle(title, fontsize=16, weight='bold', y=0.98)
            if subtitle:
                # 添加副标题
                fig.text(0.5, 0.94, subtitle, ha='center', fontsize=12, style='italic')
        
        # 添加子图标签
        if add_labels:
            elements.add_subplot_labels(fig, axes)
        
        # 应用紧凑布局
        if tight_layout:
            plt.tight_layout()
            if title:
                # 为标题留出空间
                plt.subplots_adjust(top=0.9)
        
        return fig, axes

# 创建全局预设管理器实例
presets = PresetManager()