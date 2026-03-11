from Cryptodome.Hash import SHA256
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Util import Counter
from Cryptodome.Cipher import AES
from Cryptodome.PublicKey import RSA
from Cryptodome import Hash
from Cryptodome.PublicKey import ECC
import numpy as np
import time
import shamir as sh
from config import *
from utilitybelt import secure_randint as randint
from shamir import MAX_PRIME
import hashlib
import datetime


# 自动填充，密钥必须是16字节倍数
def pad(text):
    while len(text) % 16 != 0:
        text += b' '
    return text


def prg(seed, length):
    seed = seed % 2 ** 128
    data = seed.to_bytes(16, 'big')
    rand_list = []
    for i in range(length):
        # 使用SHA256算法计算字符串的哈希值
        sha256_hash = hashlib.sha256(data).digest()
        rand_list.append(int.from_bytes(sha256_hash, 'big') % MAX_INPUT)
        data = sha256_hash
    return np.array(rand_list, dtype=np.int64)


# AES encrypt
def aes_ctr_encrypt(plaintext, key):
    nonce = b'0000'
    ctr = Counter.new(64, prefix=nonce, suffix=b'ABCD', little_endian=True, initial_value=10)
    key = pad(key)
    plaintext = plaintext
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.encrypt(plaintext)


# AES decrypt
def aes_ctr_decrypt(ciphertext, key):
    nonce = b'0000'
    ctr = Counter.new(64, prefix=nonce, suffix=b'ABCD', little_endian=True, initial_value=10)
    key = pad(key)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    return cipher.decrypt(ciphertext)


# generate signature
def to_sign_with_private_key(plain_text, sk):
    key = RSA.import_key(sk)
    h = SHA256.new(plain_text.encode())
    signature = pkcs1_15.new(key).sign(h)
    return signature


# verify signature
def to_verify_with_public_key(signature, plain_text, pk):
    key = RSA.import_key(pk)
    h = SHA256.new(plain_text.encode())
    try:
        pkcs1_15.new(key).verify(h, signature)
    except (ValueError, TypeError):
        print("签名错误！")
        return False
    return True


# key agreement
def dh(pub, pri):
    res = pri * pub
    return int(res.x)


def dot(w1, w2):
    res = 0
    for i in range(len(w1)):
        res += (w1[i] * w2[i]) % R
        res = res % R
    return res


# 输入向量元素 < MAX_INPUT
MAX_INPUT = 2 ** 16
# 进行掩码操作和矩阵求和时的模
R = 2 ** 24
# 秘密共享字节数
SECRET_SHARE_BYTE_LENGTH = 32
# 秘密共享位数
SECRET_SHARE_BIT_LENGTH = SECRET_SHARE_BYTE_LENGTH * 8

# AES秘钥字节数
AES_KEY_BYTE_LENGTH = 32


