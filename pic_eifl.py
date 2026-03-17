import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

def pic_enc(x_ticks, y_ticks, y_visual, y1, y2, y3, y4, y5, y6, y7, x_min, x_max, x_label, y_lable, fig_name):
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
    ax.plot(x_ticks, visual_y4, marker='D', markersize=14, linewidth=2, linestyle='--')
    visual_y5 = [value_to_visual(yi, y_ticks) for yi in y5]
    ax.plot(x_ticks, visual_y5, marker='*', markersize=14, linewidth=2, linestyle='--')
    visual_y6 = [value_to_visual(yi, y_ticks) for yi in y6]
    ax.plot(x_ticks, visual_y6, marker='>', markersize=14, linewidth=2)
    visual_y7 = [value_to_visual(yi, y_ticks) for yi in y7]
    ax.plot(x_ticks, visual_y7, marker='.', markersize=14, linewidth=2)

    # 添加标题和标签
    ax.set_xlabel(x_label, fontsize=16)
    ax.set_ylabel(y_lable, fontsize=16)

    # 添加网格线以便更好地观察
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.rcParams.update({'font.size': 12})
    ax.legend(['CASE 1', 'CASE 2-1-1', 'CASE 2-1-2', 'CASE 2-2-1', 'CASE 2-2-2',  'FSMSA', 'VeSAFL'], loc='upper left',)
    # plt.tight_layout()
    plt.savefig(fig_name)


def pic_compare(x1, y1, y2, y3, y4, y5, y6,x_min, x_max, y_min, y_max, x_label, y_lable, fig_name):
    plt.figure(dpi=1000, figsize=(6, 5))
    plt.subplots_adjust(0.14, 0.13, 0.98, 0.98)
    # plt.title("title")  # 括号当中输入标题的名称
    plt.xlim(x_min, x_max)  # x轴坐标轴
    plt.ylim(y_min, y_max)  # y轴坐标轴
    # plt.xticks([10000, 20000, 30000, 40000, 50000], fontsize=22)
    plt.xticks(x1, fontsize=20)
    plt.yticks([y_min, y_min+1*(y_max-y_min)/5, y_min+2*(y_max-y_min)/5,
                y_min+3*(y_max-y_min)/5, y_min+4*(y_max-y_min)/5, y_max], fontsize=20)
    plt.xlabel(x_label, fontsize=20)  # x轴标签
    plt.ylabel(y_lable, fontsize=20)  # y轴标签
    ax = plt.gca()  # 获得坐标轴的句柄
    ax.spines['bottom'].set_linewidth(2)  # 设置底部坐标轴的粗细
    ax.spines['left'].set_linewidth(2)  # 设置左边坐标轴的粗细
    ax.spines['right'].set_linewidth(2)  # 设置右边坐标轴的粗细
    ax.spines['top'].set_linewidth(2)
    plt.plot(x1, y1, marker='s', markersize=16, linewidth=4)
    plt.plot(x1, y2, marker='X', markersize=16, linewidth=4)
    plt.plot(x1, y3, marker='^', markersize=16, linewidth=4)
    plt.plot(x1, y4, marker='D', markersize=16, linewidth=4)
    plt.plot(x1, y5, marker='*', markersize=16, linewidth=4)
    plt.plot(x1, y6, marker='.', markersize=16, linewidth=4)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.rcParams.update({'font.size': 14})
    # plt.legend(['EIFL', 'VCD-FL', 'VERIFL', 'VERSA'])
    # plt.legend(['EIFL', 'VCD-FL'])
    plt.legend(['0 dropout:EIFL', '10% dropout:EIFL', '20% dropout:EIFL','0 dropout:VCD-FL', '10% dropout:VCD-FL', '20% dropout:VCD-FL'])
    plt.savefig(fig_name)


SGD = [7.81526094, 5.28184062, 4.01513047, 3.25510437, 2.74842031]
OFL = [0.07283594, 0.05455729, 0.04541797, 0.03993437, 0.03627865]
SIGFL = [3.072, 2.155, 1.697, 1.422, 1.23866667]


