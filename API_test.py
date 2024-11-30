import requests
import base64

    # Define the path to the image file
image_path = f'C:/Users/user/desktop/Python_lessons/mindmaps_images/mindmap(central image)/images/train/support_mindmap.jpg'


def test_endpoint():
        # Define the URL endpoint
        url = "https://mindmaps-analysis.onrender.com/analyze/"

        # Open the image file in binary mode and read its content
        image_data = encode_image(image_path)
        print(image_data)
           

        # Set the headers to indicate that you're sending JSON data
        headers = {"Content-Type": "application/json", "Accept": "application/json"}  # Adjust content type based on your image format
        payload = {"image": str(image_data)}

        # Make a POST request to the endpoint with the image data
        response = requests.post(url, headers=headers, json=payload)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content (expected string response)
            print(response.text)
        else:
            print("Error:", response.status_code)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return (base64.b64encode(image_file.read()).decode("utf-8"))
    

test_endpoint()
