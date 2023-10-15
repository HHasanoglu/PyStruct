from enum import Enum
from Assembler import Assembler, eRestraint
from Elements import TrussElement
from Node import TrussNode
import math


class eBenchmarkTests(Enum):
    Test1 = 1
    Test2 = 2
    Test3 = 3
    Test4 = 4
    Test5 = 5
    
class eResultToShow(Enum):
    Dispx = 0
    Dispy = 1
    Dispxy = 2
    Stress = 3
    Strain = 4

class TrussSolverHelper:
  
    def __init__(self):
        self._nodeList = []
        self._elementList = []
        

    @property
    def NodeList(self):
        return self._nodeList

    @property
    def ElementList(self):
        return self._elementList

    def AddNode(self, NodeID, Xcoord, Ycoord):
        node=TrussNode(NodeID, Xcoord, Ycoord)
        self._nodeList.append(node)

    def AddMember(self, memberLabel, nodeI, nodeJ, E, Area):
        nodei = self.GetNodeById(nodeI)
        nodej = self.GetNodeById(nodeJ)
        self._elementList.append(TrussElement(memberLabel, nodei, nodej, E, Area))

    def AddLoad(self, nodeId, fx, fy):
        node = self.GetNodeById(nodeId)
        node.Fx = fx
        node.Fy = fy

    def AddRestrainedNode(self, nodeId, isXRestrained, isYRestrained):
        node = self.GetNodeById(nodeId)
        if isinstance(node, TrussNode):
            node.XRestraint = eRestraint.Restrained if isXRestrained else eRestraint.Free
            node.YRestraint = eRestraint.Restrained if isYRestrained else eRestraint.Free

    def GetNodeById(self, NodeId):
        return next((x for x in self._nodeList if x.ID == NodeId), None)

    def ClearNodeAndElements(self):
        self._nodeList.clear()
        self._elementList.clear()

    def AnalyzeModel(self):
        isAnalysisSuccessful = False
        if len(self._elementList) > 0 and len(self._nodeList) > 0:
            assembler = Assembler(self._elementList, self._nodeList)
            isAnalysisSuccessful = True
        return isAnalysisSuccessful

    def GetMinValueForColorMap(self, type):
        minValue = 0
        if self._nodeList is not None:
            if type == eResultToShow.Dispx:
                minValue = min(abs(x.Dispx) for x in self._nodeList)
            elif type == eResultToShow.Dispy:
                minValue = min(abs(x.Dispy) for x in self._nodeList)
            elif type == eResultToShow.Dispxy:
                minValue = min(abs(x.Dispxy) for x in self._nodeList)
            else:
                minValue = min(abs(x.Dispy) for x in self._nodeList)
        return minValue

    def GetMaxValueForColorMap(self, type):
        maxValue = 0
        if self._nodeList is not None:
            if type == eResultToShow.Dispx:
                maxValue = max(abs(x.Dispx) for x in self._nodeList)
            elif type == eResultToShow.Dispy:
                maxValue = max(abs(x.Dispy) for x in self._nodeList)
            elif type == eResultToShow.Dispxy:
                maxValue = max(abs(x.Dispxy) for x in self._nodeList)
            else:
                maxValue = max(abs(x.Dispy) for x in self._nodeList)
        return maxValue

    def SetExample(self, test):
        self.ClearNodeAndElements()
        if test == eBenchmarkTests.Test1:
            self.CreateExample1()
        elif test == eBenchmarkTests.Test2:
            self.CreateExample2()
        elif test == eBenchmarkTests.Test3:
            self.CreateExample3()
        elif test == eBenchmarkTests.Test4:
            self.CreateExample4()
        elif test == eBenchmarkTests.Test5:
            self.CreateExample5()
        else:
            self.CreateExample5()

    def CreateExample1(self):
        self.AddNode(1, 0, 0)
        self.AddNode(2, 5, 8.66)
        self.AddNode(3, 15, 8.66)
        self.AddNode(4, 20, 0)
        self.AddNode(5, 10, 0)
        self.AddNode(6, 10, -5)
        E = 200 * math.pow(10, 9)
        A = 5000
        self.AddMember(1, 1, 2, E, A)
        self.AddMember(2, 2, 3, E, A)
        self.AddMember(3, 3, 4, E, A)
        self.AddMember(4, 4, 5, E, A)
        self.AddMember(5, 1, 5, E, A)
        self.AddMember(6, 2, 5, E, A)
        self.AddMember(7, 3, 5, E, A)
        self.AddMember(8, 5, 6, E, A)
        self.AddRestrainedNode(4, True, True)
        self.AddRestrainedNode(6, True, True)
        self.AddLoad(1, 0, -200000)

    def CreateExample2(self):
        self.AddNode(1, 0, 0)
        self.AddNode(2, 1, 0)
        self.AddNode(3, 0.5, 1)
        E = 1 * math.pow(10, 6)
        A = 10000
        self.AddMember(1, 1, 2, E, A)
        self.AddMember(2, 2, 3, E, A)
        self.AddMember(3, 3, 1, E, A)
        self.AddRestrainedNode(1, True, True)
        self.AddRestrainedNode(2, False, True)
        self.AddLoad(3, 0, -20)

    def CreateExample3(self):
        E = 2 * math.pow(10, 11)
        A = 5000

        self.AddNode(1, 0, 6)
        self.AddNode(2, 4, 6)
        self.AddNode(3, 8, 6)
        self.AddNode(4, 12, 6)
        self.AddNode(5, 16, 6)
        self.AddNode(6, 12, 2)
        self.AddNode(7, 8, 0)
        self.AddNode(8, 4, 2)

        self.AddMember(1, 1, 2, E, A)
        self.AddMember(2, 2, 3, E, A)
        self.AddMember(3, 3, 4, E, A)
        self.AddMember(4, 4, 5, E, A)
        self.AddMember(5, 5, 6, E, A)
        self.AddMember(6, 6, 7, E, A)
        self.AddMember(7, 7, 8, E, A)
        self.AddMember(8, 1, 8, E, A)
        self.AddMember(9, 2, 8, E, A)
        self.AddMember(10, 3, 7, E, A)
        self.AddMember(11, 4, 6, E, A)
        self.AddMember(12, 3, 8, E, A)
        self.AddMember(13, 3, 6, E, A)

        self.AddRestrainedNode(1, True, True)
        self.AddRestrainedNode(5, False, True)

        self.AddLoad(2, 0, -10000)
        self.AddLoad(3, 0, -30000)
        self.AddLoad(4, 0, -5000)

    def CreateExample4(self):
        E = 200 * math.pow(10, 9)
        A = 5000
        node=0
        for x, y in [(0, 0), (10, 10), (20, 8.333), (30, 6.667), (40, 5), (50, 3.333), (60, 1.667), (70, 3.333), (80, 1.667), (90, 3.333), (100, 5), (110, 6.667), (120, 8.333), (130, 10), (140, 0), (130, 0), (120, 0), (110, 0), (100, 0), (90, 0), (80, 0), (70, 0), (60, 0), (50, 0), (40, 0), (30, 0), (20, 0), (10, 0)]:
            node += 1
            self.AddNode(node, x, y)

        member = 1
        for i in range(1, 28):
            if i != 15:
                self.AddMember(member, i, i + 1, E, A)
                member+=1
                

        end = 28
        for i in range(2, 15):
            self.AddMember(member, i, end, E, A)
            member += 1
            end -= 1

        self.AddMember(member + 1, 3, 28, E, A)
        self.AddMember(member + 2, 4, 27, E, A)
        self.AddMember(member + 3, 5, 26, E, A)
        self.AddMember(member + 4, 6, 25, E, A)
        self.AddMember(member + 5, 7, 24, E, A)
        self.AddMember(member + 6, 7, 22, E, A)
        self.AddMember(member + 7, 9, 22, E, A)
        self.AddMember(member + 8, 9, 20, E, A)
        self.AddMember(member + 9, 10, 19, E, A)
        self.AddMember(member + 10, 11, 18, E, A)
        self.AddMember(member + 11, 12, 17, E, A)
        self.AddMember(member + 12, 13, 16, E, A)

        self.AddRestrainedNode(1, True, True)
        self.AddRestrainedNode(15, True, True)
        self.AddRestrainedNode(16, True, True)
        self.AddRestrainedNode(28, True, True)

        for i in range(17, 28):
            self.AddLoad(i, 0, -40000)

    def CreateExample5(self):
        E = 200 * math.pow(10, 9)
        A = 5000
        node = 0

        for i in range(18):
            self.AddNode(i + 1, node, 0)
            node += 10

        member = 0
        for i in range(1, 31):
            self.AddMember(member + 1, i, i + 1, E, A)
            member += 1

        end = 32
        for i in range(2, 17):
            self.AddMember(member, i, end, E, A)
            member += 1
            end -= 1

        self.AddMember(member + 1, 1, 32, E, A)
        self.AddMember(member + 2, 3, 32, E, A)
        self.AddMember(member + 3, 3, 30, E, A)
        self.AddMember(member + 4, 4, 29, E, A)
        self.AddMember(member + 5, 6, 29, E, A)
        self.AddMember(member + 6, 7, 28, E, A)
        self.AddMember(member + 7, 8, 27, E, A)
        self.AddMember(member + 8, 9, 26, E, A)
        self.AddMember(member + 9, 9, 24, E, A)
        self.AddMember(member + 10, 10, 23, E, A)
        self.AddMember(member + 11, 11, 22, E, A)
        self.AddMember(member + 12, 12, 21, E, A)
        self.AddMember(member + 13, 14, 21, E, A)
        self.AddMember(member + 14, 15, 20, E, A)
        self.AddMember(member + 15, 15, 18, E, A)

        self.AddRestrainedNode(1, True, True)
        self.AddRestrainedNode(17, True, True)
        self.AddRestrainedNode(21, True, True)
        self.AddRestrainedNode(29, True, True)

        for i in range(6, 13):
            self.AddLoad(i, 0, -200000)
