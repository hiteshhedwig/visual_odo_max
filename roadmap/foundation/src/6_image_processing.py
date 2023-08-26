# Project 6: Image Processing Toolbox

#     Objective: Develop a toolbox that can apply various image processing techniques like filtering, edge detection, and histogram equalization to input images.
#     Skills Gained: Familiarity with basic image processing techniques and their effects on images.
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
import cv2
import numpy as np
from enum import Enum

def nearest_odd(n):
    if n % 2 == 1:  # The number is already odd
        return n
    elif n % 2 == 0:  # The number is even
        # Choose between n-1 (previous odd) and n+1 (next odd)
        # Since both are equidistant, we can return either. For this example, we'll return n-1.
        return n - 1
    

class IMG_PROCESS_OPS(Enum):
    MEDIAN_BLUR = 1
    CANNY_EDGE  = 2

class ImageProcessingToolbox(object):
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)

    def detect_edges_sobel(self, upper_threshold):
        return cv2.Canny(self.image, 0, upper_threshold)
    
    def apply_median_filter(self, kernel_size):
        return cv2.medianBlur(self.image, kernel_size)
    
    def reset_image(self):
        self.image = cv2.imread(self.image_path)



class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_process = ImageProcessingToolbox("/home/hedwig/Downloads/Us3xkADP_400x400.jpg")
        self.current_ops = ""

        self.setWindowTitle('Image Toolbox')
        self.setGeometry(100, 100, 800, 600)

        # Create main layout
        layout = QHBoxLayout()

        # Image part
        self.image_label = QLabel(self)
        pixmap = self.cv_to_qtimage(self.image_process.image)
        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        # Control panel
        button_layout = QVBoxLayout()

        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)  # Set maximum as 100 for percentage
        self.slider.setValue(50)     # Set default value
        self.slider.valueChanged.connect(self.slider_changed)
        button_layout.addWidget(self.slider)

        # Button
        self.btn = QPushButton('Reset image!', self)
        self.btn.clicked.connect(self.on_btn_click)
        button_layout.addWidget(self.btn)

        self.btn1 = QPushButton('Median Blur!', self)
        self.btn1.setCheckable(True)
        self.btn1.clicked.connect(self.on_median_blur)
        button_layout.addWidget(self.btn1)

        self.btn2 = QPushButton('edge detection!', self)
        self.btn2.setCheckable(True)
        self.btn2.clicked.connect(self.on_canny_edge)
        button_layout.addWidget(self.btn2)

        layout.addLayout(button_layout)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def on_median_blur(self,checked):
        if checked:
            self.on_canny_edge(False)
            self.btn2.setChecked(False)

            self.btn1.setText(f"{IMG_PROCESS_OPS.MEDIAN_BLUR.name} - ON")
            self.current_ops = IMG_PROCESS_OPS.MEDIAN_BLUR.name
        else:
            self.btn1.setText("Median Blur!")

    def on_canny_edge(self,checked):
    
        if checked:
            self.on_median_blur(False)
            self.btn1.setChecked(False)

            self.btn2.setText(f"{IMG_PROCESS_OPS.CANNY_EDGE.name} - ON")
            self.current_ops = IMG_PROCESS_OPS.CANNY_EDGE.name
        else:
            self.btn2.setText("edge detection!")

    def on_btn_click(self, value):
        print(" button ", value)
        self.current_ops = value
        self.image_process.reset_image()
        self.slider.setValue(50) 
        self.update_image(self.image_process.image)

    def cv_to_qtimage(self, cv_img):
        height, width = cv_img.shape[:2]
        if len(cv_img.shape) == 3:  # Color image
            bytes_per_line = 3 * width
            q_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        else:  # Grayscale image
            bytes_per_line = width
            q_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)

        pixmap = QPixmap.fromImage(q_img)
        return pixmap
    
    def update_image(self, img):
        self.image_label.setPixmap(self.cv_to_qtimage(img))

    def slider_changed(self, value):
        # This method gets called when slider value changes
        if self.current_ops == IMG_PROCESS_OPS.MEDIAN_BLUR.name:
            kernal_size= int(((100+value)/200)*21)
            pix_image = self.image_process.apply_median_filter(nearest_odd(kernal_size))
            self.update_image(pix_image)

        if self.current_ops == IMG_PROCESS_OPS.CANNY_EDGE.name:
            upper_bound = value*2.44
            pix_image = self.image_process.detect_edges_sobel(upper_bound)
            self.update_image(pix_image)

        
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())