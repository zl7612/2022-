# -*- coding:utf-8 -*-
# 开发时间：2021/11/120:06
import random
import matplotlib.pyplot as plt
# from Instance import hun_index, sort_Priority,blendings,Process,Machine,State,Job
# from Instance import  Jobs as Joblist
# from Instance_0313 import hun_index, sort_Priority,blendings,Process,Machine,State,Job
from Instance_0313 import  Jobs as Joblist
import numpy as np
import seaborn as sns
from Instance_0313 import sort_Priority #0330增加的
from data_prepare import hun_index,blendings,Process,Machine,State,Job,Priority,change_order #0330增加的
sns.set()

class Item:
    def __init__(self):
        self.start = []#工件：各个工序加工开始时间的数组  机器：加工各个工件的开始时间数组
        self.end = []#工件：各个工序加工完成时间的数组  机器：加工各个工件的完成时间数组
        self._on = []#工件：各个工序加工对应机器的编号数组 机器：依次加工工件的编号
        self.T = []#工件：各个工序的加工时间数组 机器：在该机器上依次加工工件的加工时间数组
        self.last_ot = 0 # 工件：上一工序完工时间 机器：上一工件的完工时间
        self.L = 0 #累计加工时间
        self.process = []#工件在各工序的加工方式编码
        self.order = 0

    def update(self, s, e, on, t): #每次加工后更新每个item内的信息
        """
        功能：在对每个工序的机器和工件进行选择后，更新机和工件的加工信息
        :param s: 工序开始加工时间
        :param e: 工序结束加工时间
        :param on: 选择加工的机台/工件
        :param t: 工序加工时长
        :return: 机台已经加工的总时间/加工该工件所消耗时间
        """
        self.start.append(s)
        self.end.append(e)
        self._on.append(on)
        self.T.append(t)
        self.last_ot = e # 不是数组，不断更新，直至工件的最后一个工序
        self.L += t

    def reset(self):
        self.start = []  # 工件：各个工序加工开始时间的数组  机器：加工各个工件的开始时间数组
        self.end = []  # 工件：各个工序加工完成时间的数组  机器：加工各个工件的完成时间数组
        self._on = []  # 工件：各个工序加工对应机器的编号数组 机器：依次加工工件的编号
        self.T = []  # 工件：各个工序的加工时间数组 机器：在该机器上依次加工工件的加工时间数组
        self.last_ot = 0  # 工件：上一工序完工时间 机器：上一工件的完工时间
        self.L = 0  # 累计加工时间


