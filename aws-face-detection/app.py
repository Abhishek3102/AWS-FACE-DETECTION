import streamlit as st
import boto3
import requests
from PIL import Image
from io import BytesIO

import os

os.environ['AWS_ACCESS_KEY_ID'] = 'AKIA3LK5DDGGF6OWPCHF'
os.environ['AWS_SECRET_ACCESS_KEY'] = '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'

def load_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img

# Create a client for the Amazon Rekognition service
rekognition_client = boto3.client('rekognition','ap-south-1')

# Define the Streamlit app
def app():
    # Set the page title
    st.set_page_config(page_title='Image Comparison App', page_icon=':camera:', layout='wide')
    st.title('Image Comparison App')
    
    # Create two input boxes for URL input
    url1 = st.text_input('Enter URL of image 1:')

    if url1:
        image1 = load_image(url1)

    url2 = st.text_input('Enter URL of image 2:')
    
    if url2:
        image2 = load_image(url2)
    
    col1, col2 = st.columns(2)
    if url1:
        with col1:
            st.image(image1, use_column_width=False,width=400)
    
    if url2:
        with col2:
            st.image(image1, use_column_width=False,width=400)
    
    # Create a button to compare the images
    if st.button('Compare Images'):
        # Use the Amazon Rekognition service to compare the images
        try:
            response = rekognition_client.compare_faces(
                SourceImage={
                    'S3Object': {
                        'Bucket': 'cclproject24',
                        'Name': 'image1.jpg'
                    }
                },
                TargetImage={
                    'S3Object': {
                        'Bucket': 'cclproject24',
                        'Name': 'image2.jpg'
                    }
                }
            )
            similarity = response['FaceMatches'][0]['Similarity']
            st.success(f'The similarity between the two images is {similarity}%')
        except Exception as e:
            st.error(f'Error: {str(e)}')
        
        # Send a POST request to the backend
        data = {'url1': url1, 'url2': url2}
        try:
            response = requests.post('http://23.22.183.178:8000/compare_faces', json=data)
            if response.status_code == 200:
                st.success('The request was sent successfully.')
            else:
                st.warning(f'The request was not successful. Status code: {response.status_code}')
        except Exception as e:
            st.error(f'Error: {str(e)}')

if __name__ == '__main__':
    app()