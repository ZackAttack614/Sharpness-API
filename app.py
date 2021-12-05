import glob
import json
from flask import Flask, Response, request
app = Flask(__name__)

data = dict()
for dir in glob.glob('data/game_*'):
  game_num = int(dir.split('_')[-1])
  data[game_num] = dict()
  for depth in [1, 5, 10, 15, 20]:
    with open(f'{dir}/evals_depth_{depth}.json') as fin:
      data[game_num][depth] = json.load(fin)

def make_response(d):
  resp = Response(d)
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return resp

@app.route('/games')
def games():
  return make_response(json.dumps([key for key in data.keys()]))

@app.route('/eval')
def eval():
  depth = request.args.get("depth")
  game_num = request.args.get("game")
  body = dict()

  try:
    depth = int(depth)
    game_num = int(game_num)
  except:
    return make_response(body)

  if depth is None or game_num is None:
    return make_response(body)
  if game_num not in data.keys():
    return make_response(body)
  if depth not in data.get(game_num).keys():
    return make_response(body)

  for i, (k, v) in enumerate(data[game_num][depth].items()):
    body[k] = max(v.get('evals')) * (-1 if i % 2 == 1 else 1)

  return make_response(json.dumps(body))

@app.route('/sharpness')
def sharpnesss():
  depth = request.args.get("depth")
  game_num = request.args.get("game")
  color = request.args.get("color")

  if depth is None or game_num is None:
    return make_response({})
  try:
    depth = int(depth)
    game_num = int(game_num)
  except:
    return make_response({})

  if game_num not in data.keys():
    return make_response({})
  if depth not in data.get(game_num).keys():
    return make_response({})
  if color is not None:
    if color.lower().strip() == 'white':
      body = dict()
      for i, (k, v) in enumerate(data[game_num][depth].items()):
        if i % 2 == 1:
          continue
        body[k] = v
      return make_response(json.dumps(body))
    elif color.lower().strip() == 'black':
      body = dict()
      for i, (k, v) in enumerate(data[game_num][depth].items()):
        if i % 2 == 0:
          continue
        body[k] = v
      return make_response(json.dumps(body))
    else:
      return make_response(json.dumps(data[game_num][depth]))
  else:
    return make_response(json.dumps(data[game_num][depth]))

app.run(host='0.0.0.0')
