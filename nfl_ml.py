import nflgame as nfl
from pandas import Series, DataFrame
import pandas as pd

y = range(2013,2014)
gametype = ['PRE', 'REG','POST']
home_away_iter = ['HOME','AWAY']

def raw_nfl_data_df():
    data = []
    print "%s, %s, %s, %s, %s, %s, %s, %s" % ( "season","week","REG_POST","home","home_score",
        "away", "away_score", "home_score_margin")
    for s in y:
            for k in gametype:
                    games = nfl.games(s,kind=k)
                    for g in games:
                            row = {}
                            row['season'] = g.season()
                            row['week'] = g.schedule['week']
                            row['gametype'] = k
                            row['home_team'] = g.home
                            row['score_home'] = g.score_home
                            row['away_team'] = g.away
                            row['score_away'] = g.score_away
                            row['score_home_margin'] = g.score_home-g.score_away
                            data.append(row)
##    print data
    df = DataFrame(data,columns=['season','week','gametype','home_team','score_home','away_team','score_away','score_home_margin'])
    return df

def raw_nfl_data_out():
    print "%s,%s,%s,%s,%s,%s,%s,%s" % ( "season","week","gametype","home","home_score","away","away_score","home_score_margin" )
    for s in y:
            for k in gametype:
                    games = nfl.games(s,kind=k)
                    for g in games:
                        print "%i, %i, %s, %s, %i, %s, %i, %i" % (g.season(), g.schedule['week'],k ,g.home,g.score_home,g.away,g.score_away,g.score_home-g.score_away)

def raw_nfl_data_xtab_out():
    cols = ["season","week","gametype","team","team_home_flag"
                                        ,"oppnt","oppnt_away_flag","team_score","oppnt_score","team_win_flag"]
    print "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % tuple(cols)
    # print "%s, %s, %s,%s,%s,%s,%s,%s,%s,%s" % ( "season","week","gametype","team","team_home_flag"
    #                                     ,"oppnt","oppnt_away_flag","team_score","oppnt_score","team_win_flag")
    for s in y:
            for k in gametype:
                    games = nfl.games(s,kind=k)
                    for g in games:
                        for i in home_away_iter:
                            if i == 'HOME':
                                print "%i, %i, %s, %s,%s, %s, %s, %i,%i,%s " % (g.season(), g.schedule['week'],k ,g.home,'HOME',g.away,'AWAY',g.score_home,
                                                                          g.score_away,(g.score_home > g.score_away) * 1)
                            else:
                                print "%i, %i, %s, %s,%s, %s, %s, %i,%i,%s " % (g.season(), g.schedule['week'],k ,g.away,'AWAY',g.home,'HOME',g.score_away,
                                                                          g.score_home,(g.score_away > g.score_home) * 1)

def raw_nfl_data_xtab_df():
    data = []
    teams = ['NYJ']  # [v[0] for v in nfl.teams]
    for team in teams:
        for s in y:
                for k in gametype:
                    try:
                        games = nfl.games(s,kind=k,home=team, away=team)
                        for g in games:
                            for i in home_away_iter:
                                row = {}
                                if i == 'HOME':
                                    row['eid'] = g.eid
                                    row['season'] = g.season()
                                    row['week'] = g.schedule['week']
                                    row['gametype'] = k
                                    row['team'] = g.home
                                    row['team_home_flag'] = 'HOME'
                                    row['oppnt'] = g.away
                                    row['oppnt_away_flag'] = 'AWAY'
                                    row['team_score'] = g.score_home
                                    row['oppnt_score'] = g.score_away
                                    row['team_win'] = (g.score_home > g.score_away) * 1
                                    row['team_lose'] = (g.score_home < g.score_away) * 1
                                else:
                                    row['eid'] = g.eid
                                    row['season'] = g.season()
                                    row['week'] = g.schedule['week']
                                    row['gametype'] = k
                                    row['team'] = g.away
                                    row['team_home_flag'] = 'AWAY'
                                    row['oppnt'] = g.home
                                    row['oppnt_away_flag'] = 'HOME'
                                    row['team_score'] = g.score_away
                                    row['oppnt_score'] = g.score_home
                                    row['team_win'] = (g.score_away > g.score_home) * 1
                                    row['team_lose'] = (g.score_away < g.score_home) * 1
                                data.append(row)
                    except:
                        pass
                        #  print 'no games for ', s, team, k
    df = DataFrame(data,columns=['eid', 'season','week','gametype','team','team_home_flag',
                                 'oppnt', 'oppnt_away_flag','team_score','oppnt_score','team_win','team_lose'])
    return df

def team_data(df):
    teams = [v[0] for v in nfl.teams]
    for team in teams:
        if team == 'NYJ':
            teamdf = df[df.team == team]
            teamdf = teamdf.sort_index(by=['team', 'eid'], ascending=[True, True] )
            teamdf.index = teamdf['eid']
            teamdf['total_wins'] = teamdf[teamdf['gametype'] == 'REG'].team_win.cumsum()
            teamdf['total_losses'] = teamdf[teamdf['gametype'] == 'REG'].team_lose.cumsum()
            teamdf['team_total_score'] = teamdf[teamdf['gametype'] == 'REG'].team_score.cumsum()
            teamdf['oppnt_total_score'] = teamdf[teamdf['gametype'] == 'REG'].oppnt_score.cumsum()
            teamdf['games_played'] = teamdf.total_wins + teamdf.total_losses
            teamdf['win_pct'] = teamdf.total_wins / teamdf.games_played
            teamdf['team_avg_score'] = teamdf.team_total_score / teamdf.games_played
            teamdf['oppnt_avg_score'] = teamdf.oppnt_total_score / teamdf.games_played
            print teamdf
            teamdf.to_csv('nyj2013.csv')
            # print teamdf

def main():
    df = raw_nfl_data_xtab_df()
#    df = df.reindex(index=['team', 'eid'])
    team_data(df)

if __name__ == "__main__":
    main()
