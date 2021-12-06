import json
from flask import Flask, Response, request
from flask_api_cache import ApiCache
from google.cloud import bigquery
from google.oauth2 import service_account

cache_expiry_time = 100
credentials = service_account.Credentials.from_service_account_file(
    'lichess-analysis-abe717c29e85.json')
bigquery_client = bigquery.Client(project='lichess-analysis', credentials=credentials)

dataset_ref = bigquery_client.dataset('games')
table_ref = dataset_ref.table('sharpness')
table = bigquery_client.get_table(table_ref)

app = Flask(__name__)

def make_response(d):
  resp = Response(d)
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return resp

@app.route('/games')
@ApiCache(expired_time=cache_expiry_time)
def games():
  query = f'''
    SELECT DISTINCT(game_number)
    FROM `lichess-analysis.games.sharpness`
  '''
  r = list(bigquery_client.query(query).result())
  return json.dumps([r[i]['game_number'] for i in range(len(r))])

@app.route('/sharpness')
@ApiCache(expired_time=cache_expiry_time)
def sharpnesss():
  depth = request.args.get("depth")
  game_num = request.args.get("game")
  color = request.args.get("color")

  if depth is None or game_num is None:
    return make_response(json.dumps({}))
  try:
    depth = int(depth)
    game_num = int(game_num)
  except:
    return make_response(json.dumps({}))

  query = f'''
    SELECT halfmove
    FROM `lichess-analysis.games.sharpness`
    WHERE game_number = {game_num} AND depth = {depth}
  '''
  r = list(bigquery_client.query(query).result())
  if not any(r):
    return make_response(json.dumps({}))

  results = {str(i): v for i, v in enumerate(r[0][0])}
  if color is not None:
    if color.lower().strip() == 'white':
      for i in range(1, len(results), 2):
        del results[str(i)]
    elif color.lower().strip() == 'black':
      for i in range(0, len(results), 2):
        del results[str(i)]

  return make_response(json.dumps(results))

app.run(host='0.0.0.0')
