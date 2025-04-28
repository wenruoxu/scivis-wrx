# Scivis - 科研绘图环境一体化管理系统使用指南

## 1. 介绍

Scivis是一个为科研绘图设计的Python包，提供了统一、系统化的绘图环境，帮助科研人员创建高质量、风格一致的可视化图表。该系统管理颜色、主题、图表元素和预设样式，简化了科研绘图的工作流程。

### 主要特点

- **统一的颜色管理**：预设调色板、色彩角色定义和渐变色管理
- **一致的主题系统**：适用于不同场景的主题预设，如学术论文、演示文稿等
- **标准化的图表元素**：统一的网格、标注、标签和图例样式
- **预设组合**：常用的图表类型和布局预设
- **实用工具**：工作流管理、图表导出、样式定制等辅助功能

## 2. 安装

### 从源码安装

```bash
git clone https://github.com/yourusername/scivis.git
cd scivis
pip install -e .
```

### 依赖项

Scivis依赖以下Python包：

- matplotlib
- numpy
- pandas
- scipy (可选，用于某些高级分析功能)

## 3. 快速入门

### 基本用法示例

```python
import matplotlib.pyplot as plt
import numpy as np
import scivis as sv

# 应用主题
sv.themes.apply_theme('clean')

# 创建图表
fig, ax = plt.subplots(figsize=(8, 5))

# 使用颜色系统
primary_color = sv.colors.get_color('primary')
secondary_color = sv.colors.get_color('secondary')

# 绘制数据
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

ax.plot(x, y1, color=primary_color, label='sin(x)')
ax.plot(x, y2, color=secondary_color, label='cos(x)')

# 设置标签
sv.elements.set_labels(ax, title="基本波形图", xlabel="X", ylabel="Y")

# 设置网格
sv.elements.set_grid(ax, style='default')

# 设置图例
sv.elements.set_legend(ax, style='default')

# 保存图表
sv.utils.save_figure(fig, "basic_example.png")

# 显示图表
plt.show()
```

### 使用预设组合

```python
import matplotlib.pyplot as plt
import numpy as np
import scivis as sv

# 应用学术主题
sv.themes.apply_theme('academic')

# 使用学术线图预设
fig, ax = sv.presets.apply_preset('line_academic', 
                               title="实验结果", 
                               xlabel="时间 (s)", 
                               ylabel="温度 (°C)")

# 绘制数据
x = np.linspace(0, 10, 50)
y = np.sin(x) * np.exp(-0.1 * x)
ax.plot(x, y, marker='o', markersize=4)

# 添加注释
sv.elements.add_annotation(ax, 2, np.sin(2) * np.exp(-0.1 * 2), 
                         "峰值", style='callout')

# 保存图表
sv.utils.save_figure(fig, "academic_example.png", dpi=300)

# 显示图表
plt.show()
```

## 4. 模块详解

### 4.1 颜色管理 (colors)

颜色管理模块提供了统一的颜色定义和调色板管理。

#### 主要功能

- **基础颜色**：获取定义好的基础颜色
- **调色板**：使用预设的调色板或创建自定义调色板
- **渐变色**：获取渐变色列表或创建自定义渐变
- **颜色角色**：获取具有特定语义角色的颜色（如主体、背景、强调等）

#### 示例

```python
# 获取基础颜色
primary = sv.colors.get_color('primary')
accent = sv.colors.get_color('accent')

# 获取调色板
palette = sv.colors.get_palette('vibrant', n=5)

# 获取渐变色
gradient = sv.colors.get_gradient('blues', n=10)

# 创建自定义调色板
sv.colors.create_custom_palette('my_palette', 
                              ['#ff0000', '#00ff00', '#0000ff'])

# 更新颜色角色
sv.colors.update_role('highlight', '#ff5500')

# 显示调色板
sv.colors.show_palette('default')
```

### 4.2 主题管理 (themes)

主题管理模块提供了整体图表风格的预设和管理功能。

#### 主要功能

- **预设主题**：应用内置主题
- **自定义主题**：创建和修改主题
- **预览主题**：查看主题效果

#### 示例

