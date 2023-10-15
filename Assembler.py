from enum import Enum
import numpy as np
from scipy.linalg import inv

class eRestraint(Enum):
    Free = 0
    Restrained = 1
    
class Assembler:
    def __init__(self, ElementList, Nodes):
        KGlobal = self.get_assemble_matrix(Nodes, ElementList)
        KGReduced = self.get_assembled_reduced_matrix(Nodes, ElementList)
        self.show_matrix_representation(KGReduced)
        forceReduced = self.get_reduced_force_vector(Nodes)
        displacement = self.get_displacement_vector(KGReduced, forceReduced)
        TotalDisplacementVector = self.get_total_displacement(Nodes, displacement)
        reactions = self.get_reactions(KGlobal, TotalDisplacementVector)

    def show_matrix_representation(self, matrix):
        for row in matrix:
            print('\t'.join(map(str, row)))

    def get_reactions(self, KG, displacements_total):
        return KG @ displacements_total

    def get_assemble_matrix(self, Nodes, ElementsList):
        dof_per_node = Nodes[0].DofPerNode
        Ndof = len(Nodes) * dof_per_node
        KG = np.zeros((Ndof, Ndof), dtype=float)
        arr2d = self.get_mapping_array_primary(Nodes)
        G = np.zeros(2 * dof_per_node, dtype=int)

        kk = 0
        for element in ElementsList:
            kk += 1
            Kg = element.get_global_stiffness_matrix()
            for i in range(dof_per_node):
                G[i] = arr2d[element.Nodes[0].ID - 1, i]
                G[i + dof_per_node] = arr2d[element.Nodes[1].ID - 1, i]

            for i in range(2 * dof_per_node):
                P = G[i]
                for j in range(2 * dof_per_node):
                    Q = G[j]
                    KG[P, Q] = KG[P, Q] + Kg[i, j]

        return KG

    def get_assembled_reduced_matrix(self, Nodes, ElementsList):
        arr2d, count = self.get_mapping_array(Nodes)
        dof_per_node = Nodes[0].DofPerNode
        G = np.zeros(2 * dof_per_node, dtype=int)
        KGReduced = np.zeros((count, count), dtype=float)

        for element in ElementsList:
            for i in range(dof_per_node):
                G[i] = arr2d[element.Nodes[0].ID - 1, i]
                G[i + dof_per_node] = arr2d[element.Nodes[1].ID - 1, i]

            Kg = element.get_global_stiffness_matrix()
            for i in range(2 * dof_per_node):
                for j in range(2 * dof_per_node):
                    P = G[i]
                    Q = G[j]
                    if P != -1 and Q != -1:
                        KGReduced[P, Q] = KGReduced[P, Q] + Kg[i, j]

        return KGReduced

    def get_reduced_force_vector(self, Nodes):
        dof_per_node = Nodes[0].DofPerNode
        arr2d, count = self.get_mapping_array(Nodes)
        force_reduced = np.zeros((count, 1), dtype=float)

        for node in Nodes:
            for i in range(dof_per_node):
                Q = arr2d[node.ID - 1, i]
                if Q != -1:
                    if i == 0:
                        force_reduced[Q, 0] = node.Fx
                    elif i == 1:
                        force_reduced[Q, 0] = node.Fy

        return force_reduced

    def get_mapping_array(self, Nodes):
        dof_per_node = Nodes[0].DofPerNode
        arr2d = np.zeros((len(Nodes), dof_per_node), dtype=int)
        count = 0

        for node in Nodes:
            row_id = node.ID
            if node.XRestraint == eRestraint.Restrained:
                arr2d[row_id - 1, 0] = -1
            if node.YRestraint == eRestraint.Restrained:
                arr2d[row_id - 1, 1] = -1
            # if isinstance(node, FrameNode) and node.RotationRestraint == eRestraint.Restrained:
            #     arr2d[row_id - 1, 2] = -1

        for i in range(len(Nodes)):
            for j in range(dof_per_node):
                if arr2d[i, j] == 0:
                    arr2d[i, j] = count
                    count += 1

        return arr2d, count

    def get_mapping_array_primary(self, Nodes):
        dof_per_node = Nodes[0].DofPerNode
        count = 0
        arr2d = np.zeros((len(Nodes), dof_per_node), dtype=int)

        for i in range(len(Nodes)):
            for j in range(dof_per_node):
                arr2d[i, j] = count
                count += 1

        return arr2d

    def get_displacement_vector(self, KGReduced, forceReduced):
        return np.dot(inv(KGReduced), forceReduced)

    def get_total_displacement(self, Nodes, displacements):
        dof_per_node = Nodes[0].DofPerNode
        arr2d, count = self.get_mapping_array(Nodes)
        number_of_dof = len(Nodes) * dof_per_node
        displacements_total = np.zeros((number_of_dof, 1), dtype=float)

        for i in range(len(Nodes)):
            for j in range(dof_per_node):
                Q = arr2d[i, j]
                if Q != -1:
                    Id = dof_per_node * i + j
                    displacements_total[Id, 0] = displacements[Q, 0]
                    node = next((x for x in Nodes if x.ID == i + 1), None)
                    if j == 0:
                        node.Dispx = displacements[Q, 0]
                    elif j == 1:
                        node.Dispy = displacements[Q, 0]
                    # elif isinstance(node, FrameNode):
                    #     node.Rotation = displacements[Q, 0]

        return displacements_total
