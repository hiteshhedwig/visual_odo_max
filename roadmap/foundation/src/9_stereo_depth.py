# Depth Estimation from Stereo
# - **Objective**: Capture images from a stereo camera setup and implement algorithms like block matching or semi-global block matching for depth estimation from disparity.
# - **Skills Gained**: Application of camera models, calibration, and feature matching to estimate depth in a scene.

import numpy as np
import cv2
import re
import matplotlib.pyplot as plt
import glob


def load_pfm(file_path):
    with open(file_path, 'rb') as file:
        # Read header
        color = None
        width = None
        height = None
        scale = None
        endian = None

        header = file.readline().rstrip()
        if header == b'PF':
            color = True
        elif header == b'Pf':
            color = False
        else:
            raise Exception('Not a PFM file.')

        dim_match = re.match(r'^(\d+)\s(\d+)\s$', file.readline().decode('utf-8'))
        if dim_match:
            width, height = map(int, dim_match.groups())
        else:
            raise Exception('Malformed PFM header.')

        scale = float(file.readline().rstrip())
        if scale < 0:  # little-endian
            endian = '<'
            scale = -scale
        else:
            endian = '>'  # big-endian

        data = np.fromfile(file, endian + 'f')
        shape = (height, width, 3) if color else (height, width)

        return np.reshape(data, shape), scale


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

def load_images(basepath):
    # Read the images
    img0 = cv2.imread(f"{basepath}/im0.png")
    img1 = cv2.imread(f"{basepath}/im1.png")
    
    # Convert to grayscale
    img0_gray = cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    
    # Apply histogram equalization
    img0_eq = cv2.equalizeHist(img0_gray)
    img1_eq = cv2.equalizeHist(img1_gray)
    
    # Apply Gaussian blur for noise reduction
    img0_blur = cv2.GaussianBlur(img0_eq, (5, 5), 0)
    img1_blur = cv2.GaussianBlur(img1_eq, (5, 5), 0)
    
    # Load and preprocess ground truth
    groundtruth, _ = load_pfm(f"{basepath}/disp0.pfm")
    groundtruth[np.isinf(groundtruth)] = 0
    groundtruth = normalize_image(groundtruth)
    groundtruth = cv2.flip(groundtruth, 0)
    
    return img0_blur, img1_blur, groundtruth


def sgdm(cf, img0, img1, groundtruth):
    left_img = img0 #cv2.cvtColor(img0, cv2.COLOR_BGR2GRAY)
    right_img = img1 #cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    
    window_size = 5
    min_disp = 16
    rounded_ndisp = (cf.ndisp + 15) // 16 * 16
    
    stereo = cv2.StereoSGBM_create(
        minDisparity=min_disp,
        numDisparities=int(rounded_ndisp),
        blockSize=15,
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
    display_images(img1, disparity, groundtruth)

def display_images(right_img, disparity, groundtruth):
    right_img = cv2.resize(right_img, (640, 480))
    disparity_normalized = normalize_image(disparity)
    
    combined_image = combine_images(right_img, disparity_normalized, groundtruth)
    cv2.imshow('Normalized Disparity Map', combined_image)
    cv2.waitKey(0)

def normalize_image(image):
    image = cv2.resize(image, (640, 480))
    min_val, max_val = image.min(), image.max()
    normalized = ((image - min_val) / (max_val - min_val) * 255).astype('uint8')
    return normalized

def combine_images(right_img, disparity, groundtruth):
    disparity = cv2.cvtColor(disparity, cv2.COLOR_GRAY2BGR)
    groundtruth = cv2.cvtColor(groundtruth, cv2.COLOR_GRAY2BGR)
    return cv2.hconcat([disparity, groundtruth])

def main():
    PATH = "roadmap/foundation/assets/stereo_data"
    
    for basepath in glob.glob(f"{PATH}/*"):
        print(f"Loading Stereo data from {basepath}")
        
        file_data = read_calib_file(f"{basepath}/calib.txt")
        cf = CalibrationFile(file_data)
        cf.parse()
        
        img0, img1, groundtruth = load_images(basepath)
        sgdm(cf, img0, img1, groundtruth)


if __name__ == '__main__':
    main()