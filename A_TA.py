import numpy as np
import time
# import shamir as sh
from config import *
from utilitybelt import secure_randint as randint
# from shamir import MAX_PRIME
import hashlib
from A_Client import Client
from A_VS import VS
from A_AS import AS

# 输入向量元素 < MAX_INPUT
MAX_INPUT = 2 ** 16
# 进行掩码操作和矩阵求和时的模
R = 2 ** 24

import time
from ecdsa import SigningKey, SECP256k1
import hashlib
from EIFL import prg
import numpy as np

class TA:
    def __init__(self, config):
        self.config = config
        self.client_num = config["client_num"]
        self.GRA_NUM = config["model_dimension"]
        # 1. 生成密钥对（默认曲线SECP256k1）
        private_key_list = []
        public_key_list = []
        for i in range(self.client_num+2):
            private_key = SigningKey.generate(curve=SECP256k1)
            private_key_list.append(private_key)
            public_key = private_key.get_verifying_key()
            public_key_list.append(public_key)
        self.client_list = []
        for i in range(self.client_num):
            client = Client(i, config, private_key_list[i], public_key_list)
            self.client_list.append(client)
        
        self.the_vs = VS(config, private_key_list[self.client_num], public_key_list)
        
        self.the_as = AS(config, private_key_list[self.client_num+1], public_key_list)


    def get(self):
        return self.client_list, self.the_vs, self.the_as
