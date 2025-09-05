from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/button_clicked", methods=["POST"])
def button_clicked():
    print("clicked")
    data = request.get_json()  # receive JSON from JS
    for key, value in data.items():
        print(f"{key}: {value}")  # print each textarea value in terminal
    return "Received news data!"




if __name__ == "__main__":
    app.run(debug=True)
