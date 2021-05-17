from src.ab_split_input_to_stats_odds.convert_odds_stats_file import SplitOddsStatsFile
from src.cons_paths import leagues

### SPLIT FILES FROM 01_RAW FOR STATS AND ODDS FILE
for league in leagues:
    split_stats_odds = SplitOddsStatsFile(league)
    if league != "GR_super_league":
        split_stats_odds.run_split(init_year=2003, end_year=2021)