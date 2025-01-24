# CBB_DB_AI_Integrated
College Basketball Database integrated with AI (Chat GPT) to process natural language questions, create and SQL query, run the query, and then interpret the data and return a natural language response. 

**config.json** Contains openAI key and Org Id

**bot.py** Initializes the database, connects to model on openAI, feeds OpenAI prompts and questions, tracks responses.

**schema.png** Visual representation of DB structure.

**setup_data.sql** Inserts CBB data into database. (We have fake data as of this point, one of the next steps should be connecting to real-time data.)

**setup_tables.sql** Creates database tables.