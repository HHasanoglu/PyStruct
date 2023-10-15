import math
import numpy as np

class TrussElement:
    
    def __init__(self, member_label, nodei, nodej, E, A):
        self._Id = member_label
        self._nodes = [nodei, nodej]
        self._E = E
        self._A = A

    @property
    def Nodes(self):
        return self._nodes
    
    def get_member_length(self):
        NodeI = self._nodes[0]
        NodeJ = self._nodes[1]
        return math.sqrt((NodeJ.Xcoord - NodeI.Xcoord) ** 2 + (NodeJ.Ycoord - NodeI.Ycoord) ** 2)

    def get_member_angle(self):
        NodeI = self._nodes[0]
        NodeJ = self._nodes[1]
        return math.atan2((NodeJ.Ycoord - NodeI.Ycoord), (NodeJ.Xcoord - NodeI.Xcoord))

    def get_member_angle_as_degree(self):
        return self.get_member_angle() * 180 / math.pi

    def get_transpose_matrix(self):
        theta = self.get_member_angle()
        transpose_matrix = np.zeros((2, 4))
        cos_theta = math.cos(theta) if abs(math.cos(theta)) >= 1e-10 else 0
        sin_theta = math.sin(theta) if abs(math.sin(theta)) >= 1e-10 else 0

        transpose_matrix[0, 0] = cos_theta
        transpose_matrix[0, 1] = sin_theta
        transpose_matrix[1, 2] = cos_theta
        transpose_matrix[1, 3] = sin_theta

        return transpose_matrix

    def get_local_stiffness_matrix(self):
        L = self.get_member_length()
        K = self._E * self._A / L
        k_local = np.array([[K, -K], [-K, K]])
        return k_local

    def get_global_stiffness_matrix(self):
        T = self.get_transpose_matrix()
        k_local = self.get_local_stiffness_matrix()
        return np.dot(np.dot(T.T, k_local), T)

    def get_global_displacement_vector(self):
        number_of_nodes = len(self._nodes)
        dof_per_node = self._nodes[0].DofPerNode
        displacement = np.zeros((dof_per_node * number_of_nodes, 1))

        for i in range(number_of_nodes):
            for j in range(dof_per_node):
                node = self._nodes[i]
                displacement[dof_per_node * i + j, 0] = node.DisplacementVector[j]

        return displacement

    def get_local_displacement_vector(self):
        return np.dot(self.get_transpose_matrix(), self.get_global_displacement_vector())

    def get_local_force_vector(self):
        return np.dot(self.get_local_stiffness_matrix(), self.get_local_displacement_vector())





