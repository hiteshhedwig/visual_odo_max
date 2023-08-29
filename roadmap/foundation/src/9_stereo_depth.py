# Depth Estimation from Stereo
# - **Objective**: Capture images from a stereo camera setup and implement algorithms like block matching or semi-global block matching for depth estimation from disparity.
# - **Skills Gained**: Application of camera models, calibration, and feature matching to estimate depth in a scene.

import numpy as np
import cv2
import re
import matplotlib.pyplot as plt

def read_calib_file(filename):
    """
    The function `read_calib_file` reads the contents of a file and returns them as a list of lines.
    
    :param filename: The filename parameter is a string that represents the name of the file you want to
    read. It should include the file extension (e.g., "calibration.txt")
    :return: a list of strings, where each string represents a line from the file.
    """
    with open(filename, 'r', encoding='utf-8') as file_handle:
        lines = file_handle.readlines()
        return lines

class CalibrationFile():
    def __init__(self, data_file):
        self.data = data_file

    def camera_matrix(self, rows):
        """
        The function "camera_matrix" takes a list of lists as input and converts each element to a float,
        returning a new list of lists.
        
        :param rows: The parameter "rows" is a list of lists. Each inner list represents a row of a matrix.
        Each element in the inner list is a number
        :return: a matrix, where each element is a float value.
        """
        return [[float(x) for x in row] for row in rows]

    def parse_camera_matrices(self, line):
        """
        The function `parse_camera_matrices` takes a line of text containing a camera matrix in string
        format, extracts the matrix values using regular expressions, splits the values into rows, and
        assigns the resulting matrix to an attribute of the object.
        
        :param line: The `line` parameter is a string that contains the camera matrix information in the
        format `attr=str_matrix`. The `attr` is the attribute name that will be set on the object, and
        `str_matrix` is a string representation of the camera matrix
        """
        attr, str_matrix = line.split("=")
        # Using regex to extract matrix values
        numbers = re.findall(r'(\d+\.\d+|\d+)', str_matrix)
        # Splitting numbers into rows (assuming a 3x3 matrix)
        rows = [numbers[i:i+3] for i in range(0, len(numbers), 3)]
        mat = self.camera_matrix(rows)
        setattr(self, attr, mat)

    def parse_metadata(self, line):
        """
        The function `parse_metadata` takes a line of text, splits it by "=", removes any trailing
        whitespace, and sets an attribute on the object with the first element as the attribute name and the
        second element as the attribute value converted to a float.
        
        :param line: The `line` parameter is a string that represents a line of metadata
        """
        line = [ll.rstrip() for ll in line.split("=")]
        setattr(self, line[0], float(line[1]))

    def parse_line(self, line, line_num):
        """
        The function `parse_line` parses different types of data based on the line number.
        
        :param line: The `line` parameter is a string that represents a line of text that needs to be parsed
        :param line_num: The `line_num` parameter represents the line number of the current line being
        parsed
        """
        if line_num in [0,1]:
            self.parse_camera_matrices(line)
        if line_num in [3,4,5,6,7,8] :
            self.parse_metadata(line)

    def parse(self):
        """
        The function iterates over each line in the data and calls another function to parse each line.
        """
        for idx, line in enumerate(self.data):
            self.parse_line(line, idx)

def main():
    file_data = read_calib_file("roadmap/foundation/assets/stereo_data/artroom1/calib.txt")

    cf = CalibrationFile(file_data)
    cf.parse()
    # bm(cf)
    sgdm(cf)

# Getting Started with Block Matching 
def bm(cf):
    left_img = cv2.imread('roadmap/foundation/assets/stereo_data/artroom1/im0.png', 0)
    right_img = cv2.imread('roadmap/foundation/assets/stereo_data/artroom1/im1.png', 0)

    rounded_ndisp = (int(cf.ndisp) + 15) // 16 * 16  # Round to the nearest multiple of 16
    stereo = cv2.StereoBM_create(numDisparities=rounded_ndisp, blockSize=15)

    disparity = stereo.compute(left_img, right_img)

    plt.imshow(disparity, 'gray')
    plt.show()

# Semi-Global Block Matching (SGBM)
def sgdm(cf) :
    left_img = cv2.imread('roadmap/foundation/assets/stereo_data/artroom1/im0.png', 0)
    right_img = cv2.imread('roadmap/foundation/assets/stereo_data/artroom1/im1.png', 0)

    window_size = 5
    min_disp = 16
    rounded_ndisp = (int(cf.ndisp) + 15) // 16 * 16  # Round to the nearest multiple of 16
    num_disp = rounded_ndisp
    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=num_disp,
        blockSize=16,
        P1=8 * 3 * window_size ** 2,
        P2=32 * 3 * window_size ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=15,
        speckleWindowSize=0,
        speckleRange=2,
        preFilterCap=63,
        mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
    )

    disparity = stereo.compute(left_img, right_img)
    plt.imshow(disparity, 'gray')
    plt.show()


if __name__ == '__main__':
    main()