"""
工具函数模块 - 提供各种辅助函数和自动化工具
"""
import os
import datetime
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from typing import Dict, List, Tuple, Union, Optional, Any, Callable
from matplotlib.animation import FuncAnimation
import re
import inspect
import pandas as pd

def setup_chinese_font():
    """设置中文字体支持"""
    # 获取系统中所有可用字体
    font_list = fm.findSystemFonts()
    
    # 检查系统中是否有 Microsoft YaHei 字体
    msyh = [f for f in font_list if 'microsoft' in f.lower() and 'yahei' in f.lower()]
    if msyh:
        # 使用微软雅黑
        plt.rcParams['font.family'] = ['Microsoft YaHei']
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
        print("使用微软雅黑字体")
    else:
        # 如果没有微软雅黑，尝试使用其他中文字体
        chinese_fonts = ['SimHei', 'SimSun', 'NSimSun', 'FangSong', 'KaiTi']
        for font in chinese_fonts:
            if any(font.lower() in f.lower() for f in font_list):
                plt.rcParams['font.family'] = [font]
                plt.rcParams['font.sans-serif'] = [font]
                print(f"使用 {font} 字体")
                break
    
    # 设置默认字体大小
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 12
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    plt.rcParams['legend.fontsize'] = 9
    
    # 修复负号显示
    plt.rcParams['axes.unicode_minus'] = False
    
    # 设置matplotlib的默认字体
    plt.rcParams['mathtext.fontset'] = 'stix'  # 使用STIX字体，它支持中文
    
    # 强制使用中文字体，不使用Arial
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'SimSun', 'NSimSun', 'FangSong', 'KaiTi']
    
    # 设置tkinter字体
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # 隐藏主窗口
        # 设置tkinter默认字体
        default_font = tk.font.nametofont("TkDefaultFont")
        default_font.configure(family=plt.rcParams['font.family'][0])
        # 设置tkinter文本字体
        text_font = tk.font.nametofont("TkTextFont")
        text_font.configure(family=plt.rcParams['font.family'][0])
        # 设置tkinter固定宽度字体
        fixed_font = tk.font.nametofont("TkFixedFont")
        fixed_font.configure(family=plt.rcParams['font.family'][0])
    except Exception as e:
        print(f"设置tkinter字体时出错: {e}")
    
    # 验证字体设置
    current_font = plt.rcParams['font.family']
    print(f"当前使用的字体: {current_font}")

