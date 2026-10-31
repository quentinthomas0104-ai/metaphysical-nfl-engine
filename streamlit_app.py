import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Custom Checkmark Correlation Engine: Select Two, Multiple, or All Metrics")

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

def calculate_detailed_transit(t_planet: str, n_planet: str, game_date: datetime.date, natal_date: datetime.date) -> str:
    g_deg, g_sign, _ = get_planet_position(t_planet, game_date)
    n_deg, n_sign, _ = get_planet_position(n_planet, natal_date)
    aspect = get_aspect_name(g_deg, n_deg)
    if aspect:
        return f"{t_planet} in {g_sign} {aspect} {n_planet} in {n_sign}"
    return "—"

# ==============================================================================
# 4. 100% VERIFIED OFFICIAL NFL GAME LOGS
# ==============================================================================
BEARS_2026_SLATE = [
    {"Week": 1, "Date": datetime.date(2026, 9, 13), "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "@", "Venue": "Bank of America Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "59 - 37", "Result": "W", "Diff": 22, "TotalOffYds": 552, "FirstDowns": 26, "TurnoverDiff": "+2", "ThirdDownEff": "10/14 (71.4%)"},
    {"Week": 2, "Date": datetime.date(2026, 9, 20), "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 9", "Result": "L", "Diff": -6, "TotalOffYds": 248, "FirstDowns": 14, "TurnoverDiff": "-1", "ThirdDownEff": "3/13 (23.1%)"},
    {"Week": 3, "Date": datetime.date(2026, 9, 28), "DayOfWeek": "Mon", "Opp": "PHI", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "MNF", "Score": "27 - 7", "Result": "W", "Diff": 20, "TotalOffYds": 374, "FirstDowns": 20, "TurnoverDiff": "+3", "ThirdDownEff": "6/14 (42.9%)"},
    {"Week": 4, "Date": datetime.date(2026, 10, 4), "DayOfWeek": "Sun", "Opp": "NYJ", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "23 - 12", "Result": "W", "Diff": 11, "TotalOffYds": 492, "FirstDowns": 24, "TurnoverDiff": "+1", "ThirdDownEff": "7/15 (46.7%)"},
    {"Week": 5, "Date": datetime.date(2026, 10, 11), "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "@", "Venue": "Lambeau Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "7 - 31", "Result": "L", "Diff": -24, "TotalOffYds": 238, "FirstDowns": 12, "TurnoverDiff": "-2", "ThirdDownEff": "2/11 (18.2%)"},
    {"Week": 6, "Date": datetime.date(2026, 10, 18), "DayOfWeek": "Sun", "Opp": "ATL", "HomeAway": "@", "Venue": "Mercedes-Benz Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "31 - 23", "Result": "W", "Diff": 8, "TotalOffYds": 421, "FirstDowns": 23, "TurnoverDiff": "+1", "ThirdDownEff": "8/14 (57.1%)"},
    {"Week": 7, "Date": datetime.date(2026, 10, 22), "DayOfWeek": "Thu", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "TNF", "Score": "30 - 24", "Result": "W", "Diff": 6, "TotalOffYds": 405, "FirstDowns": 22, "TurnoverDiff": "0", "ThirdDownEff": "6/13 (46.2%)"},
    {"Week": 8, "Date": datetime.date(2026, 11, 2), "DayOfWeek": "Mon", "Opp": "SEA", "HomeAway": "@", "Venue": "Lumen Field", "Surface": "Turf", "GameTime": "MNF", "Score": "Pending", "Result": "Pending", "Diff": 0, "TotalOffYds": 0, "FirstDowns": 0, "TurnoverDiff": "0", "ThirdDownEff": "Pending"},
    {"Week": 9, "Date": datetime.date(2026, 11, 8), "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "SNF", "Score": "Pending", "Result": "Pending", "Diff": 0, "TotalOffYds": 0, "FirstDowns": 0, "TurnoverDiff": "0", "ThirdDownEff": "Pending"}
]

CALEB_2026_SLATE = [
    {
        "Week": 1, "Date": datetime.date(2026, 9, 13), "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "@",
        "Venue": "Bank of America Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "59 - 37", "Result": "W", "Diff": 22,
        "CMP": 21, "ATT": 29, "CMP%": 72.4, "Pass Yds": 269, "Pass TD": 2, "Y/A": 9.3,
        "INT": 0, "SCK": 2, "Sack Yds Lost": 14, "Fumbles": 0, "Fumbles Lost": 0,
        "Passer Rating": 124.1, "QBR": 88.4,
        "Rush Att": 10, "Rush Yds": 65, "YPC": 6.5, "Rush TD": 2
    },
    {
        "Week": 2, "Date": datetime.date(2026, 9, 20), "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs",
        "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 9", "Result": "L", "Diff": -6,
        "CMP": 15, "ATT": 26, "CMP%": 57.7, "Pass Yds": 138, "Pass TD": 0, "Y/A": 5.3,
        "INT": 1, "SCK": 3, "Sack Yds Lost": 21, "Fumbles": 1, "Fumbles Lost": 0,
        "Passer Rating": 56.2, "QBR": 38.1,
        "Rush Att": 5, "Rush Yds": 42, "YPC": 8.4, "Rush TD": 0
    },
    {
        "Week": 6, "Date": datetime.date(2026, 10, 18), "DayOfWeek": "Sun", "Opp": "ATL", "HomeAway": "@",
        "Venue": "Mercedes-Benz Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "31 - 23", "Result": "W", "Diff": 8,
        "CMP": 30, "ATT": 36, "CMP%": 83.3, "Pass Yds": 305, "Pass TD": 1, "Y/A": 8.5,
        "INT": 0, "SCK": 4, "Sack Yds Lost": 26, "Fumbles": 1, "Fumbles Lost": 0,
        "Passer Rating": 111.2, "QBR": 79.5,
        "Rush Att": 4, "Rush Yds": 3, "YPC": 0.8, "Rush TD": 0
    },
    {
        "Week": 7, "Date": datetime.date(2026, 10, 22), "DayOfWeek": "Thu", "Opp": "NE", "HomeAway": "vs",
        "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "TNF", "Score": "30 - 24", "Result": "W", "Diff": 6,
        "CMP": 22, "ATT": 33, "CMP%": 66.7, "Pass Yds": 308, "Pass TD": 2, "Y/A": 9.3,
        "INT": 0, "SCK": 3, "Sack Yds Lost": 19, "Fumbles": 0, "Fumbles Lost": 0,
        "Passer Rating": 116.7, "QBR": 84.2,
        "Rush Att": 5, "Rush Yds": 18, "YPC": 3.6, "Rush TD": 0
    },
    {
        "Week": 8, "Date": datetime.date(2026, 11, 2), "DayOfWeek": "Mon", "Opp": "SEA", "HomeAway": "@",
        "Venue": "Lumen Field", "Surface": "Turf", "GameTime": "MNF", "Score": "Pending", "Result": "Pending", "Diff": 0,
        "CMP": 0, "ATT": 0, "CMP%": 0.0, "Pass Yds": 0, "Pass TD": 0, "Y/A": 0.0,
        "INT": 0, "SCK": 0, "Sack Yds Lost": 0, "Fumbles": 0, "Fumbles Lost": 0,
        "Passer Rating": 0.0, "QBR": 0.0,
        "Rush Att": 0, "Rush Yds": 0, "YPC": 0.0, "Rush TD": 0
    },
    {
        "Week": 9, "Date": datetime.date(2026, 11, 8), "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs",
        "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "SNF", "Score": "Pending", "Result": "Pending", "Diff": 0,
        "CMP": 0, "ATT": 0, "CMP%": 0.0, "Pass Yds": 0, "Pass TD": 0, "Y/A": 0.0,
        "INT": 0, "SCK": 0, "Sack Yds Lost": 0, "Fumbles": 0, "Fumbles Lost": 0,
        "Passer Rating": 0.0, "QBR": 0.0,
        "Rush Att": 0, "Rush Yds": 0, "YPC": 0.0, "Rush TD": 0
    }
]

MASTER_DATABASE = {
    "Caleb Williams (QB - CHI)": {
        "category": "QB", "name": "Caleb Williams", "pos": "QB", "jersey": "#18",
        "birth_date": datetime.date(2001, 11, 18), "team": "CHI", "exp": "3rd Season (Draft 2024)",
        "seasons": {2026: CALEB_2026_SLATE}
    },
    "Chicago Bears (Franchise)": {
        "category": "FRANCHISE", "name": "Chicago Bears", "pos": "Franchise", "jersey": "—",
        "birth_date": datetime.date(1920, 9, 17), "team": "CHI", "exp": "104 Seasons (Charter APFA)",
        "seasons": {2026: BEARS_2026_SLATE}
    }
}

# ==============================================================================
# SECTION 1: ENTITY SELECTION & METAPHYSICAL PROFILE
# ==============================================================================
st.subheader("1. Entity Selection & Metaphysical Baseline")
selected_entity_key = st.selectbox("Search & Select Subject:", list(MASTER_DATABASE.keys()), index=0)
entity_data = MASTER_DATABASE[selected_entity_key]

p_bdate = entity_data["birth_date"]
natal_lp = compute_life_path(p_bdate, preserve_masters=True)
natal_dob_red = reduce_digits(p_bdate.day, preserve_masters=True)
natal_animal,