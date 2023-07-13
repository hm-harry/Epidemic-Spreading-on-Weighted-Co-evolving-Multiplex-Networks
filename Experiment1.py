# Code provided by Wu Huiming

import sys
import random
import time
import matplotlib.pyplot as plt
import copy
import numpy as np

class Node(object):
    nodeName = None
    # 存储点的地址
    linkedNodes = None
    # 存储点的名称
    linkedNodesDemo = None
    # 存储边权 传播层
    linkedNodesWeight = None
    # 存储点的数量
    linkedNodesAmount = 0
    # 存储点的边权和 传播层
    linkedWeightAmount = 0
    # 存储点的最大边权
    MaxWeightEdge = 0
    # 点的状态 信息层
    nodeStateI = None
    # 点的状态 传播层
    nodeStateB = None
    
 
    def __init__(self, name):
        if self.nodeName is None:
            self.nodeName = ""
        if self.linkedNodes is None:
            self.linkedNodes = []
        if self.linkedNodesDemo is None:
            self.linkedNodesDemo = []
        if self.linkedNodesWeight is None:
            self.linkedNodesWeight = []
        if self.nodeStateI is None:
            self.nodeStateI = "U"
        if self.nodeStateB is None:
            self.nodeStateB = "S"
        self.nodeName = name
 
    def add(self, node):
        str1 = "".join(node.nodeName)
        str2 = "".join(self.nodeName)
 
        self.linkedNodes.append(node)
        self.linkedNodesDemo.append(str1)
        self.linkedNodesAmount += 1
        node.linkedNodes.append(self)
        node.linkedNodesDemo.append(str2)
        node.linkedNodesAmount += 1
    
    def addweight(self, node, weight, delta):
        for i in range(self.linkedNodesAmount):
            add = delta * self.linkedNodesWeight[i] / self.linkedWeightAmount
            self.linkedWeightAmount += add
            self.linkedNodesWeight[i] += add
            if self.linkedNodesWeight[i] > self.MaxWeightEdge:
                self.MaxWeightEdge = self.linkedNodesWeight[i]
            if self.linkedNodes[i].linkedNodesDemo.count(self.nodeName) != 0:
                Index = self.linkedNodes[i].linkedNodesDemo.index(self.nodeName)
                self.linkedNodes[i].linkedWeightAmount += add
                self.linkedNodes[i].linkedNodesWeight[Index] += add
                if self.linkedNodes[i].linkedNodesWeight[Index] > self.linkedNodes[i].MaxWeightEdge:
                    self.linkedNodes[i].MaxWeightEdge = self.linkedNodes[i].linkedNodesWeight[Index]
            else:
                print("err" + self.nodeName + self.linkedNodes[i].nodeName)
        
        if weight > self.MaxWeightEdge:
                self.MaxWeightEdge = weight
        
        str1 = "".join(node.nodeName)
        str2 = "".join(self.nodeName)
        
        self.linkedNodes.append(node)
        self.linkedNodesDemo.append(str1)
        self.linkedNodesWeight.append(weight)
        self.linkedNodesAmount += 1
        self.linkedWeightAmount += weight
        node.linkedNodes.append(self)
        node.linkedNodesDemo.append(str2)
        node.linkedNodesWeight.append(weight)
        node.linkedNodesAmount += 1
        node.linkedWeightAmount += weight
        if len(self.linkedNodesWeight) != self.linkedNodesAmount or len(node.linkedNodesWeight) != node.linkedNodesAmount:
            print(self.nodeName + " " + node.nodeName)
        
    def sub(self, node):
        str1 = "".join(node.nodeName)
        str2 = "".join(self.nodeName)
        self.linkedNodes.remove(node)
        self.linkedNodesDemo.remove(str1)
        self.linkedNodesAmount -= 1
        node.linkedNodes.remove(self)
        node.linkedNodesDemo.remove(str2)
        node.linkedNodesAmount -= 1
    
    def subweight(self, node):
        str1 = "".join(node.nodeName)
        str2 = "".join(self.nodeName)
        if self.linkedNodes.count(node) != 0:
                Index = self.linkedNodes.index(node)
                self.linkedWeightAmount -= self.linkedNodesWeight[Index]
                del self.linkedNodesWeight[Index]
        if node.linkedNodes.count(self) != 0:
                Index = node.linkedNodes.index(self)
                node.linkedWeightAmount -= node.linkedNodesWeight[Index]
                del node.linkedNodesWeight[Index]
        self.linkedNodes.remove(node)
        self.linkedNodesDemo.remove(str1)
        self.linkedNodesAmount -= 1
        node.linkedNodes.remove(self)
        node.linkedNodesDemo.remove(str2)
        node.linkedNodesAmount -= 1
        
        self.MaxWeightEdge = 0
        node.MaxWeightEdge = 0
        for i in range(self.linkedNodesAmount):
            if self.MaxWeightEdge < self.linkedNodesWeight[i]:
                self.MaxWeightEdge = self.linkedNodesWeight[i]
        for i in range(node.linkedNodesAmount):
            if node.MaxWeightEdge < node.linkedNodesWeight[i]:
                node.MaxWeightEdge = node.linkedNodesWeight[i]

