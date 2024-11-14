import os
import uuid
from datetime import datetime

from werkzeug.utils import secure_filename

# Define the path for storing uploads
UPLOAD_FOLDER = os.path.join('app', 'static', 'uploads')


def save_image(file):
    if file.filename == '':
        return None

    # Secure the filename
    filename = secure_filename(file.filename)

    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, mode=0o777)
        print("The upload folder has been created.")

    # Format the filename
    unique_id = uuid.uuid4()  # Generate a unique UUID
    name, ext = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{unique_id}-{timestamp}{ext}"

    # Save the file
    file.save(os.path.join(UPLOAD_FOLDER, filename))

    return filename
