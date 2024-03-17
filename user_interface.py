from flask import Flask, request, render_template, url_for, redirect
import pandas as pd
import sqlite3

path = ""  # Insert path here
database = path + '/database.sqlite'

conn = sqlite3.connect(database)

# Read all tables in our sqlite file
tables = pd.read_sql("""
select *
from sqlite_master
where type='table';""", conn)

# Integrate Soccer Stadium Dataset
df = pd.read_csv(f"{path}/FootballStadiums.csv")
df.to_sql("Stadium", conn, if_exists='append', index=False)
# Integrate Soccer Injury Dataset
df = pd.read_csv(f"{path}/Injury.csv")
df.to_sql("Injury", conn, if_exists='append', index=False)

# Now, check out on the tables we have
Player_Attributes = pd.read_sql("""select * from Player_Attributes;""", conn)
Player = pd.read_sql("""select * from Player;""", conn)
Match = pd.read_sql("""select * from Match;""", conn)
League = pd.read_sql("""select * from League;""", conn)
Country = pd.read_sql("""select * from Country;""", conn)
Team = pd.read_sql("""select * from Team;""", conn)
Team_Attributes = pd.read_sql("""select * from Team_Attributes;""", conn)
Stadium = pd.read_sql("""select distinct * from Stadium;""", conn)
Injury = pd.read_sql("""select distinct * from Injury;""", conn)

Player_new = pd.read_sql(""" 
select 
pa.player_api_id as Player_api_id,
p.player_name as player_name, 
strftime('%d-%m-%Y',p.birthday) as DOB,
max(p.height) as Height,
max(p.weight) as Weight,
max(pa.overall_rating) as Rating,
max(pa.potential) as Potenital,
pa.preferred_foot as Preferred_Foot,
pa.attacking_work_rate as Attacking_Work_Rate,
pa.defensive_work_rate as Defensive_Work_Rate
from player p 
join player_attributes pa on p.player_api_id=pa.player_api_id and p.player_fifa_api_id=pa.player_fifa_api_id
group by p.player_name

""", conn)

Match_new = pd.read_sql(""" 
select
a.match_api_id,
a.countryname,
a.leaguename,
ht.team_long_name as home_team_name,
ht.team_short_name as Home_Team_Short_Name,
at.team_long_name as away_team_name,
at.team_short_name as Away_Team_Short_Name,
a.season,
strftime('%d-%m-%Y',a.date) as Date,
a.stage,
a.home_team_goal,
a.away_team_goal,
case 
when a.home_team_goal - a.away_team_goal > 0 then ht.team_short_name
when a.home_team_goal - a.away_team_goal < 0 then at.team_short_name else 'Tie' end as Match_Winner
from (
select 
match_api_id,
country_team_league_table.countryname,
country_team_league_table.leaguename,
home_team_goal,
away_team_goal,
season,
date,
stage
from match m 
join team t on t.team_api_id=m.home_team_api_id or t.team_api_id=m.away_team_api_id
join (select 
country_league_table.countryname,
league_teams_table.LeagueName,
league_teams_table.Teamintheleague from (
select
l.name as LeagueName,
t.team_long_name as TeamInTheLeague
from league l 
join match m on l.country_id=m.country_id
join team t on  m.home_team_api_id=t.team_api_id
group by l.name,t.team_long_name) league_teams_table join (select c.id,
l.name as leagueName,
c.name as countryName
from league l
join country c on c.id=l.id
group by c.name,l.name) country_league_table on league_teams_table.leaguename=country_league_table.leaguename) country_team_league_table on t.team_long_name=country_team_league_table.teamintheleague
group by match_api_id ) a join (select  
match_api_id,
home_team_api_id,
team_long_name,
team_short_name
from match m
join team t on t.team_api_id=m.home_team_api_id
group by match_api_id) ht on a.match_api_id=ht.match_api_id 
join (select  
match_api_id,
away_team_api_id,
team_long_name,
team_short_name
from match m
join team t on t.team_api_id=m.away_team_api_id
group by match_api_id) at on a.match_api_id=at.match_api_id

""", conn)

