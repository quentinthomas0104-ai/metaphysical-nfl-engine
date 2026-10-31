import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Past Research & Future Edge Forecaster: Expanded Pipeline, Dedicated Transits, Power#, & Predictive Analytics")

# ==============================================================================
# 1. CORE NUMEROLOGY & VIBRATIONAL ENGINE (PRESERVES MASTER NUMBERS)
# ==============================================================================
def reduce_digits(n: int, preserve_masters: bool = True) -> int:
    """Reduces an integer to a single digit (1-9), preserving master numbers 11, 22, 33."""
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
# 3. WESTERN ASTROLOGY (ALL 10 BODIES & TRANSIT MATRIX)
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

def calculate_detailed_transit(t_planet: str, n_planet: str, game_date: datetime.date, natal_date: datetime.date) -> str:
    g_deg, g_sign, _ = get_planet_position(t_planet, game_date)
    n_deg, n_sign, _ = get_planet_position(n_planet, natal_date)
    aspect = get_aspect_name(g_deg, n_deg)
    if aspect:
        return f"{t_planet} in {g_sign} {aspect} {n_planet} in {n_sign}"
    return "—"

# ==============================================================================
# 4. MODULE 1: EXPANDED DATABASE & REPOSITORY
# ==============================================================================
# Official NFL 32-Franchise Inception Charter Dates
ALL_32_FRANCHISES = {
    "Arizona Cardinals": datetime.date(1898, 1, 1),
    "Atlanta Falcons": datetime.date(1965, 6, 30),
    "Baltimore Ravens": datetime.date(1996, 2, 9),
    "Buffalo Bills": datetime.date(1959, 10, 28),
    "Carolina Panthers": datetime.date(1993, 10, 26),
    "Chicago Bears": datetime.date(1920, 9, 17),
    "Cincinnati Bengals": datetime.date(1967, 5, 23),
    "Cleveland Browns": datetime.date(1946, 4, 20),
    "Dallas Cowboys": datetime.date(1960, 1, 28),
    "Denver Broncos": datetime.date(1959, 8, 14),
    "Detroit Lions": datetime.date(1930, 7, 12),
    "Green Bay Packers": datetime.date(1919, 8, 11),
    "Houston Texans": datetime.date(1999, 10, 6),
    "Indianapolis Colts": datetime.date(1953, 1, 23),
    "Jacksonville Jaguars": datetime.date(1993, 11, 30),
    "Kansas City Chiefs": datetime.date(1959, 8, 14),
    "Las Vegas Raiders": datetime.date(1960, 1, 30),
    "Los Angeles Chargers": datetime.date(1959, 8, 14),
    "Los Angeles Rams": datetime.date(1936, 2, 13),
    "Miami Dolphins": datetime.date(1965, 8, 16),
    "Minnesota Vikings": datetime.date(1960, 1, 28),
    "New England Patriots": datetime.date(1959, 11, 16),
    "New Orleans Saints": datetime.date(1966, 11, 1),
    "New York Giants": datetime.date(1925, 8, 1),
    "New York Jets": datetime.date(1959, 8, 14),
    "Philadelphia Eagles": datetime.date(1933, 7, 8),
    "Pittsburgh Steelers": datetime.date(1933, 7, 8),
    "San Francisco 49ers": datetime.date(1946, 6, 4),
    "Seattle Seahawks": datetime.date(1974, 6, 4),
    "Tampa Bay Buccaneers": datetime.date(1974, 4, 24),
    "Tennessee Titans": datetime.date(1959, 8, 14),
    "Washington Commanders": datetime.date(1932, 7, 9)
}

