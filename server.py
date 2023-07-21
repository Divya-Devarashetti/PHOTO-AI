from flask import Flask, render_template, request, redirect
import requests
import openai
import os

app = Flask(__name__)
openai.api_key = "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"

#mask_path = "C:\\Users\\HP PRO BOOK\\Downloads\\mask (1).png"
output_folder = os.path.join(app.static_folder, 'gen_images')

# Define the folder where uploaded images will be saved
app.config["IMAGE_UPLOADS"] = "C:\\Users\\HP PRO BOOK\\Documents\\web app\\static\\img\\uploads"


@app.route('/')
def index():
    return render_template('index.html')


mask_path = "C:\\Users\\HP PRO BOOK\\Downloads\\mask (1).png"
@app.route('/generate_images', methods=['POST'])
def generate_images():
    if request.method == 'POST':
        num_images_input = request.form.get('num-images-input')
        num_images = int(num_images_input) if num_images_input else 0
        prompt = request.form.get('prompt-input')

        filename = None  # Initialize filename with a default value

        if 'image' in request.files:
            # Check if an image was uploaded
            image = request.files['image']
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))

            print("Image saved")

            # Determine the appropriate mask path based on the filename of the uploaded image
            if filename and ('girl' in filename.lower()):
                mask_path = "C:\\Users\\HP PRO BOOK\\Downloads\\girl_mask.png"
            else:
                mask_path = "C:\\Users\\HP PRO BOOK\\Downloads\\boy_mask.png"
            
            generated_image_paths = []
        
            for i in range(1, num_images + 1):
                with open(os.path.join(app.config["IMAGE_UPLOADS"], image.filename), "rb") as model_file, open(mask_path, "rb") as mask_file:
                    response = openai.Image.create_edit(
                        image=model_file,
                        mask=mask_file,
                        prompt=prompt,
                        n=num_images,
                        size="1024x1024"
                    )
                
                image_url = response['data'][0]['url']
                response = requests.get(image_url)
                image_path = os.path.join(output_folder, f"g_img{i}.png")
                with open(image_path, "wb") as image_file:
                    image_file.write(response.content)
                generated_image_paths.append(image_path)

            return render_template('index.html', image_paths=generated_image_paths, uploaded_image_path=image_path)
    
    return redirect(request.url)

if __name__ == '__main__':
    app.run()

