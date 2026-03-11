def verify(public_key, signature, message):
    try:
        public_key.verify(signature, message)
        # print("✅ 签名验证成功")
        return True
    except Exception as e:
        print(f"❌ 签名验证失败: {e}")
        return False
    
from ecdsa import SigningKey, SECP256k1
import time
import numpy as np


private_key = SigningKey.generate(curve=SECP256k1)
grad = np.random.randint(1, 2*16, 100000)
start = time.time()
# for i in range(self.client_num):
#     prg(i, self.GRA_NUM)
signature = private_key.sign(grad.tobytes())
sign_time = time.time() - start
print(f"签名时间：{sign_time}")

start = time.time()
verify(private_key.get_verifying_key(), signature, grad.tobytes())
verify_time = time.time() - start
print(f"验证时间：{verify_time}")
