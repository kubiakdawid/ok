from flask import Flask, render_template, request, send_file
#from Generator import Generator


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)