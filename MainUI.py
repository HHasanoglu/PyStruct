import sys
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget, QPushButton
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6 import uic
from TrussHelper import TrussSolverHelper

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self._helper=TrussSolverHelper()

        # Load the UI from 'Main.ui' and set it as the central widget
        uic.loadUi('UI/Main.ui', self)
        central_widget = self.centralWidget()

        # Create a vertical layout for the Matplotlib plot
        layout = QVBoxLayout(central_widget)

        # Create a Matplotlib figure and canvas
        self.figure = Figure(figsize=(10,25))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Set the alignment of the layout within the central widget
        layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Set the central widget to use the layout
        central_widget.setLayout(layout)

        self.btnSolve.clicked.connect(self.btnSolveClicked)

    def btnSolveClicked(self):
        self._helper.CreateExample6()
        self._helper.AnalyzeModel()
        self.PlotElements()
        

    def PlotElements(self):
       # Clear the previous plot
        self.figure.clear()
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.grid()
        self.ax.set_xlabel('X (m)')
        self.ax.set_ylabel('Y (m)')
        self.ax.set_zlabel('Z (m)')
        self.ax.set_title('Structure to analyze')
        self.ax.grid(False)
           # Hide the 3D plot walls
        self.ax.xaxis.pane.fill = False
        self.ax.yaxis.pane.fill = False
        self.ax.zaxis.pane.fill = False

        for node in self._helper.NodeList:
            x, y, z = node.coordinates
            self.ax.scatter(x, y, z, c='r', marker='o')  # 'r' for red points, 'o' for circular markers
            self.ax.text(x, y, z, f'{node.label}', fontsize=12, ha='right')

        # Plot members
        for mbr in self._helper._elementList:
            node_i = mbr.nodeI
            node_j = mbr.nodeJ

            x1, y1, z1 = node_i.coordinates
            x2, y2, z2 = node_j.coordinates

            # Add a Matplotlib plot for the current member
            self.ax.plot([x1, x2], [y1, y2], [z1, z2], color='b')  # 'b' for blue lines
        self.ax.set_box_aspect([4, 2, 2])  # This makes the plot a cube
        self.canvas.draw()


    # def Plot(self):
    #     # Clear the previous plot
    #     self.ax.clear()

    #     # # Add a Matplotlib plot
    #     # x_data = [1, 2, 3, 4, 25]
    #     # y_data = [2, 4, 1, 3, 5]
    #     # self.ax.plot(x_data, y_data)
    #     # self.ax.set_xlabel('X-axis')
    #     # self.ax.set_ylabel('Y-axis')

    #     axes = self.figure.add_axes([0.1,0.1,3,3]) 
    #     self.figure.gca().set_aspect('equal', adjustable='box')

    #     #Plot members
    #     members=self._helper._elementList
    #     for mbr in members:  
    #         node_i = mbr.Nodes[0] #Node number for node i of this member
    #         node_j = mbr.Nodes[1] #Node number for node j of this member   
    
    #         ix = node_i.Xcoord #x-coord of node i of this member
    #         iy = node_i.Ycoord #y-coord of node i of this member
    #         jx = node_j.Xcoord #x-coord of node j of this member
    #         jy = node_j.Ycoord #y-coord of node j of this member
    
    #     # Add a Matplotlib plot
    #     x_data = [ix, jx]
    #     y_data = [iy, jy]
    #     self.ax.plot(x_data, y_data)
    #     self.canvas.draw()


    

app = QApplication(sys.argv)
window = MainUI()
window.showMaximized()
sys.exit(app.exec())
