# coding:utf-8
from flask import Flask, render_template, request
import os
import cv2
from PIL import Image
import hashlib
import datetime as dt
from settings import *
from pixel_converter import *
pixel_html_pre_path = 'pixel'
pixel_html_pro_path = '.html'
html_lang = 'tch'
def get_pixel_html_name():
    return pixel_html_pre_path + '_' + html_lang + pixel_html_pro_path
pixel_html_path = get_pixel_html_name()
static_path = 'static/'
app = Flask(__name__)
max_size_num = 2
max_size_length = 2048
config = {'MAX_CONTENT_LENGTH': 1024 * 1024 * max_size_num, 'DEBUG': False}
app.config.update(config)

@app.route("/english",methods=['POST','GET'])
def english():
    global pixel_html_path, html_lang
    html_lang = 'en'
    pixel_html_path = get_pixel_html_name()
    return render_template(pixel_html_path)

@app.route("/traditional_chinese")
def traditional_chinese():
    global pixel_html_path, html_lang
    html_lang = 'tch'
    pixel_html_path = get_pixel_html_name()
    return render_template(pixel_html_path)

@app.route('/', methods=['GET'])
def index():
    return render_template(pixel_html_path)

@app.route('/', methods=['POST'])
def post():
    img = request.files['image']
    last_image_name = request.values['last_image']
    format_support = ['mp4', 'avi', 'gif','png','jpg','jpeg']
    print(last_image_name)
    if img:
        last_image_name = None
        img_file_name = img.filename
    elif '.' in last_image_name:
        img_file_name = last_image_name
        img_path = last_image_name
        result_path = last_image_name.replace('img', 'results')
    elif not img and not last_image_name:
        last_image_name = None
        error='沒有選擇圖片'
        return render_template(pixel_html_path, error=error)
    if img_file_name.split('.')[-1].lower() not in format_support:
        error = "不支持這個格式。"
        return render_template(pixel_html_path, error=error)
    k = int(request.form['k'])
    scale = int(request.form['scale'])
    blur = int(request.form['blur'])
    erode = int(request.form['erode'])
    saturation = int(request.form['saturation'])
    contrast = int(request.form['contrast'])
    # contrast = 0
    # saturation = 0
    try:
        alpha = bool(int(request.form['alpha']))
    except:
        alpha = False
    try:
        to_tw = bool(int(request.form['to_tw']))
    except:
        to_tw = False
    img_name = hashlib.md5(str(dt.datetime.now()).encode('utf-8')).hexdigest()

    if img:
        # if upload new img
        img_path = os.path.join(static_path+'img', img_name + os.path.splitext(img_file_name)[-1])
        result_path = os.path.join(static_path+'results', img_name + os.path.splitext(img_file_name)[-1])
        img.save(img_path)

    file_format = os.path.splitext(img_file_name)[-1].replace('.', '')
    if not file_format in ['mp4', 'avi', 'flv']:
        with Image.open(img_path) as img_pl:
            if max(img_pl.size) > max_size_length:
                img_pl.thumbnail((max_size_length, max_size_length), Image.ANTIALIAS)
                img_pl.save(img_path)
    # commands
    command_dict = pixel_set_to_dict(k=k, scale=scale, blur=blur, erode=erode, alpha=alpha, to_tw=to_tw, saturation=saturation, contrast=contrast)
    img_res, colors = convert(img_path, command_dict)
    if file_format in ['gif', 'GIF']:
        return render_template(pixel_html_path, org_img=img_path, result=result_path, colors=colors, last_image=img_path)
    elif file_format in ['mp4', 'avi', 'flv']:
        return render_template(pixel_html_path, org_img=img_path, vid_result=result_path, colors=colors, last_image=img_path)
    else:
        cv2.imwrite(result_path, img_res)
        return render_template(pixel_html_path, org_img=img_path, result=result_path, colors=colors, last_image=img_path)

@app.errorhandler(413)
def error_file_size(e):
    error = '文件太大。 最大上傳大小為 ' + str(max_size_num) + 'MB。' + '  如果想要編輯大於' + str(max_size_num) + 'MB的檔案，請參考看看本地版：https://github.com/JingShing-Tools/Pixel-Art-transform-in-python'# + "<a href='https://github.com/JingShing-Tools/Pixel-Art-transform-in-python' target='_blank'>如果要沒有限制的本地版本，可以點擊這裡<\\a>"
    return render_template(pixel_html_path, error=error), 413

@app.errorhandler(404)
def not_found(e):
    error = 'Not found'
    return render_template(pixel_html_path, error=error), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
