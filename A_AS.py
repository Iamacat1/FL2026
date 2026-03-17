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


class AS:
    def __init__(self, config, private_key, public_key_list):
        
        self.config = config
        self.GRA_NUM = config["model_dimension"]
        self.client_num = config["client_num"]
        self.public_key_list = public_key_list
        
        self.private_key = private_key
        self.public_key = private_key.get_verifying_key()
        self.time = []

    def agg(self, vs_grad_list):
        self.vs_grad_list = vs_grad_list
        start = time.time()
        vs_public_key = self.public_key_list[self.client_num]
        for i in range(self.client_num):
            vs_grad = vs_grad_list[i]
            gra_sig,vs_signature  = vs_grad[0], vs_grad[1]
            grad_iter,signature  = gra_sig[0], gra_sig[1]
            client_public_key = self.public_key_list[i]
            msg = b''.join([grad_iter.tobytes(), signature])
            verify(vs_public_key, vs_signature, msg)
            verify(client_public_key, signature, grad_iter)
            if i == 0:
                agg_grad = grad_iter[:self.GRA_NUM]
            else:
                agg_grad = (agg_grad +grad_iter[:self.GRA_NUM])
        
        agg_grad = np.append(agg_grad, 1)
        self.agg_sig = (agg_grad, self.private_key.sign(agg_grad.tobytes()))
        
        self.agg_time = time.time() - start
        self.time.append(self.agg_time)
        return self.agg_sig
    
    def agg_malicious(self, vs_grad_list):
        self.vs_grad_list = vs_grad_list
        for i in range(self.client_num):
            vs_grad = vs_grad_list[i]
            gra_sig,vs_signature  = vs_grad[0], vs_grad[1]
            grad_iter,signature  = gra_sig[0], gra_sig[1]
            if i == 0:
                agg_grad = grad_iter[:self.GRA_NUM]
            else:
                agg_grad = (agg_grad +grad_iter[:self.GRA_NUM])
        agg_grad[self.GRA_NUM-1] += 1  # 篡改聚合结果
        agg_grad = np.append(agg_grad, 1)
        self.agg_sig = (agg_grad, self.private_key.sign(agg_grad.tobytes()))
        return self.agg_sig

    def rebuttal(self, p_sig):
        start = time.time()
        p, sig = p_sig[0], p_sig[1]
        verify(self.public_key_list[self.client_num], sig, np.array(p).tobytes())
        U = prg(p[-2], self.GRA_NUM)
        for i in range(self.client_num):
            vs_grad = self.vs_grad_list[i]
            gra_sig, vs_signature  = vs_grad[0], vs_grad[1]
            grad_iter, client_signature  = gra_sig[0], gra_sig[1]
            proof = dot(U, grad_iter[:self.GRA_NUM])
            
            if proof != p[i]:
                print(f"客户端{i}的梯度有问题！")
                msg = np.array(p).tobytes() + sig + grad_iter.tobytes() + client_signature + vs_signature
                signature = self.private_key.sign(msg)
                self.rebuttal_time = time.time() - start
                self.time.append(self.rebuttal_time)
                return p_sig, vs_grad, signature
        msg = np.array(p).tobytes() + sig
        signature = self.private_key.sign(msg)
        self.rebuttal_time = time.time() - start
        self.time.append(self.rebuttal_time)
        return p_sig, None, signature
    
    # 恶意的AS：直接转发
    def rebuttal_malicious_2_2_2(self, p_sig):
        p, sig = p_sig[0], p_sig[1]
        msg = np.array(p).tobytes() + sig
        signature = self.private_key.sign(msg)
        return p_sig, None, signature
    
    # 恶意的AS：伪造证据
    def rebuttal_malicious_2_1_2(self, p_sig):
        p, sig = p_sig[0], p_sig[1]
        # 随便选一个客户端的梯度作为伪造的证据
        vs_grad = self.vs_grad_list[-1]
        gra_sig, vs_signature  = vs_grad[0], vs_grad[1]
        grad_iter, client_signature  = gra_sig[0], gra_sig[1]
        msg = np.array(p).tobytes() + sig + grad_iter.tobytes() + client_signature + vs_signature
        signature = self.private_key.sign(msg)
        return p_sig, vs_grad, signature
    
    def get_time(self):
        print(f"AS各阶段时间：{self.time}")
        self.total_time = sum(self.time)
        print(f"AS总时间：{self.total_time}")
        return self.total_time