# 返回某个无权网络的所有节点的度总和
def allDegree(list):
    sum = 0
    for w in range(0, len(list)):
        sum = sum + list[w].linkedNodesAmount
    return sum
    
# 返回某个加权网络的所有节点的度总和
def allDegreeWeight(list):
    sum = 0
    for w in range(0, len(list)):
        sum = sum + list[w].linkedWeightAmount
    return sum
    
#     建立BA网络 初始全连接m0个节点 每次增加m条边  总共N个节点
def BANetwork(N, m, m0):
    BANodeList = []
    # 初始化一列节点（BA）,有m0个初始节点
    for i in range(0, m0):
        nodeName = "A" + str(i)
        BANodeList.append(Node(nodeName))
        
    for i in range(m0 - 1):
        for j in range(i + 1, m0):
            BANodeList[i].add(BANodeList[j])
        
    #     BA内部以指定概率连边
    while m0 < N:
        nodeName = "A" + str(m0)
        BANodeList.append(Node(nodeName))
        count= 0
        while count < m:
            for i in range(0, m0):
                rateNumber = random.uniform(0, 1)
                if rateNumber < BANodeList[i].linkedNodesAmount / allDegree(BANodeList) and (BANodeList[m0].nodeName not in BANodeList[i].linkedNodesDemo):
                    BANodeList[i].add(BANodeList[m0])
                    count += 1
                if count >= m:
                    break
        m0 += 1
    return BANodeList
    
#     建立BBV网络
def BBVNetwork(N, m, m0, weight, delta):
    BBVNodeList = []
    # 初始化一列节点（BBV）,有m0个初始节点
    for i in range(0, m0):
        nodeName = "B" + str(i)
        BBVNodeList.append(Node(nodeName))
    
    for i in range(m0 - 1):
        for j in range(i + 1, m0):
            BBVNodeList[i].addweight(BBVNodeList[j], weight, delta)

    #     BBV内部以指定概率连边
    while m0 < N:
        nodeName = "B" + str(m0)
        BBVNodeList.append(Node(nodeName))
        count = 0
        count2 = 0
        while count < m:
            for i in range(0, m0):
                rateNumber = random.uniform(0, 1)
                if (rateNumber < BBVNodeList[i].linkedWeightAmount / allDegreeWeight(BBVNodeList)) and (BBVNodeList[m0].nodeName not in BBVNodeList[i].linkedNodesDemo):
                    BBVNodeList[i].addweight(BBVNodeList[m0], weight, delta)
                    count += 1
                if count >= m:
                    break
        m0 += 1
    return BBVNodeList

#     SIS
#     N为单层节点总数
#     S为健康且会被感染的状态;
#     I为感染状态，且会传播;
#     R为康复状态，且没有感染能力
#     P为上层网络UA传播的概率系数 P2为得知消息之后断边重连的概率 B1为未知消息的传播概率系数 B2为已知消息的传播概率系数 Y为I节点自愈为R节点的概率
def SIS(N, P, P2, B1, B2, Y, recursionTime, averageTime):
    startTime = time.time()
    
    UListCopy = [0] * recursionTime
    AListCopy = [0] * recursionTime
    SListCopy = [0] * recursionTime
    IListCopy = [0] * recursionTime
    
    averageI = 1
