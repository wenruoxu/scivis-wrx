"""
图表元素管理模块 - 提供各种图表元素的标准化设置和创建方法
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Dict, List, Tuple, Union, Optional, Any, Callable
from .colors import colors
from matplotlib.legend import Legend
from matplotlib.colorbar import Colorbar

class ElementManager:
    """图表元素管理器类"""
    
    def __init__(self):
        # 存储预设的标注样式
        self.annotation_styles = {
            'default': {
                'xytext': (0, 10),
                'textcoords': 'offset points',
                'fontsize': 10,
                'color': colors.get_color('foreground'),
                'ha': 'center',
                'va': 'bottom',
                'bbox': dict(boxstyle='round,pad=0.3', fc='white', ec='gray', alpha=0.7),
                'arrowprops': dict(arrowstyle='->', connectionstyle='arc3,rad=0', color='gray'),
            },
            'simple': {
                'xytext': (0, 10),
                'textcoords': 'offset points',
                'fontsize': 10,
                'color': colors.get_color('foreground'),
                'ha': 'center',
                'va': 'bottom',
            },
            'flagpole': {
                'xytext': (0, 15),
                'textcoords': 'offset points',
                'fontsize': 10,
                'color': colors.get_color('foreground'),
                'ha': 'center',
                'va': 'bottom',
                'arrowprops': dict(arrowstyle='-', color='gray'),
            },
            'callout': {
                'xytext': (30, 20),
                'textcoords': 'offset points',
                'fontsize': 10,
                'color': colors.get_color('foreground'),
                'ha': 'left',
                'va': 'center',
                'bbox': dict(boxstyle='round,pad=0.5', fc='white', ec='gray', alpha=0.7),
                'arrowprops': dict(arrowstyle='fancy', connectionstyle='arc3,rad=0.3', color='gray'),
            }
        }
        
        # 存储预设的文本框样式
        self.textbox_styles = {
            'default': {
                'fontsize': 10,
                'color': colors.get_color('foreground'),
                'bbox': dict(boxstyle='round,pad=0.5', fc='white', ec='gray', alpha=0.7),
            },
            'clean': {
                'fontsize': 10,
                'color': colors.get_color('foreground'),
                'bbox': dict(boxstyle='round,pad=0.3', fc='white', ec='white', alpha=0.5),
            },
            'highlight': {
                'fontsize': 11,
                'color': 'white',
                'weight': 'bold',
                'bbox': dict(boxstyle='round,pad=0.5', fc=colors.get_color('accent'), ec='none', alpha=0.9),
            },
            'info': {
                'fontsize': 9,
                'color': colors.get_color('foreground'),
                'style': 'italic',
                'bbox': dict(boxstyle='round,pad=0.3', fc='#e5f5fd', ec='#a8d7fd', alpha=0.9),
            }
        }
        
        # 存储预设的网格样式
        self.grid_styles = {
            'default': {
                'visible': True,
                'color': '#dddddd',
                'linestyle': '-',
                'linewidth': 0.5,
                'alpha': 0.5,
            },
            'dashed': {
                'visible': True,
                'color': '#cccccc',
                'linestyle': '--',
                'linewidth': 0.5,
                'alpha': 0.7,
            },
            'dotted': {
                'visible': True,
                'color': '#888888',
                'linestyle': ':',
                'linewidth': 0.5,
                'alpha': 0.5,
            },
            'none': {
                'visible': False,
            },
            'subtle': {
                'visible': True,
                'color': '#eeeeee',
                'linestyle': '-',
                'linewidth': 0.5,
                'alpha': 0.3,
            }
        }
        
        # 存储预设的标签样式
        self.label_styles = {
            'default': {
                'fontsize': 10,
                'color': colors.get_color('foreground'),
                'weight': 'normal',
            },
            'bold': {
                'fontsize': 10,
                'color': colors.get_color('foreground'),
                'weight': 'bold',
            },
            'large': {
                'fontsize': 12,
                'color': colors.get_color('foreground'),
                'weight': 'normal',
            },
            'highlight': {
                'fontsize': 10,
                'color': colors.get_color('accent'),
                'weight': 'bold',
            }
        }
        
        # 存储预设的图例样式
        self.legend_styles = {
            'default': {
                'loc': 'best',
                'frameon': True,
                'framealpha': 0.8,
                'facecolor': 'white',
                'edgecolor': colors.get_color('foreground_alt'),
            },
            'outside': {
                'loc': 'center left',
                'bbox_to_anchor': (1.05, 0.5),
                'frameon': True,
                'framealpha': 0.8,
                'facecolor': 'white',
                'edgecolor': colors.get_color('foreground_alt'),
            },
            'minimal': {
                'loc': 'best',
                'frameon': False,
            },
            'boxed': {
                'loc': 'best',
                'frameon': True,
                'framealpha': 1.0,
                'facecolor': 'white',
                'edgecolor': 'black',
                'shadow': True,
            }
        }
        
        # 标准线型
        self.line_styles = {
            'solid': '-',
            'dashed': '--',
            'dotted': ':',
            'dash_dot': '-.',
            'marker_only': '',
        }
        
        # 标准标记类型
        self.marker_styles = {
            'circle': 'o',
            'square': 's',
            'triangle': '^',
            'diamond': 'D',
            'plus': '+',
            'x': 'x',
            'star': '*',
            'dot': '.',
            'none': '',
        }

    def add_annotation(self, ax: plt.Axes, x: float, y: float, text: str, 
                       style: str = 'default', **kwargs) -> plt.Annotation:
        """添加标注"""
        if style not in self.annotation_styles:
            raise ValueError(f"标注样式 '{style}' 未找到")
        
        # 获取预设样式
        style_params = self.annotation_styles[style].copy()
        
        # 更新自定义参数
        style_params.update(kwargs)
        
        # 创建标注
        annotation = ax.annotate(text, xy=(x, y), **style_params)
        
        return annotation
    
    def add_textbox(self, ax: plt.Axes, x: float, y: float, text: str, 
                    style: str = 'default', **kwargs) -> plt.Text:
        """添加文本框"""
        if style not in self.textbox_styles:
            raise ValueError(f"文本框样式 '{style}' 未找到")
        
        # 获取预设样式
        style_params = self.textbox_styles[style].copy()
        
        # 更新自定义参数
        style_params.update(kwargs)
        
        # 创建文本
        text_obj = ax.text(x, y, text, **style_params)
        
        return text_obj
    
    def set_grid(self, ax: plt.Axes, style: str = 'default', 
                 which: str = 'major', axis: str = 'both') -> None:
        """设置网格"""
        if style not in self.grid_styles:
            raise ValueError(f"网格样式 '{style}' 未找到")
        
        # 获取网格样式
        grid_params = self.grid_styles[style].copy()
        
        # 移除visible参数，因为我们总是显示网格
        visible = grid_params.pop('visible', True)
        
        if visible:
            # 应用网格，不传递visible参数
            ax.grid(True, which=which, axis=axis, **grid_params)
        else:
            # 关闭网格
            ax.grid(False)
    
    def set_labels(self, ax: plt.Axes, title: Optional[str] = None, 
                   xlabel: Optional[str] = None, ylabel: Optional[str] = None, 
                   style: str = 'default') -> None:
        """设置轴标签"""
        if style not in self.label_styles:
            raise ValueError(f"标签样式 '{style}' 未找到")
        
        # 获取标签样式
        label_params = self.label_styles[style].copy()
        
        # 设置标题
        if title is not None:
            ax.set_title(title, fontsize=label_params.get('fontsize') + 2, 
                         color=label_params.get('color'), 
                         weight=label_params.get('weight'))
        
        # 设置X轴标签
        if xlabel is not None:
            ax.set_xlabel(xlabel, **label_params)
        
        # 设置Y轴标签
        if ylabel is not None:
            ax.set_ylabel(ylabel, **label_params)
    
    def set_legend(self, ax: plt.Axes, style: str = 'default', **kwargs) -> Legend:
        """设置图例"""
        if style not in self.legend_styles:
            raise ValueError(f"图例样式 '{style}' 未找到")
        
        # 获取图例样式
        legend_params = self.legend_styles[style].copy()
        
        # 更新自定义参数
        legend_params.update(kwargs)
        
        # 创建图例
        legend = ax.legend(**legend_params)
        
        return legend
    
    def get_line_style(self, style: str) -> str:
        """获取线型"""
        if style not in self.line_styles:
            raise ValueError(f"线型 '{style}' 未找到")
        return self.line_styles[style]
    
    def get_marker_style(self, style: str) -> str:
        """获取标记样式"""
        if style not in self.marker_styles:
            raise ValueError(f"标记样式 '{style}' 未找到")
        return self.marker_styles[style]
    
    def style_axis(self, ax: plt.Axes, spines: bool = True, 
                   spine_top: bool = False, spine_right: bool = False) -> None:
        """设置坐标轴样式"""
        # 设置轴线可见性
        if not spines:
            # 隐藏所有坐标轴线
            for spine in ax.spines.values():
                spine.set_visible(False)
        else:
            # 隐藏顶部和右侧轴线（如果需要）
            if not spine_top:
                ax.spines['top'].set_visible(False)
            if not spine_right:
                ax.spines['right'].set_visible(False)
    
    def clean_ticks(self, ax: plt.Axes, x: bool = True, y: bool = True) -> None:
        """简化刻度"""
        if x:
            # 简化X轴刻度
            ax.tick_params(axis='x', length=0)
            ax.xaxis.set_ticks_position('none')
        if y:
            # 简化Y轴刻度
            ax.tick_params(axis='y', length=0)
            ax.yaxis.set_ticks_position('none')
    
    def add_custom_annotation_style(self, name: str, style_params: Dict[str, Any]) -> None:
        """添加自定义标注样式"""
        self.annotation_styles[name] = style_params
    
    def add_custom_textbox_style(self, name: str, style_params: Dict[str, Any]) -> None:
        """添加自定义文本框样式"""
        self.textbox_styles[name] = style_params
    
    def add_custom_grid_style(self, name: str, style_params: Dict[str, Any]) -> None:
        """添加自定义网格样式"""
        self.grid_styles[name] = style_params
    
    def add_custom_label_style(self, name: str, style_params: Dict[str, Any]) -> None:
        """添加自定义标签样式"""
        self.label_styles[name] = style_params
    
    def add_custom_legend_style(self, name: str, style_params: Dict[str, Any]) -> None:
        """添加自定义图例样式"""
        self.legend_styles[name] = style_params
    
    def style_spines(self, ax: plt.Axes, color: str = None, width: float = None,
                     visible: Dict[str, bool] = None) -> None:
        """设置轴线样式"""
        # 默认所有轴线可见
        if visible is None:
            visible = {'top': True, 'right': True, 'bottom': True, 'left': True}
        
        # 遍历所有轴线
        for pos, spine in ax.spines.items():
            # 设置可见性
            if pos in visible:
                spine.set_visible(visible[pos])
            
            # 设置颜色
            if color is not None:
                spine.set_color(color)
            
            # 设置宽度
            if width is not None:
                spine.set_linewidth(width)
    
    def create_watermark(self, fig: plt.Figure, text: str, alpha: float = 0.1, 
                         fontsize: int = 20, color: str = 'gray', 
                         rotation: float = 30) -> plt.Text:
        """添加水印"""
        # 获取图表中心位置
        watermark = fig.text(0.5, 0.5, text, 
                            fontsize=fontsize, 
                            color=color, 
                            alpha=alpha, 
                            ha='center', 
                            va='center', 
                            rotation=rotation, 
                            transform=fig.transFigure)
        return watermark
    
    def add_subplot_labels(self, fig: plt.Figure, axes: List[plt.Axes], 
                           labels: List[str] = None, pos: Tuple[float, float] = (-0.1, 1.05),
                           fontsize: int = 12, weight: str = 'bold', 
                           **kwargs) -> List[plt.Text]:
        """为子图添加标签（例如 'A', 'B', 'C'）"""
        texts = []
        
        # 生成默认标签（如果未提供）
        if labels is None:
            labels = [chr(65 + i) for i in range(len(axes))]  # A, B, C...
        
        # 确保标签数量与子图数量一致
        if len(labels) != len(axes):
            raise ValueError("标签数量必须与子图数量一致")
        
        # 添加标签
        for ax, label in zip(axes, labels):
            text = ax.text(pos[0], pos[1], label, 
                          transform=ax.transAxes, 
                          fontsize=fontsize, 
                          weight=weight, 
                          **kwargs)
            texts.append(text)
        
        return texts
    
    def add_colorbar(self, fig: plt.Figure, mappable, ax: plt.Axes = None, 
                     orientation: str = 'vertical', pad: float = 0.1, 
                     size: str = '5%', label: str = None, **kwargs) -> Colorbar:
        """添加颜色条"""
        # 创建颜色条
        if ax is None:
            cbar = fig.colorbar(mappable, orientation=orientation, pad=pad, **kwargs)
        else:
            # 为特定轴添加颜色条
            from mpl_toolkits.axes_grid1 import make_axes_locatable
            divider = make_axes_locatable(ax)
            
            if orientation == 'vertical':
                cax = divider.append_axes('right', size=size, pad=pad)
            else:
                cax = divider.append_axes('bottom', size=size, pad=pad)
            
            cbar = fig.colorbar(mappable, cax=cax, orientation=orientation, **kwargs)
        
        # 设置标签
        if label is not None:
            cbar.set_label(label)
        
        return cbar

# 创建全局元素管理器实例
elements = ElementManager()