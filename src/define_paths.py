
# PATHS
def define_path(league: str) -> dict:
    path_raw = "/input/" + league + "/01_raw/"
    path_teams = "/input/" + league + "/teams/"
    path_odds_stats = "/input/" + league + "/02_odds_stats/"
    path_rating_macro = "/input/" + league + "/03_rating_macro/"
    path_rating_dynamic = "/input/" + league + "/04_rating_dynamic/"
    return {"path_raw": path_raw,
            "path_teams": path_teams,
            "path_odds_stats": path_odds_stats,
            "path_rating_macro": path_rating_macro,
            "path_rating_dynamic": path_rating_dynamic
            }