#     重复试验30次
    while averageI <= averageTime:
        #     构造ERNetwork和BBVNetwork
        BANodeList = BANetwork(N, 3, 3)
        BBVNodeList = BBVNetwork(N, 3, 3, 2, 1)
                
        # 初始化原状态
        for i in range(len(BANodeList)):
            BANodeList[i].nodeStateB = "S"
            BANodeList[i].nodeStateI = "U"
        for i in range(len(BBVNodeList)):
            BBVNodeList[i].nodeStateB = "S"
            BBVNodeList[i].nodeStateI = "U"
        
        UList = []
        AList = []
        SList = []
        IList = []
        Xline = []
        
        #     初始化感染第rand节点
        rand = int(N / 2)
        BBVNodeList[rand].nodeStateB = "I"
        BBVNodeList[rand].nodeStateI = "A"
        
        recursion = 1
        circulation = 1
        
        # 传播50遍
        while recursion <= recursionTime:
            # 存储每一遍的SIR节点个数，并存储每次传播的初始感染节点
            UAmount = 0
            AAmount = 0
            SAmount = 0
            IAmount = 0
            for i in range(0, N):
                if BANodeList[i].nodeStateI == "U":
                    UAmount += 1
                elif BANodeList[i].nodeStateI == "A":
                    AAmount += 1
                if BBVNodeList[i].nodeStateB == "S":
                    SAmount += 1
                elif BBVNodeList[i].nodeStateB == "I":
                    IAmount += 1
            UList.append(UAmount)
            AList.append(AAmount)
            SList.append(SAmount)
            IList.append(IAmount)
            Xline.append(recursion)
            
            #             打印网络平均度
#             DegreeSum = 0
#             for i in range(0, N):
#                 DegreeSum += BANodeList[i].linkedWeightAmount
#             DegreeAvg = DegreeSum / N
#             if circulation % 5 == 0:
#                 print("网络平均度", DegreeAvg, sep=":", end=',')
            
            #             统计当前循环所有感染节点，listForAllInfected
            listForAllInfected = None
            if listForAllInfected is None:
                listForAllInfected = []

            for i in range(0, N):
                if BBVNodeList[i].nodeStateB == "I":
                    listForAllInfected.append(BBVNodeList[i])
            infectedNum = len(listForAllInfected)

            #             统计当前循环所有未感染节点，listForNoInfected
            listForNoInfected = []
            for i in range(0, N):
                if BBVNodeList[i].nodeStateB == "S":
                    listForNoInfected.append(BBVNodeList[i])
            noinfectedNum = len(listForNoInfected)
            

            #         得知信息之后断开连边重新随机连接健康节点
            for i in range(0, N):
                if BBVNodeList[i].nodeStateB == "S" and BANodeList[i].nodeStateI == "A":
                    for neighbor in BBVNodeList[i].linkedNodes:
                        if neighbor.nodeStateB == "I":
                            rateNumber = random.uniform(0, 1)
                            if rateNumber <= P2:
                                INDEX = BBVNodeList[i].linkedNodes.index(neighbor)
                                EdgeWeight = BBVNodeList[i].linkedNodesWeight[INDEX]
                                BBVNodeList[i].subweight(neighbor)
                                index = random.randint(0, noinfectedNum - 1)
                                BBVNodeList[i].addweight(listForNoInfected[index], EdgeWeight, 1)
            
#             for i in range(0, N):
#                 for j in range(0, N):
#                     if BBVNodeList[i].nodeStateB == "S" and  BBVNodeList[j].nodeStateB == "I" and BBVNodeList[i].nodeName in BBVNodeList[j].linkedNodesDemo and BANodeList[i].nodeStateI == "A":
#                         rateNumber = random.uniform(0, 1)
#                         if rateNumber <= P2:
# #                             print(1) # test
#                             INDEX = BBVNodeList[i].linkedNodes.index(BBVNodeList[j])
#                             EdgeWeight = BBVNodeList[i].linkedNodesWeight[INDEX]
#                             BBVNodeList[i].subweight(BBVNodeList[j])
#                             index = random.randint(0, noinfectedNum - 1)
#                             BBVNodeList[i].addweight(listForNoInfected[index], EdgeWeight, 0)
                            
            #         BBV同层内传播
            tmp = 0 # 标志位 判断是否传播 仅第一次有用
            for i in range(0, N):
                if BBVNodeList[i].nodeStateB == "S":
                    for neighbor in BBVNodeList[i].linkedNodes:
                        if neighbor.nodeStateB == "I":
                            INDEX = BBVNodeList[i].linkedNodes.index(neighbor)
                            EdgeWeight = BBVNodeList[i].linkedNodesWeight[INDEX]
                            EdgeWeightI = BBVNodeList[i].MaxWeightEdge
                            EdgeWeightJ = neighbor.MaxWeightEdge
                            if BANodeList[i].nodeStateI == "U":
                                rateNumber = random.uniform(0, 1)
                                if rateNumber <= B1 * 2 * EdgeWeight / (EdgeWeightI + EdgeWeightJ):
                                    BBVNodeList[i].nodeStateB = "I"
                                    BANodeList[i].nodeStateI = "A"
                                    tmp = 1
                            else:
                                rateNumber = random.uniform(0, 1)
                                if rateNumber <= B2 * 2 * EdgeWeight / (EdgeWeightI + EdgeWeightJ):
                                    BBVNodeList[i].nodeStateB = "I"
                                    BANodeList[i].nodeStateI = "A"
                                    tmp = 1

            #         如果没有传播 换一个节点传播
            if tmp == 0 and recursion == 1:
                BBVNodeList[rand].nodeStateB = "S"
                BBVNodeList[rand].nodeStateI = "U"
                rand = random.randint(0, int(N / 2))
                BBVNodeList[rand].nodeStateB = "I"
                BBVNodeList[rand].nodeStateI = "A"
                UList = []
                AList = []
                SList = []
                IList = []
                Xline = []
                continue
            
            #         上层网络进行传播UA
            for i in range(0, N):
                if BANodeList[i].nodeStateI == "U":
                    for neighbor in BANodeList[i].linkedNodes:
                        if neighbor.nodeStateI == "A":
                            rateNumber = random.uniform(0, 1)
                            if rateNumber <= (P * (infectedNum) / N):
                                BANodeList[i].nodeStateI = "A"
                                if (infectedNum) / N > 1:
                                    print(1)
                                
