import pandas as pd

# 计算细纱台日产量
def spun_yarn_capacity(parameter):
    """
    :param parameter: 参数列表[细纱锭速、捻度、细纱锭数、细纱定量、细纱效率]
    :return: 细纱的台日产量
    """
    production = parameter[0]/parameter[1]*2.54/100*60*24*parameter[2]*parameter[3]*parameter[4]/10000000
    return production


# 计算粗纱台日产量
def roving_capacity(parameter):
    """
    :param parameter: 参数列表[粗纱锭速、捻度、粗纱定量、粗纱效率]
    :return: 粗纱的台日产量
    """
    production = parameter[0]/parameter[1]*2.54/100*60*24*parameter[2]*parameter[3]/1000000
    return production


# 计算并条台日常量
def merge_strip_capacity(parameter):
    """
    :param parameter: 参数列表[出条速度、并条效率、并条定量]
    :return: 并条的台日产量
    """
    production = parameter[0]*parameter[1]*parameter[2]*60*24/500000
    return production


# 计算精梳台日产量
def combing_capacity(parameter):
    """
    :param parameter:参数列表[锡林速度、给棉长度、小卷干定量、落棉率、精纺效率]
    :return:
    """
    production = parameter[0]*parameter[1]*parameter[2]*(100-parameter[3])*parameter[4]*60*24*8/10000000000*0.9
    return production


# 计算条并卷台日产量
def strip_merge_roll_capacity(parameter):
    """
    :param parameter:参数列表[出条速度、并卷定量、条并卷效率]
    :return:
    """
    production = parameter[0]*parameter[1]*parameter[2]*60*24/100000
    return production


# 计算预并条台日产量
def pre_merge_strip_capacity(parameter):
    """
    :param parameter:参数列表[出条速度、棉条定量、预并条效率]
    :return:
    """
    production = parameter[0]*parameter[1]*parameter[2]*60*24/500000*2
    return production


# 计算梳棉台日产量
def combed_cotton_capacity(parameter):
    """
    :param parameter: 参数列表[台时产量、梳棉效率]
    :return:
    """
    production = parameter[0]*parameter[1]*24/100
    return production


# 计算络筒台日产量
def winding_capacity(parameter):
    """
    :param parameter: 参数列表[速度、细纱定量、络筒效率]
    :return:
    """
    production = parameter[0]*parameter[1]*parameter[1]*60*24/10000000
    return production


# def convert_table(item_list):  # 工件
#     state = len(item_list[0]._on)
#     df = pd.DataFrame(index=range(len(item_list)*state), columns=["工件ID", "设备ID",
#                                                                   "开始时间", "结束时间", "所属工序", "所属订单"])
#     for index, values in enumerate(item_list):
#         for index_0 in range(len(values._on)):
#             df["工件ID"].iloc[index_0+((index+1)-1)*state] = index+1
#             df["设备ID"].iloc[index_0+((index+1)-1)*state] = values._on[index_0]
#             df["开始时间"].iloc[index_0+((index+1)-1)*state] = values.start[index_0]
#             df["结束时间"].iloc[index_0+((index+1)-1)*state] = values.end[index_0]
#             df["所属工序"].iloc[index_0+((index+1)-1)*state] = index_0+1
#             df["所属订单"].iloc[index_0+((index+1)-1)*state] = values.order
#     df.to_excel('结果.xlsx', index=False)

def convert_table(item_list):  # 工件
    state = len(item_list[0]._on)
    df = pd.DataFrame(index=range(len(item_list) * state), columns=["订单ID", "设备ID",
                                                                    "开始时间", "结束时间", "所属工序"])
    for index, values in enumerate(item_list):
        for index_0 in range(len(values._on)):
            df["订单ID"].iloc[index_0 + ((index + 1) - 1) * state] = index + 1
            df["设备ID"].iloc[index_0 + ((index + 1) - 1) * state] = values._on[index_0]
            df["开始时间"].iloc[index_0 + ((index + 1) - 1) * state] = values.start[index_0]
            df["结束时间"].iloc[index_0 + ((index + 1) - 1) * state] = values.end[index_0]
            df["所属工序"].iloc[index_0 + ((index + 1) - 1) * state] = index_0 + 1
    df.to_excel('结果.xlsx', index=False)






