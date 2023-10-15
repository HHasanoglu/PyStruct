
class ANode:
    
    def __init__(self, NodeID, xcoord, ycoord):
        self.NodeID = NodeID
        self.xcoord = xcoord
        self.ycoord = ycoord
        self.dofPerNode = 0  # You can set the value accordingly in your subclass
        self.xRestraint = None  # Set the default value accordingly in your subclass
        self.yRestraint = None  # Set the default value accordingly in your subclass
        self.fx = 0.0
        self.fy = 0.0
        self.dispx = 0.0
        self.dispy = 0.0


    @property
    def Xcoord(self):
        return self.xcoord

    @Xcoord.setter
    def Xcoord(self, value):
        self.xcoord = value

    @property
    def Ycoord(self):
        return self.ycoord

    @Ycoord.setter
    def Ycoord(self, value):
        self.ycoord = value

    @property
    def ID(self):
        return self.NodeID

    @ID.setter
    def ID(self, value):
        self.NodeID = value

    @property
    def DofPerNode(self):
        return self.dofPerNode

    @DofPerNode.setter
    def DofPerNode(self, value):
        self.dofPerNode = value

    @property
    def XRestraint(self):
        return self.xRestraint

    @XRestraint.setter
    def XRestraint(self, value):
        self.xRestraint = value

    @property
    def YRestraint(self):
        return self.yRestraint

    @YRestraint.setter
    def YRestraint(self, value):
        self.yRestraint = value

    @property
    def Fx(self):
        return self.fx

    @Fx.setter
    def Fx(self, value):
        self.fx = value

    @property
    def Fy(self):
        return self.fy

    @Fy.setter
    def Fy(self, value):
        self.fy = value

    @property
    def Dispx(self):
        return self.dispx

    @Dispx.setter
    def Dispx(self, value):
        self.dispx = value

    @property
    def Dispy(self):
        return self.dispy

    @Dispy.setter
    def Dispy(self, value):
        self.dispy = value

    @property
    def Dispxy(self):
        return (self.dispx ** 2 + self.dispy ** 2) ** 0.5

    def getXcoordFinal(self, magnificationFactor=100):
        return self.xcoord + magnificationFactor * self.dispx

    def getYcoordFinal(self, magnificationFactor=100):
        return self.ycoord + magnificationFactor * self.dispy

class TrussNode(ANode):
    def __init__(self, NodeID, xcoord, ycoord):
        super().__init__(NodeID, xcoord, ycoord)
        self.DofPerNode = 2
