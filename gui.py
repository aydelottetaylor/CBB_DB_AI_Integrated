import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import bot

def data_setup():
    global sqlite_cursor
    global sqlite_connection
    global open_ai_client
    global setup_tables_script
    
    sqlite_cursor, sqlite_connection, open_ai_client, school_stats_path, school_ratings_path, setup_tables_script = bot.setup()
    bot.insert_team_data(sqlite_cursor, school_stats_path, school_ratings_path)
    
def add_team_data_table():
    team_data_label = tk.Label(window, text='Team Data', font=('Arial', 11, 'bold'))
    team_data_label.pack()
    
    team_data = bot.fetch_team_data(sqlite_cursor)
    team_cols = bot.get_team_data_cols()
    
    table_frame = tk.Frame(window)
    table_frame.pack()    
    
    style = ttk.Style()
    style.configure('Treeview', rowheight=25, borderwidth=2, releif='solid')
    style.configure('Treeview.Heading', font=('Arial', 8, 'bold'))
    
    tree = ttk.Treeview(table_frame, columns = team_cols, show='headings', height=15, selectmode='browse')
    
    for col in team_cols:
        tree.heading(col, text=col, anchor='w')
        match col:
            case 'Team': tree.column(col, width=150, anchor='w')
            case 'AP Rank': tree.column(col, width=60, anchor='w')
            case 'G': tree.column(col, width=25, anchor='w')
            case 'W': tree.column(col, width=25, anchor='w')
            case 'L': tree.column(col, width=25, anchor='w')
            case 'Win %': tree.column(col, width=50, anchor='w')
            case 'OSRS': tree.column(col, width=50, anchor='w')
            case 'DSRS': tree.column(col, width=50, anchor='w')
            case 'SRS': tree.column(col, width=50, anchor='w')
            case 'SOS': tree.column(col, width=50, anchor='w')
            case 'O Rtg': tree.column(col, width=50, anchor='w')
            case 'D Rtg': tree.column(col, width=50, anchor='w')
            case 'Net Rtg': tree.column(col, width=50, anchor='w')
            case 'Conf W': tree.column(col, width=50, anchor='w')
            case 'Conf L': tree.column(col, width=50, anchor='w')
            case 'H W': tree.column(col, width=50, anchor='w')
            case 'H L': tree.column(col, width=50, anchor='w')
            case 'A W': tree.column(col, width=50, anchor='w')
            case 'A L': tree.column(col, width=50, anchor='w')
            case 'Tm Pts': tree.column(col, width=50, anchor='w')
            case 'Opp Pts': tree.column(col, width=50, anchor='w')
            case 'Mins': tree.column(col, width=50, anchor='w')
            case 'FGM': tree.column(col, width=50, anchor='w')
            case 'FGA': tree.column(col, width=50, anchor='w')
            case 'FG%': tree.column(col, width=50, anchor='w')
            case '3PM': tree.column(col, width=50, anchor='w')
            case '3PA': tree.column(col, width=50, anchor='w')
            case '3P%': tree.column(col, width=50, anchor='w')
            case 'FTM': tree.column(col, width=50, anchor='w')
            case 'FTA': tree.column(col, width=50, anchor='w')
            case 'FT%': tree.column(col, width=50, anchor='w')
            case 'O Reb': tree.column(col, width=50, anchor='w')
            case 'Tm Reb': tree.column(col, width=50, anchor='w')
            case 'Ast': tree.column(col, width=50, anchor='w')
            case 'Stl': tree.column(col, width=50, anchor='w')
            case 'Blk': tree.column(col, width=50, anchor='w')
            case 'TO': tree.column(col, width=50, anchor='w')
            case 'PF': tree.column(col, width=50, anchor='w')
            case _:  tree.column(col, width=0, anchor='w')
            
    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("evenrow", background="lightblue")
            
    for i, team in enumerate(team_data):
        team_without_conference_id = (team[0],) + team[2:]
        
        team_without_conference_id = list(team_without_conference_id)
        if team_without_conference_id[2] == None:
            team_without_conference_id[2] = ''
        team_without_conference_id = tuple(team_without_conference_id) 
        
        tag = "evenrow" if i % 2 == 0 else "oddrow"   
        
        tree.insert('', 'end', values=team_without_conference_id, tags=(tag,))
        
    scroll_bar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
    bottom_bar = ttk.Scrollbar(table_frame, orient='horizontal', command=tree.xview)
    tree.configure(yscroll=scroll_bar.set)
    tree.configure(xscroll=bottom_bar.set)
    scroll_bar.pack(side='right', fill='y')
    bottom_bar.pack(side='bottom', fill='x')
    
    tree.pack()
    
def construct_first_window():
    global window 
    
    window = tk.Tk()
    window.geometry("1200x800")
    window.title("CBB Data 2025")
    
    add_team_data_table()

def main():
    data_setup()
    construct_first_window()
    
    window.mainloop()
    

if __name__ == '__main__':
    main()