#             for i in range(0, N):
#                 for j in range(0, N):
#                     if BANodeList[i].nodeStateI == "U" and BANodeList[j].nodeStateI == "A" and (BANodeList[i].nodeName in BANodeList[j].linkedNodesDemo):
#                         rateNumber = random.uniform(0, 1)
#                         if rateNumber <= (P * (infectedNum) / N):
#                             BANodeList[i].nodeStateI = "A"
#                             if (infectedNum + RNum) / N > 1:
#                                 print(1)
                            
            #          感染节点变成易感节点
            for i in range(0, infectedNum):
                rateNumber = random.uniform(0, 1)
                if rateNumber <= Y:
                    listForAllInfected[i].nodeStateB = "S"
            
            recursion += 1
            circulation += 1
            
        for i in range(len(SListCopy)):
            UListCopy[i] += UList[i]
            AListCopy[i] += AList[i]
            SListCopy[i] += SList[i]
            IListCopy[i] += IList[i]
            
        averageI += 1
#         print() # 输出打印换行
        
    for i in range(len(SListCopy)):
        UListCopy[i] = UListCopy[i] / averageTime
        AListCopy[i] = AListCopy[i] / averageTime
        SListCopy[i] = SListCopy[i] / averageTime
        IListCopy[i] = IListCopy[i] / averageTime
    
    #     绘图
    plt.subplot(2, 1, 1)
    x = range(len(SListCopy))
    plt.plot(x, SListCopy, color='green', marker='.', linestyle='-', label='S')
    plt.plot(x, IListCopy, color='red', marker='.', linestyle='-', label='I')
    plt.title("SIS Model", fontproperties='SimHei')
    plt.legend() # 显示图例
    
    plt.subplot(2, 1, 2)
    x = range(len(UListCopy))
    plt.plot(x, UListCopy, color='green', marker='.', linestyle='-', label='U')
    plt.plot(x, AListCopy, color='red', marker='.', linestyle='-', label='A')
    plt.title("UA Model", fontproperties='SimHei')
    plt.legend() # 显示图例
    
    plt.tight_layout(pad=1.08)
    plt.show()
    finishTime = time.time()
    print("Running Time:", finishTime- startTime, "s")
    print("Finish")
    
    return SListCopy, IListCopy, UListCopy, AListCopy
    
