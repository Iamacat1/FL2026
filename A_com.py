DH_KEY_BIT = 256
SIG_KEY_BIT = 512
SIG_BIT = 512
AES_KEY_BIT = 256
RAND_BIT = 256
SECRET_SHARE_BIT = 256
COM_BIT = 128
INDEX_BIT = 10

entry_bit = 24
from config import *

class Communication:
    def __init__(self, config):
        self.client_num = config["client_num"]
        self.model_dimension = config["model_dimension"]
        # 每个客户端上传的梯度和签名
        self.client_upload_gra = self.model_dimension * entry_bit + INDEX_BIT + SIG_BIT
        # VS发送给AS的证明
        self.vs_proof = COM_BIT * self.client_num + RAND_BIT + INDEX_BIT + SIG_BIT
        
        self.agg_grad = self.client_upload_gra
        # 客户端从VS和AS收到的分享的总位数
        self.vs_share_bit = (SECRET_SHARE_BIT + SIG_BIT + INDEX_BIT) * self.client_num + SIG_BIT
        self.as_share_bit = self.vs_share_bit

    def com_client1(self):
        # 上传梯度和签名
        r0 = self.client_upload_gra
        print("客户端第0轮通信开销:", (r0)/8/1024, "KB")
        # 收到VS的分享
        r1 = self.vs_share_bit
        print("客户端第1轮通信开销:", (r1)/8/1024, "KB")
        # 收到AS的分享
        r2 = self.as_share_bit
        print("客户端第2轮通信开销:", (r2)/8/1024, "KB")
        # 收到VS重签名后的中间聚合结果
        r3 = self.agg_grad + SIG_BIT
        print("客户端第3轮通信开销:", (r3)/8/1024, "KB")
        return r0+ r1 + r2 + r3

    def verify_com_client1(self):
        r0 = SIG_BIT
        r1 = SIG_BIT * (self.client_num + 1)
        r2 = SIG_BIT * (self.client_num + 1)
        r3 = SIG_BIT * 2
        return r0 + r1 + r2 + r3

    def com_client2_1_1(self):
        # 上传梯度和签名
        r0 = self.client_upload_gra
        print("客户端第0轮通信开销:", (r0)/8/1024, "KB")
        # 收到VS的分享
        r1 = self.vs_share_bit
        print("客户端第1轮通信开销:", (r1)/8/1024, "KB")
        # 收到AS的分享
        r2 = self.as_share_bit
        print("客户端第2轮通信开销:", (r2)/8/1024, "KB")
        receive_bit = self.vs_proof + self.client_upload_gra + SIG_BIT + SIG_BIT
        receive_as_agg = self.agg_grad
        r5 = receive_bit + receive_as_agg
        print("客户端第5轮通信开销:", (r5)/8/1024, "KB")
        return r0 + r1 + r2 + r5
    
    def verify_com_client2_1_1(self):
        r0 = SIG_BIT
        r1 = SIG_BIT * (self.client_num + 1)
        r2 = SIG_BIT * (self.client_num + 1)
        r5 = (self.vs_proof + self.client_upload_gra
                           + SIG_BIT + SIG_BIT)
        return r0 + r1 + r2 + r5

    def com_client2_1_2(self):
        return self.com_client2_1_1()

    def verify_com_client2_1_2(self):
        return self.verify_com_client2_1_1()

    def com_client2_2_1(self):
        # 上传梯度和签名
        r0 = self.client_upload_gra
        print("客户端第0轮通信开销:", (r0)/8/1024, "KB")
        # 收到VS的分享
        r1 = self.vs_share_bit
        print("客户端第1轮通信开销:", (r1)/8/1024, "KB")
        # 收到AS的分享
        r2 = self.as_share_bit
        print("客户端第2轮通信开销:", (r2)/8/1024, "KB")
        receive_bit = self.vs_proof + SIG_BIT
        request_bit = self.agg_grad + SIG_BIT
        r5 = receive_bit + request_bit
        print("客户端第5轮通信开销:", (r5)/8/1024, "KB")
        return r0 + r1 + r2 + r5

    def verify_com_client2_2_1(self):
        r0 = SIG_BIT
        r1 = SIG_BIT * (self.client_num + 1)
        r2 = SIG_BIT * (self.client_num + 1)
        r5 = (self.vs_proof + SIG_BIT)
        return r0 + r1 + r2 + r5

    def com_client2_2_2(self):
        # 上传梯度和签名
        r0 = self.client_upload_gra
        print("客户端第0轮通信开销:", (r0)/8/1024, "KB")
        # 收到VS的分享
        r1 = self.vs_share_bit
        print("客户端第1轮通信开销:", (r1)/8/1024, "KB")
        # 收到AS的分享
        r2 = self.as_share_bit
        print("客户端第2轮通信开销:", (r2)/8/1024, "KB")
        receive_bit = self.vs_proof + SIG_BIT
        request_bit = self.agg_grad + SIG_BIT
        request_vs_agg_bit = self.agg_grad
        r5 = receive_bit + request_bit + request_vs_agg_bit
        print("客户端第5轮通信开销:", (r5)/8/1024, "KB")
        return  r0 + r1 + r2 + r5
    
    def verify_com_client2_2_2(self):
        return self.verify_com_client2_2_1()

    def base_com_vs(self):
        receive_client_bit = self.client_upload_gra * self.client_num
        send_to_as_bit = receive_client_bit + SIG_BIT * self.client_num
        print("VS第1轮通信开销:", (receive_client_bit + send_to_as_bit)/8/1024/1024, "MB")
        receive_as_bit = self.client_upload_gra
        return receive_client_bit + send_to_as_bit + receive_as_bit

    def com_vs_1(self):
        receive_client_bit = self.client_upload_gra * self.client_num
        send_to_as_bit = (self.client_upload_gra + SIG_BIT) * self.client_num
        # VS发送给所有客户端的分享的总位数
        send_to_client_share_bit = (self.vs_share_bit + SIG_BIT) * self.client_num
        r1 = receive_client_bit + send_to_as_bit + send_to_client_share_bit
        print("VS第1轮通信开销:", (r1)/8/1024/1024, "MB")
        receive_as_bit = self.client_upload_gra
        send_bit = (self.client_upload_gra + SIG_BIT) * self.client_num
        r3 = receive_as_bit + send_bit
        print("VS第3轮通信开销:", (r3)/8/1024/1024, "MB")
        return r1 + r3

    def verify_com_vs_1(self):
        r1 = SIG_BIT * (self.client_num + 2*self.client_num + (self.client_num + 1)*self.client_num)
        r3 = SIG_BIT + SIG_BIT * 2 * self.client_num
        return r1 + r3

    def com_vs_2_1_2(self):
        receive_client_bit = self.client_upload_gra * self.client_num
        send_to_as_bit = (self.client_upload_gra + SIG_BIT) * self.client_num
        # VS发送给所有客户端的分享的总位数
        send_to_client_share_bit = (self.vs_share_bit + SIG_BIT) * self.client_num
        r1 = receive_client_bit + send_to_as_bit + send_to_client_share_bit
        print("VS第1轮通信开销:", (r1)/8/1024/1024, "MB")
        receive_as_bit = self.client_upload_gra
        send_proof_bit = self.vs_proof
        r3 = receive_as_bit + send_proof_bit
        print("VS第3轮通信开销:", (r3)/8/1024/1024, "MB")
        # VS发送自己的聚合结果给所有客户端
        r5 = self.agg_grad * self.client_num
        print("VS第5轮通信开销:", (r5)/8/1024/1024, "MB")
        return r1 + r3 + r5

    def verify_com_vs_2_1_2(self):
        r1 = SIG_BIT * (self.client_num + 2*self.client_num + (self.client_num + 1)*self.client_num)
        r3 = SIG_BIT + self.vs_proof
        r5 = SIG_BIT * self.client_num
        return r1 + r3 + r5

    def com_vs_2_2_2(self):
        receive_client_bit = self.client_upload_gra * self.client_num
        send_to_as_bit = (self.client_upload_gra + SIG_BIT) * self.client_num
        # VS发送给所有客户端的分享的总位数
        send_to_client_share_bit = (self.vs_share_bit + SIG_BIT) * self.client_num
        r1 = receive_client_bit + send_to_as_bit + send_to_client_share_bit
        print("VS第1轮通信开销:", (r1)/8/1024/1024, "MB")
        receive_as_bit = self.client_upload_gra
        send_proof_bit = (self.vs_proof)
        r3 = receive_as_bit + send_proof_bit
        print("VS第3轮通信开销:", (r3)/8/1024/1024, "MB")
        send_as_agg_bit = (self.agg_grad + SIG_BIT) * self.client_num
        # VS发送自己的聚合结果给所有客户端
        send_agg_bit = self.agg_grad * self.client_num
        r5 = send_as_agg_bit + send_agg_bit
        print("VS第5轮通信开销:", (r5)/8/1024/1024, "MB")
        return r1 + r3 + r5

    def verify_com_vs_2_2_2(self):
        return self.verify_com_vs_2_1_2()

    def com_as_1(self):
        # 收到VS发送的每个客户端的梯度和重签名
        receive_vs_bit = (self.client_upload_gra + SIG_BIT) * self.client_num
        # 聚合结果
        send_vs_bit = self.agg_grad
        # VS发送给所有客户端的分享的总位数
        send_to_client_share_bit = (self.as_share_bit + SIG_BIT) * self.client_num
        r2 = receive_vs_bit + send_vs_bit + send_to_client_share_bit
        print("AS第2轮通信开销:", (r2)/8/1024/1024, "MB")
        return r2
    
    def verify_com_as_1(self):
        r2 = SIG_BIT * (2 * self.client_num + 1 + (self.client_num + 1)*self.client_num)
        return r2

    def com_as_2_1_1(self):
        # 收到VS发送的每个客户端的梯度和重签名
        receive_vs_bit = (self.client_upload_gra + SIG_BIT) * self.client_num
        # 聚合结果
        send_vs_bit = self.agg_grad
        # VS发送给所有客户端的分享的总位数
        send_to_client_share_bit = (self.as_share_bit + SIG_BIT) * self.client_num
        r2 = receive_vs_bit + send_vs_bit + send_to_client_share_bit
        print("AS第2轮通信开销:", (r2)/8/1024/1024, "MB")
        receive_proof_bit = self.vs_proof
        send_client_bit = (self.vs_proof + self.client_upload_gra
                           + SIG_BIT + SIG_BIT) * self.client_num
        r4 = receive_proof_bit + send_client_bit
        print("AS第4轮通信开销:", (r4)/8/1024/1024, "MB")
        r5 = self.agg_grad * self.client_num
        print("AS第5轮通信开销:", (r5)/8/1024/1024, "MB")
        return r2 + r4 + r5
    
    def verify_com_as_2_1_1(self):
        r2 = SIG_BIT * (2 * self.client_num + 1 + (self.client_num + 1)*self.client_num)
        receive_proof_bit = self.vs_proof
        send_client_bit = (self.vs_proof + self.client_upload_gra
                           + SIG_BIT + SIG_BIT) * self.client_num
        r4 = receive_proof_bit + send_client_bit
        r5 = SIG_BIT * self.client_num
        return r2 + r4 + r5
        

    def com_as_2_2_1(self):
        # 收到VS发送的每个客户端的梯度和重签名
        receive_vs_bit = (self.client_upload_gra + SIG_BIT) * self.client_num
        # 聚合结果
        send_vs_bit = self.agg_grad
        # VS发送给所有客户端的分享的总位数
        send_to_client_share_bit = (self.as_share_bit + SIG_BIT) * self.client_num
        r2 = receive_vs_bit + send_vs_bit + send_to_client_share_bit
        print("AS第2轮通信开销:", (r2)/8/1024/1024, "MB")
        receive_proof_bit = self.vs_proof
        send_client_bit = (receive_proof_bit + SIG_BIT) * self.client_num
        r4 = receive_proof_bit + send_client_bit
        print("AS第4轮通信开销:", (r4)/8/1024/1024, "MB")
        return r2 + r4

    def verify_com_as_2_2_1(self):
        r2 = SIG_BIT * (2 * self.client_num + 1 + (self.client_num + 1)*self.client_num)
        receive_proof_bit = self.vs_proof
        send_client_bit = (receive_proof_bit + SIG_BIT) * self.client_num
        r4 = receive_proof_bit + send_client_bit
        r5 = SIG_BIT * self.client_num
        return r2 + r4 + r5

