
import cv2
import os
import xml.etree.ElementTree as ET


target_image_width = 1020 #maintain 4:3 ratio
target_image_height = 780 # maitain 4:3 ratio
video_name = 'GX0110088'
annotation_path = 'annotations_CVAT/annotations.xml'


compressed_folder_path = f'compressed/{video_name}/frames_{target_image_width} x {target_image_height}'
cropped_annotations_folderpath = f'cropped/{video_name}/annotations_{target_image_width} x {target_image_height}'
os.makedirs(compressed_folder_path, exist_ok=True)
os.makedirs(cropped_annotations_folderpath, exist_ok=True)

print(f"Processing annotations_CVAT from: {annotation_path}")

tree = ET.parse(annotation_path)
root = tree.getroot()

for track in root.findall('.//track'):
    if track.attrib.get('label') == 'queen':
        for box in track.findall('box'):
            frame_num = box.attrib['frame']
            print(f"Processing frame: {frame_num}")

            image_path = os.path.join(f'frames/{video_name}/frame_{frame_num}.png')
            if not os.path.exists(image_path):
                continue

            original_image = cv2.imread(image_path)
            xtl, ytl, xbr, ybr = [float(box.attrib[attr]) for attr in ['xtl', 'ytl', 'xbr', 'ybr']]

            bbox_width = xbr - xtl
            bbox_height = ybr - ytl

            resized_image = cv2.resize(original_image, (target_image_width, target_image_height))

            cv2.imwrite(f'{compressed_folder_path}/frame_{frame_num}.png', resized_image)
            print(f"Image saved to: {compressed_folder_path}/frame_{frame_num}.png")

            # resizing the image and saving works fine
            #TODO: resize the bounding box with appropriate ratio, save to a new xml file, create pascal-voc xml file for each image based on the new bounding box.
            
            