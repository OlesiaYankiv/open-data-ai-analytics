from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)
SHARED_DIR = '/shared_data'

@app.route('/')
def index():
    quality_report = "Звіт про якість даних ще генерується..."
    research_report = "Звіт з дослідження даних ще генерується..."

    if os.path.exists(os.path.join(SHARED_DIR, 'quality_report.txt')):
        with open(os.path.join(SHARED_DIR, 'quality_report.txt'), 'r', encoding='utf-8') as f:
            quality_report = f.read()

    if os.path.exists(os.path.join(SHARED_DIR, 'research_report.txt')):
        with open(os.path.join(SHARED_DIR, 'research_report.txt'), 'r', encoding='utf-8') as f:
            research_report = f.read()

    return render_template('index.html', quality_report=quality_report, research_report=research_report)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory(SHARED_DIR, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)