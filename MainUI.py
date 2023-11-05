from ast import IsNot
from asyncio.windows_events import NULL
from logging import setLogRecordFactory
import string
import sys
from tkinter import TRUE
from typing import Self
import uuid
from xml.dom.minidom import Element
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QPushButton,
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6 import uic
from Elements import TrussElement
from Node import Node
from TrussHelper import TrussSolverHelper
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
import matplotlib.pyplot as plt


class MainUI(QMainWindow):
    # Ctor
    # region

    def __init__(self):
        super().__init__()
        self.PrepareUI()

    # endregion

    # Private Methods
    # region

    def PrepareUI(self):
        self._helper = TrussSolverHelper()
        self._helper.CreateExample7()
        self._trussElementDrawingEntity = {}
        self._highlightedElement:TrussElement=NULL

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
        self.SliderScale.setMinimum(0)
        self.SliderScale.setMaximum(100)
        self._scale = 0
        self.setWindowTitle("Your Application")
        self.setGeometry(100, 100, 800, 600)

        # Create a QTableWidget
        self.elementsTable.setColumnCount(5)  # Number of columns
        self.elementsTable.setHorizontalHeaderLabels(
            ["Element Id", "Elements Label", "Start Node", "End Node", "Length"]
        )  # Column headers
        self.elementsTable.verticalHeader().setVisible(False)
        self.elementsTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.elementsTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.elementsTable.setColumnHidden(0, True)
        self.UpdateTableData();
    

    def UpdateTableData(self):
        # Clear existing data in the table
        self.elementsTable.setRowCount(0)
        sorted_element_list:list[TrussElement] = sorted(self._helper.ElementList,key=lambda x:x.label)

        for row, element in enumerate(sorted_element_list):
            truss_element:TrussElement = element
            self.elementsTable.insertRow(row)
            row_data = [truss_element.handle , truss_element.label, truss_element.nodeI.label, truss_element.nodeJ.label, f"{truss_element.length:.2f}"]
            for col, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.elementsTable.setItem(row, col, item)
                item = self.elementsTable.item(row, col)  # Access the item in the first column (column 0)
                if item:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    def SubscribeToEvents(self):
        self.btnSolve.clicked.connect(self.btnSolveClicked)
        self.chkCompleteModel.stateChanged.connect(self.chkCompleteModel_state_changed)
        self.chkHideMembers.stateChanged.connect(self.chkHideMembers_state_changed)
        self.chkHideNodes.stateChanged.connect(self.chkHideNodes_state_changed)
        self.chkHideLoads.stateChanged.connect(self.chkHideLoads_state_changed)
        self.chkHideSupports.stateChanged.connect(self.chkHideSupports_state_changed)
        self.chkHideMemberLabel.stateChanged.connect(
            self.chkHideMemberLabel_state_changed
        )
        self.chkHideNodeLabel.stateChanged.connect(self.chkHideNodeLabel_state_changed)
        self.chkDeformedModel.stateChanged.connect(self.chkDeformedModel_state_changed)
        self.SliderScale.valueChanged.connect(self.ScaleSlider_value_changed)
        self.elementsTable.cellClicked.connect(self.elementTableCellClick)
        self.elementsTable.itemDoubleClicked.connect(self.elementTableRowDoubleClicked)

    def elementTableRowDoubleClicked(self, item: QTableWidgetItem):
        # The item parameter contains information about the double-clicked cell
        row = item.row()
        # You can now access the data in the row and do something with it
        selected_element = self._helper.ElementList[row]
    #     self.showDiagram(selected_element)

    # def showDiagram(self, element):
    #     diagram_window = DiagramWindow(element)
    #     diagram_window.show()
    #     print(f"Double-clicked on row {row} with element {selected_element.label}")



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

        self.ax.set_box_aspect([1, 1, 1])

        xmin = min(self._helper.NodeList, key=lambda x: x.coordinates[0])
        xmax = max(self._helper.NodeList, key=lambda x: x.coordinates[0])

        ymin = min(self._helper.NodeList, key=lambda x: x.coordinates[1])
        ymax = max(self._helper.NodeList, key=lambda x: x.coordinates[1])

        zmin = min(self._helper.NodeList, key=lambda x: x.coordinates[2])
        zmax = max(self._helper.NodeList, key=lambda x: x.coordinates[2])

        dx = xmax.coordinates[0] - xmin.coordinates[0]
        dy = ymax.coordinates[1] - ymin.coordinates[1]
        dz = zmax.coordinates[2] - zmin.coordinates[2]
        aspectTotal = dx + dy + dz

        self.ax.set_xlim(xmin.coordinates[0], xmax.coordinates[0])
        self.ax.set_ylim(ymin.coordinates[1], ymax.coordinates[1])
        self.ax.set_zlim(zmin.coordinates[2], zmax.coordinates[2])

        # self.ax.get_xaxis().set_major_locator(plt.AutoLocator())
        # self.ax.get_yaxis().set_major_locator(plt.AutoLocator())
        # self.ax.get_zaxis().set_major_locator(plt.AutoLocator())

        self.ax.set_box_aspect(
            [dx / aspectTotal, dy / aspectTotal, dz / aspectTotal]
        )  # This makes the plot a cube
        self.canvas.draw()

    def PlotDeflectedModel(self):
        # self.InitializePlotArena()
        # for node in self._helper.NodeList:
        #     x, y, z = node.GetDisplacedCoordinates
        #     self.DrawNode(x, y, z, "")

        # Plot members
        for mbr in self._helper._elementList:
            node_i: Node = mbr.nodeI
            node_j: Node = mbr.nodeJ
            x1, y1, z1 = node_i.GetDisplacedCoordinates(self._scale)
            x2, y2, z2 = node_j.GetDisplacedCoordinates(self._scale)
            self.TrussElementDrawingEntity[mbr.handle], = self.DrawElement(x1, y1, z1, x2, y2, z2, "y",mbr.label)

    def PlotOriginalModel(self):
        if not self._hideNodes and self._showCompleteModel:
            for node in self._helper.NodeList:
                x, y, z = node.coordinates
                label = ""
                if not self._hideNodeLabel:
                    label = node.label
                self.DrawNode(x, y, z, label)

        # Plot members
        if not self._hideMembers and self._showCompleteModel:
            for mbr in self._helper._elementList:
                node_i = mbr.nodeI
                node_j = mbr.nodeJ
                x1, y1, z1 = node_i.coordinates
                x2, y2, z2 = node_j.coordinates
                self.DrawElement(x1, y1, z1, x2, y2, z2, "gray",mbr.label)

        if not self._hideLoads and self._showCompleteModel:
            for node in self._helper.NodeList:
                self.DrawForceVector(node)

    def HighlightSelectedElment(self, mbr):
        if self._highlightedElement:
            node_i = self._highlightedElement.nodeI
            node_j = self._highlightedElement.nodeJ
            x1, y1, z1 = node_i.coordinates
            x2, y2, z2 = node_j.coordinates
            line=self.DrawElement(x1, y1, z1, x2, y2, z2, "Gray",mbr.label)

        self._highlightedElement=mbr    
        node_i = mbr.nodeI
        node_j = mbr.nodeJ
        x1, y1, z1 = node_i.coordinates
        x2, y2, z2 = node_j.coordinates
        line=self.DrawElement(x1, y1, z1, x2, y2, z2, "purple",mbr.label)
        self.canvas.draw()

    def DrawArrowUpward(self, x, y, z, magnitude: float):
        self.ax.text(x, y, z + 2.5, f"{magnitude/1000} KN", color="blue", fontsize=12)
        self.ax.quiver(x, y, z, 0, 0, 2.5, color="g", picker=5, label="Arrow")

    def DrawArrowDownWard(self, x, y, z, magnitude: float):
        self.ax.text(x, y, z + 2.5, f"{magnitude/1000} KN", color="blue", fontsize=12)
        self.ax.quiver(x, y, z + 2.5, 0, 0, -2.5, color="g", label="Arrow")

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
        label:string
    ):
        # Add a Matplotlib plot for the current member
        return self.ax.plot([x1, x2], [y1, y2], [z1, z2], color=color,label=f"{label}")  # 'b' for blue lines

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
        
    def elementTableCellClick(self):
        # Assuming self.elementsTable is your QTableWidget
        selected_items = self.elementsTable.selectedItems()
        lines = plt.gca().get_lines()
        if selected_items:
            # Get the row index from the first selected item
            selected_row = self.elementsTable.row(selected_items[0])
            handle_str = self.elementsTable.item(selected_row, 0).text()  # Assuming it's text
            handle_uuid = uuid.UUID(handle_str) 
            selectedElement= next((element for element in self._helper.ElementList if element.handle== handle_uuid),None)
            if selectedElement:
                self.HighlightSelectedElment(selectedElement)
                


    def ScaleSlider_value_changed(self, value):
        self._scale = value * 10000000
        self.PlotModel()

    def chkCompleteModel_state_changed(self, state):
        if state == 2:
            self._showCompleteModel = True
            self.chkCompleteModel = True
            self.resetAllCheckBoxesForCompleteModel()
        else:
            self._showCompleteModel = False
            self.chkCompleteModel = False

        self.PlotModel()

    def chkDeformedModel_state_changed(self, state):
        self._showDeflectedModel = state == 2
        self.PlotModel()

    def chkHideMembers_state_changed(self, state):
        self._hideMembers = state == 2
        self.PlotModel()

    def chkHideNodes_state_changed(self, state):
        self._hideNodes = state == 2
        self.PlotModel()

    def chkHideLoads_state_changed(self, state):
        self._hideLoads = state == 2
        self.PlotModel()

    def chkHideSupports_state_changed(self, state):
        self._hideSupports = state == 2
        self.PlotModel()

    def chkHideMemberLabel_state_changed(self, state):
        self._hideMemberLabel = state == 2
        self.PlotModel()

    def chkHideNodeLabel_state_changed(self, state):
        self._hideNodeLabel = state == 2
        self.PlotModel()


# endregion


app = QApplication(sys.argv)
window = MainUI()
window.showMaximized()
sys.exit(app.exec())
