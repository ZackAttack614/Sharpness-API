from google.cloud import bigquery
from google.oauth2 import service_account
import json

credentials = service_account.Credentials.from_service_account_file(
    'lichess-analysis-abe717c29e85.json')
bigquery_client = bigquery.Client(project='lichess-analysis', credentials=credentials)

dataset_ref = bigquery_client.dataset('games')
table_ref = dataset_ref.table('sharpness')
table = bigquery_client.get_table(table_ref)

game_number = 2
depth = 10

query = f'''
  SELECT halfmove
  FROM `lichess-analysis.games.sharpness`
  WHERE game_number = {game_number} AND depth = {depth}
'''

results = {str(i): v for i, v in enumerate(list(bigquery_client.query(query).result())[0][0])}
print(json.dumps(results, indent=2))
