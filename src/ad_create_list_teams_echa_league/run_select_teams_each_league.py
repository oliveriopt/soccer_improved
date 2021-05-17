from src.ad_create_list_teams_echa_league.read_teams import ReadTeams

import src.cons_paths as cons_path

# Create list of teams for all the leagues
for league in cons_path.leagues:
    if league != "GR_super_league":
        read = ReadTeams(league=league)
        read.run()
