from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from cv2 import cv2
from detect import get_res
import os

app = Flask(__name__)


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        user_input = request.form.get("name")
        basepath = os.path.dirname(__file__)
        upload_path = os.path.join(basepath, 'static/images',
                                   secure_filename(f.filename))
        f.save(upload_path)
        # 预测
        get_res(upload_path)
        res_path = os.path.join(basepath, './res/',
                                secure_filename(f.filename))
        img_1 = cv2.imread(upload_path)
        img_2 = cv2.imread(res_path)
        new_path_1 = os.path.join(basepath, 'static/images', 'ori.jpg')
        new_path_2 = os.path.join(basepath, 'static/images', 'pre.jpg')
        cv2.imwrite(new_path_1, img_1)
        cv2.imwrite(new_path_2, img_2)

        return render_template('upload_ok.html', userinput=user_input)
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)