class Client:
    def __init__(self, index, config):
        # 配置参数
        self.enc_time = 0
        self.dec_time = 0
        self.n = config["client_num"]
        self.GRA_NUM = config["model_dimension"]
        self.ROUND_TOW_DROP_RATE = config["drop_rate_one"]
        self.ROUND_THREE_DROP_RATE = config["drop_rate_two"]
        # 中间结果
        self.grad_mask_sum = None
        # 加密模型的签名
        self.sig_grad_mask_list = None
        # 加密模型
        self.grad_mask_list = None
        # 承诺的签名
        self.sig_com_list = None
        # 承诺
        self.com_list = None
        # 第一轮的三元组密文
        self.final_enc_list = None
        # 第一轮密钥协商和其他客户端约定的AES密钥
        self.aes_key_list = None
        # 所有客户端DH协议的公钥
        self.n_pk_list = None
        self.p_pk_list = None
        # 所有客户端的签名公钥
        self.k_pk_list = None
        # 生成承诺的随机向量
        self.u = None
        # 加密承诺的b掩码
        self.b_mask = None
        # 加密承诺的s掩码组
        self.s_mask_list = []
        # 与其他客户端秘钥协商约定的掩码
        self.s_list = []
        # 第二轮掉线后剩余客户端
        self.C_3 = None
        # 第三轮掉线后剩余客户端
        self.C_4 = None
        # 每一轮消耗的时间
        self.running_time_list = []
        # 每一轮验证的时间
        self.verify_time_list = []
        start = time.time()
        # 模型向量
        grad = np.random.randint(1, MAX_INPUT, self.GRA_NUM)
        # 客户端的初始模型
        self.grad = grad
        # 添加掩码后的模型向量
        self.grad_mask = grad

        # DH协议秘钥
        n_key = ECC.generate(curve='p256')
        self.n_sk = int(n_key.d)
        self.n_pk = n_key.pointQ

        p_key = ECC.generate(curve='p256')
        self.p_sk = int(p_key.d)
        self.p_pk = p_key.pointQ

        # 数字签名秘钥
        x = RSA.generate(2048)
        self.k_sk = x.export_key()  # RSA signature secret key: 2048-bit
        self.k_pk = x.publickey().export_key()  # RSA signature public key: 2048-bit

        # 对称加密秘钥
        self.sk = randint(1, MAX_PRIME - 1).to_bytes(AES_KEY_BYTE_LENGTH, 'big')
        self.sk_list = []

        # 客户端索引
        self.index = index

        # 随机生成的掩码
        self.b = 0

        running_time = time.time() - start
        # print("初始化时间：{}".format(running_time))
        self.running_time_list.append(running_time)

    # round 1 计算
    def round_one(self, n_pk_list, p_pk_list, k_pk_list):
        # print("客户端{}第1轮开始".format(self.index))
        start = time.time()
        self.n_pk_list = n_pk_list
        self.p_pk_list = p_pk_list
        self.k_pk_list = k_pk_list
        # 随机掩码b
        self.b = randint(1, MAX_PRIME - 1)
        # 对随机掩码b进行秘密共享
        coefficients = sh.coeff(int(self.n / 2), self.b)
        shares_b = sh.generate_shares(self.n, coefficient=coefficients)

        # 对私钥n_sk进行秘密共享
        coefficients = sh.coeff(int(self.n / 2), self.n_sk)
        shares_n_sk = sh.generate_shares(self.n, coefficient=coefficients)

        # 第一轮返回的密文列表
        final_enc_list = []
        # 秘钥协商生成的秘钥列表
        aes_key_list = []

        for i in range(self.n):
            if i == self.index:
                final_enc_list.append(bytes([0]))
                aes_key_list.append(bytes([0]))
                continue
            # 秘钥协商协议生成AES加密秘钥
            aes_key = dh(self.p_sk, self.p_pk_list[i]).to_bytes(AES_KEY_BYTE_LENGTH, 'big')
            aes_key_list.append(aes_key)

            # 将三个需要加密的整数打包成一个byte数组
            shares_n_sk_bytes = shares_n_sk[i][1].to_bytes(SECRET_SHARE_BYTE_LENGTH, 'big')
            shares_b_bytes = shares_b[i][1].to_bytes(SECRET_SHARE_BYTE_LENGTH, 'big')
            final_bytes = shares_n_sk_bytes + shares_b_bytes + self.sk

            final_enc = aes_ctr_encrypt(final_bytes, aes_key)
            final_enc_list.append(final_enc)
        # 保存秘钥
        self.aes_key_list = aes_key_list

        running_time = time.time() - start
        self.running_time_list.append(running_time)
        # print("第一轮计算时间：{}".format(running_time))
        return final_enc_list

    # 模拟第二轮从服务器接收数据
    def round_two(self, final_enc_list):
        # print("客户端{}第二轮开始".format(self.index))
        start = time.time()
        self.final_enc_list = final_enc_list

        for i in range(self.n):
            if i == self.index:
                self.s_list.append(0)
                continue
            self.s_list.append(dh(self.n_sk, self.n_pk_list[i]))

        for i in range(self.n):
            s_vector = prg(self.s_list[i], self.GRA_NUM + 1)
            # 用来加密向量相乘后的标量值，只需要保留最后一个元素，前GRA_NUM元素直接添加到本地模型中即可
            self.s_mask_list.append(s_vector[self.GRA_NUM])
            if self.index < i:
                self.grad_mask = self.grad_mask + s_vector[0:self.GRA_NUM]
            if self.index > i:
                self.grad_mask = self.grad_mask - s_vector[0:self.GRA_NUM]
        b_vector = prg(self.b, self.GRA_NUM + 1)
        # 用来加密向量相乘后的标量值，只需要保留最后一个元素，前GRA_NUM元素直接添加到本地模型中即可
        self.b_mask = b_vector[self.GRA_NUM]
        self.grad_mask = self.grad_mask + b_vector[0:self.GRA_NUM]
        # print("加密后的模型：{}，原始模型：{}".format(self.grad_mask, self.grad))
        sig = to_sign_with_private_key(str(self.grad_mask), self.k_sk)

        running_time = time.time() - start
        self.running_time_list.append(running_time)
        # print("第二轮计算时间：{}".format(running_time))
        return self.grad_mask, sig

    def round_three(self, g_mask_sum, C_3):
        # print("客户端{}第3轮开始".format(self.index))
        start = time.time()
        self.C_3 = C_3
        self.grad_mask_sum = g_mask_sum
        rand_hash = Hash.SHA256.new()
        rand_hash.update(str(g_mask_sum).encode())
        seed = int.from_bytes(rand_hash.digest(), 'big') % 2 ** 32
        self.u = prg(seed, self.GRA_NUM)
        # print("随机生成的向量U：{}".format(self.u))
        com = dot(self.u, self.grad)
        for i in range(C_3):
            if self.index < i:
                com = com + self.s_mask_list[i]
            if self.index > i:
                com = com - self.s_mask_list[i]
        com = com + self.b_mask
        sig = to_sign_with_private_key(str(com), self.k_sk)

        running_time = time.time() - start
        self.running_time_list.append(running_time)
        # 更新验证时间开销，第三轮都属于验证时间开销
        self.verify_time_list.append(running_time)
        # print("第三轮计算时间：{}".format(running_time))
        return com, sig

    def round_four(self, com_list, sig_com_list, grad_mask_list, sig_grad_mask_list, C_4):
        # print("客户端{}第4轮开始".format(self.index))
        self.verify_four = 0
        start = time.time()
        self.C_4 = C_4
        self.com_list = com_list
        self.sig_com_list = sig_com_list
        self.grad_mask_list = grad_mask_list
        self.sig_grad_mask_list = sig_grad_mask_list
        # 加密后的所有C_4中客户端的b的秘密共享
        share_b_enc_list = []
        # 加密后的所有掉线客户端的n_sk的秘密共享
        share_n_sk_enc_list = []
        for i in range(self.n):
            # 遍历到自己，则随意赋值list占位
            if i == self.index:
                share_b_enc_list.append(bytes([0]))
                share_n_sk_enc_list.append(bytes([0]))
                self.sk_list.append(self.sk)
                continue

            # 解密对应客户端的三元组
            final_dec = aes_ctr_decrypt(self.final_enc_list[i], self.aes_key_list[i])
            shares_n_sk_bytes = final_dec[0: SECRET_SHARE_BYTE_LENGTH]
            shares_b_bytes = final_dec[SECRET_SHARE_BYTE_LENGTH: 2 * SECRET_SHARE_BYTE_LENGTH]
            self.sk_list.append(
                final_dec[2 * SECRET_SHARE_BYTE_LENGTH: 2 * SECRET_SHARE_BYTE_LENGTH + AES_KEY_BYTE_LENGTH])

            # 如果当前客户端是掉线客户端
            if self.C_4 <= i < self.n:
                # 如果是第三轮掉线的客户端，需要验证签名
                if i < self.C_3:
                    # 验证对应客户端的加密后的输入向量的签名
                    grad_mask = self.grad_mask_list[i]
                    sig_grad_mask = self.sig_grad_mask_list[i]
                    # 记录验证掉线客户端输入向量的数字签名的时间
                    verify_start = time.time()
                    to_verify_with_public_key(sig_grad_mask, str(grad_mask), self.k_pk_list[i])
                    self.verify_four = self.verify_four + (time.time() - verify_start)
                # 掉线客户端均需加密n_sk的秘密共享
                enc_start = time.time()
                share_n_sk_enc = aes_ctr_encrypt(shares_n_sk_bytes, self.sk)
                self.enc_time = self.enc_time + (time.time() - enc_start)
                share_n_sk_enc_list.append(share_n_sk_enc)
                share_b_enc_list.append(bytes([0]))
            # 如果是在线客户端
            else:
                # 记录该轮用于验证的开始时间
                verify_start = time.time()
                # 验证对应客户端的承诺签名
                com = com_list[i]
                sig_com = sig_com_list[i]
                to_verify_with_public_key(sig_com, str(com), self.k_pk_list[i])
                self.verify_four = self.verify_four + (time.time() - verify_start)
                share_n_sk_enc_list.append(bytes([0]))
                # 加密b的秘密共享
                enc_start = time.time()
                share_b_enc = aes_ctr_encrypt(shares_b_bytes, self.sk)
                self.enc_time = self.enc_time + (time.time() - enc_start)
                share_b_enc_list.append(share_b_enc)
        enc_start = time.time()
        b_enc = aes_ctr_encrypt(self.b.to_bytes(SECRET_SHARE_BYTE_LENGTH, 'big'), self.sk)
        self.enc_time = self.enc_time + (time.time() - enc_start)

        running_time = time.time() - start
        self.verify_time_list.append(self.verify_four)
        self.running_time_list.append(running_time)
        # print("第四轮计算时间：{}".format(running_time))

        return b_enc, share_n_sk_enc_list, share_b_enc_list

    def round_five(self, b_enc_list, share_n_sk_enc_lists, share_b_enc_lists):
        # print("客户端{}第5轮开始".format(self.index))
        self.verify_five = 0
        start = time.time()
        g_result = self.grad_mask_sum
        com_result = 0
        for i in range(self.C_4, self.C_3):
            g_result = g_result - self.grad_mask_list[i]
        for i in range(self.C_4):
            if i == self.index:
                b = self.b
            else:
                dec_start = time.time()
                b_bytes = aes_ctr_decrypt(b_enc_list[i], self.sk_list[i])
                self.dec_time = self.dec_time + (time.time() - dec_start)
                b = int.from_bytes(b_bytes, 'big')
            b_vector = prg(b, self.GRA_NUM + 1)
            g_result = g_result - b_vector[0:self.GRA_NUM]
            # 记录该轮用于验证的开始时间
            verify_start = time.time()
            com_result = (com_result + self.com_list[i] - b_vector[self.GRA_NUM]) % R
            self.verify_five = self.verify_five + (time.time() - verify_start)

        # 所有离线客户端的n_sk
        x_data = [i + 1 for i in range(self.C_4)]
        la = sh.get_lagrange_basis_function_list(x_data)
        offline_n_sk = []
        for offline in range(self.C_4, self.n):
            share_n_sk_list = []
            dec_start = time.time()
            for online in range(self.C_4):
                share_n_sk_enc = share_n_sk_enc_lists[online][offline]
                share_n_sk = aes_ctr_decrypt(share_n_sk_enc, self.sk_list[online])
                share_n_sk_list.append((online + 1, int.from_bytes(share_n_sk, 'big')))
            self.dec_time = self.dec_time + (time.time() - dec_start)
            n_sk = sh.get_share_value(la, share_n_sk_list)
            offline_n_sk.append(n_sk)

        # 二维数组，用于承诺的掩码
        s_mask_lists = []
        for online in range(self.C_4):
            s_mask_list = []
            for offline in range(self.C_4, self.n):
                s = dh(self.n_pk_list[online], offline_n_sk[offline - self.C_4])
                s_vector = prg(s, self.GRA_NUM + 1)
                s_mask_list.append(s_vector[self.GRA_NUM])
                if online < offline:
                    g_result = g_result - s_vector[0:self.GRA_NUM]
                else:
                    g_result = g_result + s_vector[0:self.GRA_NUM]
            s_mask_lists.append(s_mask_list)

        # 记录该轮用于验证的开始时间
        verify_start = time.time()
        for online in range(self.C_4):
            for offline in range(self.C_4, self.C_3):
                if online < offline:
                    com_result = (com_result - s_mask_lists[online][offline - self.C_4]) % R
                else:
                    com_result = (com_result + s_mask_lists[online][offline - self.C_4]) % R

        # 计算全局模型的证据标量，与收到的各客户端的证据标量之和进行比较
        com = dot(self.u, g_result)
        if com != com_result:
            print("verify erro!")

        # 验证时间
        self.verify_five = self.verify_five + (time.time() - verify_start)
        running_time = time.time() - start
        self.verify_time_list.append(self.verify_five)
        self.running_time_list.append(running_time)
        # print("第五轮计算时间：{}".format(running_time))

        # print("客户端{}结果为：{}和{}".format(self.index, g_result, com_result))
        # print("客户端{}的各轮时间为：{}".format(self.index, self.running_time_list))
        return g_result


