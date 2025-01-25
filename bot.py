import json
from openai import OpenAI
import os
import sqlite3
from time import time


# Get current directory and setup file path generation
fdir = os.path.dirname(__file__)
def get_path(fname):
    return os.path.join(fdir, fname)

sqlite_db_path = get_path("cbb_db.sqlite")
setup_data_path = get_path("setup_data.sql")
setup_tables_path = get_path("setup_tables.sql")

# Erase db if already exists
if os.path.exists(sqlite_db_path):
    os.remove(sqlite_db_path)
    
# Start connection, create cursor, generate table, and insert data
sqlite_connection = sqlite3.connect(sqlite_db_path)
sqlite_cursor = sqlite_connection.cursor()
with (
        open(setup_tables_path) as setup_tables,
        open(setup_data_path) as setup_data
    ):
    
    setup_tables_script = setup_tables.read()
    setup_data_script = setup_data.read()
    
sqlite_cursor.executescript(setup_tables_script)
sqlite_cursor.executescript(setup_data_script)

# Setup OpenAI 
config_path = get_path('config.json')

with open(config_path) as config_file:
    config = json.load(config_file)
    
open_ai_client = OpenAI(api_key=config['open_ai_key'])


# -------------------- HELPER FUNCS -------------------- #
def run_query(query):
    return sqlite_cursor.execute(query).fetchall()

def fetch_database():
    tables = ['Commissioner', 'Conference', 'Team', 'Player']
    
    for table in tables:
        print(f"{table} Data:")
        data = run_query(f'SELECT * FROM {table}')
        for row in data:
            print('  ', row)
        print()

def get_gpt_response(query_content):
    stream = open_ai_client.chat.completions.create(
        model = 'gpt-4o',
        messages = [{'role': 'user', 'content': query_content}],
        stream = True
    )
    
    response_list = []
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_list.append(chunk.choices[0].delta.content)
            
    return "".join(response_list)

def sanitize_sql_response(response):
    start_marker = "```sql\n"
    end_marker = "```"
    
    if start_marker in response:
        response = response.split(start_marker)[1]
    if end_marker in response:
        response = response.split(end_marker)[0]
    return response
    
    
# -------------------- PROMPT SETUP -------------------- #
sql_only_request_content = 'Give me a sqlite select statement that answers the following question. Only respond with the sqlite select statement. If there is an error do not explain or talk about it.'

strategies = {
    'zero_shot': setup_tables_script + sql_only_request_content
}

questions = [
    "Which team has the most points?",
    "Which team averages the most points per game?",
    "Which team has the best assist to turnover ratio and what is their assist to turnover ratio?"
]


# -------------------- RUN PROMPTS -------------------- #
for strategy in strategies:
    responses = {'strategy': strategy, 'prompt_prefix': strategies[strategy]}
    query_results = []
    
    for question in questions:
        print(question)
        error = None
        try:
            sql_response = get_gpt_response(strategies[strategy] + ' ' + question)
            sql_response = sanitize_sql_response(sql_response)
            print(sql_response)
            query_response = str(run_query(sql_response))
            print(query_response)
            final_response_prompt = 'I asked the following question ' + question + ' and got back this response: ' + query_response + '. Please interpret this response to fit the context of the question into one single sentence. Be very specific and concise and do not say anything else besides that interpretation.'
            final_response = get_gpt_response(final_response_prompt)
            print(final_response)
        except Exception as exception:
            error = str(exception)
            print(error)
            
        query_results.append({
            'Question': question,
            'GPT Generated SQL': sql_response,
            'Response from Generated SQL': query_response,
            'Reponse Interpreted by GPT': final_response,
            'Error': error
        })
        
    responses["results"] = query_results
    
    with open(get_path(f'responses\\response_{strategy}_{time()}.json'), 'w') as file:
        json.dump(responses, file, indent=2)
            
            
            
# -------------------- CLOSE -------------------- #
sqlite_cursor.close()
sqlite_connection.close()
print("Finished!")
