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

    if function_dict[editor_function]:
        function_found = True

    if not function_found:
        output = {
            "error": True,
            "sentence": "Invalid Function",
            "answer": 0
        }
        return generate_response(output)

    else:
        query = f"{editor_function}/?text{sentence}"
        output = requests.get(query)

        return generate_response(output)


def generate_response(output):
    json_output = json.dumps(output)
    response = flask.Response(json_output)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(host = '0.0.0.0')