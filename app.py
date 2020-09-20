# Importing required libraries, obviously
import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os

st.set_option('deprecation.showfileUploaderEncoding', False)


def rotatee(image):
    '''
    Function to detect faces/eyes and smiles in the image passed to this function
    '''

    image = np.array(image.convert('RGB'))

    # Next two lines are for converting the image from 3 channel image (RGB) into 1 channel image
    #img = cv2.cvtColor(image, 1)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    rot = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    # Returning the image with bounding boxes drawn on it (in case of detected objects), and faces array
    return rot


def about():
    st.write(
        '''
        **Rotation App** is a simple web application.
        It can be used to rotate images. 

        The algorithm has four stages:

            1. Image Feature Selection 
            2. Creating  Integral Images
            3. Adaboost Training
            4. transformin 3 to 1 chanel



Read more :point_right: https://github.com/abassayyahi/rotate
        ''')


def main():
    st.title("Image Rotation 90 App :sunglasses: ")
    st.write("**Here you can upload your image**")

    activities = ["Home", "About"]
    choice = st.sidebar.selectbox("Pick something fun", activities)

    if choice == "Home":

        st.write("Go to the About section from the sidebar to learn more about it.")

        # file_buffer = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])
        # image_file = io.TextIOWrapper(file_buffer)
        image_file = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])

        if image_file is not None:

            image = Image.open(image_file)
            if st.button("Show"):
                st.image(image, use_column_width=True)

            if st.button("Rotate"):

                result_img = rotatee(image=image)

                st.image(result_img, use_column_width=True)

                st.success("ROTATE - 90 - CLOCKWISE")



    elif choice == "About":
        about()


if __name__ == "__main__":
    main()