Player_Ability = pd.read_sql(""" 
select 
pa.player_api_id as Player_api_id,
p.player_name as player_name,
max(pa.overall_rating) as Rating,
max(pa.potential) as Potenital,
0.7*max(pa.overall_rating)+0.3*max(pa.potential) as Weight_Ability
from player p 
join player_attributes pa on p.player_api_id=pa.player_api_id and p.player_fifa_api_id=pa.player_fifa_api_id
group by p.player_name

""", conn)
Player_Ability = Player_Ability.sort_values(['Weight_Ability'], ascending=False)
Player_Ability.index = range(1, len(Player_Ability.index) + 1)
Player_Ability.reset_index(level=0, inplace=True)
Player_Ability.rename(columns={"index": "rank"}, inplace=True)

df_match = Match[
    ['country_id', 'league_id', 'season', 'stage', 'date', 'match_api_id', 'home_team_api_id', 'away_team_api_id',
     'home_player_1',
     'home_player_2', 'home_player_3', 'home_player_4', 'home_player_5', 'home_player_6', 'home_player_7',
     'home_player_8', 'home_player_9',
     'home_player_10', 'home_player_11', 'away_player_1', 'away_player_2', 'away_player_3', 'away_player_4',
     'away_player_5', 'away_player_6',
     'away_player_7', 'away_player_8', 'away_player_9', 'away_player_10', 'away_player_11']]
df_match.isna().sum()
df_team = Team[['id', 'team_api_id', 'team_long_name']]
df_team.isna().sum()
df_team_attributes = Team_Attributes[['id', 'team_api_id', 'date']]
df_team_attributes.isna().sum()
df_player = Player[['player_api_id', 'player_name']]
df_player.isna().sum()
df_player_attributes = Player_Attributes[['player_api_id', 'date', 'overall_rating', 'potential']]
df_player_attributes.isna().sum()
df_player_attributes = df_player_attributes.dropna()
df_player_attributes.isna().sum()
# Combining DataFrames to Have Player Name and Player attributes in a Single Data Frame
df_comb_player = pd.merge(df_player, df_player_attributes, on="player_api_id")
df_comb_player['date'] = pd.to_datetime(df_comb_player['date'])
df_comb_player.head(1)

# Merge Team and Team Attribute Tables
df_comb_team = pd.merge(df_team, df_team_attributes, on="team_api_id")
df_comb_team['date'] = pd.to_datetime(df_comb_team['date'])


# Making the fuctions for usage

def end_of_year_player(df_comb_player, year):
    df_comb_player['date'] = pd.to_datetime(df_comb_player['date'])
    df_comb_player = df_comb_player[df_comb_player['date'].dt.year == year]
    df_comb_player = df_comb_player.sort_values('date').groupby('player_api_id').last()
    df_comb_player.reset_index(level=0, inplace=True)
    return df_comb_player[['player_api_id', 'player_name', 'date', 'overall_rating', 'potential']]


def end_of_year_team(df_comb_team):
    df_comb_team = df_comb_team.sort_values('date').groupby('team_api_id').last()
    df_comb_team.reset_index(level=0, inplace=True)
    return df_comb_team[['team_api_id', 'team_long_name', 'date']]


def team_to_player_home(df_match, year):
    players_list_home = ['date', 'home_team_api_id', 'home_player_1', 'home_player_2', 'home_player_3',
                         'home_player_4', 'home_player_5', 'home_player_6', 'home_player_7',
                         'home_player_8', 'home_player_9', 'home_player_10', 'home_player_11']
    df_match = df_match.loc[:, players_list_home]
    df_match['date'] = pd.to_datetime(df_match['date'])
    df_match = df_match[df_match['date'].dt.year == year]
    df_match = df_match.drop(['date'], axis=1)
    df_team_to_player = df_match.melt(['home_team_api_id']).sort_values('home_team_api_id')
    df_team_to_player = df_team_to_player[["home_team_api_id", "value"]]
    df_team_to_player.rename(columns={"value": "player_api_id", "home_team_api_id": "team_api_id"}, inplace=True)
    df_team_to_player = df_team_to_player.drop_duplicates()
    df_team_to_player = df_team_to_player.dropna()
    return df_team_to_player