def main():
    SListCopy11, IListCopy11, UListCopy11, AListCopy11 = SIS(500, 0, 0.6, 0.5, 0.1, 0.2, 40, 20)
    SListCopy21, IListCopy21, UListCopy21, AListCopy21 = SIS(500, 0.2, 0.6, 0.5, 0.1, 0.2, 40, 20)
    SListCopy31, IListCopy31, UListCopy31, AListCopy31 = SIS(500, 0.4, 0.6, 0.5, 0.1, 0.2, 40, 20)
    SListCopy41, IListCopy41, UListCopy41, AListCopy41 = SIS(500, 0.6, 0.6, 0.5 , 0.1, 0.2, 40, 20)
    x = range(len(IListCopy11))
    plt.xlabel("t")
    plt.ylabel("I(t)")
    plt.plot(x, IListCopy11, color='red', marker='.', linestyle='-', label='P=0')
    plt.plot(x, IListCopy21, color='blue', marker='.', linestyle='-', label='P=0.2')
    plt.plot(x, IListCopy31, color='yellow', marker='.', linestyle='-', label='P=0.4')
    plt.plot(x, IListCopy41, color='green', marker='.', linestyle='-', label='P=0.6')
    plt.title("I", fontproperties='SimHei')
    plt.legend() # 显示图例
    
    SListCopy12, IListCopy12, UListCopy12, AListCopy12 = SIS(500, 0, 0, 0.3, 0.2, 0.5, 40, 20)
    SListCopy22, IListCopy22, UListCopy22, AListCopy22 = SIS(500, 0.2, 0, 0.3, 0.2, 0.5, 40, 20)
    SListCopy32, IListCopy32, UListCopy32, AListCopy32 = SIS(500, 0.4, 0, 0.3, 0.2, 0.5, 40, 20)
    SListCopy42, IListCopy42, UListCopy42, AListCopy42 = SIS(500, 0.6, 0, 0.3, 0.2, 0.5, 40, 20)
    x = range(len(IListCopy12))
    plt.xlabel("t")
    plt.ylabel("I(t)")
    plt.plot(x, IListCopy12, color='red', marker='.', linestyle='-', label='P=0')
    plt.plot(x, IListCopy22, color='blue', marker='.', linestyle='-', label='P=0.2')
    plt.plot(x, IListCopy32, color='yellow', marker='.', linestyle='-', label='P=0.4')
    plt.plot(x, IListCopy42, color='green', marker='.', linestyle='-', label='P=0.6')
    plt.title("I", fontproperties='SimHei')
    plt.legend() # 显示图例
    
    SListCopy13, IListCopy13, UListCopy13, AListCopy13 = SIS(500, 0, 0.2, 0.3, 0.2, 0.5, 40, 20)
    SListCopy23, IListCopy23, UListCopy23, AListCopy23 = SIS(500, 0.2, 0.2, 0.3, 0.2, 0.5, 40, 20)
    SListCopy33, IListCopy33, UListCopy33, AListCopy33 = SIS(500, 0.4, 0.2, 0.3, 0.2, 0.5, 40, 20)
    SListCopy43, IListCopy43, UListCopy43, AListCopy43 = SIS(500, 0.6, 0.2, 0.3, 0.2, 0.5, 40, 20)
    x = range(len(IListCopy13))
    plt.xlabel("t")
    plt.ylabel("I(t)")
    plt.plot(x, IListCopy13, color='red', marker='.', linestyle='-', label='P=0')
    plt.plot(x, IListCopy23, color='blue', marker='.', linestyle='-', label='P=0.2')
    plt.plot(x, IListCopy33, color='yellow', marker='.', linestyle='-', label='P=0.4')
    plt.plot(x, IListCopy43, color='green', marker='.', linestyle='-', label='P=0.6')
    plt.title("I", fontproperties='SimHei')
    plt.legend() # 显示图例
    
    SListCopy14, IListCopy14, UListCopy14, AListCopy14 = SIS(500, 0, 0.4, 0.3, 0.2, 0.5, 40, 20)
    SListCopy24, IListCopy24, UListCopy24, AListCopy24 = SIS(500, 0.2, 0.4, 0.3, 0.2, 0.5, 40, 20)
    SListCopy34, IListCopy34, UListCopy34, AListCopy34 = SIS(500, 0.4, 0.4, 0.3, 0.2, 0.5, 40, 20)
    SListCopy44, IListCopy44, UListCopy44, AListCopy44 = SIS(500, 0.6, 0.4, 0.3, 0.2, 0.5, 40, 20)
    x = range(len(IListCopy14))
    plt.xlabel("t")
    plt.ylabel("I(t)")
    plt.plot(x, IListCopy14, color='red', marker='.', linestyle='-', label='P=0')
    plt.plot(x, IListCopy24, color='blue', marker='.', linestyle='-', label='P=0.2')
    plt.plot(x, IListCopy34, color='yellow', marker='.', linestyle='-', label='P=0.4')
    plt.plot(x, IListCopy44, color='green', marker='.', linestyle='-', label='P=0.6')
    plt.title("I", fontproperties='SimHei')
    plt.legend() # 显示图例
    
if __name__ == "__main__":
    main()
