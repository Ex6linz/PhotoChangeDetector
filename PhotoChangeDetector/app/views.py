from flask import request, render_template
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
from app import app


app.config['INITIAL_FILE_UPLOADS'] = os.path.join('app', 'static', 'uploads')
app.config['EXISTNG_FILE'] = os.path.join('app', 'static', 'original')
app.config['GENERATED_FILE'] = os.path.join('app', 'static', 'generated')


for path in [app.config['INITIAL_FILE_UPLOADS'], app.config['EXISTNG_FILE'], app.config['GENERATED_FILE']]:
    if not os.path.exists(path):
        os.makedirs(path)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        original_file = request.files['original_file']
        file_upload = request.files['file_upload']


        if original_file.filename == '' or file_upload.filename == '':
            return 'No selected file(s)', 400


        original_image_path = os.path.join(app.config['EXISTNG_FILE'], 'original.jpg')
        original_image = Image.open(original_file).resize((250, 160))
        original_image.save(original_image_path)


        uploaded_image_path = os.path.join(app.config['INITIAL_FILE_UPLOADS'], 'image.jpg')
        uploaded_image = Image.open(file_upload).resize((250, 160))
        uploaded_image.save(uploaded_image_path)


        original_image = cv2.imread(original_image_path)
        uploaded_image = cv2.imread(uploaded_image_path)


        original_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        uploaded_gray = cv2.cvtColor(uploaded_image, cv2.COLOR_BGR2GRAY)

        (score, diff) = structural_similarity(original_gray, uploaded_gray, full=True)
        diff = (diff * 255).astype("uint8")


        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'], 'image_diff.jpg'), diff)

        return render_template('index.html', pred=f'{round(score * 100, 2)}% correct')

# Main function
if __name__ == '__main__':
    app.run(debug=True)