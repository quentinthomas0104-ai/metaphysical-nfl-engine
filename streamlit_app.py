import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime
import copy

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Pure Cosmic Cycles: Career Logs, Dedicated Transits, Power#, & Cross-Resonance Scanner")

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
# 4. OFFICIAL VERIFIED SCHEDULE SLATES (100% AUDITED DATA)
# ==============================================================================
OFFICIAL_SCHEDULE_SLATES = {
    "2026 Chicago Bears Verified Slate": [
        {"Week": 1, "Date": datetime.date(2026, 9, 13), "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "@", "Venue": "Bank of America Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "59 - 37", "Result": "W", "Diff": "+22", "PassYds": 269, "TotalOffYds": 552},
        {"Week": 2, "Date": datetime.date(2026, 9, 20), "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 9", "Result": "L", "Diff": "-6", "PassYds": 138, "TotalOffYds": 248},
        {"Week": 3, "Date": datetime.date(2026, 9, 28), "DayOfWeek": "Mon", "Opp": "PHI", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "MNF", "Score": "27 - 7", "Result": "W", "Diff": "+20", "PassYds": 246, "TotalOffYds": 374},
        {"Week": 4, "Date": datetime.date(2026, 10, 4), "DayOfWeek": "Sun", "Opp": "NYJ", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "23 - 12", "Result": "W", "Diff": "+11", "PassYds": 190, "TotalOffYds": 492},
        {"Week": 5, "Date": datetime.date(2026, 10, 11), "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "@", "Venue": "Lambeau Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "7 - 31", "Result": "L", "Diff": "-24", "PassYds": 195, "TotalOffYds": 238},
        {"Week": 6, "Date": datetime.date(2026, 10, 18), "DayOfWeek": "Sun", "Opp": "ATL", "HomeAway": "@", "Venue": "Mercedes-Benz Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "31 - 23", "Result": "W", "Diff": "+8", "PassYds": 305, "TotalOffYds": 421},
        {"Week": 7, "Date": datetime.date(2026, 10, 22), "DayOfWeek": "Thu", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "TNF", "Score": "30 - 24", "Result": "W", "Diff": "+6", "PassYds": 308, "TotalOffYds": 405},
        {"Week": 8, "Date": datetime.date(2026, 11, 2), "DayOfWeek": "Mon", "Opp": "SEA", "HomeAway": "@", "Venue": "Lumen Field", "Surface": "Turf", "GameTime": "MNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending", "PassYds": 0, "TotalOffYds": 0},
        {"Week": 9, "Date": datetime.date(2026, 11, 8), "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "SNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending", "PassYds": 0, "TotalOffYds": 0}
    ],
    "2026 Caleb Williams Verified Game Log": [
        {"Week": 1, "Date": datetime.date(2026, 9, 13), "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "@", "Venue": "Bank of America Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "59 - 37", "Result": "W", "Diff": "+22", "PassCmp": 21, "PassAtt": 29, "PassYds": 269, "PassTD": 2, "Int": 0, "RushAtt": 10, "RushYds": 65, "RushTD": 2, "Rating": 124.1},
        {"Week": 2, "Date": datetime.date(2026, 9, 20), "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 9", "Result": "L", "Diff": "-6", "PassCmp": 15, "PassAtt": 26, "PassYds": 138, "PassTD": 0, "Int": 1, "RushAtt": 5, "RushYds": 42, "RushTD": 0, "Rating": 56.2},
        {"Week": 6, "Date": datetime.date(2026, 10, 18), "DayOfWeek": "Sun", "Opp": "ATL", "HomeAway": "@", "Venue": "Mercedes-Benz Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "31 - 23", "Result": "W", "Diff": "+8", "PassCmp": 30, "PassAtt": 36, "PassYds": 305, "PassTD": 1, "Int": 0, "RushAtt": 4, "RushYds": 3, "RushTD": 0, "Rating": 111.2},
        {"Week": 7, "Date": datetime.date(2026, 10, 22), "DayOfWeek": "Thu", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "TNF", "Score": "30 - 24", "Result": "W", "Diff": "+6", "PassCmp": 22, "PassAtt": 33, "PassYds": 308, "PassTD": 2, "Int": 0, "RushAtt": 5, "RushYds": 18, "RushTD": 0, "Rating": 116.7},
        {"Week": 8, "Date": datetime.date(2026, 11, 2), "DayOfWeek": "Mon", "Opp": "SEA", "HomeAway": "@", "Venue": "Lumen Field", "Surface": "Turf", "GameTime": "MNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending", "PassYds": 0, "PassTD": 0, "Rating": 0},
        {"Week": 9, "Date": datetime.date(2026, 11, 8), "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "SNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending", "PassYds": 0, "PassTD": 0, "Rating": 0}
    ],
    "2024 Buffalo Bills Complete Slate": [
        {"Week": 1, "Date": datetime.date(2024, 9, 8), "DayOfWeek": "Sun", "Opp": "ARI", "HomeAway": "vs", "Venue": "Highmark Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "34 - 28", "Result": "W", "Diff": "+6", "PassYds": 232, "TotalOffYds": 352},
        {"Week": 2, "Date": datetime.date(2024, 9, 12), "DayOfWeek": "Thu", "Opp": "MIA", "HomeAway": "@", "Venue": "Hard Rock Stadium", "Surface": "Grass", "GameTime": "TNF", "Score": "31 - 10", "Result": "W", "Diff": "+21", "PassYds": 139, "TotalOffYds": 314},
        {"Week": 3, "Date": datetime.date(2024, 9, 23), "DayOfWeek": "Mon", "Opp": "JAX", "HomeAway": "vs", "Venue": "Highmark Stadium", "Surface": "Turf", "GameTime": "MNF", "Score": "47 - 10", "Result": "W", "Diff": "+37", "PassYds": 263, "TotalOffYds": 388},
        {"Week": 4, "Date": datetime.date(2024, 9, 29), "DayOfWeek": "Sun", "Opp": "BAL", "HomeAway": "@", "Venue": "M&T Bank Stadium", "Surface": "Grass", "GameTime": "SNF", "Score": "10 - 35", "Result": "L", "Diff": "-25", "PassYds": 180, "TotalOffYds": 236},
        {"Week": 11, "Date": datetime.date(2024, 11, 17), "DayOfWeek": "Sun", "Opp": "KC", "HomeAway": "vs", "Venue": "Highmark Stadium", "Surface": "Turf", "GameTime": "4:25 PM", "Score": "30 - 21", "Result": "W", "Diff": "+9", "PassYds": 262, "TotalOffYds": 366},
        {"Week": 14, "Date": datetime.date(2024, 12, 8), "DayOfWeek": "Sun", "Opp": "LAR", "HomeAway": "@", "Venue": "SoFi Stadium", "Surface": "Turf", "GameTime": "4:25 PM", "Score": "42 - 44", "Result": "L", "Diff": "-2", "PassYds": 342, "TotalOffYds": 435}
    ]
}

ALL_32_FRANCHISES = {
    "Arizona Cardinals": datetime.date(1898, 1, 1), "Atlanta Falcons": datetime.date(1965, 6, 30),
    "Baltimore Ravens": datetime.date(1996, 2, 9), "Buffalo Bills": datetime.date(1959, 10, 28),
    "Carolina Panthers": datetime.date(1993, 10, 26), "Chicago Bears": datetime.date(1920, 9, 17),
    "Cincinnati Bengals": datetime.date(1967, 5, 23), "Cleveland Browns": datetime.date(1946, 4, 20),
    "Dallas Cowboys": datetime.date(1960, 1, 28), "Denver Broncos": datetime.date(1959, 8, 14),
    "Detroit Lions": datetime.date(1930, 7, 12), "Green Bay Packers": datetime.date(1919, 8, 11),
    "Houston Texans": datetime.date(1999, 10, 6), "Indianapolis Colts": datetime.date(1953, 1, 23),
    "Jacksonville Jaguars": datetime.date(1993, 11, 30), "Kansas City Chiefs": datetime.date(1959, 8, 14),
    "Las Vegas Raiders": datetime.date(1960, 1, 30), "Los Angeles Chargers": datetime.date(1959, 8, 14),
    "Los Angeles Rams": datetime.date(1936, 2, 13), "Miami Dolphins": datetime.date(1965, 8, 16),
    "Minnesota Vikings": datetime.date(1960, 1, 28), "New England Patriots": datetime.date(1959, 11, 16),
    "New Orleans Saints": datetime.date(1966, 11, 1), "New York Giants": datetime.date(1925, 8, 1),
    "New York Jets": datetime.date(1959, 8, 14), "Philadelphia Eagles": datetime.date(1933, 7, 8),
    "Pittsburgh Steelers": datetime.date(1933, 7, 8), "San Francisco 49ers": datetime.date(1946, 6, 4),
    "Seattle Seahawks": datetime.date(1974, 6, 4), "Tampa Bay Buccaneers": datetime.date(1974, 4, 24),
    "Tennessee Titans": datetime.date(1959, 8, 14), "Washington Commanders": datetime.date(1932, 7, 9)
}

# ==============================================================================
# 5. INITIALIZE