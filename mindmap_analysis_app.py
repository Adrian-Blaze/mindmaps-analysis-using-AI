import cv2
from openai import OpenAI
import base64
import os
import streamlit as st
import tempfile

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


#Use a deep learned trained model to detect the central image of the mindmap
def apply_trained_model(image):
    pass
    

# Function to encode an image into base64 format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def main():
    st.title("Mindmap AI demo")

    #Upload mindmap image to be analyzed
    uploaded_file = st.file_uploader("Upload your mindmap")
    if uploaded_file is not None:
      
        # Save the uploaded file to a temporary location
      st.image(uploaded_file, caption='Your mindmap image')  
      with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name

      image = cv2.imread(file_path)

      #Get central image and crop it out
      
  
      
      # Encode your image
      encoded_image = encode_image(file_path)

      prompt = (
      'You are a virtual lecturer grading student assignments on mind maps.'
      'Your objective is to analyze the mind map images to provide accurate and simplified feedback to a wide range of mind maps submitted by your students based on the preset rules listed below.'
      'Provide feedback to the mindmap uploaded by the student in a friendly and conversational manner.'
      'Highlight key feedback and their corresponding examples and present your analysis in clear, well-structured markdown format.'
      'Start analyzing the uploaded mindmap image from the central image ALWAYS.'
      'Always start your feedback with, \'Hello, there. Great attempt! Well done. However, here are a few observations\' or something similar in order to avoid monotony.'
      'Keep observations numbered in roman numerals, each point formatted on a new line.'
      'YOUR OUTPUT/FEEDBACK SHOULD ONLY BE PRESET RULES THAT HAVE NOT BEEN FOLLOWED, WITH SPECIFIC EXAMPLES. ALL PRESET RULES FOLLOWED SHOULD NOT BE IN THE OUTPUT.'
      'Focus on the rules not followed.'
      'Check if the central image has at least 3 colors.'
      'Check if words are written on top of branches.'
      'Check if there is only one word per branch.'
      'Check if branch lengths and word lengths are equal.'
      'Check if words and branches have the same color.'
      'Check if every word/image has a branch.'
      'Check if branch thickness indicates importance.'
      'Check if branches and words have consistent colors.'
      'Check if letter sizes indicate importance.'
      'Check if images are used effectively.'
      'Any unclear pixel or portion of the mindmaps image should be totally ignored and excluded from response output. Never assume anything.'
      )

      
      ask_button = st.button("Analyze")
     
      # Check if the ask button is clicked
      if ask_button:
    
            response = client.chat.completions.create(
              model="gpt-4-vision-preview",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {"type": "text", "text":prompt},
                    {
                      "type": "image",
                      "image":encoded_image,
                      "resize": 768
                    },
                  ],
                }
              ],
              max_tokens=500,
            )





            styled_container = '''
            <div style="background-color: #F5F5F5; padding: 10px; border-radius: 5px;">
                <p style="font-size: 20px; color: gray; font-weight: bold;">{}</p>
            </div>
            '''.format(response.choices[0].message.content)

            st.write(styled_container, unsafe_allow_html=True)

      
      
       

if __name__ == "__main__":
    main()