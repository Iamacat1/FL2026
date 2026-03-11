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


class VS:
    def __init__(self, config, private_key, public_key_list):
        self.config = config
        self.client_num = config["client_num"]
        self.GRA_NUM = config["model_dimension"]
        # 1. 生成密钥对（默认曲线SECP256k1）
        self.private_key = private_key
        self.public_key = private_key.get_verifying_key()
        self.public_key_list = public_key_list
        self.resign_time = 0
        self.verify_time = 0
        self.resign_agg_time = 0
        self.resign_correct_agg_time = 0
        self.time = []

    def sign(self, gra_sig_list):
        start = time.time()
        vs_grad_list = []
        self.grad_list = []
        for i in range(self.client_num):
            gra_sig = gra_sig_list[i]
            grad_iter,signature  = gra_sig[0], gra_sig[1]

            self.grad_list.append(grad_iter)

            public_key = self.public_key_list[i]
            verify(public_key, signature, grad_iter)
            msg = b''.join([grad_iter.tobytes(), signature])
            vs_sig = self.private_key.sign(msg)
            vs_grad_list.append((gra_sig, vs_sig))
        self.resign_time = time.time() - start
        return vs_grad_list
    
    def verify(self, agg_sig):
        start = time.time()
        as_agg_grad,agg_signature  = agg_sig[0], agg_sig[1]
        verify(self.public_key_list[self.client_num+1], agg_signature, as_agg_grad.tobytes())

        for i in range(self.client_num):
            if i == 0:
                self.agg_grad = self.grad_list[i][:self.GRA_NUM]
            else:
                self.agg_grad = self.agg_grad + self.grad_list[i][:self.GRA_NUM]
        if self.agg_grad.tolist() == as_agg_grad[:self.GRA_NUM].tolist():
            print("✅ 聚合结果正确")
            self.verify_time = time.time() - start
            return None
        else:
            print("❌ 聚合结果错误")
            U = prg(0, self.GRA_NUM)  # 重置随机数生成器以确保可重复性
            p = []
            for i in range(self.client_num):
                p_i = dot(U, self.grad_list[i][:self.GRA_NUM])
                p.append(p_i)
            p.append(0)
            p.append(0)
            sig = self.private_key.sign(np.array(p).tobytes())
            self.verify_time = time.time() - start
            return (p, sig)
        
    
    def resign_agg(self, agg_sig):
        start = time.time()
        as_agg_grad, agg_signature  = agg_sig[0], agg_sig[1]
        sig = self.private_key.sign(as_agg_grad.tobytes() + agg_signature)
        self.resign_agg_time = time.time() - start
        return (agg_sig, sig)

    def resign_correct_agg(self):
        start = time.time()
        np.append(self.agg_grad, 1)
        sig = self.private_key.sign(self.agg_grad.tobytes())
        self.resign_correct_agg_time = time.time() - start
        return (self.agg_grad, sig)

    # 恶意VS，最后一个客户端证据错误
    def verify_malicious_2_1_1(self):
        U = prg(0, self.GRA_NUM)  # 重置随机数生成器以确保可重复性
        p = []
        for i in range(self.client_num):
            p_i = dot(U, self.grad_list[i][:self.GRA_NUM])
            p.append(p_i)
        p.append(0)
        p.append(0)
        p[-3]=p[-3]+1  # 制造错误
        sig = self.private_key.sign(np.array(p).tobytes())
        return (p, sig)

    # 恶意VS，诚实生成证明
    def verify_malicious_2_2_1(self):
        U = prg(0, self.GRA_NUM)  # 重置随机数生成器以确保可重复性
        p = []
        for i in range(self.client_num):
            p_i = dot(U, self.grad_list[i][:self.GRA_NUM])
            p.append(p_i)
        p.append(0)
        p.append(0)
        sig = self.private_key.sign(np.array(p).tobytes())
        return (p, sig)
    
    def get_time(self):
        self.time = [self.resign_time, self.verify_time, self.resign_agg_time + self.resign_correct_agg_time]
        print(f"VS各阶段时间：{self.time}")
        print(f"VS总时间：{sum(self.time)}")
        return self.time