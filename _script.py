from flask import Flask, request, jsonify
from PreProcess import find_candidates
import json
import numpy as np

app = Flask(__name__)

# def listToString(s):

#     # initialize an empty string
#     str1 = ""

#     # traverse in the string
#     for ele in s:
#         str1 += ele

#     # return string
#     return str1

# @app.route('/', methods=['GET'])
# def candidates():
#     return "hello"


@app.route('/find_candidates', methods=['GET'])
def get_candidates():
    jd = request.args.get('job_description')
    matched_candidates = find_candidates(jd)
    response = json.dumps(matched_candidates, cls=NpEncoder)
    # print(demo)
    return response

    
if __name__ == '__main__':
    app.run(port=5000)


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
