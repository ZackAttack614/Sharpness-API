import json
from flask import Flask, request
app = Flask(__name__)

data = dict()
for depth in [1, 5, 10, 15, 20]:
  with open(f'game_6/evals_depth_{depth}.json') as fin:
    data[depth] = json.load(fin)

@app.route('/')
def index():
  depth = request.args.get("depth")
  if depth is None:
    return {}
  try:
    depth = int(depth)
  except:
    return {}
  if depth not in data.keys():
    return {}
  return json.dumps(data[depth])

app.run()
