CREATE TABLE commissioner (
    commissioner_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    age INTEGER,
    phone_number BIGINT,
    email VARCHAR(35)
);

CREATE TABLE conference (
    conference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conference_name VARCHAR(30) NOT NULL,
    year_founded INTEGER NOT NULL,
    subdivision VARCHAR(10) NOT NULL,
    commissioner_id INTEGER NOT NULL,
    FOREIGN KEY (commissioner_id) REFERENCES commissioner (commissioner_id)
);

CREATE TABLE team (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conference_id INTEGER NOT NULL,
    team_name VARCHAR(30) NOT NULL,
    games INTEGER NOT NULL,
    wins INTEGER NOT NULL,
    losses INTEGER NOT NULL,
    win_percentage DECIMAL(4, 3),
    strength_of_schedule DECIMAL(5, 2),
    simple_rating_system DECIMAL(5, 2),
    team_points INTEGER NOT NULL,
    opponent_points INTEGER NOT NULL,
    team_rebounds INTEGER NOT NULL,
    assists INTEGER NOT NULL,
    steals INTEGER NOT NULL,
    blocks INTEGER NOT NULL,
    turnovers INTEGER NOT NULL,
    personal_fouls INTEGER NOT NULL,
    FOREIGN KEY (conference_id) REFERENCES conference (conference_id)
);

CREATE TABLE player (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_id INTEGER NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    position VARCHAR(15) NOT NULL,
    games_played INTEGER NOT NULL,
    total_points INTEGER NOT NULL,
    total_rebounds INTEGER NOT NULL,
    total_assists INTEGER NOT NULL,
    field_goal_percentage DECIMAL(4, 1) NOT NULL,
    three_point_percentage DECIMAL(4, 1) NOT NULL,
    free_throw_percentage DECIMAL(4, 1) NOT NULL,
    effective_field_goal_percentage DECIMAL(4, 1) NOT NULL,
    FOREIGN KEY (team_id) REFERENCES team (team_id)
);

