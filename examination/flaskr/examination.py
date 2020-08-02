import time
from . import projecta as pa
from . import projectb as pb
from . import projectc as pc
from . import pyult as ult
from flask import Flask
from flask import Blueprint
from flask import render_template
from flask import request as req
from flask import flash
from flask import url_for
from flask import redirect
from flask import send_from_directory
from werkzeug.utils import secure_filename


bp = Blueprint('examination', __name__, url_prefix='/examination')

@bp.route('/exam')
def index():
    return render_template('examination/exam.html')

@bp.route('/projecta', methods=('GET','POST'))
def projecta():
    #return render_template('wordcloud/index.html')
     if req.method == 'POST':
         url = req.form['url']
         headers = req.headers
         timeout = 100
         soap = pa.get_url_content(url, headers, timeout)
         df = pa.pd.DataFrame(columns=['名称','最低价格','最高价格','产品图片链接'])
         df = pa.convert_content(df, soap)
         abspath = ult.generate_abspath(__file__, 'download')
         df.to_csv(abspath + '/result.csv', encoding='GBK')
         return send_from_directory(abspath, 'result.csv', as_attachment=True)



@bp.route('/projectb', methods=('GET','POST'))
def projectb():
    if req.method == 'POST':
        f = req.files['uploadfileb']
        filename = secure_filename(f.filename)
        abspath = ult.generate_abspath(__file__, 'upload')
        abspath = abspath + '\\' + filename
        f.save(abspath)
        print(type(req.form['aproption']))
        if req.form['aproption'] == '0':
            result = pb.efficient_apriori(pb.transcation1_generate(abspath), float(req.form['min_support']), float(req.form['min_confidence']))
            print(result)
        elif req.form['aproption'] == '1':
            result = pb.mlxtend_apriori(pb.transcation2_generate(abspath), float(req.form['min_support']), float(req.form['min_confidence']))
            print(result)
        return render_template('examination/exam.html', itemsets=result['itemsets'], rules=result['rules'])
    #return send_from_directory(abspath, 'built-in_function_time_result.csv', as_attchement=True)

@bp.route('/projectc', methods=('GET','POST'))
def projectc():
    if req.method == 'POST':
        f = req.files['uploadfilec']
        filename = secure_filename(f.filename)
        abspath = ult.generate_abspath(__file__, 'upload')
        abspath = abspath + '\\' + filename
        f.save(abspath)
        df = pc.data_import(abspath)
        tran_x = pc.data_tran(df)
        image_path = ult.generate_abspath(__file__, 'static/image/')
       # pc.sse(tran_x, image_path)
        pc.sc_scores(tran_x, image_path)
        return render_template('examination/exam.html', sse_imgsrc='sse.png', sc_imgsrc='sc_scores.png')