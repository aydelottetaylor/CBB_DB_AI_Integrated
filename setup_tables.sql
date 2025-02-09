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

CREATE TABLE team_stats (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    conference_id INTEGER NOT NULL,
    team_name VARCHAR(30) NOT NULL,
    ap_rank INTEGER, 
    games INTEGER NOT NULL,
    wins INTEGER NOT NULL,
    losses INTEGER NOT NULL,
    win_percentage DECIMAL(4, 3),
    offensive_simple_rating_system DECIMAL(5, 2),
    defensive_simple_rating_system DECIMAL(5, 2),
    simple_rating_system DECIMAL(5, 2),
    strength_of_schedule DECIMAL(5, 2),
    offensive_rating DECIMAL(6, 2),
    defensive_rating DECIMAL(6, 2),
    net_rating DECIMAL(6, 2),
    conference_wins INTEGER NOT NULL,
    conference_losses INTEGER NOT NULL,
    home_wins INTEGER NOT NULL,
    home_losses INTEGER NOT NULL,
    away_wins INTEGER NOT NULL,
    away_losses INTEGER NOT NULL,
    team_points INTEGER NOT NULL,
    opponent_points INTEGER NOT NULL,
    minutes_played INTEGER NOT NULL,
    field_goals_made INTEGER NOT NULL,
    field_goals_attempted INTEGER NOT NULL,
    field_goal_percentage DECIMAL(4, 3),
    three_pointers_made INTEGER NOT NULL,
    three_pointers_attempted INTEGER NOT NULL,
    three_point_percentage DECIMAL(4, 3),
    free_throws_made INTEGER NOT NULL,
    free_throws_attempted INTEGER NOT NULL,
    free_throw_percentage DECIMAL(4, 3),
    offensive_rebounds INTEGER NOT NULL,
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
    FOREIGN KEY (team_id) REFERENCES team_stats (team_id)
);

