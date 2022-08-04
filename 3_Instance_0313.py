import random
import math
import calculate_time as ct
import numpy as np
# from data_prepare import State,Machine,JobWeight,G
from data_prepare import hun_index,blendings,Process,Machine,State,Job,Jobs,dic_order,dic_process,H,Priority #0330增加的
from data_prepare import dic_order_material,dic_order_process
random.seed(32)

def sort_Priority(list0):
    # 将优先级高的工件提到最前面（假设第1-6个工件要求最先完成）
    p1 = []
    p2 = []
    for i in list0:
        if i in Priority:
            p1.append(i)
        else:
            p2.append(i)
    p1.extend(p2)
    return p1

#
# """初始化参数，包括工序，机器，订单重量，粒度"""
# Job = 0
# State = 14
# # Machine = [6,14,8,3,2,11,3,3,4,12,3,9,44,55]
# Machine = [7,15,9,4,3,12,4,4,5,13,4,10,45,56] # 多一台虚拟机器,实际的机器量
# # Machine = [7,15,9,4,3,12,4,4,5,13,4,10,15,10] # 多一台虚拟机器,减少最后两个工序机器量,便于看图
# # H = [500, 500, 500, 600, 600, 600, 400, 400, 200, 200, 200, 200, 200, 200, 200, 200, 200, 400, 400, 400, 500, 500, 500]
# JobWeight = [7000,13000,6000,40000,30000,6000,4000,12000,8000,6000,4000]
# G = [2000,4000,3000,8000,6000,3000,2000,3000,2000,3000,2000] #粒度
# # G = [1000,2000,1500,4000,3000,1000,700,2000,1500,3000,2000] #粒度缩小
# # G = [7000,13000,6000,40000,30000,6000,4000,12000,8000,6000,4000] #不拆分
# Jobs = [0] * len(JobWeight)
# # blendings= [[[0, 1, 2, 3], [4, 5, 6, 7]], [[20, 21], [22, 23]], [[24, 25, 26, 27], [28, 29, 30, 31]], [[32, 33], [34, 35]]]
#
#
# """计算工件总量以及拆分后的列表，存放每一个订单拆为几个工件"""
# # 计算Job,工件总数
# for i in range(len(JobWeight)):
#     Jobs[i] = math.ceil(JobWeight[i] / G[i]) #计算工件数向上取整（不准确）
#     Job += Jobs[i] # Job:30
# print('Jobs=',Jobs)
# print('Job=',Job)
#
#
# """将工件按订单区分开来"""
# #Order_to_Job=  [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19], [20, 21], [22, 23], [24, 25, 26, 27], [28, 29, 30, 31], [32, 33], [34, 35]]
# Order_to_Job = []
# boundary_L = 0
# boundary_R = Jobs[0]
# for i in range(len(JobWeight)):
#     Job_Scope = [i for i in range(boundary_L,boundary_R)]
#     Order_to_Job.append(Job_Scope)
#     if (i != len(JobWeight)-1):
#         boundary_L += Jobs[i]
#         boundary_R = boundary_L+Jobs[i+1]
#     else:
#         boundary_L = 0
#         boundary_R = 0
#     # print('boundary_L=',boundary_L,'boundary_R=',boundary_R)
# print('Order_to_Job= ',Order_to_Job)
#
#
# """计算H，存放每一个工件的重量，len(H)=Job"""
# # 计算H
# H = []
# for i in range(len(Jobs)):
#     for j in range(Jobs[i] - 1):
#         H.append(G[i])
#     H.append(JobWeight[i] - G[i]*(Jobs[i]-1))
#
#
# """存放加工方式，属于某一个订单，计算改纺时使用"""
# # 存放加工方式
# Process = []
# for i in range(len(Jobs)):
#     for j in range(Jobs[i]):
#         process0 = []
#         for k in range(State):
#             process0.append(i+1)
#         Process.append(process0)
#
#
# """挑选出混纺工件"""
# hun_index = 6 # 从0开始算
# hun=[[0,1],[5,6],[7,8],[9,10]]##原料0和1混纺，原料5和6混纺……（从0开始数）按订单
# blendings = [[[],[]],[[],[]],[[],[]],[[],[]]]# 两个品种需要混纺的工件编号
# for i in range(len(hun)):
#     k = 0
#     for j in hun[i]:
#         n = 0##混纺工件起始序号
#         for m in range(j):
#             n += Jobs[m]
#         for p in range(Jobs[j]):
#             blendings[i][k].append(n+p)
#         k+=1
#
#
# """设置具有优先级的工件"""
# Priority = []
# # Priority = [0,1,2,3,4,5,6,7] # 具有优先级的工件
#
#
# """将工序索引按字典储存"""
# dic_process= {'梳棉':[0,1,2],
#        '预并条':[3],
#        '条并卷':[4],
#        '精梳':[5],
#        '预并条混':[6],
#        '并条':[7,8,9,10],
#        '粗纱':[11],
#        '细纱':[12],
#        '络筒':[13]}
#
#
# """PT需要工件编号，调整为看订单，创建订单编号和工件的字典，a(棉)，b(涤纶)代表拆分，1，2代表同类型"""
# #Jobs= [4, 4, 2, 5, 5, 2, 2, 4, 4, 2, 2]
# Job_ID = [] #存放工件所属订单索引，从0开始，36个工件
# for i in range(len(JobWeight)):
#     for j in range(Jobs[i]):
#         Job_ID.append(i)
# print("Job_ID= " , Job_ID)
# dic_order = {'L02-1045-076JLT-a':Order_to_Job[0],
#        'L02-1045-076JLT-b':Order_to_Job[1],
#        'L04-2080-073JLT-1':Order_to_Job[2],
#        'L04-2080-073JLT-2':Order_to_Job[3],
#        'L04-2080-073JLT-3':Order_to_Job[4],
#        'L03-1045-074JLT-1-a':Order_to_Job[5],
#        'L03-1045-074JLT-1-b':Order_to_Job[6],
#        'L03-1045-074JLT-2-a':Order_to_Job[7],
#        'L03-1045-074JLT-2-b':Order_to_Job[8],
#        'L03-1045-074JLT-ZF-a':Order_to_Job[9],
#        'L03-1045-074JLT-ZF-b':Order_to_Job[10]}
# print("dic_order['L02-1045-076JLT-b']=",dic_order['L02-1045-076JLT-b'])

