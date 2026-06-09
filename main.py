import base64
from flask import Flask, render_template, request
import cv2
import numpy as np

app = Flask(__name__)


def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


@app.route('/', methods=['GET', 'POST'])
def index():
    img_data = None
    colors = []

    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file and file.filename != '':

            nparr = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)


            file.seek(0)
            encoded = base64.b64encode(file.read()).decode('utf-8')
            img_data = f"data:image/jpeg;base64,{encoded}"


            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pixels = img.reshape(-1, 3)

            unique_colors, counts = np.unique(pixels, axis=0, return_counts=True)
            hex_codes = [rgb_to_hex(color) for color in unique_colors]
            percentages = (counts / counts.sum()) * 100


            colors = [
                {"color_code": code, "color_percentage": round(pct, 2)}
                for code, pct in zip(hex_codes, percentages)
            ]
            
            colors = sorted(colors, key=lambda x: x['color_percentage'], reverse=True)[:10]

    return render_template('index.html', image_data=img_data, color_list=colors)


if __name__ == '__main__':
    app.run(debug=True)