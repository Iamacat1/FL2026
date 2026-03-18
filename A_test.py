from A_AS import AS
from A_VS import VS
from A_TA import TA
from A_Client import Client
import numpy as np
import time
from ecdsa import SigningKey, SECP256k1
import hashlib
from EIFL import prg
from config import *
import copy


def case1(client_list, the_vs, the_as):
    gra_sig_list = []
    for client in client_list:
        grad_iter, signature = client.sign()
        gra_sig_list.append((grad_iter, signature))
    vs_grad_list = the_vs.sign(gra_sig_list)
    agg_sig = the_as.agg(vs_grad_list)
    the_vs.verify(agg_sig)
    vs_agg_sig = the_vs.resign_agg(agg_sig)
    client_list[0].verify_as(vs_agg_sig)
    client_list[0].get_time()
    the_vs.get_time()
    the_as.get_time()

def case2_1_1(client_list, the_vs, the_as):
    print("\n\n--- VS恶意行为case 2-1-1 ---")
    gra_sig_list = []
    for client in client_list:
        grad_iter, signature = client.sign()
        gra_sig_list.append((grad_iter, signature))
    vs_grad_list = the_vs.sign(gra_sig_list)
    agg_sig = the_as.agg(vs_grad_list)
    p_sig = the_vs.verify_malicious_2_1_1()
    p_sig, vs_grad, signature = the_as.rebuttal(p_sig)
    client_list[0].verify(p_sig, vs_grad, signature, None)
    client_list[0].verify_correct_agg(agg_sig, "case2_1_1")
    client_list[0].get_time()
    the_as.get_time()

def case2_2_1(client_list, the_vs, the_as):
    print("\n\n--- VS恶意行为case 2-2-1 ---")
    gra_sig_list = []
    for client in client_list:
        grad_iter, signature = client.sign()
        gra_sig_list.append((grad_iter, signature))
    vs_grad_list = the_vs.sign(gra_sig_list)
    agg_sig = the_as.agg(vs_grad_list)
    vs_agg_sig = the_vs.resign_agg(agg_sig)
    p_sig = the_vs.verify_malicious_2_2_1()
    p_sig, vs_grad, signature = the_as.rebuttal(p_sig)
    client_list[0].verify(p_sig, None, signature, vs_agg_sig)
    client_list[0].verify_correct_agg(agg_sig, "case2-2-1")
    client_list[0].get_time()
    the_as.get_time()

def case2_1_2(client_list, the_vs, the_as):
    print("\n\n--- AS恶意行为case 2-1-2 ---")
    gra_sig_list = []
    for client in client_list:
        grad_iter, signature = client.sign()
        gra_sig_list.append((grad_iter, signature))
    vs_grad_list = the_vs.sign(gra_sig_list)
    agg_sig = the_as.agg_malicious(vs_grad_list)
    p_sig = the_vs.verify(agg_sig)
    p_sig, vs_grad, signature = the_as.rebuttal_malicious_2_1_2(p_sig)
    client_list[0].verify(p_sig, vs_grad, signature, None)
    correct_agg_sig = the_vs.resign_correct_agg()
    client_list[0].verify_correct_agg(correct_agg_sig, "case2_1_2")
    client_list[0].get_time()
    the_vs.get_time()

def case2_2_2(client_list, the_vs, the_as):
    print("\n\n--- AS恶意行为case 2-2-2 ---")
    gra_sig_list = []
    for client in client_list:
        grad_iter, signature = client.sign()
        gra_sig_list.append((grad_iter, signature))
    vs_grad_list = the_vs.sign(gra_sig_list)
    agg_sig = the_as.agg_malicious(vs_grad_list)
    p_sig = the_vs.verify(agg_sig)
    p_sig, vs_grad, signature = the_as.rebuttal_malicious_2_2_2(p_sig)
    vs_agg_sig = the_vs.resign_agg(agg_sig)
    client_list[0].verify(p_sig, None, signature, vs_agg_sig)
    correct_agg_sig = the_vs.resign_correct_agg()
    client_list[0].verify_correct_agg(correct_agg_sig, "case2_2_2")
    client_list[0].get_time()
    the_vs.get_time()

if __name__ == "__main__":
    client_time_1 = []
    client_time_211 = []
    client_time_212 = []
    client_time_221 = []
    client_time_222 = []

    vs_time_1 = []
    vs_time_212 = []
    vs_time_222 = []

    as_time_1 = []
    as_time_211 = []
    as_time_221 = []

    for config in client_config_list:
        the_ta = TA(config)
        client_list, the_vs, the_as = the_ta.get()

        new_client_list1 = copy.deepcopy(client_list)
        new_the_as1 = copy.deepcopy(the_as)
        new_the_vs1 = copy.deepcopy(the_vs)
        case1(new_client_list1, new_the_vs1, new_the_as1)
        client_time_1.append(new_client_list1[0].total_time)
        vs_time_1.append(new_the_vs1.total_time)
        as_time_1.append(new_the_as1.total_time)

        new_client_list2 = copy.deepcopy(client_list)
        new_the_as2 = copy.deepcopy(the_as)
        new_the_vs2 = copy.deepcopy(the_vs)
        case2_1_1(new_client_list2, new_the_vs2, new_the_as2)
        client_time_211.append(new_client_list2[0].total_time)
        as_time_211.append(new_the_as2.total_time)

        new_client_list3 = copy.deepcopy(client_list)
        new_the_as3 = copy.deepcopy(the_as)
        new_the_vs3 = copy.deepcopy(the_vs)
        case2_2_1(new_client_list3, new_the_vs3, new_the_as3)
        client_time_221.append(new_client_list3[0].total_time)
        as_time_221.append(new_the_as3.total_time)

        new_client_list4 = copy.deepcopy(client_list)
        new_the_as4 = copy.deepcopy(the_as)
        new_the_vs4 = copy.deepcopy(the_vs)
        case2_1_2(new_client_list4, new_the_vs4, new_the_as4)
        client_time_212.append(new_client_list4[0].total_time)
        vs_time_212.append(new_the_vs4.total_time)

        new_client_list5 = copy.deepcopy(client_list)
        new_the_as5 = copy.deepcopy(the_as)
        new_the_vs5 = copy.deepcopy(the_vs)
        case2_2_2(new_client_list5, new_the_vs5, new_the_as5)
        client_time_222.append(new_client_list5[0].total_time)
        vs_time_222.append(new_the_vs5.total_time)
    print(f"正常情况客户端时间：{client_time_1}")    
    print(f"正常情况VS时间：{vs_time_1}")    
    print(f"正常情况AS时间：{as_time_1}")
    print(f"VS恶意行为case 2-1-1客户端时间：{client_time_211}")
    print(f"VS恶意行为case 2-1-1 AS时间：{as_time_211}")
    print(f"VS恶意行为case 2-2-1 客户端时间：{client_time_221}")
    print(f"VS恶意行为case 2-2-1 AS时间：{as_time_221}")
    print(f"AS恶意行为case 2-1-2 客户端时间：{client_time_212}")
    print(f"AS恶意行为case 2-1-2 VS时间：{vs_time_212}")
    print(f"AS恶意行为case 2-2-2 客户端时间：{client_time_222}")
    print(f"AS恶意行为case 2-2-2 VS时间：{vs_time_222}")    