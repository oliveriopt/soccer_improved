from src.ac_calculate_rating_macro.create_rating_total_home_away import CreateRating
from src.ac_calculate_rating_macro.correction_rating_minima import CorrectionRating
from src.ac_calculate_rating_macro.calculate_rating_macro_initial import CalculateRatingFixoInitialEpoca

import src.cons_paths as cons_path

#Create formula macro 1 para todas as equipas PAG 2/4 NGM equation
for league in cons_path.leagues:
    if league != "GR_super_league":
        rating_macro_1 = CreateRating(league=league)
        rating_macro_1.run_rating(init_year=2003, end_year=2021)

#Create correction in case the team is not in the season, SEE PAG 2/$ NGM equation
        correction_for_minima = CorrectionRating(league=league)
        correction_for_minima .run()

        rating_fixo = CalculateRatingFixoInitialEpoca(league=league)
        rating_fixo.run()


#STATIC RATING CALCULATED WITHIN THIS FOLDER:
type_rating = ["static_ft_total", "static_ft_home", "static_ft_away", "static_ft_total_g>15", "static_ft_total_g>25",
               "static_ft_total_g>35", "static_ft_total_g>15", "static_ft_total_g>25",
               "static_ft_total_g>35", "static_ft_home_g>15", "static_ft_home_g>25",
               "static_ft_home_g>35", "static_ft_away_g>15", "static_ft_away_g>25",
               "static_ft_away_g>35", "static_ft_total_g<15", "static_ft_total_g<25",
               "static_ft_total_g<35", "static_ft_total_g<15", "static_ft_total_g<25",
               "static_ft_total_g<35", "static_ft_home_g<15", "static_ft_home_g<25",
               "static_ft_home_g<35", "static_ft_away_g<15", "static_ft_away_g<25",
               "static_ft_away_g<35", "static_ht_total", "static_ht_home", "static_ht_away", "static_ht_total_g>15",
               "static_ht_total_g>25",
               "static_ht_total_g>35", "static_ht_total_g>15", "static_ht_total_g>25",
               "static_ht_total_g>35", "static_ht_home_g>15", "static_ht_home_g>25",
               "static_ht_home_g>35", "static_ht_away_g>15", "static_ht_away_g>25",
               "static_ht_away_g>35", "static_ht_total_g<15", "static_ht_total_g<25",
               "static_ht_total_g<35", "static_ht_total_g<15", "static_ht_total_g<25",
               "static_ht_total_g<35", "static_ht_home_g<15", "static_ht_home_g<25",
               "static_ht_home_g<35", "static_ht_away_g<15", "static_ht_away_g<25",
               "static_ht_away_g<35"]