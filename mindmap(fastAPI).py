from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import base64
import tempfile
import uvicorn
import os

key = os.getenv("API_KEY")

app = FastAPI()

# Define Pydantic model for input data
class Image(BaseModel):
    image: str

# Initialize OpenAI and YOLO models
client = OpenAI(api_key=key)

# Function to perform object detection
def apply_trained_model(image_path):
    pass
    
# Function to encode an image into base64 format
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# API home endpoint
@app.get("/")
async def index():
        return('Welcome to demo')

# API endpoint to analyze uploaded image
@app.post("/analyze/")
def analyze_image(data: Image):
    try:

        #_, temp_file_path = tempfile.mkstemp(suffix=".png")
        data = data.dict()
        encoded_image = data['image']
        prompt = """
            You are a virtual lecturer grading student assignments on mind maps.
            Your objective is to analyze the mind map image and provide accurate and simplified feedback to a wide range of
            mind maps submitted by your students based on the preset rules listed below.
            You are provide feedback to the mindmap uploaded by the student in a friendly and conversational manner.
            You are to start analyzing the uploaded mindmap image from the central image ALWAYS.
            Always start your feedback with, 'Hello, there. Great attempt! Welldone. However, here are a few observations' or something similar in order to avoid monotony.
            Keep observations numbered in roman numerals.

            Here are the specific preset rules to guide your feedback:
            - At the centre - we need to find out if only words are written or there is an image as well.
            If no image found - respond with ‘This Mind Map has only words in the Center, the Mind Map should have an image in the centre’.

            - We need to then find out if there are at least 3 colours in that image. If there are less than 3 colours respond with
            ‘Your central image has just [list colour], use at least 3 colours in the central image’\

            - If there are mind map branches that have its associated words not on the top of it's respective branches, respond with "Words to be written on TOP of the Branches"\
            - If there are mind map branches that have more than one word per respective branch, respond with "Use just one word per branch" \
            - If there are mind map branches that are not of equal length with the word on it, respond with "Length of word must equal to length of Branch line" \
            - If there are mind map branches is of very distinctive different colour with its associated word and not same or different shades of themselves, respond with "Words in SAME COLOUR as Branch"\
            - If there are images or words without an associated mind map branch, respond with "Every word and image needs to be supported by a branch" \
            - If all mind map branches are of similar thickness, respond with "Thickness of branch line shows importance" \
            - If any mind map branch and its respective associated word or line are of very distinctive different colours and not same or different shades of themselves, respond with "In a branch - Start to finish - SAME colour of Lines AND Words" \
            - If all letters in words associated with mind map branches are of similar sizes, respond with "Size of letters shows importance - BIG, BOLD are more important" \
            - If most mind map branches are without associated images, respond with "Use more images in the Mind Map" \
            """
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image", "image": encoded_image, "resize": 768},
                    ],
                }
            ],
            max_tokens=500,
        )
        return {"feedback": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app)