from math import fabs
import string
import uuid
from typing import List, Tuple

class Node:
    """
    A class to represent a node in a truss structure.

    Attributes:
        _guid (uuid.UUID): A unique identifier for the node.
        _coordinates (Tuple[float, float, float]): 3D coordinates (x, y, z) of the node.
        _displacements (List[float]): Displacements [dx, dy, dz, rx, ry, rz] for the node.
    """

    def __init__(self,label:int, x: float, y: float, z: float):
        """
        Initialize a new Node instance.

        Args:
            x (float): X-coordinate of the node.
            y (float): Y-coordinate of the node.
            z (float): Z-coordinate of the node.

        Returns:
            Node: A new Node instance.
        """
        self.label=label
        self._guid = uuid.uuid4()
        self._coordinates = (x, y, z)
        self._displacements: List[float] = []
        self._restraints: List[bool] = []
        self._forces: List[float] = []

    @property
    def guid(self) -> uuid.UUID:
        """
        Get the unique identifier of the node.

        Returns:
            uuid.UUID: The unique identifier.
        """
        return self._guid

    @property
    def coordinates(self) -> Tuple[float, float, float]:
        """
        Get the 3D coordinates (x, y, z) of the node.

        Returns:
            Tuple[float, float, float]: The node's coordinates.
        """
        return self._coordinates

    @property
    def displacements(self) -> List[float]:
        """
        Get the displacements [dx, dy, dz, rx, ry, rz] of the node.

        Returns:
            List[float]: The node's displacements.
        """
        return self._displacements

    @property
    def restraints(self) -> List[float]:
        """
        Get the restraints of the node.

        Returns:
            List[float]: The node's restraints.
        """
        return self._restraints

    @property
    def forces(self) -> List[float]:
        return self._forces

    @displacements.setter
    def displacements(self, values: List[float]) -> None:
        """
        Set the displacements [dx, dy, dz, rx, ry, rz] of the node.

        Args:
            values (List[float]): A list of 6 values representing displacements.
                The order of values should be [dx, dy, dz, rx, ry, rz].

        Raises:
            ValueError: If the input list does not contain 6 values.
        """
        if len(values) == 6:
            self._displacements = values
        else:
            raise ValueError("Displacements must have 6 values [dx, dy, dz, rx, ry, rz]")
    
    @restraints.setter
    def restraints(self, values: List[float]) -> None:
            self._restraints = values
            
    @forces.setter
    def forces(self, values: List[float]) -> None:
            self._forces = values
            
    def __str__(self) -> str:
        """
        Return a string representation of the node, including its GUID, coordinates, and displacements.

        Returns:
            str: A string representation of the node.
        """
        return f"Node {self.guid}: Coordinates {self.coordinates}, Displacements {self.displacements}"




# class ANode:
    
#     def __init__(self, NodeID, xcoord, ycoord):
#         self.NodeID = NodeID
#         self.xcoord = xcoord
#         self.ycoord = ycoord
#         self.dofPerNode = 0  # You can set the value accordingly in your subclass
#         self.xRestraint = None  # Set the default value accordingly in your subclass
#         self.yRestraint = None  # Set the default value accordingly in your subclass
#         self.fx = 0.0
#         self.fy = 0.0
#         self.dispx = 0.0
#         self.dispy = 0.0


#     @property
#     def Xcoord(self):
#         return self.xcoord

#     @Xcoord.setter
#     def Xcoord(self, value):
#         self.xcoord = value

#     @property
#     def Ycoord(self):
#         return self.ycoord

#     @Ycoord.setter
#     def Ycoord(self, value):
#         self.ycoord = value

#     @property
#     def ID(self):
#         return self.NodeID

#     @ID.setter
#     def ID(self, value):
#         self.NodeID = value

#     @property
#     def DofPerNode(self):
#         return self.dofPerNode

#     @DofPerNode.setter
#     def DofPerNode(self, value):
#         self.dofPerNode = value

#     @property
#     def XRestraint(self):
#         return self.xRestraint

#     @XRestraint.setter
#     def XRestraint(self, value):
#         self.xRestraint = value

#     @property
#     def YRestraint(self):
#         return self.yRestraint

#     @YRestraint.setter
#     def YRestraint(self, value):
#         self.yRestraint = value

#     @property
#     def Fx(self):
#         return self.fx

#     @Fx.setter
#     def Fx(self, value):
#         self.fx = value

#     @property
#     def Fy(self):
#         return self.fy

#     @Fy.setter
#     def Fy(self, value):
#         self.fy = value

#     @property
#     def Dispx(self):
#         return self.dispx

#     @Dispx.setter
#     def Dispx(self, value):
#         self.dispx = value

#     @property
#     def Dispy(self):
#         return self.dispy

#     @Dispy.setter
#     def Dispy(self, value):
#         self.dispy = value

#     @property
#     def Dispxy(self):
#         return (self.dispx ** 2 + self.dispy ** 2) ** 0.5

#     def getXcoordFinal(self, magnificationFactor=100):
#         return self.xcoord + magnificationFactor * self.dispx

#     def getYcoordFinal(self, magnificationFactor=100):
#         return self.ycoord + magnificationFactor * self.dispy

# class TrussNode(ANode):
#     def __init__(self, NodeID, xcoord, ycoord):
#         super().__init__(NodeID, xcoord, ycoord)
#         self.DofPerNode = 2


