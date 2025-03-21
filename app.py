from flask import Flask, render_template, request
import main

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    result = {}
    if request.method == 'POST':
        file = request.files['graph_file']
        G = main.load_graph_from_stream(file.stream)
        result = main.compute_colorings(G)
    return render_template('index.html', result=result, use_reloader=False)

if __name__ == '__main__':
    app.run(debug=True)
