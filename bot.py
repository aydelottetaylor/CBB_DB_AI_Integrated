import json
import sys
from openai import OpenAI
import os
import sqlite3
import time
import datetime
import csv

# -------------------- HELPER FUNCS -------------------- #
def get_path(fname):
    fdir = os.path.dirname(__file__)
    
    return os.path.join(fdir, fname)

def setup():

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
    
    return sqlite_cursor, sqlite_connection, open_ai_client, school_stats_path, school_ratings_path, setup_tables_script

def close_connections(sqlite_cursor, sqlite_connection):
    sqlite_cursor.close()
    sqlite_connection.close()
    
    print("Goodbye!")

def run_query(query, sqlite_cursor):
    return sqlite_cursor.execute(query).fetchall()

def fetch_database(sqlite_cursor):
    tables = ['Commissioner', 'Conference', 'Team_stats', 'Player']
    
    for table in tables:
        print(f"{table} Data:")
        data = run_query(f'SELECT * FROM {table}', sqlite_cursor)
        for row in data:
            print('  ', row)
        print()

def get_gpt_response(query_content, open_ai_client):
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
                if ratings_row["AP Rank"] != '':
                    ap_rank = int(ratings_row["AP Rank"])
                else:
                    ap_rank = None
                games = int(row["G"])
                wins = int(row["W"])
                losses = int(row["L"])
                win_percentage = float(row["W-L%"])
                offensive_simple_rating_system = float(ratings_row["OSRS"])
                defensive_simple_rating_system = float(ratings_row["DSRS"])
                simple_rating_system = float(ratings_row["SRS"])
                strength_of_schedule = float(ratings_row["SOS"])
                offensive_rating = float(ratings_row["ORtg"])
                defensive_rating = float(ratings_row["DRtg"])
                net_rating = float(ratings_row["NRtg"])
                conference_wins = int(row["CW"])
                conference_losses = int(row["CL"])
                home_wins = int(row["HW"])
                home_losses = int(row["HL"])
                away_wins = int(row["AW"])
                away_losses = int(row["AL"])
                team_points = int(row["Tm."])
                opponent_points = int(row["Opp."])
                minutes_played = int(row['MP'])
                field_goals_made = int(row['FG'])
                field_goals_attempted = int(row['FGA'])
                field_goal_percentage = float(row['FG%'])
                three_pointers_made = int(row['3P'])
                three_pointers_attempted = int(row['3PA'])
                three_point_percentage = float(row['3P%'])
                free_throws_made = int(row['FT'])
                free_throws_attempted = int(row['FTA'])
                free_throw_percentage = float(row['FT%'])
                offensive_rebounds = int(row['ORB'])
                team_rebounds = int(row["TRB"])
                assists = int(row["AST"])
                steals = int(row["STL"])
                blocks = int(row["BLK"])
                turnovers = int(row["TOV"])
                personal_fouls = int(row["PF"])
        
                cursor.execute(
                    """
                    INSERT INTO team_stats (
                        conference_id, team_name, ap_rank, games, wins, losses, win_percentage, offensive_simple_rating_system, defensive_simple_rating_system, 
                        simple_rating_system, strength_of_schedule, offensive_rating, defensive_rating, net_rating, 
                        conference_wins, conference_losses, home_wins, home_losses, away_wins, away_losses, 
                        team_points, opponent_points, minutes_played, field_goals_made, field_goals_attempted, 
                        field_goal_percentage, three_pointers_made, three_pointers_attempted, three_point_percentage, 
                        free_throws_made, free_throws_attempted, free_throw_percentage, offensive_rebounds,
                        team_rebounds, assists, steals, blocks, turnovers, personal_fouls
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        conference_id, team_name, ap_rank, games, wins, losses, win_percentage, offensive_simple_rating_system, defensive_simple_rating_system, 
                        simple_rating_system, strength_of_schedule, offensive_rating, defensive_rating, net_rating, 
                        conference_wins, conference_losses, home_wins, home_losses, away_wins, away_losses, 
                        team_points, opponent_points, minutes_played, field_goals_made, field_goals_attempted, 
                        field_goal_percentage, three_pointers_made, three_pointers_attempted, three_point_percentage, 
                        free_throws_made, free_throws_attempted, free_throw_percentage, offensive_rebounds,
                        team_rebounds, assists, steals, blocks, turnovers, personal_fouls
                    )
                )
                
def send_question_get_response(question, sqlite_cursor, open_ai_client):
    sql_response = get_gpt_response(question, open_ai_client)
    sql_response = sanitize_sql_response(sql_response)
    # print(sql_response)
    query_response = str(run_query(sql_response, sqlite_cursor))
    # print(query_response)
    final_response_prompt = ('I asked this question: ' + 
                            question + ' And got back this response: ' + 
                            query_response + 
                            '. Please interpret this response to fit the context of the question into one single sentence. Be very specific and concise and do not say anything else besides that interpretation. Format the data into a table or visual if you need to.')
    final_response = get_gpt_response(final_response_prompt, open_ai_client)
    # print(final_response)
    return sql_response, query_response, final_response


# -------------------- MAIN -------------------- #
def main():
    if len(sys.argv) != 2:
        print("Usage: python file.py <0 or 1>")
        sys.exit(1)
        
    sqlite_cursor, sqlite_connection, open_ai_client, school_stats_path, school_ratings_path, setup_tables_script = setup()
    insert_team_data(sqlite_cursor, school_stats_path, school_ratings_path)
    print(fetch_database(sqlite_cursor))
    
    sql_only_request_content = 'Give me a sqlite select statement that answers the following question. Only respond with the sqlite select statement. If there is an error do not explain or talk about it. Here is the question: '
        
    mode = int(sys.argv[1])
    if mode not in (0, 1):
        print("Error: Second argument must be either 0 or 1")
        sys.exit(1)
    
    if mode == 0:
        # -------------- PROMPT SETUP -------------- #
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


        # -------------- RUN PROMPTS -------------- #
        for strategy in strategies:
            responses = {'strategy': strategy, 'prompt_prefix': strategies[strategy]}
            query_results = []
            
            for question in questions:
                # print(question)
                error = None
                try:
                    prepared_question = strategies[strategy] + ' ' + question
                    sql_response, query_response, final_response = send_question_get_response(prepared_question, sqlite_cursor, open_ai_client)
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
                
            responses['results'] = query_results
            
            timestamp = time.time()
            date_time = datetime.datetime.fromtimestamp(timestamp)
            
            with open(get_path(f'responses\\response_{strategy}_{date_time.strftime("%Y-%m-%d_%H-%M-%S")}.json'), 'w') as file:
                json.dump(responses, file, indent=2)
    elif mode == 1:
        
        another = "Yes"
        while (another == "Yes"):
            question = input("Please enter your question: ")
            prepared_question = setup_tables_script + sql_only_request_content + question
            
            error = None
            try:
                sql_response, query_response, final_response = send_question_get_response(prepared_question, sqlite_cursor, open_ai_client)
                print('   Answer: ', final_response)
                print()
            except Exception as exception:
                error = str(exception)
                print(error)
            
            timestamp = time.time()
            date_time = datetime.datetime.fromtimestamp(timestamp)
                
            query_results = {
                'Timestamp': date_time.strftime("%Y-%m-%d %H:%M:%S"),
                'Question': question,
                'GPT Generated SQL': sql_response,
                'Response from Generated SQL': query_response,
                'Reponse Interpreted by GPT': final_response,
                'Error': error
            }
                
            with open("responses/all/responses.json", "a") as file:
                json.dump(query_results, file, indent=2)
            
            another = input("Do you have another question? <Yes or No>")
                
                
                
    close_connections(sqlite_cursor, sqlite_connection)
            
if __name__ == "__main__":
    main()        

