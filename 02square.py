import sys
from OpenGL.GL import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import *
from camera import MayaCamera

class GLWidget(QGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.camera = MayaCamera()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)

    def paintGL(self):
        # Clear the screen
        glClearColor(1.0, 0.5, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Setup camera
        glMatrixMode(GL_PROJECTION)
        glLoadMatrixf(self.camera.proj_matrix.data())
        glMatrixMode(GL_MODELVIEW)
        glLoadMatrixf(self.camera.view_matrix.data())

        # Draw a square
        glColor3f(0.0, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex3f(-1, -1, 0)
        glVertex3f(1, -1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(-1, 1, 0)
        glEnd()

        # Tell the widget to redraw next time
        self.update()

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        self.camera.aspect = float(width) / height

    def mousePressEvent(self, event):
        self.last_pos = event.posF()

    def mouseMoveEvent(self, event):
        dxy = event.posF() - self.last_pos
        dx = dxy.x() / self.width()
        dy = dxy.y() / self.height()
        if event.buttons() & Qt.LeftButton:
            self.camera.rotate(dx, dy)
        elif (event.buttons() & Qt.MidButton) or event.modifiers():
            self.camera.pan(dx, dy)
        elif event.buttons() & Qt.RightButton:
            self.camera.zoom(dx, dy)
        self.last_pos = event.posF()

    def wheelEvent(self, event):
        self.camera.zoom(event.delta() / 360.0, 0.0)

if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = GLWidget()
    w.resize(512, 512)
    w.show()
    w.raise_()
    a.exec_()
