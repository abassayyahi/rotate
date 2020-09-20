import streamlit as st
import cv2

st.title("Hello World")
st.subheader("Welcom to my first app")
activities = ["home", "about"]
choice = st.sidebar.selectbox("Pick something fun", activities)

if choice == "Home":
	st.write("Go to the About section from the sidebar to learn more about it.")

	# Upload file
	image_file = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])

	if image_file is not None:
		image = image.open(image_file)

		if st.button("Process"):

			# Result image
			img_rotate_90_clockwise = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
			cv2.imshow('rotate_90', img_rotate_90_clockwise)
			cv2.imwrite('output.jpg',img_rotate_90_clockwise)

			cv2.waitKey()
			cv2.destroyALLWindows()