"""开始求PT,PT存放加工时间,三维数组，从外到里为工序、机器、工件"""
def Generate(State,Job,Machine):
    PT=[]
    for i in range(State):
        Si=[]
        # if((i==0)|(i==1)|(i==2)):#梳棉
        if (i in dic_process['梳棉']):
            for j in range(Machine[i]):
                S0=[]
                for k in range(Job):
                    """全部设为一个值"""
                    # parameters=[34,90]
                    # S0.append(H[k]/ct.combed_cotton_capacity(parameters)*24)
                    # S0.append(H[k]/600)
                    """根据工件编号"""
                    # if(k >= 0 and k < 4):
                    #     S0.append(H[k]/600)
                    # elif(k >= 4 and k < 8):
                    #     S0.append(H[k]/432)
                    # elif(k >= 8 and k < 20):
                    #     S0.append(H[k]/600)
                    # elif((k==20)|(k==21)|(k==24)|(k==25)|(k==26)|(k==27)):
                    #     S0.append(H[k]/600)
                    # elif ((k==22) | (k==23) | (k==28) | (k==29) | (k==30) | (k==31)):
                    #     S0.append(H[k]/497)
                    # elif((k== 32 )| (k==33)):
                    #     S0.append(H[k]/600)
                    # elif((k==34) | (k==35)):
                    #     S0.append(H[k] / 497)
                    """根据订单字典"""
                    if (k in dic_order['L02-1045-076JLT-a']):
                        S0.append(H[k] / 600)
                    elif (k in dic_order['L02-1045-076JLT-b']):
                        S0.append(H[k] / 432)
                    elif ((k in dic_order['L04-2080-073JLT-1'])|(k in dic_order['L04-2080-073JLT-2'])|(k in dic_order['L04-2080-073JLT-3'])):
                        S0.append(H[k] / 600)
                    elif ((k in dic_order['L03-1045-074JLT-1-a'])|(k in dic_order['L03-1045-074JLT-2-a'])):
                        S0.append(H[k] / 600)
                    elif ((k in dic_order['L03-1045-074JLT-1-b'])|(k in dic_order['L03-1045-074JLT-2-b'])):
                        S0.append(H[k] / 497)
                    elif (k in dic_order['L03-1045-074JLT-ZF-a']):
                        S0.append(H[k] / 600)
                    elif (k in dic_order['L03-1045-074JLT-ZF-b']):
                        S0.append(H[k] / 497)
                Si.append(S0)
        elif(i in dic_process['预并条']):#预并条
            for j in range(Machine[i]):
                S0=[]
                for k in range(Job):
                    # parameters=[800,26,70]
                    # S0.append(H[k]/ct.pre_merge_strip_capacity(parameters)*24*5)#??
                    # S0.append(H[k]/2664)
                    """工件编号"""
                    # if(k >= 0 and k < 8):
                    #     S0.append(H[k]/2664)
                    # elif(k >= 8 and k < 20):
                    #     S0.append(H[k]/2664)
                    # elif(k >= 20 and k < 32):
                    #     S0.append(H[k]/2664)
                    # elif(k >= 32 and k < 36):
                    #     S0.append(H[k]/2664)
                    """根据订单字典"""
                    # if ((k in dic_order['L02-1045-076JLT-a'])|(k in dic_order['L02-1045-076JLT-b'])):
                    #     S0.append(H[k] / 2664)
                    """实际上效率全都一样，为2664"""
                    S0.append(H[k] / 2664)
                Si.append(S0)
        elif(i in dic_process['条并卷']):#条并卷
            for j in range(Machine[i]):
                S0=[]
                for k in range(Job):
                    # parameters=[180,78,50]
                    # S0.append(H[k]/ct.strip_merge_roll_capacity(parameters)*24*5)#?
                    # S0.append(H[k]/3473)
                    """工件编号"""
                    # if(k >= 0 and k < 8):
                    #     S0.append(H[k]/3473)
                    # elif(k >= 8 and k < 20):
                    #     S0.append(H[k]/3473)
                    # elif(k >= 20 and k < 32):
                    #     S0.append(H[k]/3473)
                    # elif(k >= 32 and k < 36):
                    #     S0.append(H[k]/3473)
                    """实际上效率全都一样，为3473"""
                    S0.append(H[k]/3473)
                Si.append(S0)
        elif(i in dic_process['精梳']):#精梳
            for j in range(Machine[i]):
                S0 = []
                for k in range(Job):
                    # parameters=[460,5.2,78,16.5,80]
                    # S0.append(H[k]/ct.combing_capacity(parameters)*24)
                    # S0.append(H[k]/505)
                    """工件编号"""
                    # if(k >= 0 and k < 8):
                    #     S0.append(H[k]/505)
                    # elif(k >= 8 and k < 20):
                    #     S0.append(H[k]/505)
                    # elif(k >= 20 and k < 32):
                    #     S0.append(H[k]/583)
                    # elif(k >= 32 and k < 36):
                    #     S0.append(H[k]/525)
                    """订单字典"""
                    if ((k in dic_order['L02-1045-076JLT-a'])|(k in dic_order['L02-1045-076JLT-b'])|
                    (k in dic_order['L04-2080-073JLT-1'])|(k in dic_order['L04-2080-073JLT-2'])|(k in dic_order['L04-2080-073JLT-3'])):
                        S0.append(H[k] / 505)
                    elif ((k in dic_order['L03-1045-074JLT-1-a'])|(k in dic_order['L03-1045-074JLT-1-b'])|
                    (k in dic_order['L03-1045-074JLT-2-a'])|(k in dic_order['L03-1045-074JLT-2-b'])):
                        S0.append(H[k] / 583)
                    elif ((k in dic_order['L03-1045-074JLT-ZF-a'])|(k in dic_order['L03-1045-074JLT-ZF-b'])):
                        S0.append(H[k] / 525)
                Si.append(S0)
        elif(i in dic_process['预并条混']):#预并条混
            for j in range(Machine[i]):
                S0 = []
                for k in range(Job):
                    # parameters=[800,26,70]
                    # S0.append(H[k]/ct.pre_merge_strip_capacity(parameters)*24/2*5)#?
                    S0.append(H[k]/8386)
                Si.append(S0)
        elif(i in dic_process['并条']):#并条
            for j in range(Machine[i]):
                S0 = []
                for k in range(Job):
                    # parameters=[350,80,26]
                    # S0.append(H[k]/ct.merge_strip_capacity(parameters)*24)
                    # S0.append(H[k]/2322)
                    """根据工件编号"""
                    # if(k >= 0 and k < 8):
                    #     S0.append(H[k]/2993)
                    # elif(k >= 8 and k < 20):
                    #     S0.append(H[k]/2322)
                    # elif(k >= 20 and k < 32):
                    #     S0.append(H[k]/2993)
                    # elif(k >= 32 and k < 36):
                    #     S0.append(H[k]/2993)
                    """订单字典"""
                    if ((k in dic_order['L02-1045-076JLT-a'])|(k in dic_order['L02-1045-076JLT-b'])):
                        S0.append(H[k] / 2993)
                    elif ((k in dic_order['L04-2080-073JLT-1'])|
                          (k in dic_order['L04-2080-073JLT-2'])|
                          (k in dic_order['L04-2080-073JLT-3'])):
                        S0.append(H[k] / 2322)
                    elif ((k in dic_order['L03-1045-074JLT-1-a'])|(k in dic_order['L03-1045-074JLT-1-b'])|
                          (k in dic_order['L03-1045-074JLT-2-a'])|(k in dic_order['L03-1045-074JLT-2-b'])):
                        S0.append(H[k] / 2993)
                    elif ((k in dic_order['L03-1045-074JLT-ZF-a'])|(k in dic_order['L03-1045-074JLT-ZF-b'])):
                        S0.append(H[k] / 2993)
                Si.append(S0)
        elif(i in dic_process['粗纱']):#粗纱
            for j in range(Machine[i]):
                S0 = []
                for k in range(Job):
                    # parameters=[950,1.42,5.9,80]
                    # S0.append(H[k]/ct.roving_capacity(parameters)*24/100)#公式待定
                    # S0.append(H[k]/2466)
                    """根据工件编号"""
                    # if(k >= 0 and k < 8):
                    #     S0.append(H[k]/2979)
                    # elif(k >= 8 and k < 20):
                    #     S0.append(H[k]/740)
                    # elif(k >= 20 and k < 32):
                    #     S0.append(H[k]/2647)
                    # elif(k >= 32 and k < 36):
                    #     S0.append(H[k]/2726)
                    """订单字典"""
                    if ((k in dic_order['L02-1045-076JLT-a']) | (k in dic_order['L02-1045-076JLT-b'])):
                        S0.append(H[k] / 2979)
                    elif ((k in dic_order['L04-2080-073JLT-1']) |
                          (k in dic_order['L04-2080-073JLT-2']) |
                          (k in dic_order['L04-2080-073JLT-3'])):
                        S0.append(H[k] / 740)
                    elif ((k in dic_order['L03-1045-074JLT-1-a']) | (k in dic_order['L03-1045-074JLT-1-b']) |
                          (k in dic_order['L03-1045-074JLT-2-a']) | (k in dic_order['L03-1045-074JLT-2-b'])):
                        S0.append(H[k] / 2647)
                    elif ((k in dic_order['L03-1045-074JLT-ZF-a']) | (k in dic_order['L03-1045-074JLT-ZF-b'])):
                        S0.append(H[k] / 2726)
                Si.append(S0)
        elif(i in dic_process['细纱']):#细纱
            for j in range(Machine[i]):
                S0 = []
                for k in range(Job):
                    # parameters=[18500,30,1104,0.97,96.5]
                    # S0.append(H[k]/ct.spun_yarn_capacity(parameters)*24/10)#公式待定
                    # S0.append(H[k]/141)
                    """根据工件编号"""
                    # if(k >= 0 and k < 8):
                    #     S0.append(H[k]/122.77)
                    # elif(k >= 8 and k < 20):
                    #     S0.append(H[k]/103.27)
                    # elif(k >= 20 and k < 32):
                    #     S0.append(H[k]/291.99)
                    # elif(k >= 32 and k < 36):
                    #     S0.append(H[k]/275.31)
                    """订单字典"""
                    if ((k in dic_order['L02-1045-076JLT-a']) | (k in dic_order['L02-1045-076JLT-b'])):
                        S0.append(H[k] / 122.77)
                    elif ((k in dic_order['L04-2080-073JLT-1']) |
                          (k in dic_order['L04-2080-073JLT-2']) |
                          (k in dic_order['L04-2080-073JLT-3'])):
                        S0.append(H[k] / 103.27)
                    elif ((k in dic_order['L03-1045-074JLT-1-a']) | (k in dic_order['L03-1045-074JLT-1-b']) |
                          (k in dic_order['L03-1045-074JLT-2-a']) | (k in dic_order['L03-1045-074JLT-2-b'])):
                        S0.append(H[k] / 291.99)
                    elif ((k in dic_order['L03-1045-074JLT-ZF-a']) | (k in dic_order['L03-1045-074JLT-ZF-b'])):
                        S0.append(H[k] / 275.31)
                Si.append(S0)
        elif(i in dic_process['络筒']):#络筒
            for j in range(Machine[i]):
                S0 = []
                for k in range(Job):
                    # parameters=[1250,0.97,72]
                    # S0.append(H[k]/ct.winding_capacity(parameters)*24/10000)##公式待定
                    # S0.append(H[k]/144)
                    """根据工件编号"""
                    # if(k >= 0 and k < 8):
                    #     S0.append(H[k]/(15.72*12))
                    # elif(k >= 8 and k < 20):
                    #     S0.append(H[k]/(8.83*12))
                    # elif(k >= 20 and k < 32):
                    #     S0.append(H[k]/(17.07*12))
                    # elif(k >= 32 and k < 36):
                    #     S0.append(H[k]/(14.41*12))
                    """订单字典"""
                    if ((k in dic_order['L02-1045-076JLT-a']) | (k in dic_order['L02-1045-076JLT-b'])):
                        S0.append(H[k] / (15.72*12))
                    elif ((k in dic_order['L04-2080-073JLT-1']) |
                          (k in dic_order['L04-2080-073JLT-2']) |
                          (k in dic_order['L04-2080-073JLT-3'])):
                        S0.append(H[k] / (8.83*12))
                    elif ((k in dic_order['L03-1045-074JLT-1-a']) | (k in dic_order['L03-1045-074JLT-1-b']) |
                          (k in dic_order['L03-1045-074JLT-2-a']) | (k in dic_order['L03-1045-074JLT-2-b'])):
                        S0.append(H[k] / (17.07*12))
                    elif ((k in dic_order['L03-1045-074JLT-ZF-a']) | (k in dic_order['L03-1045-074JLT-ZF-b'])):
                        S0.append(H[k] / (14.41*12))
                Si.append(S0)
        PT.append(Si)

    for i in range(State): #将所有工序的0号机器设为虚拟机（加工时间极短）
        for j in range(Job):
            PT[i][0][j]=0 #虚拟机加工时间
    # 使需跳过某工序的原料品种选择虚拟机
    # Jobs= [2, 4, 2, 5, 5, 2, 1, 4, 2, 2, 1]
    # 棉:0,2,3,4,5,7,9
    # 涤:1,6,8,10
    # hun=[[0,1],[5,6],[7,8],[9,10]]
    t = 0
    for i in range(len(Jobs)):  # 遍历所有订单 len(Jobs)=11
        for j in range(Jobs[i]):
            if (i in dic_order_material['棉无需混纺']):
            # if ((i == 2)|(i == 3)|(i == 4)): #棉无需混纺
                for k in range(State):
                    if (k in dic_order_process['棉无需混纺']):
                    # if ((k == 1) | (k == 3) | (k == 4) | (k == 5) | (k == 9) | (k == 11) | (k == 12) | (k == 13)):# 要经过的工序
                        PT[k][0][t] = 1000000  # 不选择虚拟机,即要经过此工序
            elif (i in dic_order_material['棉需混纺']):
            # elif ((i == 0)|(i == 5)|(i == 7)|(i == 9)):#棉需混纺
                for k in range(State):
                    if (k in dic_order_process['棉需混纺']):
                    # if ((k == 1) | (k == 3) | (k == 4) | (k == 5) | (k == 6) | (k == 9) | (k == 11) | (k == 12) | (k == 13)):
                        PT[k][0][t] = 1000000
            elif (i in dic_order_material['涤纶需混纺']):
            # elif ((i == 1)|(i == 6)|(i == 8)|(i == 10)):#涤纶需混纺
                for k in range(State):
                    if (k in dic_order_process['涤纶需混纺']):
                    # if ((k == 2) | (k == 3) | (k == 6) | (k == 10) | (k == 11) | (k == 12) | (k == 13)):
                        PT[k][0][t] = 1000000

            t += 1
    return PT

print('H=',H)
#输出PT
print('blendings=',blendings)
PT=Generate(State, Job, Machine)
# print('len(PT)=',len(PT))
# # print('PT=',PT)
# for i in range(State):
#     for j in range(Machine[i]):
#
#         for k in range(Job):
#             print(PT[i][j][k], end=" ")
#         print("\n")