"""
scivis - 科研绘图环境一体化管理系统
==================================

提供统一、系统化的Python科研绘图工具，帮助科研人员创建高质量、风格一致的可视化图表。

主要模块:
- colors: 颜色管理
- themes: 主题管理
- elements: 图表元素管理
- presets: 预设组合管理
- utils: 工具函数

使用示例:
    
    import scivis as sv
    
    # 应用主题
    sv.themes.apply_theme('academic')
    
    # 创建图表
    fig, ax = sv.presets.apply_preset('line_academic', 
                                     title="实验结果", 
                                     xlabel="时间 (s)", 
                                     ylabel="温度 (°C)")
    
    # 绘制数据
    x = [0, 1, 2, 3, 4, 5]
    y = [20, 23, 25, 28, 32, 35]
    ax.plot(x, y, color=sv.colors.get_color('primary'), 
           marker=sv.elements.get_marker_style('circle'))
    
    # 添加注释
    sv.elements.add_annotation(ax, 5, 35, "峰值", style='callout')
    
    # 保存图表
    sv.utils.save_figure(fig, "experiment_results.png")

"""

# 导入主要组件
from .colors import colors
from .themes import themes
from .elements import elements
from .presets import presets
from .utils import utils, figure_manager, data_preprocessor, style_exporter, setup_chinese_font

# 版本信息
__version__ = '0.1.0'

# 设置中文字体支持
setup_chinese_font()