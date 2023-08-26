# Project 6: Image Processing Toolbox

#     Objective: Develop a toolbox that can apply various image processing techniques like filtering, edge detection, and histogram equalization to input images.
#     Skills Gained: Familiarity with basic image processing techniques and their effects on images.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np

class ImageProcessingToolbox(object):
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)

    def detect_edges_sobel(self):
        sobelx = cv2.Sobel(self.image, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(self.image, cv2.CV_64F, 0, 1, ksize=5)
        return np.hypot(sobelx, sobely)
    
    def apply_median_filter(self, kernel_size=7):
        return cv2.medianBlur(self.image, kernel_size)



class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.image_process = ImageProcessingToolbox("/home/hedwig/Downloads/Us3xkADP_400x400.jpg")

        # Set window title and size
        self.setWindowTitle('Image Toolbox')
        self.setGeometry(100, 100, 800, 600)

        # Create main layout
        layout = QVBoxLayout()

        # Create and add QLabel to display image
        self.image_label = QLabel(self)
        pixmap = self.cv_to_qtimage(self.image_process.image)
        self.image_label.setPixmap(pixmap)
        layout.addWidget(self.image_label)

        # Create and add QSlider as a trackbar
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)  # Set maximum as 100 for percentage
        self.slider.setValue(50)     # Set default value
        self.slider.valueChanged.connect(self.slider_changed)
        layout.addWidget(self.slider)

        self.setLayout(layout)

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
    
    def update_image(self, pixmap):
        self.image_label.setPixmap(pixmap)

    def slider_changed(self, value):
        # This method gets called when slider value changes
        print(f"Slider value: {value}")
        if value > 50 :
            pix_image = self.cv_to_qtimage(self.image_process.apply_median_filter())
            self.update_image(pix_image)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())