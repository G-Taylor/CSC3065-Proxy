import json
from flask import Flask, request
import requests
import flask 
from function_list import FUNCTIONS   

app = Flask(__name__)


@app.route("/")
def proxy_home():

    function_found = False
    # get parameters
    sentence = request.args.get('text')
    editor_function = request.args.get('func')

    # check external list of function endpoints to find a match
    for func, url in FUNCTIONS.items():
        if func == editor_function:
            function_found = True
            editor_function = url

    # Output for an incorrect function
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

    # Output for an invalid sentence
    elif sentence == "" or sentence == None:
        output = {
            "error": True,
            "sentence": "No Text Entered",
            "answer": 0
        }
        json_output = json.dumps(output)
        response = flask.Response(json_output)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    # Get response from valid function and query
    else:
        query = editor_function + "/?text=" + sentence
        output = requests.get(query)
        # Output for an invalid response
        if output.status_code != 200:
            output = {
            "error": True,
            "sentence": "Incorrect Respone, Error Code: " + output.status_code,
            "answer": 0
            }
            json_output = json.dumps(output)
            response = flask.Response(json_output)
            response.headers['Content-Type'] = 'application/json'
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        else:
            response = flask.Response(output)
            response.headers['Content-Type'] = 'application/json'
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug=True)