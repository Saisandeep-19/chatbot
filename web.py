from flask import Flask, render_template, request, jsonify
from chatbot import get_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.form["message"]
        response = get_response(user_input)
        return jsonify({"response": response})
    except Exception as e:
        import traceback
        traceback.print_exc()  
        return jsonify({"response": f"⚠ Error: {str(e)}"})
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)