if __name__ == "__main__":
    client_1 = []
    client_211 = []
    client_212 = []
    client_221 = []
    client_222 = []

    vs_1 = []
    vs_212 = []
    vs_222 = []

    as_1 = []
    as_211 = []
    as_221 = []
    for config in model_config_list:
        print("客户端数量:", config["client_num"], "模型维度:", config["model_dimension"])
        com = Communication(config)
        print("case1---------------------")
        # print("case1 客户端通信开销:", com.com_client1()/8/1024, "KB")
        # print("case1 VS通信开销:", com.com_vs_1()/8/1024/1024, "MB")
        # print("case1 AS通信开销:", com.com_as_1()/8/1024/1024, "MB")
        client_1.append(com.verify_com_client1()/8/1024/1024)
        vs_1.append(com.verify_com_vs_1()/8/1024/1024)
        as_1.append(com.verify_com_as_1()/8/1024/1024)

        print("case2-1-1---------------------")
        # print("case2-1-1 客户端通信开销:", com.com_client2_1_1()/8/1024, "KB")
        # print("case2-1-1 AS通信开销:", com.com_as_2_1_1()/8/1024/1024, "MB")
        client_211.append(com.verify_com_client2_1_1()/8/1024/1024)
        as_211.append(com.verify_com_as_2_1_1()/8/1024/1024)

        print("case2-1-2---------------------")
        # print("case2-1-2 客户端通信开销:", com.com_client2_1_2()/8/1024, "KB")
        # print("case2-1-2 VS通信开销:", com.com_vs_2_1_2()/8/1024/1024, "MB")
        client_212.append(com.verify_com_client2_1_2()/8/1024/1024)
        vs_212.append(com.verify_com_vs_2_1_2()/8/1024/1024)

        print("case2-2-1---------------------")
        # print("case2-2-1 客户端通信开销:", com.com_client2_2_1()/8/1024, "KB")
        # print("case2-2-1 AS通信开销:", com.com_as_2_2_1()/8/1024/1024, "MB")
        client_221.append(com.verify_com_client2_2_1()/8/1024/1024)
        as_221.append(com.verify_com_as_2_2_1()/8/1024/1024)

        print("case2-2-2---------------------")
        # print("case2-2-2 客户端通信开销:", com.com_client2_2_2()/8/1024, "KB")
        # print("case2-2-2 VS通信开销:", com.com_vs_2_2_2()/8/1024/1024, "MB")
        client_222.append(com.verify_com_client2_2_2()/8/1024/1024)
        vs_222.append(com.verify_com_vs_2_2_2()/8/1024/1024)
    print("客户端开销-----------------------------")
    print("case1=", client_1)
    print("case211=", client_211)
    print("case212=", client_212)
    print("case221=", client_221)
    print("case222=", client_222)
    print("VS开销-----------------------------")
    print("case1=", vs_1)
    print("case212=", vs_212)
    print("case222=", vs_222)
    print("AS开销-----------------------------")
    print("case1=", as_1)
    print("case211=", as_211)
    print("case221=", as_221) 