EXPANDED_CAREER_DATABASE = {
    # ------------------ QUARTERBACKS ------------------
    "Josh Allen (QB - BUF)": {
        "category": "QB", "name": "Josh Allen", "pos": "QB", "jersey": "#17",
        "birth_date": datetime.date(1996, 5, 21), "team": "BUF", "exp": "7th Season (Draft 2018)",
        "seasons": {
            2024: [
                {"Week": 1, "Date": datetime.date(2024, 9, 8), "DayOfWeek": "Sun", "Opp": "ARI", "HomeAway": "vs", "GameType": "Regular Season", "Venue": "Highmark Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "34 - 28", "Result": "W", "Diff": "+6", "PassCmp": 18, "PassAtt": 23, "PassCmpPct": 78.3, "PassYds": 232, "PassTD": 2, "PassYPA": 10.1, "Int": 0, "Sacks": 2, "SackYdsLost": 14, "Fumbles": 0, "FumblesLost": 0, "Rating": 137.7, "QBR": 86.4, "RushAtt": 9, "RushYds": 39, "RushYPC": 4.3, "RushTD": 2, "Rush20Plus": 1, "BrokenTackles": 2, "Targets": 0, "Rec": 0, "RecYds": 0, "RecYPR": 0.0, "RecTD": 0, "YAC": 0, "Rec20Plus": 0, "Rec50Plus": 0, "ScrimmageYds": 271, "Touches": 9, "TotalTDs": 4, "StdFPts": 29.2, "HalfPPR": 29.2, "PPRFPts": 31.2, "FGM": 0, "FGA": 0, "FG_Pct": 0.0, "XPM": 0, "XPA": 0, "LongestFG": 0},
                {"Week": 2, "Date": datetime.date(2024, 9, 12), "DayOfWeek": "Thu", "Opp": "MIA", "HomeAway": "@", "GameType": "Regular Season", "Venue": "Hard Rock Stadium", "Surface": "Grass", "GameTime": "TNF", "Score": "31 - 10", "Result": "W", "Diff": "+21", "PassCmp": 13, "PassAtt": 19, "PassCmpPct": 68.4, "PassYds": 139, "PassTD": 1, "PassYPA": 7.3, "Int": 0, "Sacks": 1, "SackYdsLost": 7, "Fumbles": 0, "FumblesLost": 0, "Rating": 107.1, "QBR": 68.2, "RushAtt": 2, "RushYds": 2, "RushYPC": 1.0, "RushTD": 0, "Rush20Plus": 0, "BrokenTackles": 0, "Targets": 0, "Rec": 0, "RecYds": 0, "RecYPR": 0.0, "RecTD": 0, "YAC": 0, "Rec20Plus": 0, "Rec50Plus": 0, "ScrimmageYds": 141, "Touches": 2, "TotalTDs": 1, "StdFPts": 11.8, "HalfPPR": 11.8, "PPRFPts": 11.8, "FGM": 0, "FGA": 0, "FG_Pct": 0.0, "XPM": 0, "XPA": 0, "LongestFG": 0},
                {"Week": 11, "Date": datetime.date(2024, 11, 17), "DayOfWeek": "Sun", "Opp": "KC", "HomeAway": "vs", "GameType": "Regular Season", "Venue": "Highmark Stadium", "Surface": "Turf", "GameTime": "4:25 PM", "Score": "30 - 21", "Result": "W", "Diff": "+9", "PassCmp": 27, "PassAtt": 40, "PassCmpPct": 67.5, "PassYds": 262, "PassTD": 1, "PassYPA": 6.6, "Int": 1, "Sacks": 0, "SackYdsLost": 0, "Fumbles": 0, "FumblesLost": 0, "Rating": 83.5, "QBR": 88.6, "RushAtt": 12, "RushYds": 55, "RushYPC": 4.6, "RushTD": 1, "Rush20Plus": 1, "BrokenTackles": 3, "Targets": 0, "Rec": 0, "RecYds": 0, "RecYPR": 0.0, "RecTD": 0, "YAC": 0, "Rec20Plus": 0, "Rec50Plus": 0, "ScrimmageYds": 317, "Touches": 12, "TotalTDs": 2, "StdFPts": 24.0, "HalfPPR": 24.0, "PPRFPts": 24.0, "FGM": 0, "FGA": 0, "FG_Pct": 0.0, "XPM": 0, "XPA": 0, "LongestFG": 0},
                {"Week": 14, "Date": datetime.date(2024, 12, 8), "DayOfWeek": "Sun", "Opp": "LAR", "HomeAway": "@", "GameType": "Regular Season", "Venue": "SoFi Stadium", "Surface": "Turf", "GameTime": "4:25 PM", "Score": "42 - 44", "Result": "L", "Diff": "-2", "PassCmp": 22, "PassAtt": 37, "PassCmpPct": 59.5, "PassYds": 342, "PassTD": 3, "PassYPA": 9.2, "Int": 0, "Sacks": 1, "SackYdsLost": 8, "Fumbles": 0, "FumblesLost": 0, "Rating": 114.9, "QBR": 89.2, "RushAtt": 10, "RushYds": 82, "RushYPC": 8.2, "RushTD": 3, "Rush20Plus": 2, "BrokenTackles": 3, "Targets": 0, "Rec": 0, "RecYds": 0, "RecYPR": 0.0, "RecTD": 0, "YAC": 0, "Rec20Plus": 0, "Rec50Plus": 0, "ScrimmageYds": 424, "Touches": 10, "TotalTDs": 6, "StdFPts": 43.9, "HalfPPR": 43.9, "PPRFPts": 43.9, "FGM": 0, "FGA": 0, "FG_Pct": 0.0, "XPM": 0, "XPA": 0, "LongestFG": 0}
            ],
            2023: [
                {"Week": 1, "Date": datetime.date(2023, 9, 11), "DayOfWeek": "Mon", "Opp": "NYJ", "HomeAway": "@", "GameType": "Regular Season", "Venue": "MetLife Stadium", "Surface": "Turf", "GameTime": "MNF", "Score": "16 - 22", "Result": "L", "Diff": "-6", "PassCmp": 29, "PassAtt": 40, "PassCmpPct": 72.5, "PassYds": 236, "PassTD": 1, "PassYPA": 5.9, "Int": 3, "Sacks": 5, "SackYdsLost": 32, "Fumbles": 2, "FumblesLost": 1, "Rating": 62.1, "QBR": 35.8, "RushAtt": 6, "RushYds": 36, "RushYPC": 6.0, "RushTD": 0, "Rush20Plus": 0, "BrokenTackles": 1, "Targets": 0, "Rec": 0, "RecYds": 0, "RecYPR": 0.0, "RecTD": 0, "YAC": 0, "Rec20Plus": 0, "Rec50Plus": 0, "ScrimmageYds": 272, "Touches": 6, "TotalTDs": 1, "StdFPts": 11.0, "HalfPPR": 11.0, "PPRFPts": 11.0, "FGM": 0, "FGA": 0, "FG_Pct": 0.0, "XPM": 0, "XPA": 0, "LongestFG": 0},
                {"Week": 4, "Date": datetime.date(2023, 10, 1), "DayOfWeek": "Sun", "Opp": "MIA", "HomeAway": "vs", "GameType": "Regular Season", "Venue": "Highmark Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "48 - 20", "Result": "W", "Diff": "+28", "PassCmp": 21, "PassAtt": 25, "PassCmpPct": 84.0, "PassYds": 320, "PassTD": 4, "PassYPA": 12.8, "Int": 0, "Sacks": 2, "SackYdsLost": 16, "Fumbles": 0, "FumblesLost": 0, "Rating": 158.3, "QBR": 98.6, "RushAtt": 4, "RushYds": 17, "RushYPC": 4.3, "RushTD": 1, "Rush20Plus": 0, "BrokenTackles": 1, "Targets": 0, "Rec": 0, "RecYds": 0, "RecYPR": 0.0, "RecTD": 0, "YAC": 0, "Rec20Plus": 0, "Rec50Plus": 0, "ScrimmageYds": 337, "Touches": 4, "TotalTDs": 5, "StdFPts": 36.5, "HalfPPR": 36.5, "PPRFPts": 36.5, "FGM": 0, "FGA": 0, "FG_Pct": 0.0, "XPM": 0, "XPA": 0, "LongestFG": 0}
            ]
        }
    },
    "Patrick Mahomes (QB - KC)": {
        "category": "QB", "name": "Patrick Mahomes", "pos": "QB", "jersey": "#15",
        "birth_date": datetime.date(1995, 9, 17), "team": "KC", "exp": "8th Season (Draft 2017)",
        "seasons": {
            2024: [
                {"Week": 1, "Date": datetime.date(2024, 9, 5), "DayOfWeek": "Thu", "Opp": "BAL", "HomeAway": "vs", "GameType": "Regular Season", "Venue": "Arrowhead Stadium", "Surface": "Grass", "GameTime": "TNF", "Score": "27 - 20", "Result": "W", "Diff": "+7", "PassCmp": 20, "PassAtt": 28, "PassCmpPct": 71.4, "PassYds": 291, "PassTD": 1, "PassYPA": 10.4, "Int": 1, "Sacks": 1, "SackYdsLost": 6, "Fumbles": 0, "FumblesLost": 0, "Rating": 101.9, "QBR": 77.2, "RushAtt": 3, "RushYds": 3, "RushYPC": 1.0, "RushTD": 0, "Rush20Plus": 0, "BrokenTackles": 0, "Targets": 0, "Rec": 0, "RecYds": 0, "RecYPR": 0.0, "RecTD": 0, "YAC": 0, "Rec20Plus": 0, "Rec50Plus": 0, "ScrimmageYds": 294, "Touches": 3, "TotalTDs": 1, "StdFPts": 16.9, "HalfPPR": 16.9, "PPRFPts": 16.9, "FGM": 0, "FGA": 0, "FG_Pct": 0.0, "XPM": 0, "XPA": 0, "LongestFG": 0},
                {"Week": 9, "Date": datetime.date(2024, 11, 4), "DayOfWeek": "Mon", "Opp": "TB", "HomeAway": "vs", "GameType": "Regular Season", "Venue": "Arrowhead Stadium", "Surface": "Grass", "GameTime": "MNF", "Score": "30 - 24", "Result": "W", "Diff": "+6", "PassCmp": 34, "PassAtt": 44, "PassCmpPct": 77.3, "PassYds": 291, "PassTD": 3, "PassYPA": 6.6, "Int": 0, "Sacks": 4, "SackYdsLost": 22, "Fumbles": 0, "FumblesLost": 0, "Rating": 116.8, "QBR": 88.5, "RushAtt": 2, "RushYds": 9, "RushYPC": 4.5, "RushTD": 0, "Rush20Plus": 0, "BrokenTackles": 0, "Targets": 0, "Rec": 0, "RecYds": 0, "RecYPR": 0.0, "RecTD": 0, "YAC": 0, "Rec20Plus": 0, "Rec50Plus": 0, "ScrimmageYds": 300, "Touches": 2, "TotalTDs": 3, "StdFPts": 24.5, "HalfPPR": 24.5, "PPRFPts": 24.5, "FGM": 0, "FGA": 0, "FG_Pct": 0.0, "XPM": 0, "XPA": 0, "LongestFG": 0}
            ]
        }
    },
    "Tom Brady (QB - NE)": {
        "category": "QB", "name": "Tom Brady", "pos": "QB", "jersey": "#12",
        "birth_date": datetime.date(1977, 8, 3), "team": "NE", "exp": "23 Seasons (Legend)",
        "seasons": {
            2007: [
                {"Week": 1, "Date": datetime.date(2007, 9, 9), "DayOfWeek": "Sun", "Opp": "NYJ", "HomeAway": "@", "GameType": "Regular Season", "Venue": "Giants Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "38 - 14", "Result": "W", "Diff": "+24", "PassCmp": 22, "PassAtt": 28, "PassCmpPct": 78.6, "PassYds": 297, "PassTD": 3, "PassYPA": 10.6, "Int": 0, "Sacks": 1, "SackYdsLost": 7, "Fumbles": 0, "FumblesLost": 0, "Rating": 146.6, "QBR": 91.2, "RushAtt": 2, "RushYds": 3, "RushYPC": 1.5, "RushTD": 0, "Rush20Plus": 0, "BrokenTackles": 0, "Targets": 0, "Rec": 0, "RecYds": 0, "RecYPR": 0.0, "RecTD": 0, "YAC": 0, "Rec20Plus": 0, "Rec50Plus": 0, "ScrimmageYds": 300, "Touches": 2, "TotalTDs": 3, "StdFPts": 23.9, "HalfPPR": 23.9, "PPRFPts": 23.9, "FGM": 0, "FGA": 0, "FG_Pct": 0.0, "XPM": 0, "XPA": 0, "LongestFG": 0}
            ]
        }
    },
    # ------------------ SKILL PLAYERS ------------------
    "Walter Payton (RB - CHI)": {
        "category": "SKILL", "name": "Walter Payton", "pos": "RB", "jersey": "#34",
        "birth_date": datetime.date(1954, 7, 25), "team": "CHI", "exp": "13 Seasons (Hall of Fame)",
        "seasons": {
            1977: [
                {"Week": 1, "Date": datetime.date(1977, 9, 18), "DayOfWeek": "Sun", "Opp": "DET", "HomeAway": "vs", "GameType": "Regular Season", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "30 - 20", "Result": "W", "Diff": "+10", "RushAtt": 24, "RushYds": 160, "RushYPC": 6.7, "RushTD": 2, "Rush20Plus": 2, "BrokenTackles": 5, "Targets": 2, "Rec": 2, "RecYds": 18, "RecYPR": 9.0, "RecTD": 0, "YAC": 12, "Rec20Plus": 0, "Rec50Plus": 0, "Fumbles": 0, "FumblesLost": 0, "ScrimmageYds": 178, "Touches": 26, "TotalTDs": 2, "StdFPts": 29.8, "HalfPPR": 30.8, "PPRFPts": 31.8},
                {"Week": 10, "Date": datetime.date(1977, 11, 20), "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "GameType": "Regular Season", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "10 - 7", "Result": "W", "Diff": "+3", "RushAtt": 40, "RushYds": 275, "RushYPC": 6.9, "RushTD": 1, "Rush20Plus": 3, "BrokenTackles": 9, "Targets": 1, "Rec": 1, "RecYds": 6, "RecYPR": 6.0, "RecTD": 0, "YAC": 6, "Rec20Plus": 0, "Rec50Plus": 0, "Fumbles": 0, "FumblesLost": 0, "ScrimmageYds": 281, "Touches": 41, "TotalTDs": 1, "StdFPts": 34.1, "HalfPPR": 34.6, "PPRFPts": 35.1}
            ]
        }
    },
    "Derrick Henry (RB - BAL)": {
        "category": "SKILL", "name": "Derrick Henry", "pos": "RB", "jersey": "#22",
        "birth_date": datetime.date(1994, 1, 4), "team": "BAL", "exp": "9th Season (Draft 2016)",
        "seasons": {
            2024: [
                {"Week": 4, "Date": datetime.date(2024, 9, 29), "DayOfWeek": "Sun", "Opp": "BUF", "HomeAway": "vs", "GameType": "Regular Season", "Venue": "M&T Bank Stadium", "Surface": "Grass", "GameTime": "SNF", "Score": "35 - 10", "Result": "W", "Diff": "+25", "RushAtt": 24, "RushYds": 199, "RushYPC": 8.3, "RushTD": 1, "Rush20Plus": 2, "BrokenTackles": 6, "Targets": 1, "Rec": 1, "RecYds": 10, "RecYPR": 10.0, "RecTD": 1, "YAC": 10, "Rec20Plus": 0, "Rec50Plus": 0, "Fumbles": 1, "FumblesLost": 0, "ScrimmageYds": 209, "Touches": 25, "TotalTDs": 2, "StdFPts": 32.9, "HalfPPR": 33.4, "PPRFPts": 33.9}
            ]
        }
    },
    # ------------------ FRANCHISES ------------------
    "Chicago Bears (Franchise)": {
        "category": "FRANCHISE", "name": "Chicago Bears", "pos": "Franchise", "jersey": "—",
        "birth_date": datetime.date(1920, 9, 17), "team": "CHI", "exp": "104 Seasons (Charter APFA)",
        "seasons": {
            1920: [
                {"Week": 1, "Date": datetime.date(1920, 10, 3), "DayOfWeek": "Sun", "Opp": "Moline Tractors", "HomeAway": "vs", "GameType": "Inaugural Game", "Venue": "Staley Field", "Surface": "Grass", "GameTime": "2:30 PM", "Score": "20 - 0", "Result": "W", "Diff": "+20", "TotalOffYds": 285, "FirstDowns": 14, "TurnoverDiff": "+3", "ThirdDownEff": "N/A (Historical)"},
                {"Week": 11, "Date": datetime.date(1920, 11, 28), "DayOfWeek": "Sun", "Opp": "Chicago Cardinals", "HomeAway": "@", "GameType": "Rivalry Game", "Venue": "Normal Park", "Surface": "Grass", "GameTime": "2:30 PM", "Score": "6 - 7", "Result": "L", "Diff": "-1", "TotalOffYds": 210, "FirstDowns": 10, "TurnoverDiff": "-1", "ThirdDownEff": "N/A (Historical)"}
            ],
            2024: [
                {"Week": 1, "Date": datetime.date(2024, 9, 8), "DayOfWeek": "Sun", "Opp": "TEN", "HomeAway": "vs", "GameType": "Regular Season", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "24 - 17", "Result": "W", "Diff": "+7", "TotalOffYds": 148, "FirstDowns": 11, "TurnoverDiff": "+3", "ThirdDownEff": "2/14 (14.3%)"}
            ]
        }
    },
    "Green Bay Packers (Franchise)": {
        "category": "FRANCHISE", "name": "Green Bay Packers", "pos": "Franchise", "jersey": "—",
        "birth_date": datetime.date(1919, 8, 11), "team": "GB", "exp": "105 Seasons (Founded 1919)",
        "seasons": {
            1921: [
                {"Week": 1, "Date": datetime.date(1921, 10, 23), "DayOfWeek": "Sun", "Opp": "Minneapolis Marines", "HomeAway": "vs", "GameType": "Inaugural APFA Game", "Venue": "Hagemeister Park", "Surface": "Grass", "GameTime": "2:30 PM", "Score": "7 - 6", "Result": "W", "Diff": "+1", "TotalOffYds": 204, "FirstDowns": 10, "TurnoverDiff": "+1", "ThirdDownEff": "N/A (Historical)"}
            ]
        }
    },
    # ------------------ HEAD COACHES ------------------
    "Andy Reid (Head Coach - KC)": {
        "category": "COACH", "name": "Andy Reid", "pos": "Head Coach", "jersey": "—",
        "birth_date": datetime.date(1958, 3, 19), "team": "KC", "exp": "26 Coaching Seasons (3x SB Champion)",
        "seasons": {
            2024: [
                {"Week": 1, "Date": datetime.date(2024, 9, 5), "DayOfWeek": "Thu", "Opp": "BAL", "HomeAway": "vs", "GameType": "NFL Kickoff Game", "Venue": "Arrowhead Stadium", "Surface": "Grass", "GameTime": "TNF", "Score": "27 - 20", "Result": "W", "Diff": "+7", "WinLossEntering": "258-144-1 (.641)", "HomeAwaySplit": "138-66-1 (.676)", "DivisionalRecord": "101-49 (.673)", "FourthDownConversions": "1/1 (100%)", "TOP": "33:36", "PenaltyCount": 6, "PenaltyYds": 45}
            ]
        }
    }
}

# Add all 32 Franchises dynamically into the database registry
for f_name, f_bdate in ALL_32_FRANCHISES.items():
    f_key = f"{f_name} (Franchise)"
    if f_key not in EXPANDED_CAREER_DATABASE:
        EXPANDED_CAREER_DATABASE[f_key] = {
            "category": "FRANCHISE", "name": f_name, "pos": "Franchise", "jersey": "—",
            "birth_date": f_bdate, "team": f_name[:3].upper(), "exp": f"Founded {f_bdate.year}",
            "seasons": {}
        }

# ==============================================================================
# 5. TOP METRIC SUMMARY CARDS & CUSTOM ENTRY PORTAL
# ==============================================================================
st.subheader("1. Entity Selection & Profile Overview")

top_col1, top_col2 = st.columns([3, 1])
with top_col1:
    selected_entity_key = st.selectbox("Search & Select Subject (Player / Coach / 32 Franchises):", list(EXPANDED_CAREER_DATABASE.keys()), index=0)

with top_col2:
    with st.expander("➕ Add Custom Subject"):
        c_name = st.text_input("Name", value="Caleb Williams")
        c_pos = st.selectbox("Role", ["QB", "SKILL", "COACH", "FRANCHISE"], index=0)
        c_team = st.text_input("Team", value="CHI")
        c_bdate = st.date_input("Birthdate / Inception", value=datetime.date(2001, 11, 18))
        if st.button("Save & Inspect Custom"):
            custom_key = f"{c_name} ({c_pos} - {c_team})"
            EXPANDED_CAREER_DATABASE[custom_key] = {
                "category": c_pos, "name": c_name, "pos": c_pos, "jersey": "Custom",
                "birth_date": c_bdate, "team": c_team, "exp": "Custom Profile", "seasons": {}
            }
            selected_entity_key = custom_key
            st.success(f"Loaded {c_name}!")

entity_data = EXPANDED_CAREER_DATABASE[selected_entity_key]

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Name", entity_data["name"])
c2.metric("Position / Role", entity_data["pos"])
c3.metric("Jersey / ID", entity_data["jersey"])
c4.metric("Birthdate / Inception", entity_data["birth_date"].strftime("%B %d, %Y"))
c5.metric("Team", entity_data["team"])
c6.metric("Experience / Seasons", entity_data["exp"])

p_bdate = entity_data["birth_date"]
natal_lp = compute_life_path(p_bdate, preserve_masters=True)
natal_dob_red = reduce_digits(p_bdate.day, preserve_masters=True)
natal_animal, natal_element, natal_polarity = get_chinese_profile(p_bdate.year)
birth_yr_red = reduce_digits(p_bdate.year, preserve_masters=False)
base_number = reduce_digits(p_bdate.month + reduce_digits(p_bdate.day, preserve_masters=False), preserve_masters=False)

# ==============================================================================
# 6. CAREER LEDGER BUILDER
# ==============================================================================
st.markdown("---")
st.subheader(f"2. Career Ledger & Historical Matches for {entity_data['name']}")

available_seasons = sorted(list(entity_data["seasons"].keys()), reverse=True)
if available_seasons:
    col_s1, col_s2 = st.columns([1, 3])
    with col_s1:
        selected_season_choice = st.selectbox(
            "Filter Season:",
            ["All Career Seasons"] + [str(s) for s in available_seasons],
            index=0
        )
    target_seasons = available_seasons if selected_season_choice == "All Career Seasons" else [int(selected_season_choice)]
else:
    target_seasons = []

raw_logs_to_process = []
for s in target_seasons:
    raw_logs_to_process.extend(entity_data["seasons"].get(s, []))

ledger_rows = []
for g in raw_logs_to_process:
    g_date = g["Date"]
    
    bday_game_year = datetime.date(g_date.year, p_bdate.month, p_bdate.day)
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
    if cat == "QB":
        primary_stat = g.get("PassYds", 0)
    elif cat == "SKILL":
        primary_stat = g.get("ScrimmageYds", 0)
    elif cat == "FRANCHISE":
        primary_stat = g.get("TotalOffYds", 0)
    elif cat == "COACH":
        primary_stat = int(str(g.get("Score", "0")).split(" - ")[0]) if " - " in str(g.get("Score")) else 0
    else:
        primary_stat = int(str(g.get("Score", "0")).split(" - ")[0]) if " - " in str(g.get("Score")) else 0
        
    stat_red = reduce_digits(primary_stat, preserve_masters=False) if primary_stat > 0 else 0
    num_match = (stat_red == pd_val) or (stat_red == ud)
    
    row = {
        "Season": g.get("Season"), "Week": g.get("Week"), "Date": g_date.strftime("%Y-%m-%d"),
        "Day of Week": g.get("DayOfWeek"), "Opponent": g.get("Opp"), "Home/Away": g.get("HomeAway"),
        "Game Type": g.get("GameType"), "Stadium / Venue": g.get("Venue"), "Surface": g.get("Surface"),
        "Game Time": g.get("GameTime"), "Final Score": g.get("Score"), "Result": g.get("Result"),
        "Point Diff": g.get("Diff"), "Life Path Number": natal_lp, "Day of Birth Reduced": natal_dob_red,
        "Chinese Zodiac Animal": natal_animal, "Fixed / Heavenly Element": natal_element,
        "Yin / Yang Polarity": natal_polarity, "Birth Year Reduction": birth_yr_red,
        "Flip Status": "Flipped" if has_flipped else "Pre-Flip", "Game Day Life Path": game_lp,
        "Power#": power_num, "Game Year Animal & Element": f"{g_element} {g_animal}",
        "Affinity Status": affinity, "Universal Year (UY)": uy, "Universal Month (UM)": um,
        "Universal Day (UD)": ud, "Personal Year (PY)": py, "Personal Month (PM)": pm,
        "Personal Day (PD)": pd_val, "Stat Vibration": stat_red,
        "Harmonic Match": "⚡ NUM MATCH" if num_match and primary_stat > 0 else "—",
        "Sun Transit": calculate_detailed_transit("Sun", "Sun", g_date, p_bdate),
        "Moon Transit": calculate_detailed_transit("Moon", "Sun", g_date, p_bdate),
        "Mercury Transit": calculate_detailed_transit("Mercury", "Mercury", g_date, p_bdate),
        "Venus Transit": calculate_detailed_transit("Venus", "Venus", g_date, p_bdate),
        "Mars Transit (to Sun)": calculate_detailed_transit("Mars", "Sun", g_date, p_bdate),
        "Mars Transit (to Mars)": calculate_detailed_transit("Mars", "Mars", g_date, p_bdate),
        "Jupiter Transit (to Sun)": calculate_detailed_transit("Jupiter", "Sun", g_date, p_bdate),
        "Jupiter Transit (to Mars)": calculate_detailed_transit("Jupiter", "Mars", g_date, p_bdate),
        "Saturn Transit (to Sun)": calculate_detailed_transit("Saturn", "Sun", g_date, p_bdate),
        "Saturn Transit (to Mars)": calculate_detailed_transit("Saturn", "Mars", g_date, p_bdate),
        "Uranus Transit": calculate_detailed_transit("Uranus", "Sun", g_date, p_bdate),
        "Neptune Transit": calculate_detailed_transit("Neptune", "Sun", g_date, p_bdate),
        "Pluto Transit": calculate_detailed_transit("Pluto", "Sun", g_date, p_bdate),
    }
    
    if cat == "QB":
        row.update({
            "Std FPts": g.get("StdFPts"), "Half-PPR": g.get("HalfPPR"), "Full PPR": g.get("PPRFPts"),
            "CMP": g.get("PassCmp"), "ATT": g.get("PassAtt"), "CMP%": g.get("PassCmpPct"),
            "Pass Yds": g.get("PassYds"), "Pass TDs": g.get("PassTD"), "Y/A": g.get("PassYPA"),
            "INT": g.get("Int"), "SCK": g.get("Sacks"), "Sack Yds Lost": g.get("SackYdsLost"),
            "Fumbles": g.get("Fumbles"), "Fumbles Lost": g.get("FumblesLost"),
            "Passer Rating": g.get("Rating"), "QBR": g.get("QBR"),
            "CAR": g.get("RushAtt"), "Rush Yds": g.get("RushYds"), "YPC": g.get("RushYPC"),
            "Rush TDs": g.get("RushTD"), "20+ Yd Runs": g.get("Rush20Plus"), "Broken Tackles": g.get("BrokenTackles"),
            "TGT": g.get("Targets"), "REC": g.get("Rec"), "Rec Yds": g.get("RecYds"),
            "YPR": g.get("RecYPR"), "Rec TDs": g.get("RecTD"), "YAC": g.get("YAC"),
            "Scrimmage Yds": g.get("ScrimmageYds"), "Total Touches": g.get("Touches"), "Total TDs": g.get("TotalTDs"),
            "FGM": g.get("FGM"), "FGA": g.get("FGA"), "FG%": g.get("FG_Pct"),
            "XPM": g.get("XPM"), "XPA": g.get("XPA"), "Longest FG": g.get("LongestFG")
        })
    elif cat == "SKILL":
        row.update({
            "CAR": g.get("RushAtt"), "Rush Yds": g.get("RushYds"), "YPC": g.get("RushYPC"),
            "Rush TDs": g.get("RushTD"), "20+ Yd Runs": g.get("Rush20Plus"), "Broken Tackles": g.get("BrokenTackles"),
            "TGT": g.get("Targets"), "REC": g.get("Rec"), "Rec Yds": g.get("RecYds"),
            "YPR": g.get("RecYPR"), "Rec TDs": g.get("RecTD"), "YAC": g.get("YAC"),
            "20+ Yd Receptions": g.get("Rec20Plus"), "50+ Yd Receptions": g.get("Rec50Plus"),
            "Fumbles": g.get("Fumbles"), "Fumbles Lost": g.get("FumblesLost"),
            "Scrimmage Yds": g.get("ScrimmageYds"), "Total Touches": g.get("Touches"), "Total TDs": g.get("TotalTDs"),
            "Std FPts": g.get("StdFPts"), "Half-PPR": g.get("HalfPPR"), "Full PPR": g.get("PPRFPts")
        })
    elif cat == "FRANCHISE":
        row.update({
            "Total Offensive Yards": g.get("TotalOffYds"), "Total First Downs": g.get("FirstDowns"),
            "Turnover Differential": g.get("TurnoverDiff"), "Third-Down Efficiency": g.get("ThirdDownEff")
        })
    elif cat == "COACH":
        row.update({
            "Career W-L Entering": g.get("WinLossEntering"), "Home/Away Splits": g.get("HomeAwaySplit"),
            "Divisional Record": g.get("DivisionalRecord"), "4th Down Conversions": g.get("FourthDownConversions"),
            "Time of Possession": g.get("TOP"), "Penalties": g.get("PenaltyCount"), "Penalty Yards": g.get("PenaltyYds")
        })
    ledger_rows.append(row)

df = pd.DataFrame(ledger_rows)

if not df.empty:
    with st.expander("⚡ Harmonic Scanner & Filter Controls", expanded=False):
        f_c1, f_c2, f_c3, f_c4 = st.columns(4)
        with f_c1:
            match_only = st.checkbox("Show Only ⚡ NUM MATCH Hits", value=False)
        with f_c2:
            all_powers = ["All"] + sorted([str(p) for p in df["Power#"].unique() if pd.notna(p)])
            selected_power = st.selectbox("Filter by Power#:", all_powers, index=0)
        with f_c3:
            all_affinities = ["All"] + sorted([str(a) for a in df["Affinity Status"].unique() if pd.notna(a)])
            selected_affinity = st.selectbox("Filter Chinese Affinity:", all_affinities, index=0)
        with f_c4:
            all_results = ["All", "W", "L", "T"]
            selected_result = st.selectbox("Filter Game Result:", all_results, index=0)

    filtered_df = df.copy()
    if match_only:
        filtered_df = filtered_df[filtered_df["Harmonic Match"] == "⚡ NUM MATCH"]
    if selected_power != "All":
        filtered_df = filtered_df[filtered_df["Power#"].astype(str) == selected_power]
    if selected_affinity != "All":
        filtered_df = filtered_df[filtered_df["Affinity Status"] == selected_affinity]
    if selected_result != "All":
        filtered_df = filtered_df[filtered_df["Result"] == selected_result]

    def apply_visual_highlights(row):
        styles = [''] * len(row)
        if "⚡ NUM MATCH" in str(row.get("Harmonic Match", "")):
            match_idx = row.index.get_loc("Harmonic Match")
            styles[match_idx] = 'background-color: #1b4332; color: #a3e635; font-weight: bold;'
        aff = str(row.get("Affinity Status", ""))
        if "San He" in aff or "Liu He" in aff:
            aff_idx = row.index.get_loc("Affinity Status")
            styles[aff_idx] = 'background-color: #78350f; color: #fde047; font-weight: bold;'
        elif "Chong" in aff or "Xing" in aff:
            aff_idx = row.index.get_loc("Affinity Status")
            styles[aff_idx] = 'background-color: #7f1d1d; color: #fca5a5; font-weight: bold;'
        for col_name in ["Life Path Number", "Day of Birth Reduced", "Game Day Life Path", "Power#"]:
            if col_name in row and row[col_name] in [11, 22, 33]:
                c_idx = row.index.get_loc(col_name)
                styles[c_idx] = 'background-color: #3b0764; color: #d8b4fe; font-weight: bold;'
        for c_idx, col_name in enumerate(row.index):
            if "Transit" in col_name and str(row[col_name]) != "—":
                styles[c_idx] = 'background-color: #1e1b4b; color: #93c5fd;'
        return styles

    styled_df = filtered_df.style.apply(apply_visual_highlights, axis=1)
    st.dataframe(styled_df, use_container_width=True)

    # ==============================================================================
    # 7. MODULE 2: PREDICTIVE HARMONIC HIT STATISTICAL ANALYSIS
    # ==============================================================================
    st.markdown("---")
    st.subheader("📈 Module 2: The Predictive Edge (Harmonic Statistical Splits)")
    
    stat_c1, stat_c2, stat_c3 = st.columns(3)
    
    # 1. Power# Performance Breakdown
    with stat_c1:
        st.markdown("##### ⚡ Average Production by Power#")
        power_grp = df.groupby("Power#")
        if cat == "QB" and "Pass Yds" in df.columns:
            avg_power = power_grp["Pass Yds"].mean().round(1)
            st.dataframe(avg_power.rename("Avg Pass Yds"), use_container_width=True)
        elif cat == "SKILL" and "Scrimmage Yds" in df.columns:
            avg_power = power_grp["Scrimmage Yds"].mean().round(1)
            st.dataframe(avg_power.rename("Avg Scrimmage Yds"), use_container_width=True)
        else:
            win_power = power_grp["Result"].apply(lambda s: (s == "W").mean() * 100).round(1)
            st.dataframe(win_power.rename("Win %"), use_container_width=True)

    # 2. Chinese Affinity Impact Splits
    with stat_c2:
        st.markdown("##### 🐉 Win % by Chinese Astrology Alignment")
        aff_grp = df.groupby("Affinity Status")["Result"].apply(lambda s: (s == "W").mean() * 100).round(1)
        st.dataframe(aff_grp.rename("Win %"), use_container_width=True)

    # 3. Harmonic Hit Correlation
    with stat_c3:
        st.markdown("##### 🎯 Harmonic Match Edge")
        tot = len(df)
        hits = len(df[df["Harmonic Match"] == "⚡ NUM MATCH"])
        win_hits = len(df[(df["Harmonic Match"] == "⚡ NUM MATCH") & (df["Result"] == "W")])
        win_pct = round(win_hits / hits * 100, 1) if hits > 0 else 0
        st.metric("Total Historical Harmonic Hits", f"{hits} / {tot}")
        st.metric("Win Rate on Harmonic Match Games", f"{win_pct}%")

else:
    st.info("No recorded historical logs currently stored for this subject. Use the forecaster below to audit upcoming games!")

# ==============================================================================
# 8. FUTURE GAME FORECASTER (MATCHUP ENGINE FOR UPCOMING GAMES)
# ==============================================================================
st.markdown("---")
st.subheader("🔮 Upcoming Game Forecaster (Future Dates & Unplayed Games)")
st.caption("Calculate exact upcoming astrological transits, Power#, and Personal Day vibrations before kickoff.")

fc_col1, fc_col2, fc_col3 = st.columns(3)
with fc_col1:
    future_date = st.date_input("Target Kickoff Date:", value=datetime.date(2026, 11, 8))
with fc_col2:
    future_opp = st.text_input("Upcoming Opponent:", value="KC")
with fc_col3:
    future_home_away = st.selectbox("Location:", ["vs (Home)", "@ (Away)"], index=0)

# Compute future vibrations
f_bday_year = datetime.date(future_date.year, p_bdate.month, p_bdate.day)
f_has_flipped = future_date >= f_bday_year
f_cycle_year = future_date.year if f_has_flipped else future_date.year - 1
f_cycle_yr_red = reduce_digits(f_cycle_year, preserve_masters=False)

f_py = reduce_digits(base_number + f_cycle_yr_red, preserve_masters=False)
f_pm = reduce_digits(f_py + future_date.month, preserve_masters=False)
f_pd = reduce_digits(f_pm + reduce_digits(future_date.day, preserve_masters=False), preserve_masters=False)

f_uy = reduce_digits(future_date.year, preserve_masters=False)
f_um = reduce_digits(f_uy + future_date.month, preserve_masters=False)
f_ud = reduce_digits(f_um + reduce_digits(future_date.day, preserve_masters=False), preserve_masters=False)

f_power = reduce_digits(future_date.day, preserve_masters=True)
f_game_lp = compute_life_path(future_date, preserve_masters=True)

f_animal, f_element, _ = get_chinese_profile(future_date.year)
f_affinity = evaluate_affinity(natal_animal, f_animal)

st.markdown(f"#### ⚡ Kickoff Forecast: {entity_data['name']} {future_home_away} {future_opp} on `{future_date.strftime('%A, %B %d, %Y')}`")

r1, r2, r3, r4, r5 = st.columns(5)
r1.metric("Game Power#", f"{f_power}")
r2.metric("Active Personal Day (PD)", f"{f_pd}")
r3.metric("Universal Day (UD)", f"{f_ud}")
r4.metric("Personal Year (PY)", f"{f_py}")
r5.metric("Cycle Flip Status", "Flipped" if f_has_flipped else "Pre-Flip")

st.markdown("##### 🪐 Active Planetary Transits at Kickoff Sky")
future_transit_list = []
for p in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]:
    n_deg, n_sign, _ = get_planet_position(p, p_bdate)
    g_deg, g_sign, _ = get_planet_position(p, future_date)
    asp = get_aspect_name(g_deg, n_deg)
    if asp:
        future_transit_list.append({
            "Celestial Body": p,
            "Transit Sky Position": f"{g_sign}",
            "Natal Blueprint Position": f"{n_sign}",
            "Active Aspect": f"⚡ {p} in {g_sign} {asp} {p} in {n_sign}"
        })

if future_transit_list:
    st.dataframe(pd.DataFrame(future_transit_list), use_container_width=True)
else:
    st.info("No major exact 0°, 60°, 90°, 120°, or 180° aspects detected on this date.")

if "San He" in f_affinity or "Liu He" in f_affinity:
    st.success(f"🌟 Positive Astrological Alignment: {f_affinity} is active for this matchup.")
elif "Chong" in f_affinity or "Xing" in f_affinity:
    st.warning(f"⚠️ High Friction Warning: Matchup takes place during a {f_affinity} cycle.")
else:
    st.info(f"Neutral Alignment: {f_affinity}")