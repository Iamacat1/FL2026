import numpy as np
import time
# import shamir as sh
# from config import *
from utilitybelt import secure_randint as randint
# from shamir import MAX_PRIME
import hashlib

# 输入向量元素 < MAX_INPUT
MAX_INPUT = 2 ** 16
# 进行掩码操作和矩阵求和时的模
R = 2 ** 24

import time
from ecdsa import SigningKey, SECP256k1
import hashlib
from EIFL import *
import numpy as np
from A_utils import *


class Client:
    def __init__(self, index, config, private_key, public_key_list):
        self.sign_time = 0
        self.r3_time = 0
        self.verify_time = 0
        self.verify_correct_time = 0
        self.index = index
        self.config = config
        self.GRA_NUM = config["model_dimension"]
        self.client_num = config["client_num"]
        self.public_key_list = public_key_list
        self.private_key = private_key
        self.public_key = private_key.get_verifying_key()
        # 模型向量
        grad = np.random.randint(1, MAX_INPUT, self.GRA_NUM)
        self.grad_iter = np.append(grad, 1)

    def sign(self):
        start = time.time()
        # for i in range(self.client_num):
        #     prg(i, self.GRA_NUM)
        signature = self.private_key.sign(self.grad_iter.tobytes())
        self.sign_time = time.time() - start
        return self.grad_iter, signature

    def verify_as(self, vs_agg_sig):
        start = time.time()
        agg_sig, vs_sig = vs_agg_sig[0], vs_agg_sig[1]
        # 验证VS给聚合结果的签名
        verify(self.public_key_list[self.client_num], vs_sig, agg_sig[0].tobytes() + agg_sig[1])
        # 验证AS给聚合结果的签名
        verify(self.public_key_list[self.client_num+1], agg_sig[1], agg_sig[0].tobytes())
        self.r3_time = time.time() - start


    def verify(self, p_sig, vs_grad, signature, agg_sig):
        start = time.time()
        if vs_grad is not None:
            self.verify_2_1(p_sig, vs_grad, signature)
        else:
            self.verify_2_2(p_sig, signature, agg_sig)
        self.verify_time = time.time() - start

    def verify_2_1(self, p_sig, vs_grad, signature):
        p, sig = p_sig[0], p_sig[1]

        gra_sig, vs_signature  = vs_grad[0], vs_grad[1]
        grad_iter, client_signature  = gra_sig[0], gra_sig[1]

        msg = np.array(p).tobytes() + sig + grad_iter.tobytes() + client_signature + vs_signature
        verify(self.public_key_list[self.client_num+1], signature, msg)
        verify(self.public_key_list[self.client_num], sig, np.array(p).tobytes())
        verify(self.public_key_list[self.client_num], vs_signature, grad_iter.tobytes()+ client_signature)
        verify(self.public_key_list[-3], client_signature, grad_iter)
        
        U = prg(p[-2], self.GRA_NUM)
        
        proof = dot(U, grad_iter[:self.GRA_NUM])
        if proof != p[-3]:
            print(f"证明有问题，VS是恶意的")
        else:
            print(f"证明验证通过！AS是恶意的")
    
    def verify_2_2(self, p_sig, signature, vs_agg_sig):
        # AS的消息和签名
        p, sig = p_sig[0], p_sig[1]
        agg_sig, vs_sig = vs_agg_sig[0], vs_agg_sig[1]
        msg = np.array(p).tobytes() + sig
        # 验证AS给证据的签名
        verify(self.public_key_list[self.client_num+1], signature, msg)
        # 验证VS给证据的签名
        verify(self.public_key_list[self.client_num], sig, np.array(p).tobytes())
        # 验证VS给聚合结果的签名
        verify(self.public_key_list[self.client_num], vs_sig, agg_sig[0].tobytes() + agg_sig[1])
        # 验证AS给聚合结果的签名
        verify(self.public_key_list[self.client_num+1], agg_sig[1], agg_sig[0].tobytes())
        U = prg(p[-2], self.GRA_NUM)
        proof_vs = sum(p[:self.client_num]) % R
        proof_as = dot(U, agg_sig[0])
        if proof_vs != proof_as:
            print(f"聚合有问题！AS是恶意的")
        else:
            print(f"聚合结果验证通过！VS是恶意的")

    def verify_correct_agg(self, agg_sig, flag):
        start = time.time()
        agg_grad, agg_signature  = agg_sig[0], agg_sig[1]
        if flag == "case2_1_1" or flag == "case2-2-1":
            verify(self.public_key_list[self.client_num+1], agg_signature, agg_grad.tobytes())
        else:
            verify(self.public_key_list[self.client_num], agg_signature, agg_grad.tobytes())
        self.verify_correct_time = time.time() - start

    def get_time(self):
        self.time = [self.sign_time, self.r3_time, self.verify_time + self.verify_correct_time]
        print(f"客户端{self.index}各阶段时间：{self.time}")
        self.total_time = sum(self.time)+(self.client_num*2+5)*0.001
        print(f"客户端{self.index}总时间：{self.total_time}")
        return self.total_time

if __name__ == '__main__':
    # start = time.time()
    # for i in range(50):
    #     prg(i, 50000)    
    # sign_time = time.time() - start
    # print(f"生成随机数时间：{sign_time}")
    grad_list = []
    for i in range(100):
        grad = np.random.randint(1, MAX_INPUT, 100000)
        grad_list.append(grad)
    start = time.time()
    for i in range(100):
        if i == 0:
            agg_grad = grad_list[i]
        else:
            agg_grad = agg_grad + grad_list[i]
    print(f"求和时间：{time.time() - start}")