class Scheduling:
    def __init__(self, J_num, Machine, State, PT): #工件数、并行机数组、工序数、加工时间数组
        self.M = Machine
        self.J_num = J_num
        self.State = State
        self.PT = PT
        self.Create_Job()
        self.Create_Machine()
        self.fitness = 0  # 适应度
        self.change = 0 #改纺次数
        self.change2 = 0
        self.change3 = 0

    def Create_Job(self): # 创建Jobs数组，存放各个工件及初始信息(item对象)
        """

        :return:
        """
        self.Jobs = [] #变为类的属性？Jobs工件个数个括号
        for i in range(self.J_num):
            J = Item() #初始化工件对象
            J.process=Process[i]#[1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            #添加改纺属性？？？

            #输出工件所属订单
            # p=0
            # o=1
            # for j in range(len(Joblist)):
            #     p+=Joblist[j]
            #     if (p<=i):
            #        if ((j==3)|(j==5)):
            #            continue
            #        else:
            #            o += 1
            #     else:
            #        break
            # J.order = o

            self.Jobs.append(J)#定义一个属性jobs，为item列表，每一个item对应一个工件，其中保存工件的加工信息

    def Create_Machine(self): # 创建Machines(机台),存放时间属性
        self.Machines = []
        for i in range(len(self.M)):  # 突出机器的阶段性，即各阶段有哪些机器（M为并行机数组）
            State_i = []
            for j in range(self.M[i]):  # M[i]为第i个工序的机台数量
                Ma = Item() #创建机器对象
                State_i.append(Ma) # 一个机台的时间属性
            self.Machines.append(State_i)  # State_i为i工序所有机台的对象数组 Machine二维数组，第一维工序，第二位（内部）工序有的台数

    # 第stage阶段的解码
    def Stage_Decode(self, CHS, Stage): #针对一个工件加工顺序(一条染色体CHS,为一个下标数组，表示加工顺序)，和某个工序
        if Stage != hun_index: #不是第6个工序（混纺工序）
            for i in CHS: # CHS为初始种群中的一条染色体，i为工件编号(随机排序

                # 选择机台
                last_od = self.Jobs[i].last_ot #工件i上一工序完工时间
                last_Md = [self.Machines[Stage][M_i].last_ot for M_i in range(self.M[Stage])]  # 该工序的各个并行机加工上一工件的完成时间 数组
                last_ML = [self.Machines[Stage][M_i].L for M_i in range(self.M[Stage])]  # 各个机器的负载（总加工时间）,每阶段更新一次 数组
                M_time = [self.PT[Stage][M_i][i] for M_i in range(self.M[Stage])]  # 在该工序中各个并行机加工i号工件的加工时间 数组
                O_et = [max(last_od,last_Md[_]) + M_time[_] for _ in range(self.M[Stage])] # 计算各个机台若加工当前工件的理论完工时间 数组

                # print('工序'++'机器组合'+'加工工件'+str(i)+'用时')

                minIndex = O_et.index(min(O_et)) #完工时间最小的机台下标 可能为数或数组

                # print('工序'+str(Stage+1)+'加工工件'+str(i+1)+'的最小机台下标为'+str(minIndex+1))

                if isinstance(minIndex, int) :#如果返回结果是一个数，即机台唯一
                    Machine = minIndex # 确定加工该工件的该工序的并行机编号
                else:#如果是数组，即机台不唯一
                    minML = max(last_ML)  # 初始化为最大负荷值
                    for j in minIndex:
                        if minML > last_ML[j]:
                            minML = last_ML[j]
                            Machine = j #找出minML中负荷值为最小负荷的机台编号
                if (self.PT[Stage][0][i] < 1): #判断为应该选择虚拟机
                        Machine = 0
                s = max(last_od, last_Md[Machine]) #确定该工件的该工序开始加工时间 = max(工件上一工序的完工时间，该工序加工机器的上一工件加工的完成时间)
                t = M_time[Machine] # 加工时间 = 机器加工时间
                #设置改纺目标？
                e = s + t #完工时间 = 开始加工时间 + 机器加工时间

                p=len(self.Machines[Stage][Machine]._on) # _on不断增加
                if ((Machine!=0) & (p!=0)):
                    process1 = self.Jobs[i].process[Stage]
                    # print('self.Jobs[i].process=============',self.Jobs[i].process)
                    j = self.Machines[Stage][Machine]._on[p-1]#当前选择的机台上一加工工件序号
                    process2 = self.Jobs[j].process[Stage]
                    # if (process1 != process2):
                    # if(process1!=process2 and process1!=2 and process1!=3 and process1!=4):
                    if ([process1,process2] in change_order):
                        self.change +=1
                    '''增加改纺的等级'''
                    # if(process1!=process2 and process1!=2 and process1!=3 and process1!=4 and 0<=Stage<6):
                    #     self.change +=1
                    # elif(process1!=process2 and process1!=2 and process1!=3 and process1!=4 and 7<=Stage<12):
                    #     self.change2 +=1
                    # elif(process1!=process2 and process1!=2 and process1!=3 and process1!=4 and Stage==12):
                    #     self.change3 +=1

                self.Jobs[i].update(s, e, Machine, t) #更新工件的item参数
                self.Machines[Stage][Machine].update(s, e, i, t) #更新机台的item参数？？？
                # self.Machines[Stage][0].last_ot = 0 #将虚拟机的上一工序完工时间改为0，保证该选的选虚拟机
                self.Machines[Stage][0].reset()


                if e > self.fitness:
                    self.fitness = e #适应度即所有工件中所有工序的最大完工时间
            # print('last_MLLLLLLLL=',len(last_ML))


        else: #是混纺工序
            p3 = []  # 已经考虑过的混纺工件
            # blendings= [[[0, 1, 2, 3], [4, 5, 6, 7]], [[20, 21], [22, 23]], [[24, 25, 26, 27], [28, 29, 30, 31]], [[32, 33], [34, 35]]]
            # 例子
            # CHS = [4, 14, 33, 7, 31, 13, 0, 11, 19, 15, 22, 30, 17, 21, 16, 35, 18, 12, 23, 32, 25, 26, 34, 27, 6, 24,1, 8, 5, 29, 3, 9, 2, 10, 28, 20]
            # blending_materials = [[0, 1, 3, 2], [4, 7, 6, 5], [21, 20], [22, 23], [25, 26, 27, 24], [31, 30, 29, 28], [33, 32], [35, 34]]
            ###改进后
            blending_materials = [[] for _ in range(2 * len(blendings))]
            flag = 0
            for q in range(len(blendings)):
                if (flag == q):
                    for j in CHS:
                        if (j in blendings[q][0]):
                            blending_materials[2*q].append(j) #将CHS中需要混纺的按顺序提取
                        elif (j in blendings[q][1]):
                            blending_materials[2*q+1].append(j)
                flag += 1

            blending_materials_1d = []#将blending_materials转为一维数组
            for item in blending_materials:
                for i in item:
                    blending_materials_1d.append(i)

            for i in CHS:
                if (i not in blending_materials_1d): #i不需要混纺
                    s = self.Jobs[i].last_ot
                    t = 0  # 加工时间为0
                    e = s + t
                    Machine = 0  # 第一台机器为虚拟机

                    self.Jobs[i].update(s, e, Machine, t)  # 更新工件的item参数
                    self.Machines[Stage][Machine].update(s, e, i, t)  # 更新机台的item参数
                    self.Machines[Stage][0].reset()
                    # self.Machines[Stage][0].last_ot = 0  # 将虚拟机的上一工序完工时间改为0，保证该选的选虚拟机
                    if e > self.fitness:
                        self.fitness = e  # 适应度即所有工件中所有工序的最大完工时间

                ###改进后
                elif (i not in p3):
                    # global n
                    for q in range(len(blendings)):
                        if (i in blending_materials[2 * q]):
                            m = blending_materials[2 * q].index(i)
                            n = blending_materials[2 * q + 1][m]
                            p3.append(i)
                            p3.append(n)
                        elif (i in blending_materials[2 * q + 1]):
                            m = blending_materials[2 * q + 1].index(i)
                            n = blending_materials[2 * q][m]
                            p3.append(i)
                            p3.append(n)

                    nn = n
                    ii = i

                    # last_od = self.Jobs[n].last_ot  # 两个混纺工件上一工序完工时间较大值？
                    # last_Md = [self.Machines[Stage][M_i].last_ot for M_i in range(self.M[Stage])]  # 该工序的各个并行机加工上一工件的完成时间 数组
                    # last_ML = [self.Machines[Stage][M_i].L for M_i in range(self.M[Stage])]  # 各个机器的负载（总加工时间）,每阶段更新一次 数组
                    # M_time = [self.PT[Stage][M_i][i] for M_i in range(self.M[Stage])]  # 在该工序中各个并行机加工i号工件的加工时间 数组
                    # O_et = [max(last_od,last_Md[_]) + M_time[_] for _ in range(self.M[Stage])]  # 计算各个机台若加工当前工件的理论完工时间 数组
                    # minIndex = O_et.index(min(O_et))  # 完工时间最小的机台下标 可能为数或数组
                    # if isinstance(minIndex, int):  # 如果是数，机台唯一
                    #     Machine = minIndex  # 确定加工该工件的该工序的并行机编号
                    # else:  # 如果是数组，机台不唯一
                    #     minML = max(last_ML)  # 初始化为最大负荷值
                    #     for j in minIndex:
                    #         if minML > last_ML[j]:
                    #             minML = last_ML[j]
                    #             Machine = j  # 找出minML中负荷值为最小负荷的机台编号
                    #
                    # s = max(last_od, last_Md[Machine])  # 开始加工时间 = max(工件上一工序的完工时间，该工序加工机器的上一工件加工的完成时间)
                    # t = M_time[Machine]  # 加工时间 = 机器加工时间
                    # e = s + t  # 完工时间 = 开始加工时间 + 机器加工时间
                    #
                    # self.Jobs[i].update(s, e, Machine, t)  # 更新混纺工件i的信息
                    # self.Jobs[n].update(e, e + t, Machine, t)  # 更新另一混纺工件n的信息
                    # self.Machines[Stage][Machine].update(s, e, i, t)  # 更新加工机器的加工信息
                    # self.Machines[Stage][Machine].update(e, e + t, n, t)
                    # if (e + t) > self.fitness:  # 更新最大完工时间
                    #     self.fitness = e + t

                    # last_od = self.Jobs[nn].last_ot  # 两个混纺工件上一工序完工时间较大值？
                    last_od = max(self.Jobs[nn].last_ot,self.Jobs[ii].last_ot)  # 两个混纺工件上一工序完工时间较大值？
                    last_Md = [self.Machines[Stage][M_i].last_ot for M_i in
                               range(self.M[Stage])]  # 该工序的各个并行机加工上一工件的完成时间 数组
                    last_ML = [self.Machines[Stage][M_i].L for M_i in range(self.M[Stage])]  # 各个机器的负载（总加工时间）,每阶段更新一次 数组
                    M_time = [self.PT[Stage][M_i][i] for M_i in range(self.M[Stage])]  # 在该工序中各个并行机加工i号工件的加工时间 数组
                    O_et = [max(last_od, last_Md[_]) + M_time[_] for _ in
                            range(self.M[Stage])]  # 计算各个机台若加工当前工件的理论完工时间 数组
                    minIndex = O_et.index(min(O_et))  # 完工时间最小的机台下标 可能为数或数组
                    if isinstance(minIndex, int):  # 如果是数，机台唯一
                        Machine = minIndex  # 确定加工该工件的该工序的并行机编号
                    else:  # 如果是数组，机台不唯一
                        minML = max(last_ML)  # 初始化为最大负荷值
                        for j in minIndex:
                            if minML > last_ML[j]:
                                minML = last_ML[j]
                                Machine = j  # 找出minML中负荷值为最小负荷的机台编号

                    s = max(last_od, last_Md[Machine])  # 开始加工时间 = max(工件上一工序的完工时间，该工序加工机器的上一工件加工的完成时间)
                    t = M_time[Machine]  # 加工时间 = 机器加工时间
                    e = s + t  # 完工时间 = 开始加工时间 + 机器加工时间

                    self.Jobs[i].update(s, e, Machine, t)  # 更新混纺工件i的信息
                    self.Jobs[nn].update(e, e + t, Machine, t)  # 更新另一混纺工件n的信息
                    self.Machines[Stage][Machine].update(s, e, i, t)  # 更新加工机器的加工信息
                    self.Machines[Stage][Machine].update(e, e + t, n, t)
                    if (e + t) > self.fitness:  # 更新最大完工时间
                        self.fitness = e + t


        # print('last_MLLLLLLLL=',len(last_ML),'&',last_ML)


    # 解码
    def Decode01(self, CHS): #CHS为传入的一条染色体
        for i in range(self.State): # 对各个工序依次进行以下操作

            self.Stage_Decode(CHS, i)#传入工序编号和该工序工件加工顺序
            Job_end = [self.Jobs[j].last_ot for j in range(self.J_num)] #通过循环获取各个工序的所有工件的完工时间，最后一个工序job_end的最大值就是这批工件的完工时间
            # Job_end按照升序排列后的下标（即各工件在第一阶段加工完成到达第二阶段的顺序）
            CHS = sorted(range(len(Job_end)), key=lambda k: Job_end[k], reverse=False) #更新下一工序的工件加工顺序
            #将优先级高的工件提到最前面（假设第1-6个工件要求最先完成）
            CHS = sort_Priority(CHS)

    # 解码
    def Decode(self, CHS):  # CHS为传入的一条染色体
        for i in range(self.State):  # 对各个工序依次进行以下操作
            self.Stage_Decode(CHS, i)  # 传入工序编号和该工序工件加工顺序
            # Job_end = [self.Jobs[j].last_ot for j in range(self.J_num)] #通过循环获取各个工序的所有工件的完工时间，最后一个工序job_end的最大值就是这批工件的完工时间
            Job_end = [self.Jobs[j].last_ot for j in CHS]  # 通过循环获取各个工序的所有工件的完工时间，最后一个工序job_end的最大值就是这批工件的完工时间
            # Job_end按照升序排列后的下标（即各工件在第一阶段加工完成到达第二阶段的顺序）
            CHS = sorted(CHS, key=lambda k: Job_end[k], reverse=False)
            # 将优先级高的工件提到最前面（假设第1-6个工件要求最先完成）
            CHS = sort_Priority(CHS)


    # 画甘特图
    def Gantt(self):
        fig = plt.figure()
        M = ['red', 'blue', 'yellow', 'orange', 'green', 'moccasin', 'purple', 'pink', 'navajowhite', 'Thistle',
             'Magenta', 'SlateBlue', 'RoyalBlue', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue','navajowhite', 'navy',
             'sandybrown','antiquewhite','aqua','aquamarine','azure','beige','bisque', 'blueviolet','brown','burlywood',
             'cadetblue','chartreuse','chocolate','coral','cornflowerblue','cornsilk','aliceblue','crimson', 'deepskyblue','dimgray',
             'dodgerblue','firebrick','floralwhite','forestgreen','sienna','salmon','whitesmoke','yellowgreen','powderblue',
                                                                                                            'red',
             'blue', 'yellow', 'orange', 'green', 'moccasin', 'purple', 'pink', 'navajowhite', 'Thistle',
             'Magenta', 'SlateBlue', 'RoyalBlue', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
             'navajowhite', 'navy',
             'sandybrown', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blueviolet', 'brown',
             'burlywood',
             'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'aliceblue', 'crimson',
             'deepskyblue', 'dimgray',
             'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'sienna', 'salmon', 'whitesmoke', 'yellowgreen',
             'powderblue',
             'red', 'blue', 'yellow', 'orange', 'green', 'moccasin', 'purple', 'pink', 'navajowhite', 'Thistle',
             'Magenta', 'SlateBlue', 'RoyalBlue', 'Aqua', 'floralwhite', 'ghostwhite', 'goldenrod', 'mediumslateblue',
             'navajowhite', 'navy',
             'sandybrown', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'blueviolet', 'brown',
             'burlywood',
             'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'aliceblue', 'crimson',
             'deepskyblue', 'dimgray',
             'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'sienna', 'salmon', 'whitesmoke', 'yellowgreen',
             'powderblue'
             ]
        # for i in range(Job):
        #     M.append()
        M_num = 0
        for i in range(len(self.M)): # self.M表示机器数组
            for j in range(self.M[i]):
                if(j==0):continue #绘图跳过虚拟机
                for k in range(len(self.Machines[i][j].start)):
                    Start_time = self.Machines[i][j].start[k]
                    End_time = self.Machines[i][j].end[k]
                    Job = self.Machines[i][j]._on[k]
                    plt.barh(M_num, width=End_time - Start_time, height=0.8, left=Start_time, \
                             color=M[Job], edgecolor='black')
                    plt.text(x=Start_time + ((End_time - Start_time) / 2 - 0.25), y=M_num - 0.2,
                             s='',size=10,fontproperties='Times New Roman') #绘制甘特图组成部分
                M_num += 1
        # plt.yticks(np.arange(M_num + 1), np.arange(1, M_num + 2), size=5, fontproperties='Times New Roman')
        # plt.yticks(np.arange(M_num), ['1-1','1-2','1-3','1-4','2-1','2-2','2-3','2-4','3-1','3-2','3-3','3-4','4-1','4-2','4-3','4-4','4-5','5-1','5-2','5-3','6-1','6-2','6-3','7-1','7-2','7-3','8-1','8-2','8-3'\
        #                                   ,'9-1','9-2','9-3','9-4','10-1','10-2','10-3','11-1','11-2','11-3','11-4','12-1',
        #                               '12-2','12-3','12-4','13-1','13-2','13-3','13-4','14-1','14-2','14-3','14-4'], fontproperties='Times New Roman')

        # plt.yticks(np.arange(M_num),
        #            ['1-1', '1-2', '1-3', '1-4',
        #             '2-1', '2-2', '2-3', '2-4',
        #             '3-1', '3-2', '3-3', '3-4',
        #             '4-1', '4-2', '4-3', '4-4', '4-5',
        #             '5-1', '5-2', '5-3',
        #             '6-1', '6-2', '6-3',
        #             '7-1', '7-2', '7-3',
        #             '8-1', '8-2','8-3' ,
        #             '9-1','9-2','9-3','9-4',
        #             '10-1','10-2','10-3',
        #             '11-1','11-2','11-3','11-4',
        #             '12-1','12-2','12-3','12-4',
        #             '13-1','13-2','13-3','13-4',
        #             '14-1','14-2','14-3','14-4'], fontproperties='Times New Roman')

        y=[]
        for i in range(len(Machine)):
            for j in range(Machine[i]-1):
                y.append(str(i+1)+'-'+str(j+1))
        plt.yticks(np.arange(M_num),y,size = 3.5,fontproperties='Times New Roman')


        plt.ylabel("机器", size=12, fontproperties='SimSun')
        plt.xlabel("时间", size=12, fontproperties='SimSun')
        # plt.tick_params(labelsize=20)
        plt.tick_params(direction='in')
        # plt.savefig("result.png",dpi=200)
        plt.show()

    def ShowJobs(self): #输出结果表
        print("fitness",self.fitness," 改纺次数",self.change)
        # print("fitness", self.fitness, " 改纺次数", self.change + self.change2 + self.change3)
        for i in range(len(self.Jobs)):
            print("工件",i+1)
            print(self.Jobs[i].start)
            for j in range(len(self.Jobs[i].start)): #
                print('工序',j+1,' 加工机台：',self.Jobs[i]._on[j]+1,' 开始时间：',self.Jobs[i].start[j],' 结束时间：',self.Jobs[i].end[j])