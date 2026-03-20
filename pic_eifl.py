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
    # 客户端验证时间，模型参数10w，客户端20-100
    
    FSMSA_client = [24.60459237098694, 24.281709390878678, 24.331447072823842, 24.049496069550514, 24.226350915431976]
    VeSAFL_client = [21.5, 21.5, 21.5, 21.5, 21.5]
    case1 = [0.04849164009094238, 0.08785005569458008, 0.12783122062683105, 0.16785744667053223, 0.2078820037841797]
    case211 = [0.12435976982116699, 0.1617500400543213, 0.202131986618042, 0.24372200012207032, 0.2819143104553223]
    case221 = [0.11914484024047851, 0.1594903087615967, 0.20157098770141602, 0.24069241523742677, 0.2810648250579834]
    case212 = [0.12030450820922851, 0.1603920078277588, 0.2017660140991211, 0.23933342933654786, 0.2786696720123291]
    case222 = [0.11867873191833496, 0.15800376892089846, 0.19888877868652344, 0.24114541053771973, 0.2795406150817871]
    
    x1 = [20, 40, 60, 80, 100]
    y_ticks = [0, 1, 10, 100, 1000]
    y_visual = [0, 1, 10, r'$10^2$', r'$10^3$']
    pic_enc(x1, y_ticks, y_visual,  case1, case211, case212, case221, case222, FSMSA_client, VeSAFL_client, 15, 105, "Client Number", "Verification time (s)",
                "diff_ver_time_about_client.pdf")

    # 客户端验证时间，客户端100，模型参数2-10w
    x1 = [2, 4, 6, 8, 10]
    y_ticks = [0, 1, 10, 100, 1000]
    y_visual = [0, 1, 10, r'$10^2$', r'$10^3$']
    # -------客户端计算开销对比
    FSMSA_client = [2.59, 5.2, 7.8, 10.25, 12.78]
    VeSAFL_client = [4.3, 8.6, 12.9, 17.2, 21.5]
    case1 = [0.20677717208862306, 0.20698602676391603, 0.20765932083129884, 0.20789058685302736, 0.20774682044982912]
    case211 = [0.2239638137817383, 0.23922713279724123, 0.253065185546875, 0.26760967254638673, 0.2880855369567871]
    case221 = [0.22292907714843752, 0.23782928466796877, 0.254633264541626, 0.2647519874572754, 0.284970121383667]
    case212 = [0.2228816318511963, 0.23646338462829591, 0.25220020294189455, 0.26541479110717775, 0.27899630546569826]
    case222 = [0.22414310455322267, 0.2361393737792969, 0.25110347747802736, 0.2647381591796875, 0.28102667808532716]
    
    # pic_enc(x1, y_ticks, y_visual, case1, case211, case212, case221, case222, FSMSA_client, VeSAFL_client, 1.5, 10.5, "Model Dimension (x10\u2074)", "Verification time (s)",
    #             "diff_ver_time_about_model.pdf")

    # 客户端验证通信开销，模型参数10w，客户端20-100
    case1= [0.00274658203125, 0.00518798828125, 0.00762939453125, 0.01007080078125, 0.01251220703125]
    case211= [0.289309024810791, 0.292055606842041, 0.294802188873291, 0.297548770904541, 0.300295352935791]
    case212= [0.289309024810791, 0.292055606842041, 0.294802188873291, 0.297548770904541, 0.300295352935791]
    case221= [0.003083467483520508, 0.005830049514770508, 0.008576631546020508, 0.011323213577270508, 0.014069795608520508]
    case222= [0.003083467483520508, 0.005830049514770508, 0.008576631546020508, 0.011323213577270508, 0.014069795608520508]
    FSMSA = [244.14410400390625, 244.14471435546875, 244.14532470703125, 244.14593505859375, 244.14654541015625]
    VeSAFL = [24.41, 24.41, 24.41, 24.41, 24.41]

    x1 = [20, 40, 60, 80, 100]
    y_ticks = [0, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]
    y_visual = [0, r'$10^{-2}$', r'$10^{-1}$', 1, 10, r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
    pic_enc(x1, y_ticks, y_visual, case1, case211, case212, case221, case222, FSMSA, VeSAFL, 15, 105, "Client Number", "Verification communication (MB)",
                "diff_ver_com_about_client.pdf")

    # 客户端验证通信开销，客户端100，模型参数2-10w
    case1 = [0.01251220703125, 0.01251220703125, 0.01251220703125, 0.01251220703125, 0.01251220703125]
    case211 = [0.07141351699829102, 0.12863397598266602, 0.18585443496704102, 0.24307489395141602, 0.300295352935791]
    case212 = [0.07141351699829102, 0.12863397598266602, 0.18585443496704102, 0.24307489395141602, 0.300295352935791]
    case221 = [0.014069795608520508, 0.014069795608520508, 0.014069795608520508, 0.014069795608520508, 0.014069795608520508]
    case222 = [0.014069795608520508, 0.014069795608520508, 0.014069795608520508, 0.014069795608520508, 0.014069795608520508]
    FSMSA = [48.83404541015625, 97.66217041015625, 146.49029541015625, 195.31842041015625, 244.14654541015625]
    VeSAFL = [4.88, 9.77, 14.65, 19.53, 24.41]

    x1 = [2, 4, 6, 8, 10]
    y_ticks = [0, 0.01, 0.1, 1, 10, 100, 1000, 10000, 100000]
    y_visual = [0, r'$10^{-2}$', r'$10^{-1}$', 1, 10, r'$10^2$', r'$10^3$', r'$10^4$', r'$10^5$']
    pic_enc(x1, y_ticks, y_visual, case1, case211, case212, case221, case222, FSMSA, VeSAFL, 1.5, 10.5, "Model Dimension (x10\u2074)", "Verification communication (MB)",
                "diff_ver_com_about_model.pdf")



    
    
    

    