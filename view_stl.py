""" This sample code shows how to show plotly graph on PyQt widget."""

import os
from pathlib import Path
import numpy as np
import open3d as o3d

import plotly.graph_objects as go
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QUrl


class Widget(QtWidgets.QWidget):
    """ Widget class to show plotly graph on
    QtWebEngineWidgets.QWebEngineView """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button = QtWidgets.QPushButton('Plot', self)
        self.browser = QtWebEngineWidgets.QWebEngineView(self)

        vlayout = QtWidgets.QVBoxLayout(self)
        vlayout.addWidget(self.button, alignment=QtCore.Qt.AlignHCenter)
        vlayout.addWidget(self.browser)

        # connect button to function show_graph
        self.button.clicked.connect(self.show_graph)
        self.resize(1000, 800)

    def show_graph(self):
        """ Function to show plotly graph on PyQt widget """
        mesh = o3d.io.read_triangle_mesh('tig_torch.stl')

        mesh.compute_vertex_normals()
        mesh.compute_triangle_normals()
        triangles = np.asarray(mesh.triangles)
        vertices = np.asarray(mesh.vertices)

        layout = go.Layout(
            scene=dict(
                aspectmode='data'
            ),
            margin=dict(l=0, r=0, b=0, t=0))

        fig = go.Figure(data=[go.Mesh3d(x=vertices[:, 0],
                                        y=vertices[:, 1],
                                        z=vertices[:, 2],
                                        i=triangles[:, 0],
                                        j=triangles[:, 1],
                                        k=triangles[:, 2],
                                        opacity=1.0,
                                        intensity=vertices[:, 2],
                                        colorbar=dict(
                                            orientation="h",
                                            thickness=10,
                                            ypad=2,
                                            xpad=100,
                                            y=-0.1),
                                        colorscale="Jet",
                                        showscale=True
                                        )],
                        layout=layout)

        # write html file
        fig.write_html('file.html', full_html=False)

        # load html file and show it on browser
        current_directory = Path(__file__).resolve().parent
        filename = os.fspath(current_directory / "file.html")
        url = QUrl.fromLocalFile(filename)
        self.browser.load(url)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.show()
    app.exec()
