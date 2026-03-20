import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

def pic_enc(x_ticks, y_ticks, y_visual, y1, y2, y3, y4, y5, x_min, x_max, x_label, y_lable, fig_name):
    # 创建图形和轴
    fig, ax = plt.subplots(dpi = 1000, figsize=(6, 5))
    plt.subplots_adjust(0.14, 0.13, 0.98, 0.98)
    # 设置轴的线条粗细
    ax.spines['bottom'].set_linewidth(2)  # 设置底部坐标轴的粗细
    ax.spines['left'].set_linewidth(2)  # 设置左边坐标轴的粗细
    ax.spines['right'].set_linewidth(2)  # 设置右边坐标轴的粗细
    ax.spines['top'].set_linewidth(2)
    # 设置Y轴的刻度位置和标签
    # 位置使用索引值，使它们在视觉上均匀分布
    ax.yaxis.set_major_locator(FixedLocator(range(len(y_ticks))))
    ax.yaxis.set_major_formatter(FixedFormatter(y_visual))
    ax.tick_params(axis='y', labelsize=14)
    # 设置Y轴的限制，使其刚好包含所有刻度
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, len(y_ticks)-0.8)

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks, fontsize=14)
    # 为了使绘图正确映射，我们需要将实际数据转换为视觉位置
    # 创建一个映射函数
    def value_to_visual(y_value, y_ticks):
        """将实际Y值转换为视觉位置"""
        # 找到y_value所在的区间
        for i in range(1, len(y_ticks)):
            if y_ticks[i-1] <= y_value <= y_ticks[i]:
                # 在区间内线性插值
                ratio = (y_value - y_ticks[i-1]) / (y_ticks[i] - y_ticks[i-1])
                return i-1 + ratio
        # 如果超出范围，使用对数增长估计
        if y_value > y_ticks[-1]:
            return len(y_ticks) - 1 + np.log(y_value / y_ticks[-1])
        else:  # y_value < y_ticks[0]
            return 0 - np.log(y_ticks[0] / y_value)

    # 转换数据并重新绘制
    visual_y1 = [value_to_visual(yi, y_ticks) for yi in y1]
    ax.plot(x_ticks, visual_y1, marker='s', markersize=14, linewidth=2, linestyle='--')
    visual_y2 = [value_to_visual(yi, y_ticks) for yi in y2]
    ax.plot(x_ticks, visual_y2, marker='X', markersize=14, linewidth=2, linestyle='--')
    visual_y3 = [value_to_visual(yi, y_ticks) for yi in y3]
    ax.plot(x_ticks, visual_y3, marker='^', markersize=14, linewidth=2, linestyle='--')
    visual_y4 = [value_to_visual(yi, y_ticks) for yi in y4]
    ax.plot(x_ticks, visual_y4, marker='D', markersize=14, linewidth=2)
    visual_y5 = [value_to_visual(yi, y_ticks) for yi in y5]
    ax.plot(x_ticks, visual_y5, marker='*', markersize=14, linewidth=2)

    # 添加标题和标签
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel(y_lable, fontsize=16)

    # 添加网格线以便更好地观察
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.rcParams.update({'font.size': 12})
    ax.legend(['CASE 1', 'CASE 2-1-1', 'CASE 2-2-1',  'FSMSA', 'VeSAFL'], loc='upper left',)
    # plt.tight_layout()
    plt.savefig(fig_name)

if __name__ == "__main__":

    # ------聚合服务器计算开销对比，客户端100，模型维度2-10w------
    FSMSA_Server = [0.52, 0.98, 1.46, 1.98, 2.5]
    case1 = [0.13919830322265625, 0.1554737091064453, 0.17753076553344727, 0.2174057960510254, 0.20925235748291016]
    case211 = [0.7193348407745361, 1.3074705600738525, 1.8761727809906006, 2.46500301361084, 3.086503267288208]
    case221 = [0.7165195941925049, 1.315122365951538, 2.0567991733551025, 2.450063943862915, 3.0353758335113525]

    # -----聚合服务器计算开销对比，模型维度10w，客户端数量20-100------
    FSMSA_Server = [0.52, 0.98, 1.46, 1.98, 2.5]
    case1 = [0.04558730125427246, 0.08322286605834961, 0.12588810920715332, 0.17530465126037598, 0.20845460891723633]
    case211 = [0.654512882232666, 1.257154941558838, 1.8904857635498047, 2.4753353595733643, 3.0426907539367676]
    case221 = [0.6501564979553223, 1.2999598979949951, 1.8691904544830322, 2.5273752212524414, 3.185805082321167]


    # ------聚合服务器通信开销对比，客户端100，模型维度2-10w------
    FSMSA_Server = [1513.6887817382812, 3027.3606567382812, 4541.032531738281, 6054.704406738281, 7568.376281738281]
    VeSAFL = [246.58, 493.16, 739.75, 986.33, 1204.01]
    case1= [0.62872314453125, 0.62872314453125, 0.62872314453125, 0.62872314453125, 0.62872314453125]
    case211= [6.538783311843872, 12.260829210281372, 17.982875108718872, 23.704921007156372, 29.426966905593872]
    case221= [0.8044111728668213, 0.8044111728668213, 0.8044111728668213, 0.8044111728668213, 0.8044111728668213]
    x1 = [2, 4, 6, 8, 10]
    y_ticks = [0, 1, 10, 100, 1000, 10000, 100000]
    y_visual = [0, 1, 10, r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
    pic_enc(x1, y_ticks, y_visual, case1, case211, case221, FSMSA_Server, VeSAFL, 1.5, 10.5, "Model Dimension (x10\u2074)", "Verification communication (MB)",
                "as_ver_com_model.pdf")

    # ------聚合服务器通信开销对比，模型维度10w，客户端数量20-100------
    FSMSA_Server = [1708.9902954101562, 3173.8367919921875, 4638.683288574219, 6103.52978515625, 7568.376281738281]
    VeSAFL = [256.35, 500.49, 744.63, 988.77, 1204.01]
    case1= [0.02813720703125, 0.10504150390625, 0.23077392578125, 0.40533447265625, 0.62872314453125]
    case211= [5.763446092605591, 11.587773561477661, 17.47313618659973, 23.4195339679718, 29.426966905593872]
    case221= [0.038934946060180664, 0.13875126838684082, 0.299602746963501, 0.5214893817901611, 0.8044111728668213]
    x1 = [20, 40, 60, 80, 100]
    y_ticks = [0, 1, 10, 100, 1000, 10000, 100000]
    y_visual = [0, 1, 10, r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
    pic_enc(x1, y_ticks, y_visual, case1, case211, case221, FSMSA_Server, VeSAFL, 15, 105, "Client Number", "Verification communication (MB)",
                "as_ver_com_client.pdf")
