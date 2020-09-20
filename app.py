# Importing required libraries, obviously
import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os


# Loading pre-trained parameters for the cascade classifier
# try:
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
#     smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
# except Exception:
#     st.write("Error loading cascade classifiers")

def rotatee(image):
    '''
    Function to detect faces/eyes and smiles in the image passed to this function
    '''

    
    image = np.array(image.convert('RGB'))
    
    # Next two lines are for converting the image from 3 channel image (RGB) into 1 channel image
    # img = cv2.cvtColor(new_img, 1)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    rot = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    

    # Returning the image with bounding boxes drawn on it (in case of detected objects), and faces array
    return image, rot


def about():
    st.write(
        '''
        **Haar Cascade** is an object detection algorithm.
        It can be used to detect objects in images or videos. 

        The algorithm has four stages:

            1. Haar Feature Selection 
            2. Creating  Integral Images
            3. Adaboost Training
            4. Cascading Classifiers



Read more :point_right: https://docs.opencv.org/2.4/modules/objdetect/doc/cascade_classification.html
https://sites.google.com/site/5kk73gpu2012/assignment/viola-jones-face-detection#TOC-Image-Pyramid
        ''')


def main():
    st.title("Image Rotation 90 App :sunglasses: ")
    st.write("**Using the Haar cascade Classifiers**")

    activities = ["Home", "About"]
    choice = st.sidebar.selectbox("Pick something fun", activities)

    if choice == "Home":

        st.write("Go to the About section from the sidebar to learn more about it.")
        
        # You can specify more file types below if you want
        image_file = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])

        if image_file is not None:

            image = Image.open(image_file)

            if st.button("Process"):
                
                # result_img is the image with rectangle drawn on it (in case there are faces detected)
                # result_faces is the array with co-ordinates of bounding box(es)
                result_img = rotatee(image=image)
                st.image(result_img, use_column_width = True)
                st.success("ROTATE - 90 - CLOCKWISE")

    elif choice == "About":
        about()




if __name__ == "__main__":
    main()
