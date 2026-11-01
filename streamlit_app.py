import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime

st.set_page_config(page_title="Metaphysical NFL Engine", layout="wide")

st.title("🏈 Metaphysical NFL Analytics Engine")
st.caption("32-Franchise & Personnel Registry, Multi-Entity Date Comparison, & Multi-Game Trend Visualizer")

# ==============================================================================
# 1. CORE NUMEROLOGY & VIBRATIONAL ENGINE (PRESERVES MASTER NUMBERS)
# ==============================================================================
def reduce_digits(n: int, preserve_masters: bool = True) -> int:
    if n is None:
        return 0
    n = abs(int(n))
    if preserve_masters and n in [11, 22, 33]:
        return n
    while n > 9:
        if preserve_masters and n in [11, 22, 33]:
            return n
        n = sum(int(d) for d in str(n))
    return n

def compute_life_path(d: datetime.date, preserve_masters: bool = True) -> int:
    m = reduce_digits(d.month, preserve_masters=False)
    day_red = reduce_digits(d.day, preserve_masters=preserve_masters)
    y_red = reduce_digits(d.year, preserve_masters=False)
    return reduce_digits(m + day_red + y_red, preserve_masters=preserve_masters)

# ==============================================================================
# 2. CHINESE ASTROLOGY & ELEMENTAL AFFINITY ENGINE
# ==============================================================================
CHINESE_ZODIAC = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
CHINESE_ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

SAN_HE_TRINES = {
    "Rat": ["Dragon", "Monkey"], "Dragon": ["Rat", "Monkey"], "Monkey": ["Rat", "Dragon"],
    "Ox": ["Snake", "Rooster"], "Snake": ["Ox", "Rooster"], "Rooster": ["Ox", "Snake"],
    "Tiger": ["Horse", "Dog"], "Horse": ["Tiger", "Dog"], "Dog": ["Tiger", "Horse"],
    "Rabbit": ["Goat", "Pig"], "Goat": ["Rabbit", "Pig"], "Pig": ["Rabbit", "Goat"]
}

LIU_HE_PAIRS = {
    "Rat": "Ox", "Ox": "Rat", "Tiger": "Pig", "Pig": "Tiger",
    "Rabbit": "Dog", "Dog": "Rabbit", "Dragon": "Rooster", "Rooster": "Dragon",
    "Snake": "Monkey", "Monkey": "Snake", "Horse": "Goat", "Goat": "Horse"
}

CHONG_OPPOSITIONS = {
    "Rat": "Horse", "Horse": "Rat", "Ox": "Goat", "Goat": "Ox",
    "Tiger": "Monkey", "Monkey": "Tiger", "Rabbit": "Rooster", "Rooster": "Rabbit",
    "Dragon": "Dog", "Dog": "Dragon", "Snake": "Pig", "Pig": "Snake"
}

XING_PUNISHMENTS = {
    "Tiger": ["Snake", "Monkey"], "Snake": ["Tiger", "Monkey"], "Monkey": ["Tiger", "Snake"],
    "Ox": ["Goat", "Dog"], "Goat": ["Ox", "Dog"], "Dog": ["Ox", "Goat"],
    "Rat": ["Rabbit"], "Rabbit": ["Rat"],
    "Dragon": ["Dragon"], "Horse": ["Horse"], "Rooster": ["Rooster"], "Pig": ["Pig"]
}