def team_to_player_away(df_match, year):
    players_list_away = ['date', 'away_team_api_id', 'away_player_1', 'away_player_2', 'away_player_3', 'away_player_4',
                         'away_player_5', 'away_player_6',
                         'away_player_7', 'away_player_8', 'away_player_9', 'away_player_10', 'away_player_11']
    df_match = df_match.loc[:, players_list_away]
    df_match['date'] = pd.to_datetime(df_match['date'])
    df_match = df_match[df_match['date'].dt.year == year]
    df_match = df_match.drop(['date'], axis=1)
    df_team_to_player = df_match.melt(['away_team_api_id']).sort_values('away_team_api_id')
    df_team_to_player = df_team_to_player[["away_team_api_id", "value"]]
    df_team_to_player.rename(columns={"value": "player_api_id", "away_team_api_id": "team_api_id"}, inplace=True)
    df_team_to_player = df_team_to_player.drop_duplicates()
    df_team_to_player = df_team_to_player.dropna()
    return df_team_to_player


def team_to_player(df_match, year):
    df_2 = team_to_player_home(df_match, year)
    df_1 = team_to_player_away(df_match, year)
    df_combined = [df_1, df_2]
    result = pd.concat(df_combined)
    result = result.drop_duplicates()
    return result


def top_N_team(df_comb_team, df_comb_player, df_match, season="2015/2016"):
    year = int(season.split("/")[0])
    df_end_of_year_team = end_of_year_team(df_comb_team)
    df_end_of_year_player = end_of_year_player(df_comb_player, year)
    df_team_to_player = team_to_player(df_match, year)
    df_end_of_year_player = pd.merge(df_end_of_year_player, df_team_to_player, on="player_api_id")
    df_comb_player_team_group = df_end_of_year_player.sort_values('overall_rating').groupby('team_api_id').head(16)
    df_comb_player_team_group = df_comb_player_team_group.sort_values('overall_rating').groupby('team_api_id').sum()
    df_top = pd.merge(df_comb_player_team_group, df_end_of_year_team, on="team_api_id")
    df_top = df_top[["team_api_id", "overall_rating", "team_long_name"]]
    df_top = df_top.sort_values("overall_rating")
    # df_top = df_top[-n:]
    df_top = df_top.sort_values("overall_rating", ascending=False)
    return df_top


# Season 2015/2016
df = top_N_team(df_comb_team, df_comb_player, df_match, season="2015/2016")
df.index = range(1, len(df.index) + 1)
df.reset_index(level=0, inplace=True)
df.rename(columns={"index": "rank"}, inplace=True)
Team_Ability = df

# Build the GUI with flask object
app = Flask(__name__)

# main entrance - login page, containing user identification
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if username == "admin" and password == "12345":
            return redirect(url_for('adhome', username=request.form.get('username')))  # 如果是admin，返回admin页面
        return redirect(url_for('home', username=request.form.get('username')))

# admin page allowing offical staff to make modifications to the databases
@app.route('/adhome', methods=['GET', 'POST'])
def adhome():
    if request.method == 'GET':
        return render_template('adhome.html')
    else:
        btn = request.form.get('backToLogin')
        if btn:
            return redirect(url_for('login'))
        type = request.form.get('modification')
        return redirect(url_for('modification', type=type))

# detail modification page including "insert, update and delete"
@app.route('/modification', methods=['GET', 'POST'])
def modification():
    if request.method == 'GET':
        type = request.args.get('type')
        print(type)
        return render_template('modification.html', type=type)
    else:
        submit = request.form.get('submit')
        print(submit)
        if submit == 'Insert':
            return render_template('modification.html', type='insert',
                                   msg="Insertion succeed!")
        elif submit == 'Update':
            return render_template('modification.html', type='update',
                                   msg="Updation succeed!")
        else:
            return render_template('modification.html', type='delete',
                                   msg="Deletion succeed!")
        # input_list = ['country_id', 'league_id', 'season', 'stage', 'date', 'match_api_id', 'home_team_api_id',
        #               'away_team_api_id', 'home_team_goal', 'away_team_goal', 'goal', 'shoton', 'shotoff', 'foulcommit',
        #               'card', 'cross', 'corner', 'possession']
        # input_val = []
        # for i in input_list:
        #     input_val.append(request.form.get(f'{i}'))

