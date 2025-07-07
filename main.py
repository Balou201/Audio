from flask import Flask, request, send_file, render_template
import noisereduce as nr
import numpy as np
from scipy.io import wavfile
from io import BytesIO

app = Flask(__name__, static_folder='static', template_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    f = request.files['audio']
    rate, data = wavfile.read(f)
    reduced = nr.reduce_noise(y=data, sr=rate)
    
    preset = request.form.get('preset')
    if preset == 'radio':
        reduced = reduced * 1.2
    elif preset == 'podcast':
        reduced = reduced * 1.1
    elif preset == 'asmr':
        reduced = reduced * 0.9
    
    # Clamp values to int16 range
    reduced = np.clip(reduced, -32768, 32767)
    
    out = BytesIO()
    wavfile.write(out, rate, reduced.astype(np.int16))
    out.seek(0)
    return send_file(out, as_attachment=True, download_name='voix_nettoyee.wav', mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)