```python
# 应用预设主题
sv.themes.apply_theme('academic')

# 创建自定义主题
sv.themes.create_custom_theme('my_theme', 'clean', {
    'font.family': 'serif',
    'font.size': 12,
    'axes.grid': True,
    'grid.alpha': 0.3,
})

# 修改主题参数
sv.themes.modify_theme('my_theme', {
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# 预览主题
sv.themes.preview_theme('my_theme')
```

### 4.3 图表元素 (elements)

图表元素模块提供了标准化的图表元素样式和设置。

#### 主要功能

- **标注**：添加带有预设样式的标注
- **文本框**：添加样式化的文本框
- **网格**：应用预设网格样式
- **标签**：设置标题和轴标签样式
- **图例**：应用预设图例样式
- **轴线**：自定义轴线可见性和样式

#### 示例

```python
# 添加标注
sv.elements.add_annotation(ax, 5, 10, "最大值", style='callout')

# 添加文本框
sv.elements.add_textbox(ax, 0.1, 0.9, "重要信息", style='highlight',
                       transform=ax.transAxes)

# 设置网格
sv.elements.set_grid(ax, style='dashed')

# 设置标签
sv.elements.set_labels(ax, title="实验结果", 
                     xlabel="时间 (s)", 
                     ylabel="温度 (°C)")

# 设置图例
sv.elements.set_legend(ax, style='outside')

# 设置轴线样式
sv.elements.style_axis(ax, spine_top=False, spine_right=False)
```

### 4.4 预设组合 (presets)

预设组合模块提供了常用图表类型和布局的预设组合。

#### 主要功能

- **基本图表预设**：线图、柱状图、散点图等预设
- **复合布局**：创建多子图布局
- **特殊图表**：双Y轴图、带趋势线的散点图等

#### 示例

```python
# 使用线图预设
fig, ax = sv.presets.apply_preset('line_basic', 
                                title="基本线图", 
                                xlabel="X", 
                                ylabel="Y")

# 使用柱状图预设
fig, ax, bar_width = sv.presets.apply_preset('bar_comparison', 
                                          title="对比柱状图")

# 使用散点图预设
fig, ax, scatter_params = sv.presets.apply_preset('scatter_basic',
                                               title="散点图")

# 创建复合图表布局
fig, axes = sv.presets.create_composite_figure(
    layout_type='grid',
    num_plots=4,
    figsize=(12, 10),
    title="复合图表布局"
)
```

### 4.5 工具函数 (utils)

工具函数模块提供了各种辅助功能，用于图表导出、数据处理和工作流管理。

#### 主要功能

- **图表保存**：保存图表为多种格式
- **图表注释**：自动添加数据标签、时间戳等
- **数据处理**：数据归一化、异常值检测等
- **工作流管理**：图表创建、更新和导出的工作流

#### 示例

```python
# 保存图表
sv.utils.save_figure(fig, "output.png", dpi=300, formats=['png', 'pdf', 'svg'])

# 为柱状图添加数据标签
sv.utils.auto_label_bars(ax, bars, fmt='{:.1f}')

# 添加时间戳
sv.utils.add_timestamp(fig, position='bottom_right')

# 添加拟合线
line, poly = sv.utils.add_fit_line(ax, x, y, order=2, 
                                 color='red', confidence_interval=True)

# 使用图表管理器
manager = sv.figure_manager
fig, ax = manager.create_figure("experiment_1")
# ... 绘制图表 ...
manager.export_figure("experiment_1", "output/exp1.png")
```

### 4.6 图表管理器 (figure_manager)

图表管理器提供了创建、存储、更新和导出多个图表的工作流管理。

#### 主要功能

- **图表创建和存储**：创建并管理多个图表
- **图表更新**：更新已存储的图表
- **批量导出**：导出所有或选定的图表
- **会话管理**：保存和恢复绘图会话

#### 示例

```python
# 创建图表
fig1, ax1 = sv.figure_manager.create_figure("temp_plot")
ax1.plot(time, temperature)
sv.elements.set_labels(ax1, title="温度变化", xlabel="时间", ylabel="温度")

# 创建另一个图表
fig2, ax2 = sv.figure_manager.create_figure("pressure_plot")
ax2.plot(time, pressure)
sv.elements.set_labels(ax2, title="压力变化", xlabel="时间", ylabel="压力")

# 更新图表
def add_grid(fig, ax):
    sv.elements.set_grid(ax, style='dashed')
    return True

sv.figure_manager.update_figure("temp_plot", add_grid)

# 导出所有图表
sv.figure_manager.export_all(formats=['png', 'pdf'], dpi=300)

# 保存会话
sv.figure_manager.save_session("my_session.pkl")
```

