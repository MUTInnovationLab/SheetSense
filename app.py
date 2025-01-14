from flask import Flask, render_template, send_from_directory, url_for
# make_response
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view_reports')
def view_reports():
    return render_template('reports.html')

@app.route('/view_history')
def view_history():
    return render_template('history.html')

@app.route('/manage_files')
def manage_files():
    return render_template('files.html')

# @app.route('/static/<path:filename>') 
# def custom_static(filename):
#     response = make_response(send_from_directory(os.path.join(app.root_path, 'static'), filename)) 
#     response.headers['Cache-Control'] = 'public, max-age=31536000, immutable' 
#     return response

@app.route('/static/<path:filename>') 
def custom_static(filename): 
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/favicon.ico') 
def favicon(): return send_from_directory(os.path.join(app.root_path, 'static'), 
                                          'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)
