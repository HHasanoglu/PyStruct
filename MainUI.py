import string
import sys
from tkinter import TRUE
from typing import Self
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget, QPushButton
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6 import uic
from Elements import TrussElement
from Node import Node
from TrussHelper import TrussSolverHelper
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection


class MainUI(QMainWindow):
    # Ctor
    # region

    def __init__(self):
        super().__init__()
        self._helper = TrussSolverHelper()
        self._helper.CreateExample6()

        # Load the UI from 'Main.ui' and set it as the central widget
        uic.loadUi("UI/Main.ui", self)
        central_widget = self.centralWidget()

        # Create a vertical layout for the Matplotlib plot
        layout = QVBoxLayout(central_widget)

        # Create a Matplotlib figure and canvas
        self.figure = Figure(figsize=(10, 25))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set the alignment of the layout within the central widget
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Set the central widget to use the layout
        central_widget.setLayout(layout)
        self.SubscribeToEvents()
        self.resetAllCheckBoxesForCompleteModel()
        self.InitializePlotArena()
        self._showCompleteModel = TRUE

    # endregion

    # Private Methods
    # region
    def SubscribeToEvents(self):
        self.btnSolve.clicked.connect(self.btnSolveClicked)
        self.chkCompleteModel.stateChanged.connect(self.chkCompleteModel_state_changed)
        self.chkHideMembers.stateChanged.connect(self.chkHideMembers_state_changed)
        self.chkHideNodes.stateChanged.connect(self.chkHideNodes_state_changed)
        self.chkHideLoads.stateChanged.connect(self.chkHideLoads_state_changed)
        self.chkHideSupports.stateChanged.connect(self.chkHideSupports_state_changed)
        self.chkHideMemberLabel.stateChanged.connect(self.chkHideMemberLabel_state_changed)
        self.chkHideNodeLabel.stateChanged.connect(self.chkHideNodeLabel_state_changed)
        self.chkDeformedModel.stateChanged.connect(self.chkDeformedModel_state_changed)

    def resetAllCheckBoxesForCompleteModel(self):
        self._hideMembers = False
        self._hideNodes = False
        self._hideLoads = False
        self._hideSupports = False
        self._hideMemberLabel = False
        self._hideNodeLabel = False
        self._deformedModel = False
        self._showDeflectedModel = False
        
        self.chkHideMembers.setChecked(False)
        self.chkHideNodes.setChecked(False)
        self.chkHideLoads.setChecked(False)
        self.chkHideSupports.setChecked(False)
        self.chkHideMemberLabel.setChecked(False)
        self.chkHideNodeLabel.setChecked(False)
        self.chkDeformedModel.setChecked(False)

    def PlotModel(self):
        self.InitializePlotArena()
        self.PlotOriginalModel()

        if self._showDeflectedModel:
            self.PlotDeflectedModel()

        self.ax.set_box_aspect([4, 2, 2])  # This makes the plot a cube
        self.canvas.draw()

    def PlotDeflectedModel(self):
        # self.InitializePlotArena()
        for node in self._helper.NodeList:
            x, y, z = node.GetDisplacedCoordinates
            self.DrawNode(x, y, z, "")

        # Plot members
        for mbr in self._helper._elementList:
            node_i = mbr.nodeI
            node_j = mbr.nodeJ
            x1, y1, z1 = node_i.GetDisplacedCoordinates
            x2, y2, z2 = node_j.GetDisplacedCoordinates
            self.DrawElement(x1, y1, z1, x2, y2, z2, "b")

    def PlotOriginalModel(self):
        if not self._hideNodes:
            for node in self._helper.NodeList:
                x, y, z = node.coordinates
                label = ""
                if not self._hideNodeLabel:
                    label = node.label
                self.DrawNode(x, y, z, label)

                if not self._hideLoads:
                    self.DrawForceVector(node)

        # Plot members
        if not self._hideMembers:
            for mbr in self._helper._elementList:
                node_i = mbr.nodeI
                node_j = mbr.nodeJ
                x1, y1, z1 = node_i.coordinates
                x2, y2, z2 = node_j.coordinates
                self.DrawElement(x1, y1, z1, x2, y2, z2, "gray")

    def DrawArrowUpward(self, x, y, z, magnitude: float):
        self.ax.text(x, y, z + 0.5, f"{magnitude} N", color="blue", fontsize=12)
        self.ax.quiver(x, y, z, 0, 0, 0.5, color="g", picker=5, label="Arrow")

    def DrawArrowDownWard(self, x, y, z, magnitude: float):
        self.ax.text(x, y, z + 0.5, f"{magnitude} N", color="blue", fontsize=12)
        self.ax.quiver(x, y, z + 0.5, 0, 0, -0.5, color="g", label="Arrow")

    def DrawNode(self, x: float, y: float, z: float, label: string):
        self.ax.scatter(
            x, y, z, c="r", marker="o"
        )  # 'r' for red points, 'o' for circular markers
        self.ax.text(x, y, z, f"{label}", fontsize=12, ha="right")

    def DrawForceVector(self, node: Node):
        # Define the components of the force vector
        x, y, z = node.coordinates
        force_vector = node.forces
        if len(force_vector) > 0:
            if force_vector[2] > 0:
                self.DrawArrowUpward(x, y, z, force_vector[2])
            elif force_vector[2] < 0:
                self.DrawArrowDownWard(x, y, z, force_vector[2])

    def DrawElement(
        self,
        x1: float,
        y1: float,
        z1: float,
        x2: float,
        y2: float,
        z2: float,
        color: string,
    ):
        # Add a Matplotlib plot for the current member
        self.ax.plot([x1, x2], [y1, y2], [z1, z2], color=color)  # 'b' for blue lines

    def InitializePlotArena(self):
        # Clear the previous plot
        self.figure.clear()
        self.ax = self.figure.add_subplot(111, projection="3d")
        self.ax.grid()
        self.ax.set_xlabel("X (m)")
        self.ax.set_ylabel("Y (m)")
        self.ax.set_zlabel("Z (m)")
        self.ax.set_title("Model")
        self.ax.grid(False)
        # Hide the 3D plot walls
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False

    # endregion

    # Events
    # region

    def btnSolveClicked(self):
        self._helper.AnalyzeModel()

    def chkCompleteModel_state_changed(self, state):
        self._showCompleteModel = state == 2
        self.PlotModel()

    def chkDeformedModel_state_changed(self, state):
        self.chkCompleteModel.setChecked(False)
        self._showDeflectedModel = state == 2
        self.PlotModel()

    def chkHideMembers_state_changed(self, state):
        self.chkCompleteModel.setChecked(False)
        self._hideMembers = state == 2
        self.PlotModel()

    def chkHideNodes_state_changed(self, state):
        self.chkCompleteModel.setChecked(False)
        self._hideNodes = state == 2
        self.PlotModel()

    def chkHideLoads_state_changed(self, state):
        self._hideLoads = state == 2
        self.PlotModel()

    def chkHideSupports_state_changed(self, state):
        self.chkCompleteModel.setChecked(False)
        self._hideSupports = state == 2
        self.PlotModel()

    def chkHideMemberLabel_state_changed(self, state):
        self.chkCompleteModel.setChecked(False)
        self._hideMemberLabel = state == 2
        self.PlotModel()

    def chkHideNodeLabel_state_changed(self, state):
        self.chkCompleteModel.setChecked(False)
        self._hideNodeLabel = state == 2
        self.PlotModel()


# endregion


app = QApplication(sys.argv)
window = MainUI()
window.showMaximized()
sys.exit(app.exec())
