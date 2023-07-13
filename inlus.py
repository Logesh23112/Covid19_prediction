%%writefile app5.py

import streamlit as st
from PIL import Image
from tensorflow import keras
import numpy as np



covid19_model = keras.models.load_model('/content/drive/MyDrive/Colab Notebooks/Covid/covid19model.h5')

def main():
   
    st.title("COVID-19 Detector Using Deep Learning")
    col1, col2, col3 = st.columns(3)
   
    img_normal = Image.open("/content/drive/MyDrive/Colab Notebooks/Covid/ref_images/xray_normal.png")
    col1.subheader("NORMAL")
    col1.image(img_normal, use_column_width=True, caption='Normal')
       
    img_neumonia_virica = Image.open("/content/drive/MyDrive/Colab Notebooks/Covid/ref_images/xray_neumonia_virica.png")
    col2.subheader("NUEMONIA VIRICA")
    col2.image(img_neumonia_virica, use_column_width=True, caption='Neumonia V�rica')
   
    img_covid19 = Image.open("/content/drive/MyDrive/Colab Notebooks/Covid/ref_images/xray_covid.png")
    col3.subheader("COVID19")
    col3.image(img_covid19, use_column_width=True, caption='COVID19')
   
    image_object = st.file_uploader("Please Upload Image", type=["png", "jpg", "jpeg"])

    if image_object is not None:
       
        radiografia_img = Image.open(image_object)
       
        img_temp_file = 'radiografia-tmp.' + radiografia_img.format
       
        radiografia_img.save(img_temp_file)

        keras_img_object = keras.preprocessing.image.load_img(img_temp_file, target_size=(256, 256))
       
        img_array = keras.preprocessing.image.img_to_array(keras_img_object)
        img_array = img_array / 255.0
        img_array = img_array.reshape(-1, 256, 256, 1)
       
        predictions = covid19_model.predict(img_array)
        final_prediction_array = predictions[0]
       
        class_names = ['COVID-19', 'NORMAL', 'NEUMONIA-V�RICA']
       
        prediccion = class_names[np.argmax(final_prediction_array)]
        probabilidad = 100 * np.max(final_prediction_array)
       
        st.image(radiografia_img, width=250)
        st.write(f'Predicci�n: {prediccion} - Probabilidad: {probabilidad:.4f}')
                      

if __name__ == '__main__':
    main()