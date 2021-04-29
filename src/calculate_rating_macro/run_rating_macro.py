from src.calculate_rating_macro.create_rating_total_home_away import CreateRating
from src.calculate_rating_macro.correction_rating_minima import CorrectionRating
from src.calculate_rating_macro.calculate_rating_macro_initial import CalculateRatingFixoInitialEpoca

rating = CreateRating()
rating.run_rating()
correction = CorrectionRating()
correction.run()
rating_fixo = CalculateRatingFixoInitialEpoca()
rating_fixo.run()