def get_chinese_profile(year: int):
    z_idx = (year - 4) % 12
    e_idx = ((year - 4) // 2) % 5
    polarity = "Yang" if (year % 2 == 0) else "Yin"
    return CHINESE_ZODIAC[z_idx], CHINESE_ELEMENTS[e_idx], polarity

def evaluate_affinity(natal_animal: str, game_year_animal: str) -> str:
    if game_year_animal in SAN_HE_TRINES.get(natal_animal, []):
        return "✨ San He (Trine Harmony)"
    if LIU_HE_PAIRS.get(natal_animal) == game_year_animal:
        return "🤝 Liu He (Secret Friend)"
    if CHONG_OPPOSITIONS.get(natal_animal) == game_year_animal:
        return "⚔️ Chong (Direct Clash)"
    if game_year_animal in XING_PUNISHMENTS.get(natal_animal, []):
        return "⚠️ Xing (Punishment / Friction)"
    return "Neutral Alignment"

# ==============================================================================
# 3. WESTERN ASTROLOGY (ALL 10 BODIES)
# ==============================================================================
SIGNS_ORDER = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANET_PERIODS = {
    "Sun": 365.256, "Moon": 27.321, "Mercury": 87.969, "Venus": 224.701,
    "Mars": 686.980, "Jupiter": 4332.589, "Saturn": 10759.22,
    "Uranus": 30685.4, "Neptune": 60189.0, "Pluto": 90560.0
}

J2000_LONGITUDES = {
    "Sun": 280.46, "Moon": 218.32, "Mercury": 252.25, "Venus": 181.98,
    "Mars": 355.43, "Jupiter": 34.35, "Saturn": 50.44, "Uranus": 314.05,
    "Neptune": 303.48, "Pluto": 251.52
}

def get_planet_position(planet: str, d: datetime.date):
    epoch = datetime.date(2000, 1, 1)
    days = (d - epoch).days
    rate = 360.0 / PLANET_PERIODS[planet]
    deg = (J2000_LONGITUDES[planet] + (days * rate)) % 360.0
    sign_idx = int(deg // 30)
    sign_name = SIGNS_ORDER[sign_idx]
    deg_in_sign = deg % 30.0
    return deg, sign_name, deg_in_sign

def get_aspect_name(deg1: float, deg2: float) -> str:
    diff = abs(deg1 - deg2) % 360
    if diff > 180:
        diff = 360 - diff
    if diff <= 8.0:
        return "Conj (0°)"
    elif abs(diff - 60.0) <= 5.0:
        return "Sext (60°)"
    elif abs(diff - 90.0) <= 7.0:
        return "Square (90°)"
    elif abs(diff - 120.0) <= 8.0:
        return "Trine (120°)"
    elif abs(diff - 180.0) <= 8.0:
        return "Opp (180°)"
    return ""

def calculate_detailed_transit(t_planet: str, n_planet: str, target_date: datetime.date, natal_date: datetime.date) -> str:
    g_deg, g_sign, _ = get_planet_position(t_planet, target_date)
    n_deg, n_sign, _ = get_planet_position(n_planet, natal_date)
    aspect = get_aspect_name(g_deg, n_deg)
    if aspect:
        return f"{t_planet} in {g_sign} {aspect} {n_planet} in {n_sign}"
    return "—"

# ==============================================================================
# 4. VERIFIED HISTORICAL GAME LOG ARCHIVES
# ==============================================================================
BEARS_2026_SLATE = [
    {"Week": 1, "Date": "2026-09-13", "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "@", "Venue": "Bank of America Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "59 - 37", "Result": "W", "Diff": 22, "TotalOffYds": 552, "FirstDowns": 26, "TurnoverDiff": "+2", "ThirdDownEff": "10/14 (71.4%)"},
    {"Week": 2, "Date": "2026-09-20", "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 9", "Result": "L", "Diff": -6, "TotalOffYds": 248, "FirstDowns": 14, "TurnoverDiff": "-1", "ThirdDownEff": "3/13 (23.1%)"},
    {"Week": 3, "Date": "2026-09-28", "DayOfWeek": "Mon", "Opp": "PHI", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "MNF", "Score": "27 - 7", "Result": "W", "Diff": 20, "TotalOffYds": 374, "FirstDowns": 20, "TurnoverDiff": "+3", "ThirdDownEff": "6/14 (42.9%)"},
    {"Week": 4, "Date": "2026-10-04", "DayOfWeek": "Sun", "Opp": "NYJ", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "23 - 12", "Result": "W", "Diff": 11, "TotalOffYds": 492, "FirstDowns": 24, "TurnoverDiff": "+1", "ThirdDownEff": "7/15 (46.7%)"},
    {"Week": 5, "Date": "2026-10-11", "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "@", "Venue": "Lambeau Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "7 - 31", "Result": "L", "Diff": -24, "TotalOffYds": 238, "FirstDowns": 12, "TurnoverDiff": "-2", "ThirdDownEff": "2/11 (18.2%)"},
    {"Week": 6, "Date": "2026-10-18", "DayOfWeek": "Sun", "Opp": "ATL", "HomeAway": "@", "Venue": "Mercedes-Benz Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "31 - 23", "Result": "W", "Diff": 8, "TotalOffYds": 421, "FirstDowns": 23, "TurnoverDiff": "+1", "ThirdDownEff": "8/14 (57.1%)"},
    {"Week": 7, "Date": "2026-10-22", "DayOfWeek": "Thu", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "TNF", "Score": "30 - 24", "Result": "W", "Diff": 6, "TotalOffYds": 405, "FirstDowns": 22, "TurnoverDiff": "0", "ThirdDownEff": "6/13 (46.2%)"},
    {"Week": 8, "Date": "2026-11-02", "DayOfWeek": "Mon", "Opp": "SEA", "HomeAway": "@", "Venue": "Lumen Field", "Surface": "Turf", "GameTime": "MNF", "Score": "Pending", "Result": "Pending", "Diff": 0, "TotalOffYds": 0, "FirstDowns": 0, "TurnoverDiff": "0", "ThirdDownEff": "Pending"},
    {"Week": 9, "Date": "2026-11-08", "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "SNF", "Score": "Pending", "Result": "Pending", "Diff": 0, "TotalOffYds": 0, "FirstDowns": 0, "TurnoverDiff": "0", "ThirdDownEff": "Pending"}
]

CALEB_2026_SLATE = [
    {"Week": 1, "Date": "2026-09-13", "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "@", "Venue": "Bank of America Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "59 - 37", "Result": "W", "Diff": 22, "CMP": 21, "ATT": 29, "CMP%": 72.4, "Pass Yds": 269, "Pass TD": 2, "Y/A": 9.3, "INT": 0, "SCK": 2, "Sack Yds Lost": 14, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 124.1, "QBR": 88.4, "Rush Att": 10, "Rush Yds": 65, "YPC": 6.5, "Rush TD": 2},
    {"Week": 2, "Date": "2026-09-20", "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 9", "Result": "L", "Diff": -6, "CMP": 15, "ATT": 26, "CMP%": 57.7, "Pass Yds": 138, "Pass TD": 0, "Y/A": 5.3, "INT": 1, "SCK": 3, "Sack Yds Lost": 21, "Fumbles": 1, "Fumbles Lost": 0, "Passer Rating": 56.2, "QBR": 38.1, "Rush Att": 5, "Rush Yds": 42, "YPC": 8.4, "Rush TD": 0},
    {"Week": 6, "Date": "2026-10-18", "DayOfWeek": "Sun", "Opp": "ATL", "HomeAway": "@", "Venue": "Mercedes-Benz Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "31 - 23", "Result": "W", "Diff": 8, "CMP": 30, "ATT": 36, "CMP%": 83.3, "Pass Yds": 305, "Pass TD": 1, "Y/A": 8.5, "INT": 0, "SCK": 4, "Sack Yds Lost": 26, "Fumbles": 1, "Fumbles Lost": 0, "Passer Rating": 111.2, "QBR": 79.5, "Rush Att": 4, "Rush Yds": 3, "YPC": 0.8, "Rush TD": 0},
    {"Week": 7, "Date": "2026-10-22", "DayOfWeek": "Thu", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "TNF", "Score": "30 - 24", "Result": "W", "Diff": 6, "CMP": 22, "ATT": 33, "CMP%": 66.7, "Pass Yds": 308, "Pass TD": 2, "Y/A": 9.3, "INT": 0, "SCK": 3, "Sack Yds Lost": 19, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 116.7, "QBR": 84.2, "Rush Att": 5, "Rush Yds": 18, "YPC": 3.6, "Rush TD": 0},
    {"Week": 8, "Date": "2026-11-02", "DayOfWeek": "Mon", "Opp": "SEA", "HomeAway": "@", "Venue": "Lumen Field", "Surface": "Turf", "GameTime": "MNF", "Score": "Pending", "Result": "Pending", "Diff": 0, "CMP": 0, "ATT": 0, "CMP%": 0.0, "Pass Yds": 0, "Pass TD": 0, "Y/A": 0.0, "INT": 0, "SCK": 0, "Sack Yds Lost": 0, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 0.0, "QBR": 0.0, "Rush Att": 0, "Rush Yds": 0, "YPC": 0.0, "Rush TD": 0},
    {"Week": 9, "Date": "2026-11-08", "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "SNF", "Score": "Pending", "Result": "Pending", "Diff": 0, "CMP": 0, "ATT": 0, "CMP%": 0.0, "Pass Yds": 0, "Pass TD": 0, "Y/A": 0.0, "INT": 0, "SCK": 0, "Sack Yds Lost": 0, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 0.0, "QBR": 0.0, "Rush Att": 0, "Rush Yds": 0, "YPC": 0.0, "Rush TD": 0}
]

CALEB_2024_SLATE = [
    {"Week": 1, "Date": "2024-09-08", "DayOfWeek": "Sun", "Opp": "TEN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "24 - 17", "Result": "W", "Diff": 7, "CMP": 14, "ATT": 29, "CMP%": 48.3, "Pass Yds": 93, "Pass TD": 0, "Y/A": 3.2, "INT": 0, "SCK": 2, "Sack Yds Lost": 29, "Fumbles": 1, "Fumbles Lost": 0, "Passer Rating": 55.7, "QBR": 32.4, "Rush Att": 5, "Rush Yds": 15, "YPC": 3.0, "Rush TD": 0},
    {"Week": 2, "Date": "2024-09-15", "DayOfWeek": "Sun", "Opp": "HOU", "HomeAway": "@", "Venue": "NRG Stadium", "Surface": "Turf", "GameTime": "8:20 PM", "Score": "13 - 19", "Result": "L", "Diff": -6, "CMP": 23, "ATT": 37, "CMP%": 62.2, "Pass Yds": 174, "Pass TD": 0, "Y/A": 4.7, "INT": 2, "SCK": 7, "Sack Yds Lost": 40, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 51.0, "QBR": 24.1, "Rush Att": 5, "Rush Yds": 44, "YPC": 8.8, "Rush TD": 0},
    {"Week": 3, "Date": "2024-09-22", "DayOfWeek": "Sun", "Opp": "IND", "HomeAway": "@", "Venue": "Lucas Oil Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "16 - 21", "Result": "L", "Diff": -5, "CMP": 33, "ATT": 52, "CMP%": 63.5, "Pass Yds": 363, "Pass TD": 2, "Y/A": 7.0, "INT": 2, "SCK": 4, "Sack Yds Lost": 31, "Fumbles": 1, "Fumbles Lost": 1, "Passer Rating": 80.8, "QBR": 48.2, "Rush Att": 1, "Rush Yds": 8, "YPC": 8.0, "Rush TD": 0},
    {"Week": 4, "Date": "2024-09-29", "DayOfWeek": "Sun", "Opp": "LAR", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "24 - 18", "Result": "W", "Diff": 6, "CMP": 17, "ATT": 23, "CMP%": 73.9, "Pass Yds": 157, "Pass TD": 1, "Y/A": 6.8, "INT": 0, "SCK": 3, "Sack Yds Lost": 24, "Fumbles": 1, "Fumbles Lost": 0, "Passer Rating": 106.6, "QBR": 70.3, "Rush Att": 5, "Rush Yds": 12, "YPC": 2.4, "Rush TD": 0},
    {"Week": 5, "Date": "2024-10-06", "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "36 - 10", "Result": "W", "Diff": 26, "CMP": 20, "ATT": 29, "CMP%": 69.0, "Pass Yds": 304, "Pass TD": 2, "Y/A": 10.5, "INT": 0, "SCK": 1, "Sack Yds Lost": 8, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 126.2, "QBR": 84.1, "Rush Att": 5, "Rush Yds": 34, "YPC": 6.8, "Rush TD": 0},
    {"Week": 6, "Date": "2024-10-13", "DayOfWeek": "Sun", "Opp": "JAX", "HomeAway": "vs", "Venue": "Tottenham Hotspur Stadium", "Surface": "Turf", "GameTime": "9:30 AM", "Score": "35 - 16", "Result": "W", "Diff": 19, "CMP": 23, "ATT": 29, "CMP%": 79.3, "Pass Yds": 226, "Pass TD": 4, "Y/A": 7.8, "INT": 1, "SCK": 3, "Sack Yds Lost": 5, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 124.4, "QBR": 82.5, "Rush Att": 4, "Rush Yds": 56, "YPC": 14.0, "Rush TD": 0},
    {"Week": 8, "Date": "2024-10-27", "DayOfWeek": "Sun", "Opp": "WAS", "HomeAway": "@", "Venue": "Northwest Stadium", "Surface": "Grass", "GameTime": "4:25 PM", "Score": "15 - 18", "Result": "L", "Diff": -3, "CMP": 10, "ATT": 24, "CMP%": 41.7, "Pass Yds": 131, "Pass TD": 0, "Y/A": 5.5, "INT": 0, "SCK": 3, "Sack Yds Lost": 26, "Fumbles": 1, "Fumbles Lost": 1, "Passer Rating": 59.6, "QBR": 35.8, "Rush Att": 9, "Rush Yds": 47, "YPC": 5.2, "Rush TD": 0},
    {"Week": 9, "Date": "2024-11-03", "DayOfWeek": "Sun", "Opp": "ARI", "HomeAway": "@", "Venue": "State Farm Stadium", "Surface": "Grass", "GameTime": "4:05 PM", "Score": "9 - 29", "Result": "L", "Diff": -20, "CMP": 22, "ATT": 41, "CMP%": 53.7, "Pass Yds": 217, "Pass TD": 0, "Y/A": 5.3, "INT": 0, "SCK": 6, "Sack Yds Lost": 45, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 68.8, "QBR": 41.2, "Rush Att": 4, "Rush Yds": 5, "YPC": 1.2, "Rush TD": 0},
    {"Week": 10, "Date": "2024-11-10", "DayOfWeek": "Sun", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 19", "Result": "L", "Diff": -16, "CMP": 16, "ATT": 30, "CMP%": 53.3, "Pass Yds": 120, "Pass TD": 0, "Y/A": 4.0, "INT": 0, "SCK": 9, "Sack Yds Lost": 51, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 63.2, "QBR": 28.6, "Rush Att": 2, "Rush Yds": 15, "YPC": 7.5, "Rush TD": 0},
    {"Week": 11, "Date": "2024-11-17", "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "19 - 20", "Result": "L", "Diff": -1, "CMP": 23, "ATT": 31, "CMP%": 74.2, "Pass Yds": 231, "Pass TD": 0, "Y/A": 7.4, "INT": 0, "SCK": 3, "Sack Yds Lost": 19, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 95.0, "QBR": 68.4, "Rush Att": 9, "Rush Yds": 70, "YPC": 7.8, "Rush TD": 0},
    {"Week": 12, "Date": "2024-11-24", "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "27 - 30", "Result": "L", "Diff": -3, "CMP": 32, "ATT": 47, "CMP%": 68.1, "Pass Yds": 340, "Pass TD": 2, "Y/A": 7.2, "INT": 0, "SCK": 3, "Sack Yds Lost": 20, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 103.2, "QBR": 74.5, "Rush Att": 6, "Rush Yds": 33, "YPC": 5.5, "Rush TD": 0},
    {"Week": 13, "Date": "2024-11-28", "DayOfWeek": "Thu", "Opp": "DET", "HomeAway": "@", "Venue": "Ford Field", "Surface": "Turf", "GameTime": "12:30 PM", "Score": "20 - 23", "Result": "L", "Diff": -3, "CMP": 20, "ATT": 39, "CMP%": 51.3, "Pass Yds": 256, "Pass TD": 3, "Y/A": 6.6, "INT": 0, "SCK": 5, "Sack Yds Lost": 33, "Fumbles": 0, "Fumbles Lost": 0, "Passer Rating": 97.8, "QBR": 66.8, "Rush Att": 4, "Rush Yds": 39, "YPC": 9.8, "Rush TD": 0},
    {"Week": 14, "Date": "2024-12-08", "DayOfWeek": "Sun", "Opp": "SF", "HomeAway": "@", "Venue": "Levi's Stadium", "Surface": "Grass", "GameTime": "4:25 PM", "Score": "13 - 38", "Result": "L", "Diff": -25, "CMP": 17, "ATT": 23, "CMP%": 73.9, "Pass Yds": 134, "Pass TD": 2, "Y/A": 5.8, "INT": 0, "SCK": 7, "Sack Yds Lost": 46, "Fumbles": 1, "Fumbles Lost": 1, "Passer Rating": 116.9, "QBR": 55.4, "Rush Att": 4, "Rush Yds": 27, "YPC": 6.8, "Rush TD": 0},
    {"Week": 15, "Date": "2024-12-16", "DayOfWeek": "Mon", "Opp": "MIN", "HomeAway": "@", "Venue": "U.S. Bank Stadium", "Surface": "Turf", "GameTime": "8:00 PM", "Score": "12 - 30", "Result": "L", "Diff": -18, "CMP": 18, "ATT": 31, "CMP%": 58.1, "Pass Yds": 191, "Pass TD": 1, "Y/A": 6.2, "INT": 0, "SCK": 2, "Sack Yds Lost": 25, "Fumbles": 1, "Fumbles Lost": 1, "Passer Rating": 86.9, "QBR": 44.2, "Rush Att": 4, "Rush Yds": 3, "YPC": 0.8, "Rush TD": 0},
    {"Week": 16, "Date": "2024-12-22", "DayOfWeek": "Sun", "Opp": "DET", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "17 - 34", "Result": "L", "Diff": -17, "CMP": 26, "ATT": 40, "CMP%": 65.0, "Pass Yds": 334, "Pass TD": 2, "Y/A": 8.4, "INT": 0, "SCK": 2, "Sack Yds Lost": 11, "Fumbles": 2, "Fumbles Lost": 1, "Passer Rating": 107.7, "QBR": 72.1, "Rush Att": 6, "Rush Yds": 34, "YPC": 5.7, "Rush TD": 0},
    {"Week": 17, "Date": "2024-12-26", "DayOfWeek": "Thu", "Opp": "SEA", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "8:15 PM", "Score": "3 - 6", "Result": "L", "Diff": -3, "CMP": 16, "ATT": 28, "CMP%": 57.1, "Pass Yds": 122, "Pass TD": 0, "Y/A": 4.4, "INT": 1, "SCK": 7, "Sack Yds Lost": 46, "Fumbles": 1, "Fumbles Lost": 0, "Passer Rating": 53.0, "QBR": 30.5, "Rush Att": 5, "Rush Yds": 37, "YPC": 7.4, "Rush TD": 0},
    {"Week": 18, "Date": "2025-01-05", "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "@", "Venue": "Lambeau Field", "Surface": "Grass", "GameTime": "4:25 PM", "Score": "24 - 22", "Result": "W", "Diff": 2, "CMP": 21, "ATT": 29, "CMP%": 72.4, "Pass Yds": 148, "Pass TD": 1, "Y/A": 5.1, "INT": 0, "SCK": 1, "Sack Yds Lost": 7, "Fumbles": 1, "Fumbles Lost": 0, "Passer Rating": 95.2, "QBR": 62.4, "Rush Att": 3, "Rush Yds": 10, "YPC": 3.3, "Rush TD": 0}
]

# ==============================================================================
# 5. ALL 32 FRANCHISES & KEY PERSONNEL (STRICTLY HARDCODED IN-MEMORY DICTIONARY)
# ==============================================================================
COMPLETE_32_FRANCHISES = {
    "Arizona Cardinals (Franchise)": {"category": "FRANCHISE", "name": "Arizona Cardinals", "pos": "Franchise", "jersey": "—", "birth_date": "1898-01-01", "team": "ARI", "exp": "Established 1898", "seasons": {}},
    "Atlanta Falcons (Franchise)": {"category": "FRANCHISE", "name": "Atlanta Falcons", "pos": "Franchise", "jersey": "—", "birth_date": "1965-06-30", "team": "ATL", "exp": "Awarded June 30, 1965", "seasons": {}},
    "Baltimore Ravens (Franchise)": {"category": "FRANCHISE", "name": "Baltimore Ravens", "pos": "Franchise", "jersey": "—", "birth_date": "1996-02-09", "team": "BAL", "exp": "Established Feb 9, 1996", "seasons": {}},
    "Buffalo Bills (Franchise)": {"category": "FRANCHISE", "name": "Buffalo Bills", "pos": "Franchise", "jersey": "—", "birth_date": "1959-10-28", "team": "BUF", "exp": "Founded Oct 28, 1959", "seasons": {}},
    "Carolina Panthers (Franchise)": {"category": "FRANCHISE", "name": "Carolina Panthers", "pos": "Franchise", "jersey": "—", "birth_date": "1993-10-26", "team": "CAR", "exp": "Awarded Oct 26, 1993", "seasons": {}},
    "Chicago Bears (Franchise)": {"category": "FRANCHISE", "name": "Chicago Bears", "pos": "Franchise", "jersey": "—", "birth_date": "1920-09-17", "team": "CHI", "exp": "Charter APFA Sept 17, 1920", "seasons": {"2026": BEARS_2026_SLATE}},
    "Cincinnati Bengals (Franchise)": {"category": "FRANCHISE", "name": "Cincinnati Bengals", "pos": "Franchise", "jersey": "—", "birth_date": "1967-05-23", "team": "CIN", "exp": "Founded May 23, 1967", "seasons": {}},
    "Cleveland Browns (Franchise)": {"category": "FRANCHISE", "name": "Cleveland Browns", "pos": "Franchise", "jersey": "—", "birth_date": "1944-06-04", "team": "CLE", "exp": "Founded June 4, 1944", "seasons": {}},
    "Dallas Cowboys (Franchise)": {"category": "FRANCHISE", "name": "Dallas Cowboys", "pos": "Franchise", "jersey": "—", "birth_date": "1960-01-28", "team": "DAL", "exp": "Awarded Jan 28, 1960", "seasons": {}},
    "Denver Broncos (Franchise)": {"category": "FRANCHISE", "name": "Denver Broncos", "pos": "Franchise", "jersey": "—", "birth_date": "1959-08-14", "team": "DEN", "exp": "Charter AFL Aug 14, 1959", "seasons": {}},
    "Detroit Lions (Franchise)": {"category": "FRANCHISE", "name": "Detroit Lions", "pos": "Franchise", "jersey": "—", "birth_date": "1930-07-12", "team": "DET", "exp": "Portsmouth Spartans July 12, 1930", "seasons": {}},
    "Green Bay Packers (Franchise)": {"category": "FRANCHISE", "name": "Green Bay Packers", "pos": "Franchise", "jersey": "—", "birth_date": "1919-08-11", "team": "GB", "exp": "Founded Aug 11, 1919", "seasons": {}},
    "Houston Texans (Franchise)": {"category": "FRANCHISE", "name": "Houston Texans", "pos": "Franchise", "jersey": "—", "birth_date": "1999-10-06", "team": "HOU", "exp": "Awarded Oct 6, 1999", "seasons": {}},
    "Indianapolis Colts (Franchise)": {"category": "FRANCHISE", "name": "Indianapolis Colts", "pos": "Franchise", "jersey": "—", "birth_date": "1953-01-23", "team": "IND", "exp": "Baltimore Colts Jan 23, 1953", "seasons": {}},
    "Jacksonville Jaguars (Franchise)": {"category": "FRANCHISE", "name": "Jacksonville Jaguars", "pos": "Franchise", "jersey": "—", "birth_date": "1993-11-30", "team": "JAX", "exp": "Awarded Nov 30, 1993", "seasons": {}},
    "Kansas City Chiefs (Franchise)": {"category": "FRANCHISE", "name": "Kansas City Chiefs", "pos": "Franchise", "jersey": "—", "birth_date": "1959-08-14", "team": "KC", "exp": "Dallas Texans Aug 14, 1959", "seasons": {}},
    "Las Vegas Raiders (Franchise)": {"category": "FRANCHISE", "name": "Las Vegas Raiders", "pos": "Franchise", "jersey": "—", "birth_date": "1960-01-30", "team": "LV", "exp": "Oakland Raiders Jan 30, 1960", "seasons": {}},
    "Los Angeles Chargers (Franchise)": {"category": "FRANCHISE", "name": "Los Angeles Chargers", "pos": "Franchise", "jersey": "—", "birth_date": "1959-08-14", "team": "LAC", "exp": "Charter AFL Aug 14, 1959", "seasons": {}},
    "Los Angeles Rams (Franchise)": {"category": "FRANCHISE", "name": "Los Angeles Rams", "pos": "Franchise", "jersey": "—", "birth_date": "1936-02-13", "team": "LAR", "exp": "Cleveland Rams Feb 13, 1936", "seasons": {}},
    "Miami Dolphins (Franchise)": {"category": "FRANCHISE", "name": "Miami Dolphins", "pos": "Franchise", "jersey": "—", "birth_date": "1965-08-16", "team": "MIA", "exp": "Awarded Aug 16, 1965", "seasons": {}},
    "Minnesota Vikings (Franchise)": {"category": "FRANCHISE", "name": "Minnesota Vikings", "pos": "Franchise", "jersey": "—", "birth_date": "1960-01-28", "team": "MIN", "exp": "Awarded Jan 28, 1960", "seasons": {}},
    "New England Patriots (Franchise)": {"category": "FRANCHISE", "name": "New England Patriots", "pos": "Franchise", "jersey": "—", "birth_date": "1959-11-16", "team": "NE", "exp": "Boston Patriots Nov 16, 1959", "seasons": {}},
    "New Orleans Saints (Franchise)": {"category": "FRANCHISE", "name": "New Orleans Saints", "pos": "Franchise", "jersey": "—", "birth_date": "1966-11-01", "team": "NO", "exp": "Awarded Nov 1, 1966", "seasons": {}},
    "New York Giants (Franchise)": {"category": "FRANCHISE", "name": "New York Giants", "pos": "Franchise", "jersey": "—", "birth_date": "1925-08-01", "team": "NYG", "exp": "Founded Aug 1, 1925", "seasons": {}},
    "New York Jets (Franchise)": {"category": "FRANCHISE", "name": "New York Jets", "pos": "Franchise", "jersey": "—", "birth_date": "1959-08-14", "team": "NYJ", "exp": "Titans of New York Aug 14, 1959", "seasons": {}},
    "Philadelphia Eagles (Franchise)": {"category": "FRANCHISE", "name": "Philadelphia Eagles", "pos": "Franchise", "jersey": "—", "birth_date": "1933-07-08", "team": "PHI", "exp": "Granted July 8, 1933", "seasons": {}},
    "Pittsburgh Steelers (Franchise)": {"category": "FRANCHISE", "name": "Pittsburgh Steelers", "pos": "Franchise", "jersey": "—", "birth_date": "1933-07-08", "team": "PIT", "exp": "Pittsburgh Pirates July 8, 1933", "seasons": {}},
    "San Francisco 49ers (Franchise)": {"category": "FRANCHISE", "name": "San Francisco 49ers", "pos": "Franchise", "jersey": "—", "birth_date": "1944-06-04", "team": "SF", "exp": "Charter AAFC June 4, 1944", "seasons": {}},
    "Seattle Seahawks (Franchise)": {"category": "FRANCHISE", "name": "Seattle Seahawks", "pos": "Franchise", "jersey": "—", "birth_date": "1974-06-04", "team": "SEA", "exp": "Awarded June 4, 1974", "seasons": {}},
    "Tampa Bay Buccaneers (Franchise)": {"category": "FRANCHISE", "name": "Tampa Bay Buccaneers", "pos": "Franchise", "jersey": "—", "birth_date": "1974-04-24", "team": "TB", "exp": "Awarded April 24, 1974", "seasons": {}},
    "Tennessee Titans (Franchise)": {"category": "FRANCHISE", "name": "Tennessee Titans", "pos": "Franchise", "jersey": "—", "birth_date": "1959-08-14", "team": "TEN", "exp": "Houston Oilers Aug 14, 1959", "seasons": {}},
    "Washington Commanders (Franchise)": {"category": "FRANCHISE", "name": "Washington Commanders", "pos": "Franchise", "jersey": "—", "birth_date": "1932-07-09", "team": "WAS", "exp": "Boston Braves July 9, 1932", "seasons": {}}
}

KEY_PERSONNEL = {
    "Caleb Williams (QB - CHI)": {"category": "QB", "name": "Caleb Williams", "pos": "QB", "jersey": "#18", "birth_date": "2001-11-18", "team": "CHI", "exp": "Draft 2024 (1st Overall)", "seasons": {"2026": CALEB_2026_SLATE, "2024": CALEB_2024_SLATE}},
    "Patrick Mahomes (QB - KC)": {"category": "QB", "name": "Patrick Mahomes", "pos": "QB", "jersey": "#15", "birth_date": "1995-09-17", "team": "KC", "exp": "Draft 2017 (10th Overall)", "seasons": {}},
    "Josh Allen (QB - BUF)": {"category": "QB", "name": "Josh Allen", "pos": "QB", "jersey": "#17", "birth_date": "1996-05-21", "team": "BUF", "exp": "Draft 2018 (7th Overall)", "seasons": {}},
    "Lamar Jackson (QB - BAL)": {"category": "QB", "name": "Lamar Jackson", "pos": "QB", "jersey": "#8", "birth_date": "1997-01-07", "team": "BAL", "exp": "Draft 2018 (32nd Overall)", "seasons": {}},
    "C.J. Stroud (QB - HOU)": {"category": "QB", "name": "C.J. Stroud", "pos": "QB", "jersey": "#7", "birth_date": "2001-10-03", "team": "HOU", "exp": "Draft 2023 (2nd Overall)", "seasons": {}},
    "Jayden Daniels (QB - WAS)": {"category": "QB", "name": "Jayden Daniels", "pos": "QB", "jersey": "#5", "birth_date": "2000-12-18", "team": "WAS", "exp": "Draft 2024 (2nd Overall)", "seasons": {}},
    "Andy Reid (Coach - KC)": {"category": "COACH", "name": "Andy Reid", "pos": "Coach", "jersey": "HC", "birth_date": "1958-03-19", "team": "KC", "exp": "Head Coach", "seasons": {}},
    "Matt Eberflus (Coach - CHI)": {"category": "COACH", "name": "Matt Eberflus", "pos": "Coach", "jersey": "HC", "birth_date": "1970-05-17", "team": "CHI", "exp": "Head Coach (2022-2024)", "seasons": {}},
    "Mike Ditka (Coach - CHI)": {"category": "COACH", "name": "Mike Ditka", "pos": "Coach", "jersey": "HC", "birth_date": "1939-10-18", "team": "CHI", "exp": "Hall of Fame Coach", "seasons": {}},
    "George Halas (Owner/Founder - CHI)": {"category": "OWNER", "name": "George Halas", "pos": "Owner", "jersey": "Papa Bear", "birth_date": "1895-02-02", "team": "CHI", "exp": "Founder & 6x Champion", "seasons": {}},
    "Walter Payton (RB - CHI)": {"category": "SKILL", "name": "Walter Payton", "pos": "RB", "jersey": "#34", "birth_date": "1954-07-25", "team": "CHI", "exp": "Hall of Fame Legend", "seasons": {}}
}

MASTER_DB = {**COMPLETE_32_FRANCHISES, **KEY_PERSONNEL}

if "db_storage" not in st.session_state:
    st.session_state["db_storage"] = MASTER_DB

db = st.session_state["db_storage"]
db_keys = sorted(list(db.keys()))

# ==============================================================================
# SECTION 1: SEARCH, LOOKUP & METAPHYSICAL PROFILE
# ==============================================================================
st.subheader("1. Entity Search & Metaphysical Baseline")

top_col1, top_col2 = st.columns([3, 1])

default_idx = db_keys.index("Caleb Williams (QB - CHI)") if "Caleb Williams (QB - CHI)" in db_keys else 0

with top_col1:
    selected_entity_key = st.selectbox(
        "Search Any Player, Coach, Owner, or Franchise (Active or Historical):",
        db_keys,
        index=default_idx
    )

with top_col2:
    with st.expander("➕ Onboard Any Person or Team", expanded=False):
        c_name = st.text_input("Full Name / Entity Name", value="Jim McMahon")
        c_pos = st.selectbox("Role / Category", ["QB", "SKILL", "COACH", "OWNER", "FRANCHISE"], index=0)
        c_team = st.text_input("Team Abbreviation", value="CHI")
        c_bdate = st.date_input("Birthdate / Inception Date", value=datetime.date(1959, 8, 21))
        if st.button("Save Entity to Database"):
            custom_key = f"{c_name} ({c_pos} - {c_team})"
            db[custom_key] = {
                "category": c_pos, "name": c_name, "pos": c_pos, "jersey": "Custom",
                "birth_date": c_bdate.strftime("%Y-%m-%d"), "team": c_team,
                "exp": f"{c_pos} Record", "seasons": {}
            }
            st.session_state["db_storage"] = db
            st.success(f"✅ Saved {c_name} to database!")
            st.rerun()

entity_data = db.get(selected_entity_key, MASTER_DB["Caleb Williams (QB - CHI)"])
raw_bdate = entity_data.get("birth_date", "2001-11-18")
natal_birth_date = datetime.datetime.strptime(raw_bdate, "%Y-%m-%d").date()

natal_lp = compute_life_path(natal_birth_date, preserve_masters=True)
natal_dob_red = reduce_digits(natal_birth_date.day, preserve_masters=True)
natal_animal, natal_element, natal_polarity = get_chinese_profile(natal_birth_date.year)
birth_yr_red = reduce_digits(natal_birth_date.year, preserve_masters=False)
base_number = reduce_digits(natal_birth_date.month + reduce_digits(natal_birth_date.day, preserve_masters=False), preserve_masters=False)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Name", entity_data.get("name", "Unknown"))
c2.metric("Category / Role", entity_data.get("pos", "—"))
c3.metric("Team ID", entity_data.get("team", "—"))
c4.metric("Birthdate / Inception", natal_birth_date.strftime("%B %d, %Y"))
c5.metric("Life Path Number", f"{natal_lp}")
c6.metric("Chinese Zodiac", f"{natal_element} {natal_animal}")

# ==============================================================================
# SECTION 2: CUSTOM DATE CORRELATION ENGINE (ANY DATE VS MULTIPLE ENTITIES)
# ==============================================================================
st.markdown("---")
st.subheader("2. 🌐 Custom Date Correlation Engine: Evaluate Multiple Entities on Any Chosen Date")
st.caption("Pick any calendar date, select multiple players, coaches, or franchises, and compare their simultaneous cosmic readings side-by-side.")

d_col1, d_col2 = st.columns([1, 3])
with d_col1:
    multi_eval_date = st.date_input("Target Date to Evaluate:", value=datetime.date(2026, 11, 2), key="multi_eval_date_picker")

valid_defaults = [k for k in ["Caleb Williams (QB - CHI)", "Patrick Mahomes (QB - KC)", "Lamar Jackson (QB - BAL)", "Chicago Bears (Franchise)"] if k in db_keys]

with d_col2:
    selected_entities_to_compare = st.multiselect(
        "Select Entities to Compare Simultaneously:",
        options=db_keys,
        default=valid_defaults
    )

if selected_entities_to_compare:
    multi_rows = []
    g_pow = reduce_digits(multi_eval_date.day, True)
    g_uy = reduce_digits(multi_eval_date.year, False)
    g_um = reduce_digits(g_uy + multi_eval_date.month, False)
    g_ud = reduce_digits(g_um + reduce_digits(multi_eval_date.day, False), False)
    g_lp = compute_life_path(multi_eval_date, True)
    g_anim, g_elem, _ = get_chinese_profile(multi_eval_date.year)

    for ent_key in selected_entities_to_compare:
        ent_info = db.get(ent_key)
        if not ent_info:
            continue
        e_bdate = datetime.datetime.strptime(ent_info.get("birth_date", "2000-01-01"), "%Y-%m-%d").date()
        e_lp = compute_life_path(e_bdate, True)
        e_dob = reduce_digits(e_bdate.day, True)
        e_anim, e_elem, e_pol = get_chinese_profile(e_bdate.year)
        e_base = reduce_digits(e_bdate.month + reduce_digits(e_bdate.day, False), False)

        bday_in_eval_yr = datetime.date(multi_eval_date.year, e_bdate.month, e_bdate.day)
        is_flip = multi_eval_date >= bday_in_eval_yr
        cyc_yr = multi_eval_date.year if is_flip else multi_eval_date.year - 1
        cyc_yr_red = reduce_digits(cyc_yr, False)

        e_py = reduce_digits(e_base + cyc_yr_red, False)
        e_pm = reduce_digits(e_py + multi_eval_date.month, False)
        e_pd = reduce_digits(e_pm + reduce_digits(multi_eval_date.day, False), False)

        e_aff = evaluate_affinity(e_anim, g_anim)
        mars_transit = calculate_detailed_transit("Mars", "Sun", multi_eval_date, e_bdate)
        jupiter_transit = calculate_detailed_transit("Jupiter", "Sun", multi_eval_date, e_bdate)

        pd_matches_power = (e_pd == g_pow)
        pd_matches_ud = (e_pd == g_ud)

        multi_rows.append({
            "Entity Name": ent_info.get("name", ent_key),
            "Role": ent_info.get("pos", "—"),
            "Team": ent_info.get("team", "—"),
            "Natal Life Path": str(e_lp),
            "Day of Birth Red": str(e_dob),
            "Chinese Natal Sign": f"{e_elem} {e_anim}",
            "Personal Year (PY)": f"{e_py} ({'Flipped' if is_flip else 'Pre-Flip'})",
            "Personal Month (PM)": str(e_pm),
            "Personal Day (PD)": str(e_pd),
            "Day Power#": str(g_pow),
            "Universal Day (UD)": str(g_ud),
            "PD vs Power# Match": "⚡ MATCH" if pd_matches_power else "—",
            "PD vs UD Match": "🌐 MATCH" if pd_matches_ud else "—",
            "Chinese Cycle Affinity": e_aff,
            "Mars Transit (to Sun)": mars_transit,
            "Jupiter Transit (to Sun)": jupiter_transit
        })

    if multi_rows:
        multi_df = pd.DataFrame(multi_rows)
        st.dataframe(multi_df, use_container_width=True, hide_index=True)

# ==============================================================================
# SECTION 3: MULTI-SEASON CAREER LEDGER & CHECKMARK MATRIX
# ==============================================================================
st.markdown("---")
st.subheader(f"3. Career Ledger for {entity_data.get('name', 'Selected Entity')}")

available_seasons = sorted(list(entity_data.get("seasons", {}).keys()), key=lambda x: int(x) if str(x).isdigit() else 0, reverse=True)
if available_seasons:
    season_options = [str(s) for s in available_seasons] + ["All Career Seasons"]
    selected_season_choice = st.selectbox("Filter Season:", season_options, index=0)
else:
    selected_season_choice = st.selectbox("Filter Season:", ["No Seasons Loaded"], index=0)

if selected_season_choice == "All Career Seasons":
    target_seasons = available_seasons
elif selected_season_choice in available_seasons:
    target_seasons = [selected_season_choice]
else:
    target_seasons = []

raw_logs = []
for s in target_seasons:
    raw_logs.extend(entity_data.get("seasons", {}).get(s, []))

ledger_rows = []
for g in raw_logs:
    raw_gdate = g["Date"]
    g_date = datetime.datetime.strptime(raw_gdate, "%Y-%m-%d").date() if isinstance(raw_gdate, str) else raw_gdate

    bday_game_year = datetime.date(g_date.year, natal_birth_date.month, natal_birth_date.day)
    has_flipped = g_date >= bday_game_year
    cycle_year = g_date.year if has_flipped else g_date.year - 1
    cycle_yr_red = reduce_digits(cycle_year, preserve_masters=False)
    
    py = reduce_digits(base_number + cycle_yr_red, preserve_masters=False)
    pm = reduce_digits(py + g_date.month, preserve_masters=False)
    pd_val = reduce_digits(pm + reduce_digits(g_date.day, preserve_masters=False), preserve_masters=False)
    
    uy = reduce_digits(g_date.year, preserve_masters=False)
    um = reduce_digits(uy + g_date.month, preserve_masters=False)
    ud = reduce_digits(um + reduce_digits(g_date.day, preserve_masters=False), preserve_masters=False)
    
    game_lp = compute_life_path(g_date, preserve_masters=True)
    power_num = reduce_digits(g_date.day, preserve_masters=True)
    
    g_animal, g_element, _ = get_chinese_profile(g_date.year)
    affinity = evaluate_affinity(natal_animal, g_animal)
    
    cat = entity_data.get("category", "")
    is_pending = g.get("Result") == "Pending"

    row = {
        "Season": str(g.get("Season", g_date.year)),
        "Week": f"Week {g.get('Week')}",
        "Date": g_date.strftime("%Y-%m-%d"),
        "Day of Week": g.get("DayOfWeek"),
        "Opponent": g.get("Opp"),
        "Home/Away": g.get("HomeAway"),
        "Stadium / Venue": g.get("Venue"),
        "Surface": g.get("Surface"),
        "Game Time": g.get("GameTime"),
        "Final Score": g.get("Score"),
        "Result": g.get("Result"),
        "Point Diff": g.get("Diff"),
        "Life Path Number": str(natal_lp),
        "Day of Birth Reduced": str(natal_dob_red),
        "Chinese Zodiac Animal": natal_animal,
        "Fixed / Heavenly Element": natal_element,
        "Yin / Yang Polarity": natal_polarity,
        "Birth Year Reduction": str(birth_yr_red),
        "Flip Status": "Flipped" if has_flipped else "Pre-Flip",
        "Game Day Life Path": str(game_lp),
        "Power#": str(power_num),
        "Game Year Animal & Element": f"{g_element} {g_animal}",
        "Affinity Status": affinity,
        "Universal Year (UY)": str(uy),
        "Universal Month (UM)": str(um),
        "Universal Day (UD)": str(ud),
        "Personal Year (PY)": str(py),
        "Personal Month (PM)": str(pm),
        "Personal Day (PD)": str(pd_val),
        "Sun Transit": calculate_detailed_transit("Sun", "Sun", g_date, natal_birth_date),
        "Moon Transit": calculate_detailed_transit("Moon", "Sun", g_date, natal_birth_date),
        "Mercury Transit": calculate_detailed_transit("Mercury", "Mercury", g_date, natal_birth_date),
        "Venus Transit": calculate_detailed_transit("Venus", "Venus", g_date, natal_birth_date),
        "Mars Transit (to Sun)": calculate_detailed_transit("Mars", "Sun", g_date, natal_birth_date),
        "Mars Transit (to Mars)": calculate_detailed_transit("Mars", "Mars", g_date, natal_birth_date),
        "Jupiter Transit (to Sun)": calculate_detailed_transit("Jupiter", "Sun", g_date, natal_birth_date),
        "Jupiter Transit (to Mars)": calculate_detailed_transit("Jupiter", "Mars", g_date, natal_birth_date),
        "Saturn Transit (to Sun)": calculate_detailed_transit("Saturn", "Sun", g_date, natal_birth_date),
        "Saturn Transit (to Mars)": calculate_detailed_transit("Saturn", "Mars", g_date, natal_birth_date),
        "Uranus Transit": calculate_detailed_transit("Uranus", "Sun", g_date, natal_birth_date),
        "Neptune Transit": calculate_detailed_transit("Neptune", "Sun", g_date, natal_birth_date),
        "Pluto Transit": calculate_detailed_transit("Pluto", "Sun", g_date, natal_birth_date),
    }
    
    if cat == "QB":
        row.update({
            "CMP": str(g.get("CMP")) if not is_pending else "—",
            "ATT": str(g.get("ATT")) if not is_pending else "—",
            "CMP%": f"{g.get('CMP%')}%" if not is_pending else "—",
            "Pass Yds": str(g.get("Pass Yds")) if not is_pending else "—",
            "Pass TD": str(g.get("Pass TD")) if not is_pending else "—",
            "Y/A": str(g.get("Y/A")) if not is_pending else "—",
            "INT": str(g.get("INT")) if not is_pending else "—",
            "SCK": str(g.get("SCK")) if not is_pending else "—",
            "Sack Yds Lost": str(g.get("Sack Yds Lost")) if not is_pending else "—",
            "Fumbles": str(g.get("Fumbles")) if not is_pending else "—",
            "Fumbles Lost": str(g.get("Fumbles Lost")) if not is_pending else "—",
            "Passer Rating": str(g.get("Passer Rating")) if not is_pending else "—",
            "QBR": str(g.get("QBR")) if not is_pending else "—",
            "Rush Att": str(g.get("Rush Att")) if not is_pending else "—",
            "Rush Yds": str(g.get("Rush Yds")) if not is_pending else "—",
            "YPC": str(g.get("YPC")) if not is_pending else "—",
            "Rush TD": str(g.get("Rush TD")) if not is_pending else "—",
        })
    elif cat == "FRANCHISE":
        row.update({
            "Total Offense Yds": str(g.get("TotalOffYds")) if not is_pending else "—",
            "First Downs": str(g.get("FirstDowns")) if not is_pending else "—",
            "Turnover Diff": str(g.get("TurnoverDiff")) if not is_pending else "—",
            "3rd Down Eff": str(g.get("ThirdDownEff")) if not is_pending else "—",
        })

    ledger_rows.append(row)

df = pd.DataFrame(ledger_rows)

if not df.empty:
    st.dataframe(df, use_container_width=True)

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Full Ledger to CSV",
        data=csv_data,
        file_name=f"{entity_data.get('name', 'Entity').replace(' ', '_')}_Career_Ledger.csv",
        mime="text/csv",
    )
else:
    st.info("No game logs currently populated for this subject. Use Section 2 to evaluate any date.")

# ==============================================================================
# SECTION 4: MULTI-GAME TREND VISUALIZER
# ==============================================================================
st.markdown("---")
st.subheader("4. 📈 Multi-Game Trend Visualizer: Metaphysical Cycle vs. On-Field Production")
st.caption("Plot performance trends (Passing Yards, Passer Rating, Point Differential) directly across Personal Day (PD) or Power# cycles.")

if not df.empty:
    completed_df = df[df["Result"].isin(["W", "L"])].copy()
    if not completed_df.empty:
        t_col1, t_col2 = st.columns(2)
        with t_col1:
            x_axis_choice = st.selectbox("Select Metaphysical Cycle (X-Axis):", ["Personal Day (PD)", "Power#", "Date"], index=0)
        with t_col2:
            avail_y = ["Point Diff"]
            if entity_data.get("category") == "QB":
                avail_y += ["Pass Yds", "Pass TD", "Passer Rating", "CMP%"]
            elif entity_data.get("category") == "FRANCHISE":
                avail_y += ["Total Offense Yds", "First Downs"]
            y_axis_choice = st.selectbox("Select Performance Metric (Y-Axis):", avail_y, index=0)

        completed_df[y_axis_choice] = pd.to_numeric(completed_df[y_axis_choice].astype(str).str.replace("%", ""), errors="coerce")
        chart_data = completed_df[[x_axis_choice, y_axis_choice]].dropna().sort_values(by=x_axis_choice)

        if not chart_data.empty:
            st.line_chart(chart_data.set_index(x_axis_choice))
        else:
            st.info("Insufficient numeric data to render trend chart for this metric.")
    else:
        st.info("No completed games in the current season filter to generate trend visualizer.")
else:
    st.info("Ingest game logs to activate the trend visualizer.")

# ==============================================================================
# SECTION 5: CHECKMARK CORRELATION MATRIX
# ==============================================================================
st.markdown("---")
st.subheader("5. ⚡ Checkmark Correlation Matrix")
st.caption("Place a checkmark next to any metrics or stats to isolate and correlate trends.")

metaphysical_metrics = [
    "Life Path Number", "Day of Birth Reduced", "Chinese Zodiac Animal",
    "Fixed / Heavenly Element", "Yin / Yang Polarity", "Birth Year Reduction",
    "Flip Status", "Game Day Life Path", "Power#", "Game Year Animal & Element",
    "Affinity Status", "Universal Year (UY)", "Universal Month (UM)", "Universal Day (UD)",
    "Personal Year (PY)", "Personal Month (PM)", "Personal Day (PD)",
    "Sun Transit", "Moon Transit", "Mercury Transit", "Venus Transit",
    "Mars Transit (to Sun)", "Mars Transit (to Mars)", "Jupiter Transit (to Sun)",
    "Jupiter Transit (to Mars)", "Saturn Transit (to Sun)", "Saturn Transit (to Mars)",
    "Uranus Transit", "Neptune Transit", "Pluto Transit"
]

stat_metrics = [
    "Week", "Day of Week", "Opponent", "Home/Away", "Stadium / Venue", "Surface",
    "Final Score", "Result", "Point Diff"
]

if entity_data.get("category") == "QB":
    stat_metrics += [
        "CMP", "ATT", "CMP%", "Pass Yds", "Pass TD", "Y/A", "INT", "SCK",
        "Sack Yds Lost", "Fumbles", "Fumbles Lost", "Passer Rating", "QBR",
        "Rush Att", "Rush Yds", "YPC", "Rush TD"
    ]
elif entity_data.get("category") == "FRANCHISE":
    stat_metrics += [
        "Total Offense Yds", "First Downs", "Turnover Diff", "3rd Down Eff"
    ]

for m in metaphysical_metrics:
    k = f"chk_m_{m}"
    if k not in st.session_state:
        st.session_state[k] = (m in ["Power#", "Personal Day (PD)"])

for s in stat_metrics:
    k = f"chk_s_{s}"
    if k not in st.session_state:
        st.session_state[k] = (s in ["Opponent", "Result", "Point Diff"])

def select_all_meta():
    for m in metaphysical_metrics:
        st.session_state[f"chk_m_{m}"] = True

def uncheck_all_meta():
    for m in metaphysical_metrics:
        st.session_state[f"chk_m_{m}"] = False

def select_all_stats():
    for s in stat_metrics:
        st.session_state[f"chk_s_{s}"] = True

def uncheck_all_stats():
    for s in stat_metrics:
        st.session_state[f"chk_s_{s}"] = False

def clear_everything():
    for m in metaphysical_metrics:
        st.session_state[f"chk_m_{m}"] = False
    for s in stat_metrics:
        st.session_state[f"chk_s_{s}"] = False

b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
with b_col1:
    st.button("✅ Select All Metaphysics", on_click=select_all_meta, use_container_width=True)
with b_col2:
    st.button("❌ Uncheck All Metaphysics", on_click=uncheck_all_meta, use_container_width=True)
with b_col3:
    st.button("✅ Select All Stats", on_click=select_all_stats, use_container_width=True)
with b_col4:
    st.button("❌ Uncheck All Stats", on_click=uncheck_all_stats, use_container_width=True)
with b_col5:
    st.button("🧹 Clear All Selections", on_click=clear_everything, use_container_width=True)

st.markdown("#### 🔮 Box 1: Metaphysical & Cosmic Metrics")
with st.container():
    meta_cols = st.columns(4)
    for idx, m in enumerate(metaphysical_metrics):
        col = meta_cols[idx % 4]
        col.checkbox(m, key=f"chk_m_{m}")

st.markdown("#### 🏈 Box 2: Game Log & Performance Stats")
with st.container():
    stat_cols = st.columns(4)
    for idx, s in enumerate(stat_metrics):
        col = stat_cols[idx % 4]
        col.checkbox(s, key=f"chk_s_{s}")

selected_columns = []
for m in metaphysical_metrics:
    if st.session_state.get(f"chk_m_{m}", False):
        selected_columns.append(m)

for s in stat_metrics:
    if st.session_state.get(f"chk_s_{s}", False):
        selected_columns.append(s)

# ==============================================================================
# SECTION 6: CORRELATION VIEW & TREND FILTER
# ==============================================================================
st.markdown("---")
st.subheader("6. 📊 Correlated Output View")

valid_selected = [c for c in selected_columns if c in df.columns]

if len(valid_selected) >= 2:
    st.write(f"**Currently Correlating ({len(valid_selected)} Checked Metrics):** `{', '.join(valid_selected)}`")
    
    with st.expander("🔎 Filter Values Across Checked Columns", expanded=False):
        filter_cols = st.columns(min(len(valid_selected), 4))
        active_sub_filters = {}
        for idx, col_name in enumerate(valid_selected):
            col_target = filter_cols[idx % 4]
            unique_vals = sorted(list(df[col_name].dropna().unique()), key=lambda x: str(x))
            chosen_sub_vals = col_target.multiselect(
                f"Filter {col_name}:",
                options=unique_vals,
                default=[],
                key=f"trend_filter_{col_name}"
            )
            if chosen_sub_vals:
                active_sub_filters[col_name] = chosen_sub_vals

    filtered_view_df = df[valid_selected].copy()
    if active_sub_filters:
        for c_name, v_list in active_sub_filters.items():
            filtered_view_df = filtered_view_df[filtered_view_df[c_name].isin(v_list)]

    st.dataframe(filtered_view_df, use_container_width=True)

    completed = filtered_view_df[filtered_view_df["Result"].isin(["W", "L"])] if "Result" in filtered_view_df.columns else df.iloc[filtered_view_df.index][df["Result"].isin(["W", "L"])]
    wins = (completed["Result"] == "W").sum()
    losses = (completed["Result"] == "L").sum()
    win_pct = round((wins / len(completed) * 100), 1) if len(completed) > 0 else 0.0

    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Games Displayed", f"{len(filtered_view_df)} / {len(df)}")
    rc2.metric("Straight-Up Record", f"{wins} - {losses}")
    rc3.metric("Straight-Up Win %", f"{win_pct}%")
    
    if "Point Diff" in df.columns:
        diff_vals = pd.to_numeric(df.iloc[filtered_view_df.index]["Point Diff"], errors="coerce").dropna()
        avg_diff = round(diff_vals.mean(), 1) if len(diff_vals) > 0 else 0.0
        rc4.metric("Avg Point Margin", f"{'+' if avg_diff > 0 else ''}{avg_diff}")
    else:
        rc4.metric("Avg Point Margin", "—")
else:
    st.info("Place a checkmark next to at least two metrics above to display the active correlation matrix.")