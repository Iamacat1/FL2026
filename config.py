models = [50000, 100000]
clients = [500,2000,100]
drop_rate_twos = [0, 0.1, 0.2]


# 设置模型维度为变量
def get_config_list_model(model_list, client_num, drop_rate_one, drop_rate_two):
    config_list = []
    for model in model_list:
        tmp = {
            "client_num": client_num,
            "model_dimension": model,
            "drop_rate_one": drop_rate_one,
            "drop_rate_two": drop_rate_two
        }
        config_list.append(tmp)
    return config_list


# 设置客户端数量为变量
def get_config_list_client(model, client_num_list, drop_rate_one, drop_rate_two):
    config_list = []
    for client_num in client_num_list:
        tmp = {
            "client_num": client_num,
            "model_dimension": model,
            "drop_rate_one": drop_rate_one,
            "drop_rate_two": drop_rate_two
        }
        config_list.append(tmp)
    return config_list


# 设置验证阶段掉线比例为变量
def get_config_list_drop_two(model, client_num, drop_rate_one, drop_rate_two_list):
    config_list = []
    for drop_rate_two in drop_rate_two_list:
        tmp = {
            "client_num": client_num,
            "model_dimension": model,
            "drop_rate_one": drop_rate_one,
            "drop_rate_two": drop_rate_two
        }
        config_list.append(tmp)
    return config_list


model_config_list = get_config_list_model(models, 50, 0, 0)

client_config_list = get_config_list_client(100000, clients, 0, 0)

drop_two_config_list = get_config_list_drop_two(100000, 100, 0, drop_rate_twos)
