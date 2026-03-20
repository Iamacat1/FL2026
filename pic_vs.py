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
    ax.legend(['CASE 1', 'CASE 2-1-2', 'CASE 2-2-2',  'FSMSA', 'VeSAFL'], loc='upper left',)
    # plt.tight_layout()
    plt.savefig(fig_name)

if __name__ == '__main__':
    # ------验证服务器计算开销对比，客户端100，模型维度2-10w------
    FSMSA_Initiator = [3.02, 6.1, 9.2, 12.1, 15.2]
    VeSAFL = [271.91, 527.37, 790.70, 1106.98, 1310.42]
    case1 = [0.09600329399108887, 0.11180543899536133, 0.13164544105529785, 0.1785128116607666, 0.1675581932067871]
    case212 = [0.6790590286254883, 1.256871223449707, 1.8928766250610352, 2.4140212535858154, 3.012317419052124]
    case222 = [0.6784536838531494, 1.2382333278656006, 1.8610689640045166, 2.421262502670288, 3.0296003818511963]

    # ------验证服务器计算开销对比，模型维度10w，客户端数量20-100------
    FSMSA_Initiator = [248.80251097679138, 475.1769120693207, 698.6869361400604, 924.6689944267273, 1150.3378732204437]
    VeSAFL = [275.45, 554.07, 819.36, 1097.12, 1310.42]
    case1 = [0.03923988342285156, 0.07269287109375, 0.10766959190368652, 0.1352548599243164, 0.17441272735595703]
    case212 = [0.6414215564727783, 1.2641515731811523, 1.863422155380249, 2.4368438720703125, 3.012749195098877]
    case222 = [0.64689040184021, 1.2419953346252441, 1.8583452701568604, 2.401604652404785, 3.011197805404663]




    # ------验证服务器通信开销对比，模型维度10w，客户端数量20-100------
    FSMSA_Initiator = [1708.9915161132812, 3173.8392333984375, 4638.686950683594, 6103.53466796875, 7568.382385253906]
    VeSAFL = [256.35, 500.49, 744.63, 988.77, 1204.01]
    case1= [0.03179931640625, 0.11236572265625, 0.24176025390625, 0.41998291015625, 0.64703369140625]
    case212= [0.030976533889770508, 0.11062741279602051, 0.2391064167022705, 0.4164135456085205, 0.6425487995147705]
    case222= [0.030976533889770508, 0.11062741279602051, 0.2391064167022705, 0.4164135456085205, 0.6425487995147705]
    x1 = [20, 40, 60, 80, 100]
    y_ticks = [0, 1, 10, 100, 1000, 10000, 100000]
    y_visual = [0, 1, 10, r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
    pic_enc(x1, y_ticks, y_visual, case1, case212, case222, FSMSA_Initiator, VeSAFL, 15, 105, "Client Number", "Verification communication (MB)",
                "vs_ver_com_client.pdf")
    
    # ------验证服务器通信开销对比，客户端100，模型维度2-10w------
    FSMSA_Initiator = [1513.6948852539062, 3027.3667602539062, 4541.038635253906, 6054.710510253906, 7568.382385253906]
    VeSAFL = [246.58, 493.16, 739.75, 986.33, 1204.01]
    case1= [0.64703369140625, 0.64703369140625, 0.64703369140625, 0.64703369140625, 0.64703369140625]
    case212= [0.6425487995147705, 0.6425487995147705, 0.6425487995147705, 0.6425487995147705, 0.6425487995147705]
    case222= [0.6425487995147705, 0.6425487995147705, 0.6425487995147705, 0.6425487995147705, 0.6425487995147705]
    x1 = [2, 4, 6, 8, 10]
    y_ticks = [0, 1, 10, 100, 1000, 10000, 100000]
    y_visual = [0, 1, 10, r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
    pic_enc(x1, y_ticks, y_visual, case1, case212, case222, FSMSA_Initiator, VeSAFL, 1.5, 10.5, "Model Dimension (x10\u2074)", "Verification communication (MB)",
                "vs_ver_com_model.pdf")