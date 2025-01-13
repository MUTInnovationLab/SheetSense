from flask import Flask, render_template

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

if __name__ == "__main__":
    app.run(debug=True)
