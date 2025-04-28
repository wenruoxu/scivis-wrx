"""
主题管理模块 - 管理所有绘图风格和主题设置
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from typing import Dict, List, Tuple, Union, Optional, Any
from .colors import colors

class Theme:
    """图表主题类"""
    def __init__(self, name: str, params: Dict[str, Any]):
        self.name = name
        self.params = params
    
    def apply(self) -> None:
        """应用主题到matplotlib rcParams"""
        for key, value in self.params.items():
            plt.rcParams[key] = value

class ThemeManager:
    """主题管理器类"""
    def __init__(self):
        # 存储主题
        self.themes = {}
        
        # 初始化内置主题
        self._init_default_themes()
        
        # 当前主题
        self.current_theme = None
    
    def _init_default_themes(self) -> None:
        """初始化默认主题"""
        # 清爽现代主题
        clean_theme = {
            # 字体设置
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'DejaVu Sans', 'Helvetica', 'sans-serif'],
            'font.size': 10,
            
            # 图表元素
            'figure.facecolor': colors.get_color('background'),
            'figure.edgecolor': colors.get_color('background'),
            'figure.figsize': (8, 6),
            'figure.dpi': 100,
            
            # 轴设置
            'axes.facecolor': colors.get_color('background'),
            'axes.edgecolor': colors.get_color('foreground'),
            'axes.linewidth': 1.0,
            'axes.grid': True,
            'axes.titlesize': 14,
            'axes.titleweight': 'bold',
            'axes.labelsize': 12,
            'axes.labelweight': 'normal',
            'axes.labelcolor': colors.get_color('foreground'),
            'axes.axisbelow': True,
            'axes.spines.top': False,
            'axes.spines.right': False,
            
            # 网格设置
            'grid.color': '#dddddd',
            'grid.linestyle': '-',
            'grid.linewidth': 0.5,
            'grid.alpha': 0.5,
            
            # 刻度设置
            'xtick.color': colors.get_color('foreground'),
            'ytick.color': colors.get_color('foreground'),
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'xtick.direction': 'out',
            'ytick.direction': 'out',
            'xtick.major.size': 4.0,
            'ytick.major.size': 4.0,
            'xtick.minor.size': 2.0,
            'ytick.minor.size': 2.0,
            
            # 图例设置
            'legend.fancybox': True,
            'legend.frameon': True,
            'legend.framealpha': 0.8,
            'legend.fontsize': 10,
            'legend.edgecolor': colors.get_color('foreground_alt'),
            
            # 保存图片设置
            'savefig.dpi': 300,
            'savefig.format': 'png',
            'savefig.bbox': 'tight',
            'savefig.pad_inches': 0.1,
            
            # 默认样式
            'lines.linewidth': 2,
            'lines.markersize': 8,
            'scatter.marker': 'o',
            
            # 柱状图设置
            'patch.edgecolor': 'none',
            'patch.linewidth': 0,
            
            # 默认调色板
            'axes.prop_cycle': plt.cycler('color', colors.get_palette('default')),
        }
        
        # 学术期刊主题
        academic_theme = clean_theme.copy()
        academic_theme.update({
            'font.family': 'serif',
            'font.serif': ['Times New Roman', 'DejaVu Serif', 'serif'],
            'font.size': 11,
            'figure.figsize': (6, 4.5),  # 期刊常用比例
            'axes.titlesize': 12,
            'axes.labelsize': 11,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'lines.linewidth': 1.5,
            'lines.markersize': 6,
            'axes.spines.top': True,
            'axes.spines.right': True,
            'axes.grid': False,
            'axes.prop_cycle': plt.cycler('color', colors.get_palette('scientific')),
        })
        
        # 暗色主题
        dark_theme = clean_theme.copy()
        dark_bg = '#1e1e1e'
        dark_text = '#e0e0e0'
        dark_grid = '#333333'
        dark_theme.update({
            'figure.facecolor': dark_bg,
            'figure.edgecolor': dark_bg,
            'axes.facecolor': dark_bg,
            'axes.edgecolor': dark_text,
            'axes.labelcolor': dark_text,
            'xtick.color': dark_text,
            'ytick.color': dark_text,
            'grid.color': dark_grid,
            'text.color': dark_text,
            'legend.edgecolor': dark_grid,
            'savefig.facecolor': dark_bg,
            'savefig.edgecolor': dark_bg,
            'axes.prop_cycle': plt.cycler('color', colors.get_palette('vibrant')),
        })
        
        # 演示主题 (适合幻灯片)
        presentation_theme = clean_theme.copy()
        presentation_theme.update({
            'font.size': 14,
            'figure.figsize': (10, 6),
            'axes.titlesize': 18,
            'axes.labelsize': 16,
            'xtick.labelsize': 14,
            'ytick.labelsize': 14,
            'legend.fontsize': 14,
            'lines.linewidth': 3,
            'lines.markersize': 10,
            'axes.prop_cycle': plt.cycler('color', colors.get_palette('vibrant')),
        })
        
        # 添加主题
        self.add_theme('clean', clean_theme)
        self.add_theme('academic', academic_theme)
        self.add_theme('dark', dark_theme)
        self.add_theme('presentation', presentation_theme)
    
    def add_theme(self, name: str, params: Dict[str, Any]) -> None:
        """添加新主题"""
        self.themes[name] = Theme(name, params)
    
    def get_theme(self, name: str) -> Theme:
        """获取主题"""
        if name not in self.themes:
            raise ValueError(f"主题 '{name}' 未找到")
        return self.themes[name]
    
    def apply_theme(self, name: str) -> None:
        """应用主题"""
        theme = self.get_theme(name)
        theme.apply()
        self.current_theme = name
        print(f"已应用主题: {name}")
    
    def modify_theme(self, name: str, params: Dict[str, Any]) -> None:
        """修改现有主题"""
        if name not in self.themes:
            raise ValueError(f"主题 '{name}' 未找到")
        
        theme = self.themes[name]
        theme.params.update(params)
        
        # 如果修改的是当前主题，立即应用更改
        if self.current_theme == name:
            theme.apply()
    
    def create_custom_theme(self, name: str, base_theme: str, custom_params: Dict[str, Any]) -> None:
        """基于现有主题创建自定义主题"""
        if base_theme not in self.themes:
            raise ValueError(f"基础主题 '{base_theme}' 未找到")
        
        # 复制基础主题参数
        base_params = self.themes[base_theme].params.copy()
        
        # 更新自定义参数
        base_params.update(custom_params)
        
        # 添加新主题
        self.add_theme(name, base_params)
    
    def reset_to_defaults(self) -> None:
        """重置为matplotlib默认设置"""
        mpl.rcParams.update(mpl.rcParamsDefault)
        self.current_theme = None
        print("已重置为默认设置")
    
    def list_themes(self) -> List[str]:
        """列出所有可用主题"""
        return list(self.themes.keys())
    
    def get_current_theme(self) -> Optional[str]:
        """获取当前主题名称"""
        return self.current_theme
    
    def preview_theme(self, name: str) -> None:
        """预览主题效果"""
        if name not in self.themes:
            raise ValueError(f"主题 '{name}' 未找到")
        
        # 保存当前设置
        current_params = dict(plt.rcParams)
        
        # 临时应用要预览的主题
        self.themes[name].apply()
        
        # 创建示例图
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # 示例线图
        x = [1, 2, 3, 4, 5]
        ax1.plot(x, [i**2 for i in x], label='y = x^2')
        ax1.plot(x, [i**1.5 for i in x], label='y = x^1.5')
        ax1.plot(x, [i for i in x], label='y = x')
        ax1.set_title('示例线图')
        ax1.set_xlabel('X轴')
        ax1.set_ylabel('Y轴')
        ax1.legend()
        
        # 示例柱状图
        ax2.bar(x, [i**1.5 for i in x])
        ax2.set_title('示例柱状图')
        ax2.set_xlabel('类别')
        ax2.set_ylabel('数值')
        
        plt.suptitle(f'主题预览: {name}', fontsize=16)
        plt.tight_layout()
        plt.show()
        
        # 恢复之前的设置
        for key, value in current_params.items():
            plt.rcParams[key] = value

# 创建全局主题管理器实例
themes = ThemeManager()