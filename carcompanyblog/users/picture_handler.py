from PIL import Image
import os
from flask import url_for, current_app

def add_profile_pic(pic_upload,username):
    file_name = pic_upload.filename  # grabs the name of file
    ext_type = file_name.split('.')[-1]  # grabs the extension
    storage_filename = str(username)+'.'+ext_type  # the fileName for each user in format - username.ext
    filepath = os.path.join(current_app.root_path, 'static\profile_pics', storage_filename)
    output_size = (200, 200)  # thumbnail size of profile pic
    pic = Image.open(pic_upload)  # grabs the pic into memory
    pic.thumbnail(output_size)  # converts file to fix size of 200x200

    pic.save(filepath)  # save the file to our filepath

    return storage_filename  # returns the file name along with extension