## 5. 进阶用法

### 5.1 创建完整的科研图表

```python
import numpy as np
import matplotlib.pyplot as plt
import scivis as sv

# 应用学术主题
sv.themes.apply_theme('academic')

# 准备数据
np.random.seed(42)
x = np.linspace(0, 10, 50)
y1 = 0.5 * x + 0.5 * np.random.randn(50)
y2 = 0.3 * x**2 - 0.5 * x + 0.2 * np.random.randn(50)

# 创建复合图表布局
fig, axes = sv.presets.create_composite_figure(
    layout_type='irregular', 
    num_plots=3, 
    figsize=(10, 8),
    title="实验数据分析",
    subtitle="比较不同模型的拟合效果",
    add_labels=True
)

# 主散点图 (左上)
fig_scatter, ax_scatter, scatter_params, trend_params = sv.presets.apply_preset(
    'scatter_with_trend', fig=fig, ax=axes[0],
    title="数据点与线性拟合", xlabel="X变量", ylabel="Y变量"
)

# 绘制散点和拟合线
ax_scatter.scatter(x, y1, **scatter_params, label="实验数据")

# 添加拟合线
fit_line, poly = sv.utils.add_fit_line(
    ax_scatter, x, y1, 
    order=1,
    color='red',
    linestyle='--'
)

# 残差图 (右上)
residuals = y1 - poly(x)
axes[1].scatter(x, residuals, color=sv.colors.get_color('accent'), alpha=0.7)
axes[1].axhline(y=0, linestyle='--', color='gray')
axes[1].set_title("残差分析")
axes[1].set_xlabel("X变量")
axes[1].set_ylabel("残差")
sv.elements.set_grid(axes[1], style='dashed')

# 比较图 (下部)
from scipy import stats
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y1)

ax_left = axes[2]
ax_right = ax_left.twinx()

# 线性模型
ax_left.scatter(x, y1, color=sv.colors.get_color('primary'), s=30, alpha=0.5)
linear_pred = slope * x + intercept
ax_left.plot(x, linear_pred, color=sv.colors.get_color('primary'), linestyle='-')
ax_left.set_ylabel("线性模型", color=sv.colors.get_color('primary'))
ax_left.tick_params(axis='y', colors=sv.colors.get_color('primary'))

# 二次模型
ax_right.scatter(x, y2, color=sv.colors.get_color('secondary'), s=30, alpha=0.5)
coeffs2 = np.polyfit(x, y2, 2)
poly2 = np.poly1d(coeffs2)
x_fit = np.linspace(min(x), max(x), 100)
ax_right.plot(x_fit, poly2(x_fit), color=sv.colors.get_color('secondary'), linestyle='-')
ax_right.set_ylabel("二次模型", color=sv.colors.get_color('secondary'))
ax_right.tick_params(axis='y', colors=sv.colors.get_color('secondary'))

axes[2].set_title("模型比较")
axes[2].set_xlabel("X变量")

# 保存图表
sv.utils.save_figure(fig, "scientific_figure.png", dpi=300)
```

### 5.2 扩展系统

#### 添加自定义组件

```python
# 添加自定义颜色角色
sv.colors.update_role('critical', '#ff0000')

# 添加自定义注释样式
sv.elements.add_custom_annotation_style('big_arrow', {
    'xytext': (50, 50),
    'textcoords': 'offset points',
    'fontsize': 12,
    'color': 'black',
    'ha': 'center',
    'va': 'center',
    'bbox': dict(boxstyle='round,pad=0.5', fc='yellow', ec='black', alpha=0.8),
    'arrowprops': dict(arrowstyle='fancy', connectionstyle='arc3,rad=0.3', 
                     color='black', lw=2),
})

# 添加自定义网格样式
sv.elements.add_custom_grid_style('engineering', {
    'visible': True,
    'color': '#cccccc',
    'linestyle': '-',
    'linewidth': 0.5,
    'alpha': 0.8,
})
```

