from flask import Flask, request, render_template, redirect
import boto3
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)
BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

@app.route('/')
def index():
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME)
    images = []
    for obj in objects.get('Contents', []):
        images.append(f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{obj['Key']}")
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['photo']
    if file:
        filename = secure_filename(file.filename)
        s3.upload_fileobj(file, BUCKET_NAME, filename)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
