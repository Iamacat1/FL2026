import matplotlib.pyplot as plt
import numpy as np



def pic_bar(x, group1, group2, label1, label2, x_label, y_label, fig_name):
    bar_width = 0.35
    x_positions_group1 = range(len(group1))
    x_positions_group2 = [i + bar_width for i in x_positions_group1]
    plt.figure(dpi=1000, figsize=(6, 5))
    plt.subplots_adjust(0.14, 0.13, 0.98, 0.98)
    plt.bar(x_positions_group1, group1, width=bar_width, label=label1)
    plt.bar(x_positions_group2, group2, width=bar_width, label=label2)
    plt.xlabel(x_label, fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    # plt.title('Score Comparison between Two Groups')
    plt.xticks([i + bar_width / 2 for i in x_positions_group1], x, fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(fontsize=16)
    plt.grid(axis='y', color='gray', linestyle='--', linewidth=0.5)
    ax = plt.gca()  # 获得坐标轴的句柄
    ax.spines['bottom'].set_linewidth(2)  # 设置底部坐标轴的粗细
    ax.spines['left'].set_linewidth(2)  # 设置左边坐标轴的粗细
    ax.spines['right'].set_linewidth(2)  # 设置右边坐标轴的粗细
    ax.spines['top'].set_linewidth(2)
    plt.savefig(fig_name)
# plt.show()

if __name__ == '__main__':
    # 验证时间随模型向量维度的变化,无掉线
    time1_model = [3.0662193500000003, 5.18296861, 7.27955188, 9.303917160000001, 11.25784725]
    time2_model = [0.20227646, 0.22474531, 0.25417818, 0.2738926, 0.29528257]
    model_labels = [2, 4, 6, 8, 10]
    pic_bar(model_labels, time1_model, time2_model, "Total", "Verification", "Model Dimension (x10\u2074)","Running Time(s)",
            "ver_time_about_model.pdf")

    # 验证时间随客户端数量的变化，无掉线
    time1_client = [3.0071147099999997, 5.12398179, 7.03358293, 9.380079550000001, 11.69464222]
    time2_client = [0.21293864, 0.23619119, 0.25373054, 0.2827521, 0.30407503]
    client_labels = [20, 40, 60, 80, 100]
    pic_bar(client_labels, time1_client, time2_client, "Total", "Verification", "Client Number","Running Time(s)",
            "ver_time_about_client.pdf")

    # 验证通信开销随模型向量维度的变化，无掉线
    data1_model = [0.4576416015625, 0.57208251953125, 0.6865234375, 0.80096435546875, 0.9154052734375]
    data2_model = [0.00762939453125, 0.00762939453125, 0.00762939453125, 0.00762939453125, 0.00762939453125]
    pic_bar(model_labels, data1_model, data2_model, "Total", "Verification", "Model Dimension(x10\u2074)", "Data transfer per client (MB)",
            "ver_data_about_model.pdf")
    
    # 验证通信开销随客户端数量的变化，无掉线
    data1_client = [0.5919189453125, 0.63616943359375, 0.704833984375, 0.79791259765625, 0.9154052734375]
    data2_client = [0.00152587890625, 0.0030517578125, 0.00457763671875, 0.006103515625, 0.00762939453125]
    pic_bar(client_labels, data1_client, data2_client, "Total", "Verification", "Client Number", "Data transfer per client (MB)",
                "ver_data_about_client.pdf")