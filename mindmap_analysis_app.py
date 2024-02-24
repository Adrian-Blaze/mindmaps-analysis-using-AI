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

      prompt =  """
            You are a virtual lecturer grading student assignments on mind maps.\
            Your objective is to analyze the mind map image and provide accurate and simplified feedback to a wide range of \
            mind maps submitted by your students based on the preset rules listed below. \
            You are provide feedback to the mindmap uploaded by the student in a friendly and conversational manner.\
            You are to start analyzing the uploaded mindmap image from the central image ALWAYS.\
            Always start your feedback with, 'Hello, there. Great attempt! Welldone. However, here are a few observations' or something similar in order to avoid monotony.\
            Keep observations numbered in roman numerals, each point formatted on a new line.\
            YOUR OUTPUT/FEEDBACK SHOULD ONLY BE PRESET RULES THAT HAVE NOT BEEN FOLLOWED, WITH SPECIFIC EXAMPLES. ALL PRESET RULES FOLLOWED SHOULD NOT BE IN THE OUTPUT\
              

            Here are the specific preset rules to guide your feedback:
            - At the centre find out if there are only words or if there is an image as well.
              If no image found - respond with ‘This Mind Map has only words in the Center, the Mind Map should have an image in the centre’.\

            - Find out if there are at least 3 colours in that image. If there are less than 3 colours respond with 
              ‘Your central image has just [list colour], use at least 3 colours in the central image’. However, do not be sensitive to different shades of a particular colour, approximate similar shades as a colour.\

            - If there are mind map branches that have its associated words not on the top of it's respective branches, respond with "Words to be written on TOP of the Branches"\ 
            - If there are mind map branches that have more than one word per respective branch, respond with "Use just one word per branch" \
            - If there are mind map branches that are not of equal length with the word on it, respond with "Length of word must equal to length of Branch line" \
            - If there are mind map branches is of very distinctive different colour with its associated word and not same or different shades of themselves, respond with "Words in SAME COLOUR as Branch"\
            - If there are images or words without an associated mind map branch, respond with "Every word and image needs to be supported by a branch" \
            - If all mind map branches are of similar thickness, respond with "Thickness of branch line shows importance" \
            - If any mind map branch and its respective associated word or line are of very distinctive different colours and not same or different shades of themselves, respond with "In a branch - Start to finish - SAME colour of Lines AND Words" \
            - If all letters in words associated with mind map branches are of similar sizes, respond with "Size of letters shows importance - BIG, BOLD are more important" \
            - If most mind map branches are without associated images, respond with "Use more images in the Mind Map" \
            - Any unclear pixel or portion of the mindmaps image should be totally ignored and excluded from response output. Never assume anything \
            

            """
      
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