if __name__ == '__main__':
    # 验证时间，模型参数10w，客户端20-100
    
    FSMSA_client = [12.8, 12.9, 12.9, 12.78, 12.78]
    




    FSMSA_Initiator = [13.6, 14.0, 14.4, 14.8, 15.2]
    



    FSMSA_Server = [0.52, 0.98, 1.46, 1.98, 2.5]
    
    x1 = [20, 40, 60, 80, 100]
    y_ticks = [0, 1, 2, 4, 8, 16]
    # pic_enc(x1, y_ticks, y_ticks, EIFL, VCDFL, VERIFL, VERSA, VOSA, 15, 105, 0, 15, "Client Number", "Running time for verification (s)",
    #             "diff_ver_time_about_client.pdf")

    # # 验证时间，客户端100，模型参数2-10w
    FSMSA_client = [2.59, 5.2, 7.8, 10.25, 12.78]
    case1 = [0.20677717208862306, 0.20698602676391603, 0.20765932083129884, 0.20789058685302736, 0.20774682044982912]
    case211 = [0.2239638137817383, 0.23922713279724123, 0.253065185546875, 0.26760967254638673, 0.2880855369567871]
    case221 = [0.22292907714843752, 0.23782928466796877, 0.254633264541626, 0.2647519874572754, 0.284970121383667]
    case212 = [0.2228816318511963, 0.23646338462829591, 0.25220020294189455, 0.26541479110717775, 0.27899630546569826]
    case222 = [0.22414310455322267, 0.2361393737792969, 0.25110347747802736, 0.2647381591796875, 0.28102667808532716]

    FSMSA_Initiator = [3.02, 6.1, 9.2, 12.1, 15.2]
    case1 = [0.09600329399108887, 0.11180543899536133, 0.13164544105529785, 0.1785128116607666, 0.1675581932067871]
    case212 = [0.6790590286254883, 1.256871223449707, 1.8928766250610352, 2.4140212535858154, 3.012317419052124]
    case222 = [0.6784536838531494, 1.2382333278656006, 1.8610689640045166, 2.421262502670288, 3.0296003818511963]

    FSMSA_Server = [0.52, 0.98, 1.46, 1.98, 2.5]
    case1 = [0.13919830322265625, 0.1554737091064453, 0.17753076553344727, 0.2174057960510254, 0.20925235748291016]
    case211 = [0.7193348407745361, 1.3074705600738525, 1.8761727809906006, 2.46500301361084, 3.086503267288208]
    case221 = [0.7165195941925049, 1.315122365951538, 2.0567991733551025, 2.450063943862915, 3.0353758335113525]
    # EIFL = [0.20227646, 0.22474531, 0.25417818, 0.2738926, 0.29528257]
    # VCDFL = [0.33403045177459717, 0.676944899559021, 1.0501074361801148, 1.4728528881072998, 2.040652594566345]
    # VERIFL = [2, 4, 6, 8, 10]
    # VERSA = [0.9483628273010254, 1.798457145690918, 2.679705858230591, 3.5529391765594482, 4.427247524261475]
    # VOSA = [0.7881438732147217, 1.565807819366455, 2.3634860515594482, 3.1533145904541016, 3.9277396202087402]
    # x1 = [2, 4, 6, 8, 10]
    # pic_enc(x1, y_ticks, y_ticks, EIFL, VCDFL, VERIFL, VERSA, VOSA, 1, 11, 0, 15, "Model Dimension (x10\u2074)", "Running time for verification (s)",
    #             "diff_ver_time_about_model.pdf")

    # # 验证通信开销，模型参数10w，客户端20-100
    case1= [0.00274658203125, 0.00518798828125, 0.00762939453125, 0.01007080078125, 0.01251220703125]
    case211= [0.289309024810791, 0.292055606842041, 0.294802188873291, 0.297548770904541, 0.300295352935791]
    case212= [0.289309024810791, 0.292055606842041, 0.294802188873291, 0.297548770904541, 0.300295352935791]
    case221= [0.003083467483520508, 0.005830049514770508, 0.008576631546020508, 0.011323213577270508, 0.014069795608520508]
    case222= [0.003083467483520508, 0.005830049514770508, 0.008576631546020508, 0.011323213577270508, 0.014069795608520508]
    FSMSA = [41.73, 41.73, 41.73, 41.73, 41.73]
    VeSAFL = [145, 145, 145, 145, 145]

    x1 = [20, 40, 60, 80, 100]
    y_ticks = [0, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]
    y_visual = [0, r'$10^{-2}$', r'$10^{-1}$', 1, 10, r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
    pic_enc(x1, y_ticks, y_visual, case1, case211, case212, case221, case222, FSMSA, VeSAFL, 15, 105, "Client Number", "Data for verification (MB)",
                "diff_ver_com_about_client.pdf")

    # 验证通信开销，客户端100，模型参数2-10w
    case1 = [0.01251220703125, 0.01251220703125, 0.01251220703125, 0.01251220703125, 0.01251220703125]
    case211 = [0.07141351699829102, 0.12863397598266602, 0.18585443496704102, 0.24307489395141602, 0.300295352935791]
    case212 = [0.07141351699829102, 0.12863397598266602, 0.18585443496704102, 0.24307489395141602, 0.300295352935791]
    case221 = [0.014069795608520508, 0.014069795608520508, 0.014069795608520508, 0.014069795608520508, 0.014069795608520508]
    case222 = [0.014069795608520508, 0.014069795608520508, 0.014069795608520508, 0.014069795608520508, 0.014069795608520508]
    FSMSA = [8.35, 16.69, 25.04, 33.38, 41.73]
    VeSAFL = [29, 58, 87, 116, 145]

    x1 = [2, 4, 6, 8, 10]
    y_ticks = [0, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]
    y_visual = [0, r'$10^{-2}$', r'$10^{-1}$', 1, 10, r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
    pic_enc(x1, y_ticks, y_visual, case1, case211, case212, case221, case222, FSMSA, VeSAFL, 1.5, 10.5, "Model Dimension (x10\u2074)", "Data for verification (MB)",
                "diff_ver_com_about_model.pdf")