# home page for normal customers to check information of a certain Player or Team, etc and check prediction.
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        username = request.args.get('username')
    else:
        info = request.form.get('query')
        btn = request.form.get('backToLogin')
        if btn:
            return redirect(url_for('login'))
        if info == 'Player_Ability' or info == 'Team_Ability':
            return redirect(url_for('pk', info=info))
        else:
            return redirect(url_for('query', info=info))

    return render_template('home.html', username=username if username is not None else '',
                           data=df.to_html(index=False) if df is not None else '')

# check PK between two players or two teams and see the approximate prediction
@app.route('/pk', methods=['GET', 'POST'])
def pk():
    if request.method == 'GET':
        info = request.args.get('info')
        return render_template('pk.html', info=info)
    else:
        submit = request.form.get('submit')
        if submit == 'Player PK':
            player_name1 = request.form.get('player_name1')
            player_name2 = request.form.get('player_name2')
            df = pd.DataFrame(Player_Ability)
            if player_name1 and player_name2:
                df1 = df.query('player_name == @player_name1')
                df2 = df.query('player_name == @player_name2')
                return render_template('pk.html', info='Player_Ability',
                                       data1=df1.to_html(index=False) if df1 is not None else '',
                                       data2=df2.to_html(index=False) if df2 is not None else '',
                                       msg="The player with higher Weight_Ability may have higher possibility to beat the other!")
            else:
                return render_template('pk.html', info='Player_Ability',
                                       error="Please input two player names to watch the prediction.")
        else:
            team_long_name1 = request.form.get('team_long_name1')
            team_long_name2 = request.form.get('team_long_name2')
            df = pd.DataFrame(Team_Ability)
            if team_long_name1 and team_long_name2:
                df1 = df.query('team_long_name == @team_long_name1')
                df2 = df.query('team_long_name == @team_long_name2')
                return render_template('pk.html', info='Team_Ability',
                                       data1=df1.to_html(index=False) if df1 is not None else '',
                                       data2=df2.to_html(index=False) if df2 is not None else '',
                                       msg="The team with higher overall rating may have higher possibility to win the match!")
            else:
                return render_template('pk.html', info='Team_Ability',
                                       error="Please input two team names to watch the prediction.")

# check more detailed information of a certain Player, team, match, etc
@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'GET':
        info = request.args.get('info')
        return render_template('query.html', info=info)
    else:
        submit = request.form.get('submit')
        if submit == 'check player':
            player_name = request.form.get('player_name')
            df = pd.DataFrame(Player_new)
            if player_name:
                df = df.query('player_name == @player_name')
            return render_template('query.html', info='Player_new',
                                   data=df.to_html(index=False) if df is not None else '')
        elif submit == 'check team':
            team_long_name = request.form.get('team_long_name')
            df = pd.DataFrame(Team)
            if team_long_name:
                df = df.query('team_long_name == @team_long_name')
            return render_template('query.html', info='Team',
                                   data=df.to_html(index=False) if df is not None else '')
        elif submit == 'check match':
            season = request.form.get('season')
            home_team_name = request.form.get('home_team_name')
            away_team_name = request.form.get('away_team_name')
            df = pd.DataFrame(Match_new)
            if season or home_team_name or away_team_name:
                df = df.query('season == @season and home_team_name == @home_team_name and away_team_name == '
                              '@away_team_name')
            return render_template('query.html', info='Match_new',
                                   data=df.to_html(index=False) if df is not None else '')
        elif submit == 'check stadium':
            HomeTeams = request.form.get('HomeTeams')
            df = pd.DataFrame(Stadium)
            if HomeTeams:
                df = df.query('HomeTeams == @HomeTeams')
            return render_template('query.html', info='Stadium',
                                   data=df.to_html(index=False) if df is not None else '')
        else:
            name = request.form.get('name')
            df = pd.DataFrame(Injury)
            if name:
                df = df.query('name == @name')
            return render_template('query.html', info='Injury',
                                   data=df.to_html(index=False) if df is not None else '')

# host and port can be changed as you like
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
