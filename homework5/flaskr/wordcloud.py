from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import request as req
from flask import flash
from flask import url_for
from flask import redirect
from werkzeug.utils import secure_filename
from . import wordcloudgenerate as wcg
#import wordcloudgenerate
import os
bp = Blueprint('wordcloud', __name__)

@bp.route('/')
def index():
    return render_template('wordcloud/index.html')

@bp.route('/upload', methods=('GET','POST'))
def upload():
    if req.method == 'POST':
         f = req.files['file']
         basepath = os.path.dirname(__file__)
         upload_path = os.path.join(basepath, 'upload', secure_filename(f.filename))
         upload_path = os.path.abspath(upload_path)
         f.save(upload_path)
         #return redirect(url_for('workcloud.upload'))
         print(upload_path)
         message = '上传文件成功,'
         src = wcg.create_word_cloud(upload_path)
         if src is not None:
            message += ',生成词云图片成功'
            flash(message)
            return render_template('wordcloud/index.html', imagesrc=src)
         else:
            message += ',生成词云图片失败'
            flash(message)
            return render_template('wordcloud/index.html')