import json
from openai import OpenAI
import os
import sqlite3
import time
import datetime
import csv


# Get current directory and setup file path generation
fdir = os.path.dirname(__file__)
def get_path(fname):
    return os.path.join(fdir, fname)

sqlite_db_path = get_path("cbb_db.sqlite")
setup_data_path = get_path("setup_data.sql")
setup_tables_path = get_path("setup_tables.sql")
school_stats_path = get_path("data/school_stats.csv")
school_ratings_path = get_path("data/school_ratings.csv")

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

def insert_team_data(cursor, stats_path, ratings_path):
    with open(stats_path) as stats_file, open(ratings_path) as ratings_file:
        stats_reader = csv.DictReader(stats_file, skipinitialspace=True)
        stats_reader.fieldnames = [header.strip() for header in stats_reader.fieldnames if header.strip()]

        ratings_reader = csv.DictReader(ratings_file, skipinitialspace=True)
        ratings_reader.fieldnames = [header.strip() for header in ratings_reader.fieldnames if header.strip()]
        
        ratings_data = {
            row['School']: row for row in ratings_reader
        }
        
        for row in stats_reader:
            school = row['School']
            if school in ratings_data:
                ratings_row = ratings_data[school]
                if ratings_row['Conf'] == 'Big 12':
                    conference_id = 1
                elif ratings_row['Conf'] == 'ACC':
                    conference_id = 2
                elif ratings_row['Conf'] == 'Big Ten':
                    conference_id = 3
                elif ratings_row['Conf'] == 'SEC':
                    conference_id = 4
                elif ratings_row['Conf'] == 'Big East':
                    conference_id = 5
                else:
                    conference_id = 6
                team_name = school
                games = int(row["G"])
                wins = int(row["W"])
                losses = int(row["L"])
                win_percentage = float(row["W-L%"])
                simple_rating_system = float(ratings_row["SRS"])
                strength_of_schedule = float(ratings_row["SOS"])
                team_points = int(row["Tm."])
                opponent_points = int(row["Opp."])
                team_rebounds = int(row["TRB"])
                assists = int(row["AST"])
                steals = int(row["STL"])
                blocks = int(row["BLK"])
                turnovers = int(row["TOV"])
                personal_fouls = int(row["PF"])
        
                cursor.execute(
                    """
                    INSERT INTO team (
                        conference_id, team_name, games, wins, losses, win_percentage, 
                        simple_rating_system, strength_of_schedule, team_points, opponent_points,  
                        team_rebounds, assists, steals, blocks, turnovers, personal_fouls
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        conference_id, team_name, games, wins, losses, win_percentage,
                        simple_rating_system, strength_of_schedule, team_points, opponent_points,
                        team_rebounds, assists, steals, blocks, turnovers, personal_fouls
                    )
                )

insert_team_data(sqlite_cursor, school_stats_path, school_ratings_path)
        
# print(fetch_database())

# -------------------- PROMPT SETUP -------------------- #
sql_only_request_content = 'Give me a sqlite select statement that answers the following question. Only respond with the sqlite select statement. If there is an error do not explain or talk about it.'

strategies = {
    'zero_shot': setup_tables_script + sql_only_request_content,
    'single_domain_double_shot': (setup_tables_script +
                        "List the conferences in order for highest to lowest average strength of schedule and give their average strength of schedule." +
                        "SELECT conference.conference_name, AVG(team.strength_of_schedule) AS average_strength_of_schedule\nFROM conference\nJOIN team ON conference.conference_id = team.conference_id\nGROUP BY conference.conference_id\nORDER BY average_strength_of_schedule DESC;\n" +
                        sql_only_request_content)
}

questions = [
    "Which team has the most points?",
    "Which team averages the most points per game?",
    "Which team has the best assist to turnover ratio and what is their assist to turnover ratio?",
    "Which team has the most players with over 200 total points and who are those players?",
    "Which team has the least players with over 200 points?",
    "What are the three teams with the most rebounds per game?",
    "Come up with an algorithm to recommend the top 3 most valuable players for the Big 12 conference based on individual player rating. Give their rating and team they belong to.",
    "Calculate each player's impact score that plays for Brigham Young. The Impact score is defined as: ((Player's Total Points + Total Rebounds + Total Assists) / Teams Total Games played) * Team's Win Percentage.",
    "Calculate the top 10 impact scores in the Big 12 conference. The Impact score is defined as: ((Player's Total Points + Total Rebounds + Total Assists) / Teams Total Games played) * Team's Win Percentage.",
    "What are the teams with the top five average margins of vistory?",
    "What are the teams with the top five average margins of victory adjusted for normalized strength of schedule?"
]


# -------------------- RUN PROMPTS -------------------- #
for strategy in strategies:
    responses = {'strategy': strategy, 'prompt_prefix': strategies[strategy]}
    query_results = []
    
    for question in questions:
        # print(question)
        error = None
        try:
            sql_response = get_gpt_response(strategies[strategy] + ' ' + question)
            sql_response = sanitize_sql_response(sql_response)
            # print(sql_response)
            query_response = str(run_query(sql_response))
            # print(query_response)
            final_response_prompt = ('I asked the following question ' + 
                                     question + ' and got back this response: ' + 
                                     query_response + 
                                     '. Please interpret this response to fit the context of the question into one single sentence. Be very specific and concise and do not say anything else besides that interpretation. Format the data into a table or visual if you need to.')
            final_response = get_gpt_response(final_response_prompt)
            # print(final_response)
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
    
    timestamp = time.time()
    date_time = datetime.datetime.fromtimestamp(timestamp)
    
    with open(get_path(f'responses\\response_{strategy}_{date_time.strftime("%Y-%m-%d_%H-%M-%S")}.json'), 'w') as file:
        json.dump(responses, file, indent=2)
            
            
            
# -------------------- CLOSE -------------------- #
sqlite_cursor.close()
sqlite_connection.close()
print("Finished!")
