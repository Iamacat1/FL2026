import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter

def pic_enc(x_ticks, y_ticks, y_visual, y1, y2, y3, y4, y5, x_min, x_max, y_min, y_max, x_label, y_lable, fig_name):
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
    ax.tick_params(axis='y', labelsize=16)
    # 设置Y轴的限制，使其刚好包含所有刻度
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(0, len(y_ticks)-0.8)

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_ticks, fontsize=20)
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
    ax.plot(x_ticks, visual_y1, marker='s', markersize=16, linewidth=4)
    visual_y2 = [value_to_visual(yi, y_ticks) for yi in y2]
    ax.plot(x_ticks, visual_y2, marker='X', markersize=16, linewidth=4)
    visual_y3 = [value_to_visual(yi, y_ticks) for yi in y3]
    ax.plot(x_ticks, visual_y3, marker='^', markersize=16, linewidth=4)
    visual_y4 = [value_to_visual(yi, y_ticks) for yi in y4]
    ax.plot(x_ticks, visual_y4, marker='D', markersize=16, linewidth=4)
    visual_y5 = [value_to_visual(yi, y_ticks) for yi in y5]
    ax.plot(x_ticks, visual_y5, marker='*', markersize=16, linewidth=4)
    # visual_y6 = [value_to_visual(yi, y_ticks) for yi in y6]
    # ax.plot(x_ticks, visual_y6, marker='.', markersize=16, linewidth=4)

    # 添加标题和标签
    ax.set_xlabel(x_label, fontsize=20)
    ax.set_ylabel(y_lable, fontsize=20)

    # 添加网格线以便更好地观察
    ax.grid(True, linestyle='--', alpha=0.7)
    plt.rcParams.update({'font.size': 14})
    # ax.legend(['0 dropout:EIFL', '10% dropout:EIFL', '20% dropout:EIFL','0 dropout:VCD-FL', '10% dropout:VCD-FL', '20% dropout:VCD-FL'])
    ax.legend(['EIFL', 'VCD-FL', 'VERIFL', 'VERSA', 'VOSA'])
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
    EIFL = [0.21293864, 0.23619119, 0.25373054, 0.2827521, 0.30407503]
    VCDFL = [0.9400718927383422, 1.2022410035133362, 1.4458986838658652, 1.7251800924539566, 2.040652594566345]
    VERIFL = [9.72, 9.77, 9.8, 9.9, 10]
    VERSA = [1.2049243450164795, 1.9522230625152588, 2.683027982711792, 3.488229274749756, 4.267499208450317]
    VOSA = [3.9, 4, 4, 4.02, 3.95]
    x1 = [20, 40, 60, 80, 100]
    y_ticks = [0, 1, 2, 4, 8, 16]
    pic_enc(x1, y_ticks, y_ticks, EIFL, VCDFL, VERIFL, VERSA, VOSA, 15, 105, 0, 15, "Client Number", "Running time for verification (s)",
                "diff_ver_time_about_client.pdf")

    # 验证时间，客户端100，模型参数2-10w
    EIFL = [0.20227646, 0.22474531, 0.25417818, 0.2738926, 0.29528257]
    VCDFL = [0.33403045177459717, 0.676944899559021, 1.0501074361801148, 1.4728528881072998, 2.040652594566345]
    VERIFL = [2, 4, 6, 8, 10]
    VERSA = [0.9483628273010254, 1.798457145690918, 2.679705858230591, 3.5529391765594482, 4.427247524261475]
    VOSA = [0.7881438732147217, 1.565807819366455, 2.3634860515594482, 3.1533145904541016, 3.9277396202087402]
    x1 = [2, 4, 6, 8, 10]
    pic_enc(x1, y_ticks, y_ticks, EIFL, VCDFL, VERIFL, VERSA, VOSA, 1, 11, 0, 15, "Model Dimension (x10\u2074)", "Running time for verification (s)",
                "diff_ver_time_about_model.pdf")

    # # 验证通信开销，模型参数10w，客户端20-100
    # EIFL = [0.00152587890625, 0.0030517578125, 0.00457763671875, 0.006103515625, 0.00762939453125]
    # VCDFL = [10.87188720703125, 22.31597900390625, 33.76007080078125, 45.20416259765625, 56.64825439453125]
    # VERIFL = [0.0047607421875, 0.0096435546875, 0.0145263671875, 0.0194091796875, 0.0242919921875]
    # VERSA = [0.9298324584960938, 0.9298324584960938, 0.9298324584960938, 0.9298324584960938, 0.9298324584960938]
    # VOSA = [6.103515625, 6.103515625, 6.103515625, 6.103515625, 6.103515625]

    # x1 = [20, 40, 60, 80, 100]
    # y_ticks = [0, 0.1, 1, 10, 100, 1000]
    # y_visual = [0, 0.1, 1, 10, r'$10^2$', r'$10^3$']
    # pic_enc(x1, y_ticks, y_visual, EIFL, VCDFL, VERIFL, VERSA, VOSA, 15, 105, 0, 60, "Client Number", "Data for verification (MB)",
    #             "diff_ver_com_about_client.pdf")

    # 验证通信开销，客户端100，模型参数2-10w
    # EIFL = [0.00762939453125, 0.00762939453125, 0.00762939453125, 0.00762939453125, 0.00762939453125]
    # VCDFL = [11.32965087890625, 22.6593017578125, 33.98895263671875, 45.318603515625, 56.64825439453125]
    # VERIFL = [0.0242919921875, 0.0242919921875, 0.0242919921875, 0.0242919921875, 0.0242919921875]
    # VERSA = [0.18596649169921875, 0.3719329833984375, 0.5578994750976562, 0.743865966796875, 0.9298324584960938]
    # VOSA = [1.220703125, 2.44140625, 3.662109375, 4.8828125, 6.103515625]
    # x1 = [2, 4, 6, 8, 10]
    # pic_enc(x1, y_ticks, y_visual, EIFL, VCDFL, VERIFL, VERSA, VOSA, 1, 11, 0, 60, "Model Dimension (x10\u2074)", "Data for verification (MB)",
    #             "diff_ver_com_about_model.pdf")

    # # 客户端运行时间，模型参数10w，客户端20-100
    # EIFL = [3.0071147099999997, 5.12398179, 7.03358293, 9.380079550000001, 11.69464222]
    # VCDFL = [27.98711802, 29.21853985, 30.73828499, 31.6814509, 33.14255174]
    # x1 = [20, 40, 60, 80, 100]
    # pic_compare(x1, EIFL, VCDFL, SGD, OFL, SIGFL, 15, 105, 0, 35, "Client Number", "Total running time (s)",
    #             "client_runtime_about_client.pdf")
    
    # # 客户端运行时间，客户端100，模型参数2-10w
    # EIFL = [3.0662193500000003, 5.18296861, 7.27955188, 9.303917160000001, 11.25784725]
    # VCDFL = [6.1441668, 12.21838785, 18.34293845, 24.50824653, 33.14255174]
    # x1 = [2, 4, 6, 8, 10]
    # pic_compare(x1, EIFL, VCDFL, SGD, OFL, SIGFL, 1, 11, 0, 35, "Model Dimension (x10\u2074)", "Total running time (s)",
    #             "client_runtime_about_model.pdf")

    # # 客户端通信开销，模型参数10w，客户端20-100
    # EIFL_communication_client = [0.5919189453125, 0.63616943359375, 0.704833984375, 0.79791259765625, 0.9154052734375]
    # VDC_FL_communication_client = [22.31597900390625, 45.20416259765625, 68.09234619140625, 90.98052978515625, 113.86871337890625]
    # x1 = [20, 40, 60, 80, 100]
    # y_ticks = [0, 0.1, 1, 10, 100, 1000]
    # y_visual = [0, 0.1, 1, 10, r'$10^2$', r'$10^3$']
    # pic_enc(x1, y_ticks, y_visual, EIFL_communication_client, VDC_FL_communication_client, SGD, OFL, SIGFL, 15, 105, 0, 10,
    #             "Client Number", "Total data per client (MB)",
    #             "client_data_about_client.pdf")

    # # 客户端通信开销，客户端100，模型参数2-10w
    # EIFL_communication_client = [0.4576416015625, 0.57208251953125, 0.6865234375, 0.80096435546875, 0.9154052734375]
    # VDC_FL_communication_client = [22.77374267578125, 45.5474853515625, 68.32122802734375, 91.094970703125, 113.86871337890625]
    # x1 = [2, 4, 6, 8, 10]
    # pic_enc(x1, y_ticks, y_visual, EIFL_communication_client, VDC_FL_communication_client, SGD, OFL, SIGFL, 1, 11, 0, 10, "Model Dimension (x10\u2074)", "Total data per client (MB)",
    #             "client_data_about_model.pdf")

    # # 验证时间，模型参数10w，客户端20-100
    # EIFL_drop0 = [0.12899671, 0.13661792, 0.14577322, 0.15575467, 0.16583926]
    # EIFL_drop1 = [0.14341728, 0.13746592, 0.14682036, 0.15718789, 0.16546484]
    # EIFL_drop2 = [0.13127626, 0.14041836, 0.14921543, 0.16005135, 0.169809  ]
    # VCDFL = [0.9400718927383422, 1.2022410035133362, 1.4458986838658652, 1.7251800924539566, 2.040652594566345]
    # x1 = [20, 40, 60, 80, 100]
    # pic_compare(x1, EIFL_drop0, EIFL_drop1, EIFL_drop2, VCDFL, VCDFL, VCDFL, 15, 105, 0, 3, "Client Number", "Running time for verification (s)",
    #             "veri_time_about_client_drop.pdf")
    
    
    # EIFL_drop0 = [0.08706084, 0.10587558, 0.12534291, 0.14390835, 0.16659956]
    # EIFL_drop1 = [0.08795816, 0.10697422, 0.12639234, 0.14617399, 0.16546484]
    # EIFL_drop2 = [0.08783835, 0.10807408, 0.12806255, 0.14816743, 0.169809  ]
    # VCDFL = [0.33403045177459717, 0.676944899559021, 1.0501074361801148, 1.4728528881072998, 2.040652594566345]
    # x1 = [2, 4, 6, 8, 10]
    # pic_compare(x1, EIFL_drop0, EIFL_drop1, EIFL_drop2, VCDFL, VCDFL, VCDFL, 1, 11, 0, 3, "Model Dimension (x10\u2074)", "Running time for verification (s)",
    #             "veri_time_about_model_drop.pdf")


    # EIFL_drop0 = [0.00152587890625, 0.0030517578125, 0.00457763671875, 0.006103515625, 0.00762939453125]
    # EIFL_drop1 = [0.573699951171875, 1.14739990234375, 1.721099853515625, 2.2947998046875, 2.868499755859375]
    # EIFL_drop2 = [1.1458740234375, 2.291748046875, 3.4376220703125, 4.58349609375, 5.7293701171875]
    
    # VCDFL_drop0 = [21.7437744140625, 44.6319580078125, 67.5201416015625, 90.4083251953125, 113.2965087890625]
    # VCDFL_drop1 = [20.599365234375, 42.3431396484375, 64.0869140625, 85.8306884765625, 107.574462890625]
    # VCDFL_drop2 = [19.4549560546875, 40.0543212890625, 60.6536865234375, 81.2530517578125, 101.8524169921875]
    # x1 = [20, 40, 60, 80, 100]
    # y_ticks = [0, 10, 100, 1000, 10000, 100000]
    # y_visual = [0, 10, r'$10^2$', r'$10^3$',r'$10^4$', r'$10^5$']
    # pic_enc(x1, y_ticks, y_visual, EIFL_drop0, EIFL_drop1, EIFL_drop2, VCDFL_drop0, VCDFL_drop1, VCDFL_drop2, 15, 105, 0, 100000, "Client Number", "Data for verification (MB)",
    #             "veri_com_about_client_drop.pdf")
    

    # EIFL_drop0 = [0.00762939453125, 0.00762939453125, 0.00762939453125, 0.00762939453125, 0.00762939453125]
    # EIFL_drop1 = [0.579681396484375, 1.151885986328125, 1.724090576171875, 2.296295166015625, 2.868499755859375]
    # EIFL_drop2 = [1.1517333984375, 2.296142578125, 3.4405517578125, 4.5849609375, 5.7293701171875]

    # VCDFL_drop0 = [22.6593017578125, 45.318603515625, 67.9779052734375, 90.63720703125, 113.2965087890625]
    # # 验证通信开销随模型参数变化，掉线率0.1
    # VCDFL_drop1 = [21.514892578125, 43.02978515625, 64.544677734375, 86.0595703125, 107.574462890625]
    # # 验证通信开销随模型参数变化，掉线率0.2
    # VCDFL_drop2 = [20.3704833984375, 40.740966796875, 61.1114501953125, 81.48193359375, 101.8524169921875]

    # x1 = [2, 4, 6, 8, 10]
    # y_ticks = [0, 10, 100, 1000, 10000, 100000]
    # y_visual = [0, 10, r'$10^2$', r'$10^3$',r'$10^4$', r'$10^5$']
    # pic_enc(x1, y_ticks, y_visual, EIFL_drop0, EIFL_drop1, EIFL_drop2, VCDFL_drop0, VCDFL_drop1, VCDFL_drop2, 1, 11, 0, 100000, "Model Dimension (x10\u2074)", "Data for verification (MB)",
    #             "veri_com_about_model_drop.pdf")