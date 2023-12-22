import cv2
import numpy as np
import math

def main():
    path = "CSHandwriting/"
    file_name = "oop.mt.170317.m0"
    
    for i in range(67, 72):
        subpath = "m0" + str(i) + "/"
        for j in range(1, 5):
            file_name_full = file_name + str(i) + "_p" + str(j) + ".jpg"
            image_path = os.path.join(path, subpath, file_name_full)
            save_path = "CSHandwriting_demoResult/" + subpath + file_name + str(i) + "_p" + str(j) + "_bin.png"
            process_image(image_path, save_path)


def extract_handwriting_and_printing(image, handwriting_threshold=100, printing_threshold=70):
    mask_handwriting = cv2.inRange(image, (0, 0, 0), (handwriting_threshold, handwriting_threshold, handwriting_threshold))
    inv_mask_handwriting = cv2.bitwise_not(mask_handwriting)
    kernel = np.ones((5,5), np.uint8)
    inv_mask_handwriting = cv2.erode(inv_mask_handwriting, kernel, iterations=1)
    inv_mask_handwriting = cv2.merge((inv_mask_handwriting,) * 3)
    
    handwriting = np.where(inv_mask_handwriting == 0, (255, 255, 255), image)
    printing = np.where(handwriting > (printing_threshold, printing_threshold, printing_threshold), 255, handwriting)
    
    return handwriting, printing

def find_edges(image, lower_threshold=100, upper_threshold=200):
    edges = cv2.Canny(image, lower_threshold, upper_threshold)
    return edges

def morphological_close(image, kernel_size=(5, 5)):
    kernel = np.ones(kernel_size, np.uint8)
    closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return closing

def find_horizontal_lines(image):
    img = image.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 120)
    lines = cv2.HoughLinesP(edges, 1, math.pi / 2, 2, None, 30, 1)
    for line in lines[0]:
        pt1 = (line[0], line[1])
        pt2 = (line[2], line[3])
        cv2.line(img, pt1, pt2, (0, 0, 255), 3)
    return img

def process_image(image_path, save_path):
    image = cv2.imread(image_path)
    handwriting, _ = extract_handwriting_and_printing(image)
    
    # Stage 2 - Evaluate Page Features
    bounding_boxes, smoothed_image, edges_image = evaluate_page_features(handwriting)

    # Stage 3 - Detect straight lines
    detected_lines = detect_straight_lines(handwriting)

    # Stage 4 - Construct binary regions
    binary_regions = construct_binary_regions(handwriting)

    # Stage 5 - Detect specific characters and label features
    specific_characters = detect_specific_characters(binary_regions)

    # Saving the processed images
    cv2.imwrite(save_path, handwriting)
    cv2.imwrite(save_path.replace('.png', '_smoothed.png'), smoothed_image)
    cv2.imwrite(save_path.replace('.png', '_edges.png'), edges_image)


#Stage2
    
def evaluate_page_features(handwriting_image):
    bounding_boxes = calculate_bounding_box(handwriting_image)
    smoothed_image = apply_gaussian_blur(handwriting_image)
    edges_image = apply_canny_edge_detection(handwriting_image)
    return bounding_boxes, smoothed_image, edges_image
   
def calculate_bounding_box(handwriting_image):
    contours, _ = cv2.findContours(handwriting_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    bounding_boxes = [cv2.boundingRect(contour) for contour in contours]
    return bounding_boxes 

def apply_gaussian_blur(handwriting_image, kernel_size=(5, 5)):
    return cv2.GaussianBlur(handwriting_image, kernel_size, 0)

def apply_canny_edge_detection(handwriting_image, threshold1=100, threshold2=200):
    return cv2.Canny(handwriting_image, threshold1, threshold2)


#Stage3
def detect_straight_lines(cropped_handwriting_binary):
    lines = cv2.HoughLinesP(cropped_handwriting_binary, rho=1, theta=np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(cropped_handwriting_binary, (x1, y1), (x2, y2), (255, 0, 0), 2)
    return cropped_handwriting_binary

#Stage4
def construct_binary_regions(cropped_handwriting_binary):
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(cropped_handwriting_binary, kernel, iterations=2)
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)
    return closing  


if __name__ == "__main__":
    main()