def server(config):
    n = config["client_num"]
    GRA_NUM = config["model_dimension"]
    ROUND_TOW_DROP_RATE = config["drop_rate_one"]
    ROUND_THREE_DROP_RATE = config["drop_rate_two"]
    client_list = []
    n_pk_list, p_pk_list, k_pk_list = [], [], []
    for i in range(n):
        client = Client(i, config)
        client_list.append(client)
        n_pk_list.append(client.n_pk)
        p_pk_list.append(client.p_pk)
        k_pk_list.append(client.k_pk)

    final_enc_list = []
    for i in range(n):
        client = client_list[i]
        final_enc_list.append(client.round_one(n_pk_list, p_pk_list, k_pk_list))

    # 中间结果值，各客户端加密模型之和
    g_mask_sum = [0] * GRA_NUM
    # 客户端的加密模型
    grad_mask_list = []
    # 客户端加密模型的签名
    sig_grad_mask_list = []

    # 考虑第二轮掉线的客户端
    C_3 = int(n * (1 - ROUND_TOW_DROP_RATE))
    for i in range(C_3):
        client = client_list[i]
        final_enc = [row[i] for row in final_enc_list]
        grad_mask, sig = client.round_two(final_enc)
        g_mask_sum = g_mask_sum + grad_mask
        grad_mask_list.append(grad_mask)
        sig_grad_mask_list.append(sig)

    com_list = []
    sig_com_list = []
    # 考虑第三轮掉线的客户端
    C_4 = int(n * (1 - ROUND_TOW_DROP_RATE - ROUND_THREE_DROP_RATE))
    for i in range(C_4):
        client = client_list[i]
        com, sig = client.round_three(g_mask_sum, C_3)
        com_list.append(com)
        sig_com_list.append(sig)

    b_enc_list = []
    share_n_sk_enc_lists = []
    share_b_enc_lists = []
    for i in range(C_4):
        client = client_list[i]
        b_enc, share_n_sk_enc_list, share_b_enc_list = client.round_four(com_list, sig_com_list, grad_mask_list,
                                                                         sig_grad_mask_list, C_4)
        b_enc_list.append(b_enc)
        share_n_sk_enc_lists.append(share_n_sk_enc_list)
        share_b_enc_lists.append(share_b_enc_list)

    # 计算一下真实结果
    com_sum = 0
    g_sum = [0] * GRA_NUM
    u = []
    # 计算一下平均时间
    running_time_avg = np.array([0, 0, 0, 0, 0, 0])
    verify_time_avg = np.array([0, 0, 0])
    enc_time_avg = 0
    dec_time_avg = 0
    # for i in range(C_4):
    #     client = client_list[i]
    #     client.round_five(b_enc_list, share_n_sk_enc_lists, share_b_enc_lists)
    #     g_sum += client.grad
    #     com_sum = (com_sum + com_list[i] - client.b_mask) % R
    #     u = client.u
    #     running_time_avg = running_time_avg + np.array(client.running_time_list)
    #     verify_time_avg = verify_time_avg + np.array(client.verify_time_list)
    #     enc_time_avg = enc_time_avg + client.enc_time
    #     dec_time_avg = dec_time_avg + client.dec_time
    

    # 获取当前时间
    current_time = datetime.datetime.now()
    # 打印当前时间（默认格式）
    print("当前时间（默认格式）:", current_time)

    # print("平均运行时间：{}".format(running_time_avg / C_4))
    # print("平均验证时间：{}".format(verify_time_avg / C_4))
    # print("平均加密时间：{}".format(enc_time_avg / C_4))
    # print("平均解密时间：{}".format(dec_time_avg / C_4))
    # print("模型之和的真实结果为：{}".format(g_sum))
    # print("模型验证的真实结果为：{}".format(dot(u, g_sum)))

    client = client_list[0]
    client.round_five(b_enc_list, share_n_sk_enc_lists, share_b_enc_lists)
    print("运行时间: {}".format(client.running_time_list))
    print("验证时间: {}".format(client.verify_time_list))
    print("加密时间: {}".format(client.enc_time))
    print("解密时间: {}".format(client.dec_time))


if __name__ == '__main__':
    print("开始运行")
    # for config in drop_two_config_list:
    #     server(config)

    for config in client_config_list:
        server(config)

    # for config in model_config_list:
    #     server(config)