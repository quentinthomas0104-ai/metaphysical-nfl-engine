import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime
import json
import os

st.set_page_config(page_title="Metaphysical NFL Engine", layout="wide")

st.title("🏈 Metaphysical NFL Analytics Engine")
st.caption("Universal Lookup & Metaphysical Trend Engine for Players, Coaches, Owners, & Teams")

STORAGE_FILE = "engine_storage.json"

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
# 4. INITIAL KNOWLEDGE BASE & STORAGE REPOSITORY
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

BEARS_2024_SLATE = [
    {"Week": 1, "Date": "2024-09-08", "DayOfWeek": "Sun", "Opp": "TEN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "24 - 17", "Result": "W", "Diff": 7, "TotalOffYds": 148, "FirstDowns": 11, "TurnoverDiff": "+2", "ThirdDownEff": "2/12 (16.7%)"},
    {"Week": 2, "Date": "2024-09-15", "DayOfWeek": "Sun", "Opp": "HOU", "HomeAway": "@", "Venue": "NRG Stadium", "Surface": "Turf", "GameTime": "8:20 PM", "Score": "13 - 19", "Result": "L", "Diff": -6, "TotalOffYds": 205, "FirstDowns": 15, "TurnoverDiff": "-1", "ThirdDownEff": "6/17 (35.3%)"},
    {"Week": 3, "Date": "2024-09-22", "DayOfWeek": "Sun", "Opp": "IND", "HomeAway": "@", "Venue": "Lucas Oil Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "16 - 21", "Result": "L", "Diff": -5, "TotalOffYds": 395, "FirstDowns": 26, "TurnoverDiff": "-1", "ThirdDownEff": "9/21 (42.9%)"},
    {"Week": 4, "Date": "2024-09-29", "DayOfWeek": "Sun", "Opp": "LAR", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "24 - 18", "Result": "W", "Diff": 6, "TotalOffYds": 264, "FirstDowns": 17, "TurnoverDiff": "+2", "ThirdDownEff": "4/10 (40.0%)"},
    {"Week": 5, "Date": "2024-10-06", "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "36 - 10", "Result": "W", "Diff": 26, "TotalOffYds": 424, "FirstDowns": 24, "TurnoverDiff": "+3", "ThirdDownEff": "7/13 (53.8%)"},
    {"Week": 6, "Date": "2024-10-13", "DayOfWeek": "Sun", "Opp": "JAX", "HomeAway": "vs", "Venue": "Tottenham Hotspur Stadium", "Surface": "Turf", "GameTime": "9:30 AM", "Score": "35 - 16", "Result": "W", "Diff": 19, "TotalOffYds": 373, "FirstDowns": 25, "TurnoverDiff": "+1", "ThirdDownEff": "5/10 (50.0%)"},
    {"Week": 8, "Date": "2024-10-27", "DayOfWeek": "Sun", "Opp": "WAS", "HomeAway": "@", "Venue": "Northwest Stadium", "Surface": "Grass", "GameTime": "4:25 PM", "Score": "15 - 18", "Result": "L", "Diff": -3, "TotalOffYds": 307, "FirstDowns": 15, "TurnoverDiff": "-1", "ThirdDownEff": "2/12 (16.7%)"},
    {"Week": 9, "Date": "2024-11-03", "DayOfWeek": "Sun", "Opp": "ARI", "HomeAway": "@", "Venue": "State Farm Stadium", "Surface": "Grass", "GameTime": "4:05 PM", "Score": "9 - 29", "Result": "L", "Diff": -20, "TotalOffYds": 241, "FirstDowns": 16, "TurnoverDiff": "+2", "ThirdDownEff": "3/14 (21.4%)"},
    {"Week": 10, "Date": "2024-11-10", "DayOfWeek": "Sun", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 19", "Result": "L", "Diff": -16, "TotalOffYds": 142, "FirstDowns": 11, "TurnoverDiff": "+1", "ThirdDownEff": "1/14 (7.1%)"},
    {"Week": 11, "Date": "2024-11-17", "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "19 - 20", "Result": "L", "Diff": -1, "TotalOffYds": 391, "FirstDowns": 23, "TurnoverDiff": "+1", "ThirdDownEff": "9/16 (56.3%)"},
    {"Week": 12, "Date": "2024-11-24", "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "27 - 30", "Result": "L", "Diff": -3, "TotalOffYds": 398, "FirstDowns": 20, "TurnoverDiff": "0", "ThirdDownEff": "7/17 (41.2%)"},
    {"Week": 13, "Date": "2024-11-28", "DayOfWeek": "Thu", "Opp": "DET", "HomeAway": "@", "Venue": "Ford Field", "Surface": "Turf", "GameTime": "12:30 PM", "Score": "20 - 23", "Result": "L", "Diff": -3, "TotalOffYds": 301, "FirstDowns": 17, "TurnoverDiff": "0", "ThirdDownEff": "3/12 (25.0%)"},
    {"Week": 14, "Date": "2024-12-08", "DayOfWeek": "Sun", "Opp": "SF", "HomeAway": "@", "Levi's Stadium": "Grass", "GameTime": "4:25 PM", "Score": "13 - 38", "Result": "L", "Diff": -25, "TotalOffYds": 162, "FirstDowns": 14, "TurnoverDiff": "-1", "ThirdDownEff": "3/10 (30.0%)"},
    {"Week": 15, "Date": "2024-12-16", "DayOfWeek": "Mon", "Opp": "MIN", "HomeAway": "@", "Venue": "U.S. Bank Stadium", "Surface": "Turf", "GameTime": "8:00 PM", "Score": "12 - 30", "Result": "L", "Diff": -18, "TotalOffYds": 231, "FirstDowns": 14, "TurnoverDiff": "-1", "ThirdDownEff": "4/12 (33.3%)"},
    {"Week": 16, "Date": "2024-12-22", "DayOfWeek": "Sun", "Opp": "DET", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "17 - 34", "Result": "L", "Diff": -17, "TotalOffYds": 372, "FirstDowns": 22, "TurnoverDiff": "-1", "ThirdDownEff": "6/13 (46.2%)"},
    {"Week": 17, "Date": "2024-12-26", "DayOfWeek": "Thu", "Opp": "SEA", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "8:15 PM", "Score": "3 - 6", "Result": "L", "Diff": -3, "TotalOffYds": 168, "FirstDowns": 13, "TurnoverDiff": "-1", "ThirdDownEff": "2/13 (15.4%)"},
    {"Week": 18, "Date": "2025-01-05", "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "@", "Venue": "Lambeau Field", "Surface": "Grass", "GameTime": "4:25 PM", "Score": "24 - 22", "Result": "W", "Diff": 2, "TotalOffYds": 284, "FirstDowns": 17, "TurnoverDiff": "0", "ThirdDownEff": "5/12 (41.7%)"}
]

BEARS_1985_SLATE = [
    {"Week": 1, "Date": "1985-09-08", "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "38 - 28", "Result": "W", "Diff": 10, "TotalOffYds": 384, "FirstDowns": 22, "TurnoverDiff": "+1", "ThirdDownEff": "7/14 (50.0%)"},
    {"Week": 2, "Date": "1985-09-15", "DayOfWeek": "Sun", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "20 - 7", "Result": "W", "Diff": 13, "TotalOffYds": 341, "FirstDowns": 19, "TurnoverDiff": "+2", "ThirdDownEff": "6/15 (40.0%)"},
    {"Week": 3, "Date": "1985-09-19", "DayOfWeek": "Thu", "Opp": "MIN", "HomeAway": "@", "Venue": "Metrodome", "Surface": "Turf", "GameTime": "8:00 PM", "Score": "33 - 24", "Result": "W", "Diff": 9, "TotalOffYds": 372, "FirstDowns": 23, "TurnoverDiff": "+2", "ThirdDownEff": "8/15 (53.3%)"},
    {"Week": 4, "Date": "1985-09-29", "DayOfWeek": "Sun", "Opp": "WAS", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "45 - 10", "Result": "W", "Diff": 35, "TotalOffYds": 412, "FirstDowns": 24, "TurnoverDiff": "+4", "ThirdDownEff": "7/13 (53.8%)"},
    {"Week": 5, "Date": "1985-10-06", "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "@", "Venue": "Tampa Stadium", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "27 - 19", "Result": "W", "Diff": 8, "TotalOffYds": 315, "FirstDowns": 18, "TurnoverDiff": "0", "ThirdDownEff": "5/12 (41.7%)"},
    {"Week": 6, "Date": "1985-10-13", "DayOfWeek": "Sun", "Opp": "SF", "HomeAway": "@", "Venue": "Candlestick Park", "Surface": "Grass", "GameTime": "4:00 PM", "Score": "26 - 10", "Result": "W", "Diff": 16, "TotalOffYds": 360, "FirstDowns": 21, "TurnoverDiff": "+3", "ThirdDownEff": "6/14 (42.9%)"},
    {"Week": 7, "Date": "1985-10-21", "DayOfWeek": "Mon", "Opp": "GB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "MNF", "Score": "23 - 7", "Result": "W", "Diff": 16, "TotalOffYds": 390, "FirstDowns": 24, "TurnoverDiff": "+3", "ThirdDownEff": "8/16 (50.0%)"},
    {"Week": 8, "Date": "1985-10-27", "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "27 - 9", "Result": "W", "Diff": 18, "TotalOffYds": 348, "FirstDowns": 20, "TurnoverDiff": "+2", "ThirdDownEff": "5/13 (38.5%)"},
    {"Week": 9, "Date": "1985-11-03", "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "@", "Venue": "Lambeau Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "16 - 10", "Result": "W", "Diff": 6, "TotalOffYds": 298, "FirstDowns": 17, "TurnoverDiff": "+1", "ThirdDownEff": "4/12 (33.3%)"},
    {"Week": 10, "Date": "1985-11-10", "DayOfWeek": "Sun", "Opp": "DET", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "24 - 3", "Result": "W", "Diff": 21, "TotalOffYds": 382, "FirstDowns": 22, "TurnoverDiff": "+3", "ThirdDownEff": "7/14 (50.0%)"},
    {"Week": 11, "Date": "1985-11-17", "DayOfWeek": "Sun", "Opp": "DAL", "HomeAway": "@", "Venue": "Texas Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "44 - 0", "Result": "W", "Diff": 44, "TotalOffYds": 425, "FirstDowns": 26, "TurnoverDiff": "+4", "ThirdDownEff": "9/15 (60.0%)"},
    {"Week": 12, "Date": "1985-11-24", "DayOfWeek": "Sun", "Opp": "ATL", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "36 - 0", "Result": "W", "Diff": 36, "TotalOffYds": 402, "FirstDowns": 25, "TurnoverDiff": "+3", "ThirdDownEff": "8/14 (57.1%)"},
    {"Week": 13, "Date": "1985-12-02", "DayOfWeek": "Mon", "Opp": "MIA", "HomeAway": "@", "Venue": "Orange Bowl", "Surface": "Grass", "GameTime": "MNF", "Score": "24 - 38", "Result": "L", "Diff": -14, "TotalOffYds": 315, "FirstDowns": 19, "TurnoverDiff": "-3", "ThirdDownEff": "4/11 (36.4%)"},
    {"Week": 14, "Date": "1985-12-08", "DayOfWeek": "Sun", "Opp": "IND", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "17 - 10", "Result": "W", "Diff": 7, "TotalOffYds": 330, "FirstDowns": 19, "TurnoverDiff": "+1", "ThirdDownEff": "5/13 (38.5%)"},
    {"Week": 15, "Date": "1985-12-14", "DayOfWeek": "Sat", "Opp": "NYJ", "HomeAway": "@", "Venue": "Giants Stadium", "Surface": "Turf", "GameTime": "12:30 PM", "Score": "19 - 6", "Result": "W", "Diff": 13, "TotalOffYds": 310, "FirstDowns": 18, "TurnoverDiff": "+2", "ThirdDownEff": "5/14 (35.7%)"},
    {"Week": 16, "Date": "1985-12-22", "DayOfWeek": "Sun", "Opp": "DET", "HomeAway": "@", "Venue": "Pontiac Silverdome", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "37 - 17", "Result": "W", "Diff": 20, "TotalOffYds": 395, "FirstDowns": 23, "TurnoverDiff": "+3", "ThirdDownEff": "7/13 (53.8%)"}
]

# Starting Historical Knowledge Base with Key Figures
DEFAULT_DB = {
    "Caleb Williams (QB - CHI)": {
        "category": "QB", "name": "Caleb Williams", "pos": "QB", "jersey": "#18",
        "birth_date": "2001-11-18", "team": "CHI", "exp": "3rd Season (Draft 2024)",
        "seasons": {"2026": CALEB_2026_SLATE, "2024": CALEB_2024_SLATE}
    },
    "Chicago Bears (Franchise)": {
        "category": "FRANCHISE", "name": "Chicago Bears", "pos": "Franchise", "jersey": "—",
        "birth_date": "1920-09-17", "team": "CHI", "exp": "104 Seasons (Charter APFA)",
        "seasons": {"2026": BEARS_2026_SLATE, "2024": BEARS_2024_SLATE, "1985": BEARS_1985_SLATE}
    },
    "Mike Ditka (Coach - CHI)": {
        "category": "COACH", "name": "Mike Ditka", "pos": "Coach", "jersey": "HC",
        "birth_date": "1939-10-18", "team": "CHI", "exp": "Hall of Fame Coach / TE",
        "seasons": {}
    },
    "Matt Eberflus (Coach - CHI)": {
        "category": "COACH", "name": "Matt Eberflus", "pos": "Coach", "jersey": "HC",
        "birth_date": "1970-05-17", "team": "CHI", "exp": "Head Coach (2022-2024)",
        "seasons": {}
    },
    "George Halas (Owner/Founder - CHI)": {
        "category": "OWNER", "name": "George Halas", "pos": "Owner", "jersey": "Papa Bear",
        "birth_date": "1895-02-02", "team": "CHI", "exp": "Founder & 6x Champion",
        "seasons": {}
    },
    "Walter Payton (RB - CHI)": {
        "category": "SKILL", "name": "Walter Payton", "pos": "RB", "jersey": "#34",
        "birth_date": "1954-07-25", "team": "CHI", "exp": "Hall of Fame Legend",
        "seasons": {}
    },
    "Seattle Seahawks (Franchise)": {
        "category": "FRANCHISE", "name": "Seattle Seahawks", "pos": "Franchise", "jersey": "—",
        "birth_date": "1974-06-04", "team": "SEA", "exp": "Founded 1974",
        "seasons": {}
    },
    "Tampa Bay Buccaneers (Franchise)": {
        "category": "FRANCHISE", "name": "Tampa Bay Buccaneers", "pos": "Franchise", "jersey": "—",
        "birth_date": "1974-04-24", "team": "TB", "exp": "Founded 1974",
        "seasons": {}
    }
}

def save_database(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_database():
    loaded = None
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r") as f:
                loaded = json.load(f)
        except Exception:
            loaded = None
    if not loaded:
        loaded = DEFAULT_DB

    # Sync default key figures if not yet present
    for k, v in DEFAULT_DB.items():
        if k not in loaded:
            loaded[k] = v

    if "Caleb Williams (QB - CHI)" in loaded:
        loaded["Caleb Williams (QB - CHI)"]["seasons"]["2026"] = CALEB_2026_SLATE
        loaded["Caleb Williams (QB - CHI)"]["seasons"]["2024"] = CALEB_2024_SLATE
    if "Chicago Bears (Franchise)" in loaded:
        loaded["Chicago Bears (Franchise)"]["seasons"]["2026"] = BEARS_2026_SLATE
        loaded["Chicago Bears (Franchise)"]["seasons"]["2024"] = BEARS_2024_SLATE
        loaded["Chicago Bears (Franchise)"]["seasons"]["1985"] = BEARS_1985_SLATE

    save_database(loaded)
    return loaded

if "db_storage" not in st.session_state:
    st.session_state["db_storage"] = load_database()

db = st.session_state["db_storage"]

# ==============================================================================
# SECTION 1: SEARCH, ONBOARD & METAPHYSICAL READING
# ==============================================================================
st.subheader("1. Entity Search, Lookup & Metaphysical Baseline")

top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    selected_entity_key = st.selectbox(
        "Search Any Player, Coach, Owner, or Franchise (Active or Historical):",
        list(db.keys()),
        index=0
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
                "category": c_pos, "name": c_name, "pos": c_pos, "jersey": "Historical",
                "birth_date": c_bdate.strftime("%Y-%m-%d"), "team": c_team,
                "exp": f"{c_pos} Record", "seasons": {}
            }
            save_database(db)
            st.success(f"✅ Saved {c_name} to database!")
            st.rerun()

entity_data = db[selected_entity_key]
raw_bdate = entity_data["birth_date"]
natal_birth_date = datetime.datetime.strptime(raw_bdate, "%Y-%m-%d").date()

natal_lp = compute_life_path(natal_birth_date, preserve_masters=True)
natal_dob_red = reduce_digits(natal_birth_date.day, preserve_masters=True)
natal_animal, natal_element, natal_polarity = get_chinese_profile(natal_birth_date.year)
birth_yr_red = reduce_digits(natal_birth_date.year, preserve_masters=False)
base_number = reduce_digits(natal_birth_date.month + reduce_digits(natal_birth_date.day, preserve_masters=False), preserve_masters=False)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Name", entity_data["name"])
c2.metric("Category / Role", entity_data["pos"])
c3.metric("Team ID", entity_data["team"])
c4.metric("Birthdate / Inception", natal_birth_date.strftime("%B %d, %Y"))
c5.metric("Life Path Number", f"{natal_lp}")
c6.metric("Chinese Zodiac", f"{natal_element} {natal_animal}")

# ==============================================================================
# SECTION 2: INSTANT METAPHYSICAL EVALUATOR FOR ANY DAY YOU CHOOSE
# ==============================================================================
st.markdown("---")
st.subheader(f"2. 🔮 Instant Metaphysical Reading for {entity_data['name']} on ANY Day You Choose")
st.caption("Pick any past game, future contest, or custom calendar date to see their full cosmic vibration for that day.")

eval_col1, eval_col2, eval_col3 = st.columns(3)
with eval_col1:
    chosen_eval_date = st.date_input("Select Target Date:", value=datetime.date(2026, 11, 2), key="custom_date_eval")

# Compute Exact Reading for Target Date
bday_this_year = datetime.date(chosen_eval_date.year, natal_birth_date.month, natal_birth_date.day)
is_flipped = chosen_eval_date >= bday_this_year
calc_cycle_year = chosen_eval_date.year if is_flipped else chosen_eval_date.year - 1
calc_cycle_red = reduce_digits(calc_cycle_year, False)

calc_py = reduce_digits(base_number + calc_cycle_red, False)
calc_pm = reduce_digits(calc_py + chosen_eval_date.month, False)
calc_pd = reduce_digits(calc_pm + reduce_digits(chosen_eval_date.day, False), False)

target_power = reduce_digits(chosen_eval_date.day, True)
target_uy = reduce_digits(chosen_eval_date.year, False)
target_um = reduce_digits(target_uy + chosen_eval_date.month, False)
target_ud = reduce_digits(target_um + reduce_digits(chosen_eval_date.day, False), False)
target_g_lp = compute_life_path(chosen_eval_date, True)

target_animal, target_elem, _ = get_chinese_profile(chosen_eval_date.year)
eval_affinity = evaluate_affinity(natal_animal, target_animal)

with eval_col2:
    st.metric("Personal Day (PD)", f"{calc_pd}")
    st.metric("Personal Year (PY)", f"{calc_py} ({'Flipped' if is_flipped else 'Pre-Flip'})")

with eval_col3:
    st.metric("Kickoff Power#", f"{target_power}")
    st.metric("Universal Day (UD)", f"{target_ud}")

# Resonance Check on Target Date
if calc_pd == target_power and calc_pd == target_ud:
    st.success(f"⚡ **DUAL RESONANCE:** {entity_data['name']}'s Personal Day ({calc_pd}) matches both Power# and Universal Day on this date!")
elif calc_pd == target_power:
    st.success(f"⚡ **POWER# HARMONY:** Personal Day ({calc_pd}) directly matches the day's Power# ({target_power})!")
elif calc_pd == target_ud:
    st.info(f"🌐 **UNIVERSAL HARMONY:** Personal Day ({calc_pd}) matches the Universal Day ({target_ud})!")
else:
    st.write(f"Vibrational Alignment: Neutral flow ({calc_pd}) relative to day vibration ({target_power}).")

st.write(f"**Chinese Astrology Alignment on This Date:** {eval_affinity} ({target_elem} {target_animal} Year)")

# ==============================================================================
# SECTION 3: MULTI-SEASON CAREER LEDGER & GAME LOGS
# ==============================================================================
st.markdown("---")
st.subheader(f"3. Multi-Season Career Ledger for {entity_data['name']}")

available_seasons = sorted(list(entity_data["seasons"].keys()), key=lambda x: int(x) if x.isdigit() else 0, reverse=True)
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
    raw_logs.extend(entity_data["seasons"].get(s, []))

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
    
    cat = entity_data["category"]
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
        file_name=f"{entity_data['name'].replace(' ', '_')}_Career_Ledger.csv",
        mime="text/csv",
    )
else:
    st.info("No game logs currently populated for this subject. Use Section 2 to evaluate any date.")

# ==============================================================================
# SECTION 4: CHECKMARK CORRELATION MATRIX (SELECT ANY VARIABLES)
# ==============================================================================
st.markdown("---")
st.subheader("4. ⚡ Checkmark Correlation Matrix")
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

if entity_data["category"] == "QB":
    stat_metrics += [
        "CMP", "ATT", "CMP%", "Pass Yds", "Pass TD", "Y/A", "INT", "SCK",
        "Sack Yds Lost", "Fumbles", "Fumbles Lost", "Passer Rating", "QBR",
        "Rush Att", "Rush Yds", "YPC", "Rush TD"
    ]
elif entity_data["category"] == "FRANCHISE":
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
# SECTION 5: CORRELATION VIEW & TREND FILTER
# ==============================================================================
st.markdown("---")
st.subheader("5. 📊 Correlated Output View")

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