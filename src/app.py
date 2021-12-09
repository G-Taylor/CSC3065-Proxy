import json
from flask import Flask, request
import requests
import flask    

app = Flask(__name__)


@app.route("/")
def proxy_home():

    function_dict = {
        "wordcount": "http://wordcount.40234272.qpc.hal.davecutting.uk",
        "charcount": "http://charcount.40234272.qpc.hal.davecutting.uk",
        "vowelcount": "http://vowel.40234272.qpc.hal.davecutting.uk",
        "palindrome": "http://palindrome.40234272.qpc.hal.davecutting.uk",
        "average": "http://avgword.40234272.qpc.hal.davecutting.uk",
        "and": "http://andcount.40234272.qpc.hal.davecutting.uk"
    }

    function_found = False
    sentence = request.args.get('text')
    editor_function = request.args.get('func')

    for func, url in function_dict.items():
        if func == editor_function:
            function_found = True
            editor_function = url

    if not function_found or editor_function is None:
        output = {
            "error": True,
            "sentence": "Invalid Function",
            "answer": 0
        }
        json_output = json.dumps(output)
        response = flask.Response(json_output)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    else:
        query = editor_function + "/?text=" + sentence
        output = requests.get(query)
        response = flask.Response(output)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)