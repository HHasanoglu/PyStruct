import math
import string
import numpy as np
from typing import List, Tuple
from Material import Material
from Node import Node
from Section import Section
import uuid


class TrussElement:
    """
    A class to represent a truss element that connects two nodes.

    Attributes:
        node1 (Node): The first node connected to the truss element.
        node2 (Node): The second node connected to the truss element.
        material (float): Young's Modulus of the material.
        area (float): Cross-sectional area of the truss element.
        length (float): Length of the truss element.
        forces (List[float]): Applied forces at the nodes [Fx1, Fy1, Fz1, Fx2, Fy2, Fz2].
        moments (List[float]): Applied moments at the nodes [Mx1, My1, Mz1, Mx2, My2, Mz2].
    """

    def __init__(
        self, label: int, nodeI: Node, nodeJ: Node, material: Material, section: Section
    ):
        """
        Initialize a new TrussElement instance.

        Args:
            node1 (Node): The first node connected to the truss element.
            node2 (Node): The second node connected to the truss element.
            material (float): Young's Modulus of the material.
            area (float): Cross-sectional area of the truss element.
        """
        self.handle = uuid.uuid4()
        self.label = label
        self.nodeI = nodeI
        self.nodeJ = nodeJ
        self.material = material
        self.section = section

        self.length = self.calculate_length()
        self.forces = [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ]  # Initialize applied forces to zero
        self.moments = [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        ]  # Initialize applied moments to zero
        

    def get_global_stiffness_matrix(self) -> List[List[float]]:
        TransformationMatrix = self.GetTransformationMatrix()
        Klocal = self.GetLocalStiffnessMatrix()
        Kglobal = np.dot(
            np.transpose(TransformationMatrix), np.dot(Klocal, TransformationMatrix)
        )
        return Kglobal

    def calculate_length(self) -> float:
        """
        Calculate the length of the truss element based on the coordinates of connected nodes.

        Returns:
            float: The length of the truss element.
        """
        x1, y1, z1 = self.nodeI.coordinates
        x2, y2, z2 = self.nodeJ.coordinates

        # Calculate Euclidean distance in 3D space
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5

        return length

    def set_loads(self, forces: List[float], moments: List[float]) -> None:
        """
        Set applied loads at the nodes.

        Args:
            forces (List[float]): Applied forces at the nodes [Fx1, Fy1, Fz1, Fx2, Fy2, Fz2].
            moments (List[float]): Applied moments at the nodes [Mx1, My1, Mz1, Mx2, My2, Mz2].
        """
        if len(forces) == 6 and len(moments) == 6:
            self.forces = forces
            self.moments = moments
        else:
            raise ValueError("Both forces and moments must have 6 values each.")

    def get_loads(self) -> Tuple[List[float], List[float]]:
        """
        Get applied loads at the nodes.

        Returns:
            Tuple[List[float], List[float]]: A tuple containing applied forces and moments at the nodes.
        """
        return self.forces, self.moments

    def GetLocalStiffnessMatrix(self) -> List[List[float]]:
        """
        Calculate the local stiffness matrix for the truss element in its local coordinate system.

        Returns:
            List[List[float]]: The 4x4 local stiffness matrix.
        """
        E = self.material.youngs_modulus
        A = self.section.area
        L = self.length

        # Stiffness matrix for a truss element in its local coordinate system
        k_local = (E * A) / L

        # Define the 4x4 local stiffness matrix
        stiffness_matrix_local = [[k_local, -k_local], [-k_local, k_local]]

        return stiffness_matrix_local

    def GetTransformationMatrix(self) -> List[float]:
        """
        Transform a vector from the truss element's local coordinate system to the global coordinate system.

        Args:
            local_vector (List[float]): A vector in the local coordinate system (6 DOFs for two nodes).

        Returns:
            List[float]: The vector transformed to the global coordinate system (6 DOFs for two nodes).
        """
        # Calculate the direction cosines of the truss element's orientation
        dx = self.nodeJ.coordinates[0] - self.nodeI.coordinates[0]
        dy = self.nodeJ.coordinates[1] - self.nodeI.coordinates[1]
        dz = self.nodeJ.coordinates[2] - self.nodeI.coordinates[2]

        cos_theta = dx / self.length
        cos_phi = dy / self.length
        cos_psi = dz / self.length

        # Define the 2x6 transformation matrix that includes translations and rotations
        T = np.array(
            [
                [cos_theta, cos_phi, cos_psi, 0, 0, 0],
                [0, 0, 0, cos_theta, cos_phi, cos_psi],
            ]
        )

        return T


# class TrussElement:

#     def __init__(self, member_label, nodei, nodej, E, A):
#         self._Id = member_label
#         self._nodes = [nodei, nodej]
#         self._E = E
#         self._A = A

#     @property
#     def Nodes(self):
#         return self._nodes

#     def get_member_length(self):
#         NodeI = self._nodes[0]
#         NodeJ = self._nodes[1]
#         return math.sqrt((NodeJ.Xcoord - NodeI.Xcoord) ** 2 + (NodeJ.Ycoord - NodeI.Ycoord) ** 2)

#     def get_member_angle(self):
#         NodeI = self._nodes[0]
#         NodeJ = self._nodes[1]
#         return math.atan2((NodeJ.Ycoord - NodeI.Ycoord), (NodeJ.Xcoord - NodeI.Xcoord))

#     def get_member_angle_as_degree(self):
#         return self.get_member_angle() * 180 / math.pi

#     def get_transpose_matrix(self):
#         theta = self.get_member_angle()
#         transpose_matrix = np.zeros((2, 4))
#         cos_theta = math.cos(theta) if abs(math.cos(theta)) >= 1e-10 else 0
#         sin_theta = math.sin(theta) if abs(math.sin(theta)) >= 1e-10 else 0

#         transpose_matrix[0, 0] = cos_theta
#         transpose_matrix[0, 1] = sin_theta
#         transpose_matrix[1, 2] = cos_theta
#         transpose_matrix[1, 3] = sin_theta

#         return transpose_matrix

#     def get_local_stiffness_matrix(self):
#         L = self.get_member_length()
#         K = self._E * self._A / L
#         k_local = np.array([[K, -K], [-K, K]])
#         return k_local

#     def get_global_stiffness_matrix(self):
#         T = self.get_transpose_matrix()
#         k_local = self.get_local_stiffness_matrix()
#         return np.dot(np.dot(T.T, k_local), T)

#     def get_global_displacement_vector(self):
#         number_of_nodes = len(self._nodes)
#         dof_per_node = self._nodes[0].DofPerNode
#         displacement = np.zeros((dof_per_node * number_of_nodes, 1))

#         for i in range(number_of_nodes):
#             for j in range(dof_per_node):
#                 node = self._nodes[i]
#                 displacement[dof_per_node * i + j, 0] = node.DisplacementVector[j]

#         return displacement

#     def get_local_displacement_vector(self):
#         return np.dot(self.get_transpose_matrix(), self.get_global_displacement_vector())

#     def get_local_force_vector(self):
#         return np.dot(self.get_local_stiffness_matrix(), self.get_local_displacement_vector())
