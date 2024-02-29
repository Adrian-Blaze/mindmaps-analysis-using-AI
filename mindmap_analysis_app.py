import cv2
from openai import OpenAI
import base64
import streamlit as st
import tempfile
from pypdf import PdfReader

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


#Use a deep learned trained model to detect the central image of the mindmap
def apply_trained_model(image):
    pass
    

# Function to encode an image into base64 format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
    

def convert_pdf_image_to_base64(pdf_path):
      reader = PdfReader(pdf_path)
      page = reader.pages[0]
      for image in page.images:
          image_data=image.data
                
          # Encode the image data as base64
          base64_str = base64.b64encode(image_data).decode('utf-8')
          return base64_str, image_data
   


def main():
    st.title("Mindmap AI demo")

    #Upload mindmap image to be analyzed
    uploaded_file = st.file_uploader("Upload your mindmap")
    if uploaded_file is not None:
      st.success("File uploaded successfully!")
      # Check the file type
      file_extension = uploaded_file.name.split(".")[-1].lower()
      if file_extension == "pdf":
        # If the uploaded file is a PDF
        # Read the contents of the PDF file
        pdf_content = uploaded_file.getvalue()
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
          temp_file.write(uploaded_file.read())
          file_path = temp_file.name  
        encoded_image, image_data = convert_pdf_image_to_base64(file_path)
        st.image(image_data, caption='Your mindmap image')
      else:

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
          with st.spinner("Analysing the image ..."):

             # Without Stream
            #response = client.chat.completions.create(
             # model="gpt-4-vision-preview",
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
            #  max_tokens=500,
            #)

            # Stream the response
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4-vision-preview", messages=messages, 
                max_tokens=500, stream=True
            ):
                # Check if there is content to display
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            # Final update to placeholder after the stream ends
            res = message_placeholder.markdown(full_response)
    
            # Display the response in the app
            # st.write(response.choices[0].message.content)




   
      
      
       

if __name__ == "__main__":
    main()