#### 创建自定义预设

```python
def setup_engineering_plot(fig=None, ax=None, title=None, 
                         xlabel=None, ylabel=None, grid_style='engineering'):
    """工程图表预设"""
    # 创建图表（如果未提供）
    if fig is None and ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    
    # 应用网格样式
    sv.elements.set_grid(ax, style=grid_style, which='both')
    
    # 设置标签
    sv.elements.set_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel, style='bold')
    
    # 设置轴线样式
    sv.elements.style_axis(ax, spine_top=True, spine_right=True)
    
    # 设置次刻度
    ax.minorticks_on()
    
    return fig, ax

# 添加自定义预设
sv.presets.add_preset('engineering_plot', setup_engineering_plot)
```

### 5.3 导出和共享样式

```python
# 导出颜色配置
sv.style_exporter.export_colors(sv.colors, "my_colors.json")

# 导出主题配置
theme = sv.themes.get_theme('my_theme')
sv.style_exporter.export_theme(theme, "my_theme.json")

# 导出为matplotlib样式文件
sv.style_exporter.export_matplotlib_style(theme, "my_style.mplstyle")

# 导出预设工作流为Python脚本
preset_func = sv.presets.get_preset('line_academic').setup_func
sv.style_exporter.export_preset_workflow(preset_func, "academic_line_workflow.py")
```

## 6. 最佳实践

### 6.1 科研论文图表

- 使用`academic`主题
- 保持字体一致（通常为serif）
- 使用科学调色板
- 避免过度装饰
- 使用矢量格式（PDF、SVG）保存
- 使用300 DPI或更高分辨率
- 确保图表大小适合期刊栏宽

### 6.2 演示文稿图表

- 使用`presentation`主题
- 增大字体大小和线宽
- 使用明亮的颜色和对比
- 简化图表，关注主要信息
- 添加清晰的标题和说明

### 6.3 数据探索

- 使用`clean`主题
- 添加网格以便于阅读
- 使用带有拟合线的散点图
- 添加趋势线和统计信息
- 多角度展示数据（多个子图）

## 7. 常见问题解答

**Q: 如何在多个子图中保持一致的样式？**

A: 应用主题后，使用`sv.presets.create_composite_figure()`创建子图，每个子图将自动继承全局主题样式。

**Q: 如何为特定期刊定制图表样式？**

A: 创建一个基于`academic`主题的自定义主题，调整参数以匹配期刊要求：

```python
sv.themes.create_custom_theme('journal_specific', 'academic', {
    'font.family': 'Times New Roman',
    'figure.figsize': (3.5, 2.5),  # 调整为期刊列宽
    'font.size': 8,  # 调整字体大小
})
```

**Q: 如何在多个图表之间保持一致的颜色映射？**

A: 使用相同的调色板，并为特定数据系列分配固定的颜色角色：

```python
# 定义数据系列与颜色的映射
data_colors = {
    'temperature': sv.colors.get_color('primary'),
    'pressure': sv.colors.get_color('secondary'),
    'humidity': sv.colors.get_color('tertiary'),
}

# 在所有图表中使用一致的颜色
ax1.plot(time, temp, color=data_colors['temperature'])
ax2.plot(time, pressure, color=data_colors['pressure'])
```

**Q: 如何为图表添加水印或标志？**

A: 使用`sv.elements.create_watermark()`函数：

```python
sv.elements.create_watermark(fig, "草稿", alpha=0.1, fontsize=36, rotation=30)
```

## 8. 扩展阅读

- [Matplotlib 文档](https://matplotlib.org/stable/contents.html)
- [Ten Simple Rules for Better Figures](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833)
- [Fundamentals of Data Visualization](https://clauswilke.com/dataviz/)
- [Scientific Visualization: Python + Matplotlib](https://github.com/rougier/scientific-visualization-book)

## 9. 版本历史

- **0.1.0**: 初始版本，包含核心功能

## 10. 联系方式

如有问题或建议，请联系：

- GitHub: [https://github.com/yourusername/scivis](https://github.com/yourusername/scivis)
- Email: your.email@example.com