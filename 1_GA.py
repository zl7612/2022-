# -*- coding:utf-8 -*-
# 开发时间：2021/11/120:10
from tqdm.auto import trange
import random
import numpy as np
# from Scheduling import Scheduling as Sch
# from Instance import Job, State, Machine, PT, sort_Priority
from Scheduling_0329 import Scheduling as Sch
# from Scheduling_rule import Scheduling as Sch
# from Scheduling_0316 import Scheduling as Sch
from Instance_0313 import Job, State, Machine, PT, sort_Priority
import matplotlib.pyplot as plt
import calculate_time as ct
from data_prepare import Machine,State,Job,Priority #0330增加的
from Instance_0313 import PT,sort_Priority #0330增加的

class GA:
    def __init__(self, J_num, State, Machine, PT):
        self.State = State #工序总数
        self.Machine = Machine #并行机数组
        self.PT = PT #三维数组，工件初始加工顺序（存在重复）
        self.J_num = J_num #工件数
        self.Pm = 0.8 #交叉率
        self.Pc = 0.1 #变异率
        self.Pop_size = 1 #种群规模
        self.iter = 1000 #迭代次数

    # 随机产生染色体（只针对第一个工序，具体机台和后续工序在解码过程中根据规则考虑）
    def RCH(self):
        Chromo = [i for i in range(self.J_num)] #从0开始
        random.shuffle(Chromo)
        # 将优先级高的工件提到最前面（假设第1-6个工件要求最先完成）
        Chromo = sort_Priority(Chromo)
        return Chromo


    # 生成初始种群
    def CHS(self):
        CHS = []
        for i in range(2):
            CHS.append(self.RCH())
        return CHS

    # 选择
    def Select(self, Fit_value):
        Fit = []
        for i in range(len(Fit_value)):
            fit = 1 / Fit_value[i]
            Fit.append(fit)
        Fit = np.array(Fit)
        idx = np.random.choice(np.arange(len(Fit_value)), size=len(Fit_value), replace=True,
                               p=(Fit) / (Fit.sum()))# 有放回随机选择染色体下标
        return idx

    # 交叉
    def Crossover(self, CHS1, CHS2):
        T_r = [j for j in range(self.J_num)]
        r = random.randint(2, self.J_num)  # 产生一个不大于工件编号整数r
        random.shuffle(T_r)
        R = T_r[0:r]  # 截取
        # 将父代的染色体复制到子代中去，保持他们的顺序和位置
        H1 = [CHS1[_] for _ in R]
        H2 = [CHS2[_] for _ in R]
        C1 = [_ for _ in CHS1 if _ not in H2]
        C2 = [_ for _ in CHS2 if _ not in H1]
        CHS1, CHS2 = [], []
        k, m = 0, 0
        for i in range(self.J_num):
            if i not in R:
                CHS1.append(C1[k])
                CHS2.append(C2[k])
                k += 1
            else:
                CHS1.append(H2[m])
                CHS2.append(H1[m])
                m += 1
        # 将优先级高的工件提到最前面（假设第1-6个工件要求最先完成）
        CHS1 = sort_Priority(CHS1)
        CHS2 = sort_Priority(CHS2)
        return CHS1, CHS2

    # 变异
    def Mutation(self, CHS):
        Tr = [i_num for i_num in range(self.J_num)]
        # 机器选择部分
        r = random.randint(1, self.J_num)  # 在变异染色体中选择r个位置
        random.shuffle(Tr)
        T_r = Tr[0:r]
        K = []
        for i in T_r:
            K.append(CHS[i])
        random.shuffle(K)
        k = 0
        for i in T_r:
            CHS[i] = K[k]
            k += 1
        # 将优先级高的工件提到最前面（假设第1-6个工件要求最先完成）
        CHS = sort_Priority(CHS)
        return CHS

    def main(self):
        BF = []#存放每次迭代后目前最优的适应度值
        x = [_ for _ in range(self.iter + 1)] # 生成染色体下标数组
        C = self.CHS()#生成初始种群
        Fit = []#初始化种群每个染色体对应的适应度值
        for C_i in C:#取出各个染色体，C为种群，C_i为染色体
            s = Sch(self.J_num, self.Machine, self.State, self.PT)#初始化Scheduling类
            s.Decode(C_i)#将一条染色体传入，更新相关数据
            # Fit.append(s.change)
            # Fit.append(s.fitness)
            Fit.append( 0.5*s.fitness + 0.5*s.change)#获得各个染色体的适应度数组
            # Fit.append(s.fitness + 3 * s.change + 2 * s.change2 + s.change3)  # 增加改纺难度的适应度
        best_C = None #获得最优的
        best_fit = min(Fit)#获得该种群最优适应度值
        BF.append(best_fit)#获得每一代的最优适应度值 数组
        for i in trange(self.iter): #迭代次数
            C_id = self.Select(Fit)#把当前种群每个染色体对应的适应度值传入进行选择，得到选择后的染色体下标 数组
            C = [C[_] for _ in C_id]#更新C为选择后的染色体种群
            for Ci in range(len(C)):
                if random.random() < self.Pc:#若随机概率小于变异率0.9
                    _C = [C[Ci]]#
                    CHS1, CHS2 = self.Crossover(C[Ci], random.choice(C))#交叉得到子代
                    _C.extend([CHS1, CHS2])#拼接
                    Fi = []
                    for ic in _C:#计算出交叉后子代的适应度值并放入Fi数组中
                        s = Sch(self.J_num, self.Machine, self.State, self.PT)
                        s.Decode(ic)
                        Fi.append(0.5*s.fitness+ 0.5*s.change)
                        # Fi.append(s.fitness)
                        # Fi.append(s.change)
                        # Fi.append(s.fitness+ 3 * s.change + 2 * s.change2 + s.change3) #增加改纺等级
                    C[Ci] = _C[Fi.index(min(Fi))]#将适应度最好的替换之前种群的染色体
                    Fit.append(min(Fi))
                elif random.random() < self.Pm:#交叉率
                    CHS1 = self.Mutation(C[Ci])#交叉得到一个子代
                    C[Ci] = CHS1#替换原始种群的染色体
            Fit = []#重新计算种群适应度值
            Sc = []
            for C_i in C:
                s = Sch(self.J_num, self.Machine, self.State, self.PT)
                s.Decode(C_i)
                Sc.append(s)
                # Fit.append(s.fitness + 3 * s.change + 2 * s.change2 + s.change3)#增加改纺等级
                Fit.append(0.5*s.fitness+ 0.5*s.change)
                # Fit.append(s.fitness)
                # Fit.append(s.change)
            if min(Fit) <= best_fit:#更新最优适应度值和最优的生产顺序
                best_fit = min(Fit)
                best_C = Sc[Fit.index(min(Fit))]
            BF.append(best_fit)
        plt.plot(x, BF)#画出适应度函数的变化
        # plt.savefig('fit.png')
        plt.show()
        best_C.Gantt()#画出甘特图
        best_C.ShowJobs()
        ct.convert_table(best_C.Jobs)


if __name__ == "__main__":
    g = GA(Job, State, Machine, PT) # 生成g对象，初始化属性
    g.main() #调用main函数
