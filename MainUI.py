# import sys
# from PyQt6.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QWidget, QPushButton
# from PyQt6.QtCore import Qt
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
# from PyQt6 import uic

# class MainUI(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Load the UI from 'Main.ui' and set it as the central widget
#         uic.loadUi('UI/Main.ui', self)
#         central_widget = self.centralWidget()

#         # Create a vertical layout for the Matplotlib plot
#         layout = QVBoxLayout(central_widget)

#         # Create a Matplotlib figure and canvas
#         self.figure = Figure()
#         self.canvas = FigureCanvas(self.figure)

#         # Create a reference to the Matplotlib axes for plotting
#         self.ax = self.figure.add_subplot(111)

#         # Add the Matplotlib canvas to the layout
#         layout.addWidget(self.canvas)

#         # Set the alignment of the layout within the central widget
#         layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)

#         # Set the central widget to use the layout
#         central_widget.setLayout(layout)
        

#         self.btnSolve.clicked.connect(self.btnSolveClicked)

#     def btnSolveClicked(self):
#         # Clear the previous plot
#         self.ax.clear()

#         # Add a Matplotlib plot
#         x_data = [1, 2, 3, 4, 25]
#         y_data = [2, 4, 1, 3, 5]
#         self.ax.plot(x_data, y_data)
#         self.ax.set_xlabel('X-axis')
#         self.ax.set_ylabel('Y-axis')

#         # Update the canvas
#         self.canvas.draw()

# app = QApplication(sys.argv)
# window = MainUI()
# window.showMaximized()
# sys.exit(app.exec())
