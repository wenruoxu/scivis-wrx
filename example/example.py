"""
scivis使用示例 - 展示科研绘图环境一体化管理系统的主要功能
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 导入scivis包
import scivis_wrx as sv

def example_basic_usage():
    """展示基本用法"""
    print("=== 基本用法示例 ===")
    
    # 应用主题
    sv.themes.apply_theme('clean')
    
    # 创建简单图表
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 使用颜色系统
    primary_color = sv.colors.get_color('primary')
    secondary_color = sv.colors.get_color('secondary')
    
    # 生成数据
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)
    
    # 绘制数据
    ax.plot(x, y1, color=primary_color, label='sin(x)')
    ax.plot(x, y2, color=secondary_color, label='cos(x)')
    
    # 设置标签
    sv.elements.set_labels(ax, title="基本波形图", xlabel="X", ylabel="Y")
    
    # 设置网格
    sv.elements.set_grid(ax, style='default')
    
    # 设置图例
    sv.elements.set_legend(ax, style='default')
    
    # 保存图表
    sv.utils.save_figure(fig, "outputs/basic_example.png")
    
    print("已保存: outputs/basic_example.png")
    
    # 显示图表
    plt.show()

def example_theme_comparison():
    """比较不同主题的效果"""
    print("\n=== 主题比较示例 ===")
    
    # 准备数据
    x = np.linspace(0, 10, 100)
    y = np.sin(x) * np.exp(-0.1 * x)
    
    # 获取所有主题
    theme_names = sv.themes.list_themes()
    print(f"可用主题: {theme_names}")
    
    # 创建子图布局
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    # 为每个子图应用不同主题
    for i, theme_name in enumerate(theme_names[:4]):  # 最多展示4个主题
        # 保存当前设置
        old_params = plt.rcParams.copy()
        
        # 应用主题
        sv.themes.apply_theme(theme_name)
        
        # 绘制数据
        axes[i].plot(x, y)
        axes[i].set_title(f"主题: {theme_name}")
        axes[i].set_xlabel("X")
        axes[i].set_ylabel("Y")
        
        # 恢复原来的设置
        plt.rcParams.update(old_params)
    
    # 整体标题
    fig.suptitle("不同主题的比较", fontsize=16)
    plt.tight_layout()
    
    # 保存图表
    sv.utils.save_figure(fig, "outputs/theme_comparison.png")
    
    print("已保存: outputs/theme_comparison.png")
    
    # 显示图表
    plt.show()

def example_color_palettes():
    """展示颜色调色板"""
    print("\n=== 颜色调色板示例 ===")
    
    # 获取所有调色板
    palette_names = list(sv.colors.palettes.keys())
    print(f"可用调色板: {palette_names}")
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 为每个调色板创建一个水平条
    bar_height = 0.8
    y_positions = range(len(palette_names))
    
    for i, palette_name in enumerate(palette_names):
        # 获取调色板颜色
        colors = sv.colors.get_palette(palette_name)
        
        # 绘制每个调色板中的颜色块
        start_x = 0
        for j, color in enumerate(colors):
            width = 1  # 每个颜色块的宽度
            ax.add_patch(plt.Rectangle((start_x, i - bar_height/2), width, bar_height, color=color))
            
            # 如果颜色块足够宽，添加标签
            if width >= 0.4:
                ax.text(start_x + width/2, i, color, ha='center', va='center', 
                      fontsize=8, color='white' if sv.utils.is_dark_color(color) else 'black')
            
            start_x += width
    
    # 设置坐标轴
    ax.set_xlim(0, max([len(sv.colors.get_palette(name)) for name in palette_names]))
    ax.set_ylim(-0.5, len(palette_names) - 0.5)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(palette_names)
    ax.set_xlabel("颜色索引")
    ax.set_title("可用调色板", fontsize=14)
    
    # 隐藏上边框和右边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    
    # 隐藏x轴刻度
    ax.set_xticks([])
    
    # 保存图表
    sv.utils.save_figure(fig, "outputs/color_palettes.png")
    
    print("已保存: outputs/color_palettes.png")
    
    # 显示图表
    plt.show()

def example_presets():
    """展示预设样式"""
    print("\n=== 预设样式示例 ===")
    
    # 获取所有预设
    preset_names = sv.presets.list_presets()
    print(f"可用预设: {preset_names}")
    
    # 选择几个预设进行展示
    selected_presets = ['line_basic', 'bar_comparison', 'scatter_basic', 'minimal_style']
    
    # 创建子图
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    # 数据准备
    x = np.linspace(0, 10, 20)
    y = np.sin(x) * np.exp(-0.1 * x)
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [3, 7, 5, 9, 4]
    
    # 应用预设
    for i, preset_name in enumerate(selected_presets):
        if preset_name == 'line_basic':
            # 线图预设
            sv.presets.apply_preset('line_basic', fig=fig, ax=axes[i], 
                                   title="线图预设", xlabel="X", ylabel="Y")
            axes[i].plot(x, y)
            
        elif preset_name == 'bar_comparison':
            # 柱状图预设
            fig_bar, ax_bar, bar_width = sv.presets.apply_preset('bar_comparison', 
                                                              fig=fig, ax=axes[i],
                                                              title="柱状图预设", 
                                                              xlabel="类别", 
                                                              ylabel="值")
            ax_bar.bar(categories, values, width=bar_width)
            
        elif preset_name == 'scatter_basic':
            # 散点图预设
            fig_scatter, ax_scatter, scatter_params = sv.presets.apply_preset('scatter_basic',
                                                                           fig=fig, ax=axes[i],
                                                                           title="散点图预设",
                                                                           xlabel="X",
                                                                           ylabel="Y")
            ax_scatter.scatter(x, y + 0.2 * np.random.randn(len(x)), **scatter_params)
            
        elif preset_name == 'minimal_style':
            # 简洁风格预设
            sv.presets.apply_preset('minimal_style', fig=fig, ax=axes[i],
                                   title="简洁风格预设", xlabel="X", ylabel="Y")
            axes[i].plot(x, y)
    
    # 整体标题
    fig.suptitle("预设样式展示", fontsize=16)
    plt.tight_layout()
    
    # 保存图表
    sv.utils.save_figure(fig, "outputs/preset_examples.png")
    
    print("已保存: outputs/preset_examples.png")
    
    # 显示图表
    plt.show()

def example_scientific_figure():
    """创建科研论文级别的图表"""
    print("\n=== 科研论文图表示例 ===")
    
    # 应用学术主题
    sv.themes.apply_theme('academic')
    
    # 准备数据
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    y1 = 0.5 * x + 0.5 * np.random.randn(50)
    y2 = 0.3 * x**2 - 0.5 * x + 0.2 * np.random.randn(50)
    
    # 创建复合图表布局
    fig, axes = sv.presets.create_composite_figure(layout_type='irregular', 
                                                num_plots=3, 
                                                figsize=(10, 8),
                                                title="实验数据分析",
                                                subtitle="比较不同模型的拟合效果")
    
    # 主散点图 (左上)
    fig_scatter, ax_scatter, scatter_params, trend_params = sv.presets.apply_preset(
        'scatter_with_trend', fig=fig, ax=axes[0],
        title="数据点与线性拟合", xlabel="X变量", ylabel="Y变量"
    )
    
    # 绘制散点和拟合线
    ax_scatter.scatter(x, y1, **scatter_params, label="实验数据")
    
    # 如果需要添加拟合线
    if trend_params['add']:
        # 计算拟合
        fit_line, poly = sv.utils.add_fit_line(
            ax_scatter, x, y1, 
            order=trend_params['order'],
            color=trend_params['color'],
            linestyle=trend_params['linestyle']
        )
    
    # 添加R²值
    from scipy import stats
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y1)
    r_squared = r_value**2
    
    sv.elements.add_textbox(ax_scatter, 0.05, 0.95, 
                           f"R² = {r_squared:.3f}\ny = {slope:.3f}x + {intercept:.3f}", 
                           style='info', transform=ax_scatter.transAxes)
    
    # 残差图 (右上)
    if trend_params['add']:
        residuals = y1 - poly(x)
        axes[1].scatter(x, residuals, color=sv.colors.get_color('accent'), alpha=0.7)
        axes[1].axhline(y=0, linestyle='--', color='gray')
        axes[1].set_title("残差分析")
        axes[1].set_xlabel("X变量")
        axes[1].set_ylabel("残差")
        sv.elements.set_grid(axes[1], style='dashed')
    
    # 比较图 (下部)
    # 双Y轴图，比较两个模型
    fig_dual, ax_left, ax_right = sv.presets.apply_preset(
        'dual_axis', fig=fig, ax=axes[2],
        title="模型比较", xlabel="X变量",
        y1label="线性模型", y2label="二次模型",
        color1=sv.colors.get_color('primary'),
        color2=sv.colors.get_color('secondary')
    )
    
    # 绘制线性模型预测
    ax_left.scatter(x, y1, color=sv.colors.get_color('primary'), s=30, alpha=0.5)
    linear_pred = slope * x + intercept
    ax_left.plot(x, linear_pred, color=sv.colors.get_color('primary'), linestyle='-')
    
    # 绘制二次模型
    ax_right.scatter(x, y2, color=sv.colors.get_color('secondary'), s=30, alpha=0.5)
    # 二次拟合
    coeffs2 = np.polyfit(x, y2, 2)
    poly2 = np.poly1d(coeffs2)
    x_fit = np.linspace(min(x), max(x), 100)
    ax_right.plot(x_fit, poly2(x_fit), color=sv.colors.get_color('secondary'), linestyle='-')
    
    # 添加水印
    sv.elements.create_watermark(fig, "scivis示例", alpha=0.1, fontsize=36, rotation=30)
    
    # 保存图表
    sv.utils.save_figure(fig, "outputs/scientific_figure.png", dpi=300)
    
    print("已保存: outputs/scientific_figure.png")
    
    # 显示图表
    plt.show()

def example_custom_style():
    """自定义样式示例"""
    print("\n=== 自定义样式示例 ===")
    
    # 创建自定义调色板
    sv.colors.create_custom_palette('my_palette', 
                                   ['#264653', '#2a9d8f', '#e9c46a', '#f4a261', '#e76f51'])
    
    # 创建自定义主题
    sv.themes.create_custom_theme('my_theme', 'clean', {
        'font.family': 'serif',
        'font.size': 11,
        'axes.facecolor': '#f8f9fa',
        'figure.facecolor': '#f8f9fa',
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.prop_cycle': plt.cycler('color', sv.colors.get_palette('my_palette')),
    })
    
    # 应用自定义主题
    sv.themes.apply_theme('my_theme')
    
    # 创建图表
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # 准备数据
    categories = ['类别A', '类别B', '类别C', '类别D', '类别E']
    values = [25, 40, 30, 55, 45]
    
    # 绘制条形图
    bars = ax.bar(categories, values)
    
    # 为每个条形使用不同颜色
    for i, bar in enumerate(bars):
        bar.set_color(sv.colors.get_palette('my_palette')[i])
    
    # 设置标签
    ax.set_title("自定义样式示例", fontsize=14)
    ax.set_xlabel("类别", fontsize=12)
    ax.set_ylabel("值", fontsize=12)
    
    # 自定义网格
    sv.elements.set_grid(ax, 'dashed', axis='y')
    
    # 自定义轴线样式
    sv.elements.style_spines(ax, color='#555555', width=1.0,
                            visible={'top': False, 'right': False, 'bottom': True, 'left': True})
    
    # 添加数据标签
    sv.utils.auto_label_bars(ax, bars, fmt='{:.0f}', fontsize=10)
    
    # 添加水印
    sv.elements.create_watermark(fig, "自定义样式", alpha=0.05, fontsize=36, rotation=30)
    
    # 保存图表
    sv.utils.save_figure(fig, "outputs/custom_style.png")
    
    print("已保存: outputs/custom_style.png")
    
    # 显示图表
    plt.show()

def example_composite_layout():
    """复合布局示例"""
    print("\n=== 复合布局示例 ===")
    
    # 应用主题
    sv.themes.apply_theme('clean')
    
    # 创建复合布局
    fig, axes = sv.presets.create_composite_figure(
        layout_type='grid',
        num_plots=4,
        figsize=(12, 10),
        title="复合图表布局示例",
        subtitle="展示不同类型图表的组合"
    )
    
    # 图1: 线图
    axes[0].set_title("线图")
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    axes[0].plot(x, y, color=sv.colors.get_color('primary'))
    sv.elements.set_labels(axes[0], xlabel="X", ylabel="sin(x)")
    sv.elements.set_grid(axes[0], style='default')
    
    # 图2: 柱状图
    axes[1].set_title("柱状图")
    categories = ['A', 'B', 'C', 'D', 'E']
    values = [3, 7, 5, 9, 4]
    axes[1].bar(categories, values, color=sv.colors.get_palette('pastel'))
    sv.elements.set_labels(axes[1], xlabel="类别", ylabel="值")
    sv.elements.set_grid(axes[1], style='dashed', axis='y')
    
    # 图3: 散点图
    axes[2].set_title("散点图")
    np.random.seed(42)
    x_scatter = np.random.rand(50)
    y_scatter = np.random.rand(50)
    sizes = np.random.rand(50) * 200 + 50
    colors = sv.colors.get_palette('vibrant', n=50)
    axes[2].scatter(x_scatter, y_scatter, s=sizes, c=colors, alpha=0.6)
    sv.elements.set_labels(axes[2], xlabel="X", ylabel="Y")
    sv.elements.set_grid(axes[2], style='dotted')
    
    # 图4: 饼图
    axes[3].set_title("饼图")
    labels = ['A', 'B', 'C', 'D']
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)
    axes[3].pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
              shadow=True, startangle=90, colors=sv.colors.get_palette('pastel', n=4))
    axes[3].axis('equal')
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图表
    sv.utils.save_figure(fig, "outputs/composite_layout.png")
    
    print("已保存: outputs/composite_layout.png")
    
    # 显示图表
    plt.show()

def example_workflow_manager():
    """工作流管理示例"""
    print("\n=== 工作流管理示例 ===")
    
    # 创建图表管理器实例
    manager = sv.figure_manager
    
    # 应用主题
    sv.themes.apply_theme('clean')
    
    # 创建第一个图表
    fig1, ax1 = manager.create_figure("temperature_plot", figsize=(8, 5))
    
    # 绘制温度数据
    x = np.arange(0, 24, 1)  # 时间（小时）
    temp = 20 + 5 * np.sin(np.pi * x / 12) + 2 * np.random.randn(24)  # 温度数据
    
    ax1.plot(x, temp, 'o-', color=sv.colors.get_color('primary'))
    sv.elements.set_labels(ax1, title="24小时温度变化", xlabel="时间 (小时)", ylabel="温度 (°C)")
    sv.elements.set_grid(ax1, style='default')
    
    # 创建第二个图表
    fig2, ax2 = manager.create_figure("humidity_plot", figsize=(8, 5))
    
    # 绘制湿度数据
    humidity = 60 + 10 * np.cos(np.pi * x / 12) + 5 * np.random.randn(24)  # 湿度数据
    
    ax2.plot(x, humidity, 'o-', color=sv.colors.get_color('accent'))
    sv.elements.set_labels(ax2, title="24小时湿度变化", xlabel="时间 (小时)", ylabel="湿度 (%)")
    sv.elements.set_grid(ax2, style='dashed')
    
    # 定义更新函数
    def add_mean_line(fig, ax, color='red', linestyle='--', linewidth=1):
        """添加均值线"""
        y_values = ax.lines[0].get_ydata()
        mean_value = np.mean(y_values)
        ax.axhline(mean_value, color=color, linestyle=linestyle, linewidth=linewidth,
                  label=f"均值: {mean_value:.2f}")
        ax.legend()
        return True
    
    # 更新第一个图表
    manager.update_figure("temperature_plot", add_mean_line, color='blue')
    
    # 更新第二个图表
    manager.update_figure("humidity_plot", add_mean_line, color='green')
    
    # 导出所有图表
    manager.export_all(formats=['png'], dpi=300)
    
    print("所有图表已导出到outputs目录")
    
    # 查看管理的图表
    print(f"管理的图表: {manager.list_figures()}")
    
    # 保存会话
    manager.save_session()
    
    # 显示图表
    plt.show()
    
    # 清理资源
    manager.clean_up()

def main():
    """运行所有示例"""
    # 确保输出目录存在
    import os
    os.makedirs("outputs", exist_ok=True)
    
    # 运行各个示例
    example_basic_usage()
    example_theme_comparison()
    example_color_palettes()
    example_presets()
    example_scientific_figure()
    example_custom_style()
    example_composite_layout()
    example_workflow_manager()

if __name__ == "__main__":
    main()