class VisualizationUtils:
    """可视化工具类"""
    
    @staticmethod
    def save_figure(fig, filename, dpi=300, transparent=False, bbox_inches='tight', pad_inches=0.1,
                   formats=None, create_dir=True, overwrite=True):
        """保存图表到多种格式"""
        # 确保使用中文字体
        setup_chinese_font()
        
        # 默认格式列表
        if formats is None:
            formats = ['png', 'pdf', 'svg']
        
        # 确保目录存在
        if create_dir:
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
        
        # 移除文件扩展名（如果有）
        filename_base = os.path.splitext(filename)[0]
        
        # 保存为每种格式
        saved_files = []
        for fmt in formats:
            output_file = f"{filename_base}.{fmt}"
            
            # 检查文件是否存在
            if os.path.exists(output_file) and not overwrite:
                print(f"文件已存在，跳过: {output_file}")
                continue
            
            # 保存图表
            fig.savefig(output_file, dpi=dpi, transparent=transparent, 
                        bbox_inches=bbox_inches, pad_inches=pad_inches, format=fmt)
            saved_files.append(output_file)
            print(f"已保存: {output_file}")
        
        return saved_files
    
    @staticmethod
    def create_animation(fig, update_func, frames=100, interval=50, blit=True, 
                        save_path=None, fps=20):
        """创建动画"""
        # 创建动画对象
        anim = FuncAnimation(fig, update_func, frames=frames, interval=interval, blit=blit)
        
        # 保存动画（如果指定了路径）
        if save_path:
            # 确保目录存在
            directory = os.path.dirname(save_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # 确定文件格式
            ext = os.path.splitext(save_path)[1].lower()
            
            # 保存为适当的格式
            if ext == '.gif':
                # 保存为GIF
                anim.save(save_path, writer='pillow', fps=fps)
            elif ext in ['.mp4', '.avi', '.mov']:
                # 保存为视频
                anim.save(save_path, writer='ffmpeg', fps=fps)
            else:
                raise ValueError(f"不支持的动画格式: {ext}")
            
            print(f"动画已保存: {save_path}")
        
        return anim
    
    @staticmethod
    def add_timestamp(fig, position='bottom_right', format='%Y-%m-%d %H:%M:%S', 
                     fontsize=8, alpha=0.5):
        """为图表添加时间戳"""
        # 获取当前时间
        timestamp = datetime.datetime.now().strftime(format)
        
        # 确定位置
        if position == 'bottom_right':
            x, y = 0.98, 0.02
            ha, va = 'right', 'bottom'
        elif position == 'bottom_left':
            x, y = 0.02, 0.02
            ha, va = 'left', 'bottom'
        elif position == 'top_right':
            x, y = 0.98, 0.98
            ha, va = 'right', 'top'
        elif position == 'top_left':
            x, y = 0.02, 0.98
            ha, va = 'left', 'top'
        else:
            x, y = position
            ha, va = 'right', 'bottom'
        
        # 添加时间戳
        text = fig.text(x, y, timestamp, fontsize=fontsize, alpha=alpha, 
                       ha=ha, va=va, transform=fig.transFigure)
        
        return text
    
    @staticmethod
    def auto_label_bars(ax, bars, fmt='{:.2f}', fontsize=8, rotation=0, 
                       position='top', padding=3):
        """自动为柱状图添加数值标签"""
        for bar in bars:
            height = bar.get_height()
            
            # 设置标签位置
            if position == 'top':
                xy = (bar.get_x() + bar.get_width() / 2, height)
                va = 'bottom'
                y_offset = padding
            elif position == 'middle':
                xy = (bar.get_x() + bar.get_width() / 2, height / 2)
                va = 'center'
                y_offset = 0
            elif position == 'bottom':
                xy = (bar.get_x() + bar.get_width() / 2, 0)
                va = 'top'
                y_offset = -padding
            else:
                raise ValueError(f"不支持的位置: {position}")
            
            # 添加标签
            label = fmt.format(height)
            ax.annotate(label, xy=xy, xytext=(0, y_offset), 
                        textcoords='offset points', fontsize=fontsize, 
                        ha='center', va=va, rotation=rotation)
    
    @staticmethod
    def add_fit_line(ax, x, y, order=1, color='red', linestyle='--', alpha=0.8, 
                    label=None, confidence_interval=False, ci_alpha=0.2):
        """添加拟合线（多项式）"""
        # 确保输入是numpy数组
        x_array = np.array(x)
        y_array = np.array(y)
        
        # 过滤掉NaN值
        mask = ~np.isnan(x_array) & ~np.isnan(y_array)
        x_filtered = x_array[mask]
        y_filtered = y_array[mask]
        
        if len(x_filtered) < order + 1:
            raise ValueError(f"数据点数量不足以拟合{order}阶多项式")
        
        # 计算多项式系数
        coeffs = np.polyfit(x_filtered, y_filtered, order)
        poly = np.poly1d(coeffs)
        
        # 生成平滑曲线点
        x_fit = np.linspace(np.min(x_filtered), np.max(x_filtered), 100)
        y_fit = poly(x_fit)
        
        # 创建拟合标签
        if label is None:
            if order == 1:
                # 线性拟合标签
                slope, intercept = coeffs
                label = f"y = {slope:.3f}x + {intercept:.3f}"
            elif order == 2:
                # 二次拟合标签
                a, b, c = coeffs
                label = f"y = {a:.3f}x² + {b:.3f}x + {c:.3f}"
            else:
                # 高阶多项式简单标签
                label = f"{order}阶多项式拟合"
        
        # 绘制拟合线
        line, = ax.plot(x_fit, y_fit, color=color, linestyle=linestyle, 
                       alpha=alpha, label=label)
        
        # 添加置信区间
        if confidence_interval:
            # 计算残差标准差
            y_fit_data = poly(x_filtered)
            residuals = y_filtered - y_fit_data
            std_residuals = np.std(residuals)
            
            # 绘制置信区间
            ax.fill_between(x_fit, y_fit - 2 * std_residuals, y_fit + 2 * std_residuals,
                           color=color, alpha=ci_alpha)
        
        return line, poly
    
    @staticmethod
    def auto_layout_subplots(fig, axes, figsize=None, title=None, 
                            title_fontsize=16, spacing=0.1, add_labels=True):
        """自动布局子图"""
        # 设置图表大小（如果提供）
        if figsize:
            fig.set_size_inches(figsize)
        
        # 设置标题（如果提供）
        if title:
            fig.suptitle(title, fontsize=title_fontsize)
        
        # 添加子图标签（如果需要）
        if add_labels and len(axes) > 1:
            from .elements import elements
            elements.add_subplot_labels(fig, axes)
        
        # 调整布局
        plt.tight_layout()
        
        # 调整子图间距
        fig.subplots_adjust(wspace=spacing, hspace=spacing)
        
        # 如果有标题，为其留出空间
        if title:
            plt.subplots_adjust(top=0.9)
    
    @staticmethod
    def add_data_table(ax, data, col_labels=None, row_labels=None, fontsize=10, 
                      loc='bottom', bbox=None, **kwargs):
        """为图表添加数据表格"""
        # 默认位置在图表下方
        if bbox is None:
            if loc == 'bottom':
                bbox = [0, -0.3, 1, 0.2]  # [left, bottom, width, height]
            elif loc == 'right':
                bbox = [1.05, 0, 0.3, 1]
            elif loc == 'left':
                bbox = [-0.3, 0, 0.3, 1]
            else:
                bbox = [0, -0.3, 1, 0.2]  # 默认为底部
        
        # 创建表格
        table = ax.table(cellText=data, colLabels=col_labels, rowLabels=row_labels, 
                        loc=loc, bbox=bbox, **kwargs)
        
        # 设置字体大小
        table.auto_set_font_size(False)
        table.set_fontsize(fontsize)
        
        # 自动调整单元格大小
        table.auto_set_column_width(range(len(data[0]) if data else 0))
        
        return table
    
    @staticmethod
    def style_axis_formatter(ax, x_major=None, x_minor=None, y_major=None, y_minor=None):
        """设置坐标轴刻度格式化工具"""
        # 设置X轴主刻度格式
        if x_major is not None:
            ax.xaxis.set_major_formatter(x_major)
        
        # 设置X轴次刻度格式
        if x_minor is not None:
            ax.xaxis.set_minor_formatter(x_minor)
        
        # 设置Y轴主刻度格式
        if y_major is not None:
            ax.yaxis.set_major_formatter(y_major)
        
        # 设置Y轴次刻度格式
        if y_minor is not None:
            ax.yaxis.set_minor_formatter(y_minor)
    
    @staticmethod
    def format_thousands(x, pos=None):
        """千位分隔符格式化"""
        return f"{int(x):,}" if x == int(x) else f"{x:,.2f}"
    
    @staticmethod
    def format_percentage(x, pos=None):
        """百分比格式化"""
        return f"{x:.1f}%"
    
    @staticmethod
    def add_scalebar(ax, length, location='lower right', label=None, 
                    color='black', linewidth=2, **kwargs):
        """添加比例尺"""
        # 导入matplotlib比例尺工具
        from matplotlib.patches import Rectangle
        from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
        import matplotlib.font_manager as fm
        
        # 设置字体
        fontprops = fm.FontProperties(size=10)
        
        # 创建比例尺
        scalebar = AnchoredSizeBar(ax.transData, length, label or f"{length}", 
                                  location, color=color, 
                                  frameon=False, size_vertical=linewidth,
                                  fontproperties=fontprops, **kwargs)
        
        # 添加到图表
        ax.add_artist(scalebar)
        
        return scalebar
    
    @staticmethod
    def create_patch_legend(ax, labels, colors, loc='best', **kwargs):
        """创建自定义图例"""
        import matplotlib.patches as mpatches
        
        # 创建图例元素
        patches = [mpatches.Patch(color=color, label=label) 
                  for label, color in zip(labels, colors)]
        
        # 添加图例
        legend = ax.legend(handles=patches, loc=loc, **kwargs)
        
        return legend

    def is_dark_color(self, color: str) -> bool:
        """
        判断颜色是否为深色
        
        参数:
            color (str): 颜色值，可以是颜色名称或十六进制值
            
        返回:
            bool: 如果是深色返回True，否则返回False
        """
        # 将颜色转换为RGB值
        try:
            import matplotlib.colors as mcolors
            rgb = mcolors.to_rgb(color)
            # 使用相对亮度公式: 0.299R + 0.587G + 0.114B
            luminance = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
            # 如果亮度小于0.5，认为是深色
            return luminance < 0.5
        except:
            # 如果转换失败，默认返回False
            return False

class FigureManager:
    """图表管理和工作流工具"""
    
    def __init__(self, output_dir=None):
        # 设置默认输出目录
        self.output_dir = output_dir or os.path.join(os.getcwd(), 'outputs')
        
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 存储图表字典
        self.figures = {}
        
        # 图表审计数据
        self.audit_data = {
            'created': [],
            'modified': [],
            'exported': []
        }
    
    def create_figure(self, name, figsize=(8, 6), **kwargs):
        """创建并存储新图表"""
        # 创建图表
        fig, ax = plt.subplots(figsize=figsize, **kwargs)
        
        # 存储图表
        self.figures[name] = {
            'fig': fig,
            'ax': ax,
            'created': datetime.datetime.now(),
            'modified': datetime.datetime.now(),
            'exported': False
        }
        
        # 记录审计数据
        self.audit_data['created'].append({
            'name': name,
            'time': datetime.datetime.now(),
            'figsize': figsize
        })
        
        return fig, ax
    
    def get_figure(self, name):
        """获取已存储的图表"""
        if name not in self.figures:
            raise ValueError(f"图表 '{name}' 未找到")
        
        return self.figures[name]['fig'], self.figures[name]['ax']
    
    def update_figure(self, name, func, *args, **kwargs):
        """更新已存储的图表"""
        if name not in self.figures:
            raise ValueError(f"图表 '{name}' 未找到")
        
        # 获取图表
        fig, ax = self.get_figure(name)
        
        # 应用更新函数
        result = func(fig, ax, *args, **kwargs)
        
        # 更新修改时间
        self.figures[name]['modified'] = datetime.datetime.now()
        
        # 记录审计数据
        self.audit_data['modified'].append({
            'name': name,
            'time': datetime.datetime.now(),
            'function': func.__name__
        })
        
        return result
    
    def export_figure(self, name, filename=None, formats=None, dpi=300, **kwargs):
        """导出图表"""
        if name not in self.figures:
            raise ValueError(f"图表 '{name}' 未找到")
        
        # 获取图表
        fig = self.figures[name]['fig']
        
        # 如果未指定文件名，使用图表名称
        if filename is None:
            filename = os.path.join(self.output_dir, f"{name}")
        
        # 保存图表
        saved_files = VisualizationUtils.save_figure(
            fig, filename, dpi=dpi, formats=formats, **kwargs
        )
        
        # 更新导出状态
        self.figures[name]['exported'] = True
        
        # 记录审计数据
        self.audit_data['exported'].append({
            'name': name,
            'time': datetime.datetime.now(),
            'formats': formats,
            'files': saved_files
        })
        
        return saved_files
    
    def export_all(self, formats=None, dpi=300, **kwargs):
        """导出所有图表"""
        results = {}
        
        for name in self.figures:
            output_file = os.path.join(self.output_dir, name)
            results[name] = self.export_figure(
                name, output_file, formats=formats, dpi=dpi, **kwargs
            )
        
        return results
    
    def list_figures(self):
        """列出所有已存储的图表"""
        return list(self.figures.keys())
    
    def delete_figure(self, name):
        """删除已存储的图表"""
        if name not in self.figures:
            raise ValueError(f"图表 '{name}' 未找到")
        
        # 关闭图表
        plt.close(self.figures[name]['fig'])
        
        # 删除图表
        del self.figures[name]
    
    def get_audit_report(self):
        """获取审计报告"""
        return self.audit_data
    
    def save_session(self, filename=None):
        """保存当前会话"""
        # 默认文件名
        if filename is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(self.output_dir, f"session_{timestamp}.pkl")
        
        # 创建会话数据
        session_data = {
            'audit_data': self.audit_data,
            'output_dir': self.output_dir,
            'timestamp': datetime.datetime.now()
        }
        
        # 保存会话数据
        with open(filename, 'wb') as f:
            pickle.dump(session_data, f)
        
        print(f"会话已保存: {filename}")
    
    def clean_up(self):
        """清理资源"""
        # 关闭所有图表
        for name in list(self.figures.keys()):
            plt.close(self.figures[name]['fig'])
            del self.figures[name]

class DataPreprocessor:
    """数据预处理工具类"""
    
    @staticmethod
    def clean_column_names(df):
        """清理数据框列名"""
        # 移除特殊字符，并替换空格为下划线
        df.columns = [re.sub(r'[^\w\s]', '', col).strip().replace(' ', '_').lower() for col in df.columns]
        return df
    
    @staticmethod
    def add_missing_dates(df, date_col, freq='D', fill_value=None):
        """添加缺失的日期行"""
        # 确保日期列是日期时间类型
        df[date_col] = pd.to_datetime(df[date_col])
        
        # 获取起始和结束日期
        start_date = df[date_col].min()
        end_date = df[date_col].max()
        
        # 创建完整的日期范围
        date_range = pd.date_range(start=start_date, end=end_date, freq=freq)
        
        # 创建新的数据框
        date_df = pd.DataFrame({date_col: date_range})
        
        # 合并数据
        merged_df = pd.merge(date_df, df, on=date_col, how='left')
        
        # 填充缺失值
        if fill_value is not None:
            merged_df = merged_df.fillna(fill_value)
        
        return merged_df
    
    @staticmethod
    def get_outliers(series, method='iqr', threshold=1.5):
        """检测异常值"""
        if method == 'iqr':
            # 四分位法
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - threshold * iqr
            upper_bound = q3 + threshold * iqr
            
            # 查找异常值
            outliers = series[(series < lower_bound) | (series > upper_bound)]
        
        elif method == 'zscore':
            # Z-分数法
            mean = series.mean()
            std = series.std()
            z_scores = ((series - mean) / std).abs()
            
            # 查找异常值
            outliers = series[z_scores > threshold]
        
        else:
            raise ValueError(f"不支持的方法: {method}")
        
        return outliers
    
    @staticmethod
    def bin_data(series, bins=10, labels=None, method='equal_width'):
        """数据分箱"""
        if method == 'equal_width':
            # 等宽分箱
            return pd.cut(series, bins=bins, labels=labels)
        
        elif method == 'equal_freq':
            # 等频分箱
            return pd.qcut(series, q=bins, labels=labels)
        
        else:
            raise ValueError(f"不支持的分箱方法: {method}")
    
    @staticmethod
    def pivot_table_for_heatmap(df, index_col, columns_col, values_col, aggfunc='mean'):
        """为热图创建透视表"""
        # 创建透视表
        pivot_table = pd.pivot_table(
            df, values=values_col, index=index_col, columns=columns_col, aggfunc=aggfunc
        )
        
        return pivot_table
    
    @staticmethod
    def normalize_data(data, method='minmax', feature_range=(0, 1)):
        """数据归一化"""
        if method == 'minmax':
            # 最小-最大缩放
            min_val = np.min(data)
            max_val = np.max(data)
            range_val = max_val - min_val
            
            if range_val == 0:
                return np.zeros_like(data)
            
            normalized = (data - min_val) / range_val
            
            # 调整到指定范围
            return normalized * (feature_range[1] - feature_range[0]) + feature_range[0]
        
        elif method == 'zscore':
            # Z-分数标准化
            mean = np.mean(data)
            std = np.std(data)
            
            if std == 0:
                return np.zeros_like(data)
            
            return (data - mean) / std
        
        else:
            raise ValueError(f"不支持的归一化方法: {method}")
    
    @staticmethod
    def moving_average(data, window=3, center=False):
        """计算移动平均"""
        return pd.Series(data).rolling(window=window, center=center).mean()
    
    @staticmethod
    def group_and_aggregate(df, group_cols, agg_dict):
        """分组和聚合"""
        # 执行分组和聚合
        result = df.groupby(group_cols).agg(agg_dict)
        
        # 重置索引，便于绘图
        return result.reset_index()
    
    @staticmethod
    def melt_for_facet(df, id_vars, value_vars, var_name='variable', value_name='value'):
        """为分面图准备数据（长格式）"""
        return pd.melt(df, id_vars=id_vars, value_vars=value_vars, 
                      var_name=var_name, value_name=value_name)

class StyleExporter:
    """样式导出工具"""
    
    @staticmethod
    def export_colors(colors, filename='colors.json'):
        """导出颜色配置为JSON文件"""
        # 提取颜色数据
        color_data = {
            'base_colors': colors.base_colors,
            'palettes': colors.palettes,
            'gradients': colors.gradients,
            'roles': colors.roles
        }
        
        # 保存为JSON文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(color_data, f, indent=4)
        
        print(f"颜色配置已导出: {filename}")
    
    @staticmethod
    def export_theme(theme, filename='theme.json'):
        """导出主题配置为JSON文件"""
        # 确保所有值是可序列化的
        theme_params = {}
        for key, value in theme.params.items():
            # 处理特殊的cycler类型
            if key == 'axes.prop_cycle':
                theme_params[key] = str(value)
            elif isinstance(value, (str, int, float, bool, list, dict, tuple)) or value is None:
                theme_params[key] = value
            else:
                theme_params[key] = str(value)
        
        # 保存为JSON文件
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(theme_params, f, indent=4)
        
        print(f"主题配置已导出: {filename}")
    
    @staticmethod
    def export_matplotlib_style(theme, filename='style.mplstyle'):
        """导出为matplotlib样式文件"""
        # 创建样式文件内容
        lines = []
        for key, value in theme.params.items():
            # 处理特殊值
            if key == 'axes.prop_cycle':
                # 处理颜色循环器
                colors_str = str(value)
                if 'cycler' in colors_str and 'color' in colors_str:
                    # 提取颜色列表
                    import re
                    color_match = re.search(r"color=\[(.*?)\]", colors_str)
                    if color_match:
                        colors = color_match.group(1).replace("'", "").split(', ')
                        lines.append(f"{key}: cycler('color', {str(colors)})")
            elif isinstance(value, (list, tuple)):
                # 处理列表值
                lines.append(f"{key}: {str(value)}")
            else:
                # 处理普通值
                lines.append(f"{key}: {value}")
        
        # 写入样式文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        print(f"Matplotlib样式文件已导出: {filename}")
    
    @staticmethod
    def export_preset_workflow(preset_func, filename='workflow.py'):
        """导出预设工作流为Python脚本"""
        # 获取函数源代码
        source = inspect.getsource(preset_func)
        
        # 生成完整脚本
        script = f"""
# 导入模块
import matplotlib.pyplot as plt
import numpy as np

{source}

# 示例用法
if __name__ == "__main__":
    # 创建示例数据
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # 使用预设
    fig, ax = plt.subplots()
    {preset_func.__name__}(fig, ax, title="示例图表", xlabel="X轴", ylabel="Y轴")
    
    # 绘制数据
    ax.plot(x, y)
    
    # 显示图表
    plt.show()
"""
        
        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(script)
        
        print(f"工作流脚本已导出: {filename}")
    
    @staticmethod
    def generate_documentation(package_modules, filename='documentation.md'):
        """生成文档"""
        # 文档头部
        doc = """# 科研绘图环境使用文档

本文档自动生成，包含科研绘图环境包的各模块API参考。

"""
        
        # 遍历模块
        for module_name, module in package_modules.items():
            doc += f"## {module_name}\n\n"
            
            # 获取模块中的类
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and obj.__module__ == module.__name__:
                    doc += f"### {name}\n\n"
                    
                    # 类文档
                    class_doc = inspect.getdoc(obj)
                    if class_doc:
                        doc += f"{class_doc}\n\n"
                    
                    # 获取方法
                    for method_name, method in inspect.getmembers(obj):
                        if (not method_name.startswith('_') or method_name == '__init__') and inspect.isfunction(method):
                            doc += f"#### {method_name}\n\n"
                            
                            # 方法文档
                            method_doc = inspect.getdoc(method)
                            if method_doc:
                                doc += f"{method_doc}\n\n"
                            
                            # 提取参数签名
                            try:
                                signature = inspect.signature(method)
                                doc += f"```python\n{method_name}{signature}\n```\n\n"
                            except:
                                pass
            
            doc += "---\n\n"
        
        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(doc)
        
        print(f"文档已生成: {filename}")

# 创建全局工具实例
utils = VisualizationUtils()
figure_manager = FigureManager()
data_preprocessor = DataPreprocessor()
style_exporter = StyleExporter()