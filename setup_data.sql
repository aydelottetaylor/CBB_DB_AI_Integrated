INSERT INTO commissioner (first_name, last_name, age, phone_number, email) VALUES
    ('Brett', 'Yormark', 60, 3853251234, 'brett.yormark@gmail.com'),
    ('Jim', 'Phillips', 45, 3853851234, 'chad.christensen@gmai.com'),
    ('Tony', 'Petitti', 32, 3853251234, 'tony.petitti@gmail.com'),
    ('Greg', 'Sankey', 59, 3853251234, 'greg.sankey@gmail.com'),
    ('Val', 'Ackerman', 63, 3853251234, 'val.ackerman@gmail.com');

INSERT INTO conference (conference_name, year_founded, subdivision, commissioner_id) VALUES
    ('Big 12', 1994, 'FBS', 1),
    ('ACC', 1984, 'FBS', 2),
    ('Big 10', 1896, 'FBS', 3),
    ('SEC', 1933, 'FBS', 4),
    ('Big East', 1979, 'FBS', 5);

INSERT INTO team (conference_id, team_name, games, wins, losses, win_percentage, simple_rating_system, strength_of_schedule, team_points, team_rebounds, assists, steals, blocks, turnovers, personal_fouls) VALUES
    (1, 'Arizona', 18, 12, 6, 0.667, 22.94, 9.22, 1336, 665, 241, 101, 93, 241, 291),
    (1, 'Arizona State', 18, 11, 7, 0.611, 13.59, 10.87, 1461, 689, 281, 145, 111, 221, 305),
    (1, 'Baylor', 18, 12, 6, 0.667, 19.51, 9.98, 1443, 663, 290, 156, 60, 195, 279),
    (1, 'Brigham Young', 18, 12, 6, 0.667, 16.43, 3.04, 1447, 706, 308, 135, 64, 214, 286),
    (1, 'Cincinnati', 18, 12, 6, 0.667, 15.27, 4.66, 1302, 666, 261, 131, 89, 181, 245),
    (1, 'Colorado', 18, 9, 9, 0.500, 8.45, 7.28, 1320, 633, 281, 142, 69, 272, 294),
    (1, 'Houston', 18, 15, 3, 0.833, 29.72, 7.83, 1365, 683, 238, 156, 100, 161, 296),
    (1, 'Iowa State', 18, 16, 2, 0.889, 25.31, 6.42, 1532, 678, 291, 179, 64, 186, 272),
    (1, 'Kansas', 18, 14, 4, 0.778, 23.78, 10.78, 1374, 700, 327, 120, 91, 196, 251),
    (1, 'Kansas State', 18, 7, 11, 0.389, 6.36, 5.53, 1307, 599, 294, 129, 61, 218, 278),
    (1, 'Oklahoma State', 18, 10, 8, 0.556, 4.64, 5.36, 1336, 652, 226, 157, 49, 233, 351),
    (1, 'TCU', 18, 10, 8, 0.556, 12.69, 9.69, 1258, 626, 236, 139, 61, 202, 274),
    (1, 'Texas Tech', 18, 14, 4, 0.778, 22.34, 5.06, 1493, 680, 312, 128, 49, 191, 277),
    (1, 'UCF', 18, 12, 6, 0.667, 9.62, 9.57, 1425, 668, 258, 134, 81, 231, 307),
    (1, 'Utah', 18, 11, 7, 0.611, 11.85, 4.13, 1399, 726, 346, 117, 75, 225, 321),
    (1, 'West Virginia', 18, 13, 5, 0.722, 17.30, 9.41, 1292, 621, 243, 145, 87, 194, 297),

    (2, 'Boston College', 19, 9, 10, .474, -2.66, 1.81, 1319, 663, 209, 91, 70, 231, 348);
    (2, 'California', 19, 10, 9, .526, 5.64, 5.12, 1427, 702, 195, 106, 73, 225, 311),
    (2, 'Clemson', ),
    (2, 'Duke', ),
    (2, 'Florida State', ),
    (2, 'Georgia Tech', ),
    (2, 'Louisville', ),
    (2, 'Miami (FL)', ),
    (2, 'NC State', ),
    (2, 'North Carolina', ),
    (2, 'Notre Dame', ),
    (2, 'Pittsburgh', ),
    (2, 'Southern Methodist', ),
    (2, 'Stanford', ),
    (2, 'Syracuse', ),
    (2, 'Virginia', ),
    (2, 'Virginia Tech', ),
    (2, 'Wake Forest', ),


    