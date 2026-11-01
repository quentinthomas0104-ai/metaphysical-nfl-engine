import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Step 4: Verified Multi-Season Ledgers, Checkmark Matrix, & Head-to-Head Clash Forecaster")

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

BEARS_1985_SLATE = [
    {"Week": 1, "Date": datetime.date(1985, 9, 8), "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "38 - 28", "Result": "W", "Diff": 10, "TotalOffYds": 384, "FirstDowns": 22, "TurnoverDiff": "+1", "ThirdDownEff": "7/14 (50.0%)"},
    {"Week": 2, "Date": datetime.date(1985, 9, 15), "DayOfWeek": "Sun", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "20 - 7", "Result": "W", "Diff": 13, "TotalOffYds": 341, "FirstDowns": 19, "TurnoverDiff": "+2", "ThirdDownEff": "6/15 (40.0%)"},
    {"Week": 7, "Date": datetime.date(1985, 10, 21), "DayOfWeek": "Mon", "Opp": "GB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "MNF", "Score": "23 - 7", "Result": "W", "Diff": 16, "TotalOffYds": 390, "FirstDowns": 24, "TurnoverDiff": "+3", "ThirdDownEff": "8/16 (50.0%)"},
    {"Week": 11, "Date": datetime.date(1985, 11, 17), "DayOfWeek": "Sun", "Opp": "DAL", "HomeAway": "@", "Venue": "Texas Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "44 - 0", "Result": "W", "Diff": 44, "TotalOffYds": 425, "FirstDowns": 26, "TurnoverDiff": "+4", "ThirdDownEff": "9/15 (60.0%)"}
]

ALL_32_FRANCHISES = {
    "Chicago Bears": datetime.date(1920, 9, 17),
    "Seattle Seahawks": datetime.date(1974, 6, 4),
    "Tampa Bay Buccaneers": datetime.date(1974, 4, 24),
    "Green Bay Packers": datetime.date(1919, 8, 11),
    "Kansas City Chiefs": datetime.date(1959, 8, 14),
    "Buffalo Bills": datetime.date(1959, 10, 28),
    "Detroit Lions": datetime.date(1930, 7, 12),
    "Minnesota Vikings": datetime.date(1960, 1, 28)
}

MASTER_DATABASE = {
    "Caleb Williams (QB - CHI)": {
        "category": "QB", "name": "Caleb Williams", "pos": "QB", "jersey": "#18",
        "birth_date": datetime.date(2001, 11, 18), "team": "CHI", "exp": "3rd Season (Draft 2024)",
        "seasons": {2026: CALEB_2026_SLATE}
    },
    "Chicago Bears (Franchise)": {
        "category": "FRANCHISE", "name": "Chicago Bears", "pos": "Franchise", "jersey": "—",
        "birth_date": datetime.date(1920, 9, 17), "team": "CHI", "exp": "104 Seasons (Charter APFA)",
        "seasons": {2026: BEARS_2026_SLATE, 1985: BEARS_1985_SLATE}
    },
    "Seattle Seahawks (Franchise)": {
        "category": "FRANCHISE", "name": "Seattle Seahawks", "pos": "Franchise", "jersey": "—",
        "birth_date": datetime.date(1974, 6, 4), "team": "SEA", "exp": "Founded 1974",
        "seasons": {}
    },
    "Tampa Bay Buccaneers (Franchise)": {
        "category": "FRANCHISE", "name": "Tampa Bay Buccaneers", "pos": "Franchise", "jersey": "—",
        "birth_date": datetime.date(1974, 4, 24), "team": "TB", "exp": "Founded 1974",
        "seasons": {}
    }
}

for f_name, f_bdate in ALL_32_FRANCHISES.items():
    f_key = f"{f_name} (Franchise)"
    if f_key not in MASTER_DATABASE:
        MASTER_DATABASE[f_key] = {
            "category": "FRANCHISE", "name": f_name, "pos": "Franchise", "jersey": "—",
            "birth_date": f_bdate, "team": f_name[:3].upper(), "exp": f"Founded {f_bdate.year}",
            "seasons": {}
        }

# ==============================================================================
# SECTION 1: ENTITY SELECTION & METAPHYSICAL PROFILE
# ==============================================================================
st.subheader("1. Entity Selection & Metaphysical Baseline")
selected_entity_key = st.selectbox("Search & Select Subject:", list(MASTER_DATABASE.keys()), index=0)
entity_data = MASTER_DATABASE[selected_entity_key]

natal_birth_date = entity_data["birth_date"]
natal_lp = compute_life_path(natal_birth_date, preserve_masters=True)
natal_dob_red = reduce_digits(natal_birth_date.day, preserve_masters=True)
natal_animal, natal_element, natal_polarity = get_chinese_profile(natal_birth_date.year)
birth_yr_red = reduce_digits(natal_birth_date.year, preserve_masters=False)
base_number = reduce_digits(natal_birth_date.month + reduce_digits(natal_birth_date.day, preserve_masters=False), preserve_masters=False)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Name", entity_data["name"])
c2.metric("Position / Role", entity_data["pos"])
c3.metric("Jersey / ID", entity_data["jersey"])
c4.metric("Birthdate / Inception", natal_birth_date.strftime("%B %d, %Y"))
c5.metric("Life Path Number", f"{natal_lp}")
c6.metric("Chinese Zodiac", f"{natal_element} {natal_animal}")

# ==============================================================================
# SECTION 2: CAREER LEDGER BUILDER
# ==============================================================================
st.markdown("---")
st.subheader(f"2. Multi-Season Career Ledger for {entity_data['name']}")

available_seasons = sorted(list(entity_data["seasons"].keys()), reverse=True)
selected_season_choice = st.selectbox("Filter Season:", [str(s) for s in available_seasons] + ["All Career Seasons"], index=0)

if selected_season_choice == "All Career Seasons":
    target_seasons = available_seasons
else:
    target_seasons = [int(selected_season_choice)]

raw_logs = []
for s in target_seasons:
    raw_logs.extend(entity_data["seasons"].get(s, []))

ledger_rows = []
for g in raw_logs:
    g_date = g["Date"]
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

# Full Career Ledger Display
st.dataframe(df, use_container_width=True)

csv_data = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Export Full Ledger to CSV",
    data=csv_data,
    file_name=f"{entity_data['name'].replace(' ', '_')}_Career_Ledger.csv",
    mime="text/csv",
)

# ==============================================================================
# SECTION 3: CHECKMARK CORRELATION BOX (WITH INSTANT UNCHECK BUTTONS)
# ==============================================================================
st.markdown("---")
st.subheader("⚡ Checkmark Correlation & Trend Matrix")
st.caption("Place a checkmark next to any metrics or stats to correlate them. Select two, several, or all.")

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

if entity_data["category"] == "QB":
    stat_metrics = [
        "Week", "Day of Week", "Opponent", "Home/Away", "Stadium / Venue", "Surface",
        "Final Score", "Result", "Point Diff",
        "CMP", "ATT", "CMP%", "Pass Yds", "Pass TD", "Y/A", "INT", "SCK",
        "Sack Yds Lost", "Fumbles", "Fumbles Lost", "Passer Rating", "QBR",
        "Rush Att", "Rush Yds", "YPC", "Rush TD"
    ]
else:
    stat_metrics = [
        "Week", "Day of Week", "Opponent", "Home/Away", "Stadium / Venue", "Surface",
        "Final Score", "Result", "Point Diff",
        "Total Offense Yds", "First Downs", "Turnover Diff", "3rd Down Eff"
    ]

# Initialize individual session state checkbox keys if not set
for m in metaphysical_metrics:
    k = f"chk_m_{m}"
    if k not in st.session_state:
        st.session_state[k] = (m in ["Power#", "Personal Day (PD)"])

for s in stat_metrics:
    k = f"chk_s_{s}"
    if k not in st.session_state:
        st.session_state[k] = (s in ["Opponent", "Result", "Point Diff"])

# Callback Functions for Instant Checking / Unchecking
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

# Action Buttons Bar
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

# Box 1: Metaphysical Metrics Checkboxes
st.markdown("#### 🔮 Box 1: Metaphysical & Cosmic Metrics")
with st.container():
    meta_cols = st.columns(4)
    for idx, m in enumerate(metaphysical_metrics):
        col = meta_cols[idx % 4]
        col.checkbox(m, key=f"chk_m_{m}")

# Box 2: Game Log & Box Score Stats Checkboxes
st.markdown("#### 🏈 Box 2: Game Log & Box Score Stats")
with st.container():
    stat_cols = st.columns(4)
    for idx, s in enumerate(stat_metrics):
        col = stat_cols[idx % 4]
        col.checkbox(s, key=f"chk_s_{s}")

# Gather Checked Columns
selected_columns = []
for m in metaphysical_metrics:
    if st.session_state.get(f"chk_m_{m}", False):
        selected_columns.append(m)

for s in stat_metrics:
    if st.session_state.get(f"chk_s_{s}", False):
        selected_columns.append(s)

# ==============================================================================
# SECTION 4: CORRELATION VIEW OF SELECTED CHECKED METRICS
# ==============================================================================
st.markdown("---")
st.subheader("📊 Active Correlation Matrix (Your Checked Selections)")

valid_selected = [c for c in selected_columns if c in df.columns]

if len(valid_selected) >= 2:
    st.write(f"**Currently Correlating ({len(valid_selected)} Checked Metrics):** `{', '.join(valid_selected)}`")
    
    correlation_df = df[valid_selected].copy()
    st.dataframe(correlation_df, use_container_width=True)

    if "Result" in valid_selected:
        completed = df[df["Result"].isin(["W", "L"])]
        wins = (completed["Result"] == "W").sum()
        losses = (completed["Result"] == "L").sum()
        win_pct = round((wins / len(completed) * 100), 1) if len(completed) > 0 else 0.0

        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("Games in Dataset", f"{len(df)}")
        rc2.metric("Straight-Up Record (W - L)", f"{wins} - {losses}")
        rc3.metric("Straight-Up Win %", f"{win_pct}%")
else:
    st.info("Place a checkmark next to at least two metrics above to display the active correlation matrix.")

# ==============================================================================
# SECTION 5: STEP 4 HEAD-TO-HEAD CLASH & MATCHUP FORECASTER
# ==============================================================================
st.markdown("---")
st.subheader("5. ⚔️ Head-to-Head Clash & Matchup Edge Forecaster")
st.caption("Compare two teams, coaches, or players side-by-side to calculate pre-game metaphysical advantages.")

# 1-Click Primetime Matchup Loader
with st.expander("⚡ Quick-Load Active 2026 Matchups", expanded=True):
    quick_m = st.selectbox(
        "Select Active Slate Matchup:",
        [
            "Week 8: Chicago Bears @ Seattle Seahawks (MNF - Nov 2, 2026)",
            "Week 9: Tampa Bay Buccaneers @ Chicago Bears (SNF - Nov 8, 2026)"
        ]
    )
    if st.button("Load Matchup Directly"):
        if "Week 8" in quick_m:
            st.session_state["h2h_side_a"] = "Chicago Bears (Franchise)"
            st.session_state["h2h_side_b"] = "Seattle Seahawks (Franchise)"
            st.session_state["h2h_date"] = datetime.date(2026, 11, 2)
        else:
            st.session_state["h2h_side_a"] = "Chicago Bears (Franchise)"
            st.session_state["h2h_side_b"] = "Tampa Bay Buccaneers (Franchise)"
            st.session_state["h2h_date"] = datetime.date(2026, 11, 8)
        st.rerun()

default_a = st.session_state.get("h2h_side_a", list(MASTER_DATABASE.keys())[0])
default_b = st.session_state.get("h2h_side_b", "Seattle Seahawks (Franchise)" if "Seattle Seahawks (Franchise)" in MASTER_DATABASE else list(MASTER_DATABASE.keys())[1])
default_d = st.session_state.get("h2h_date", datetime.date(2026, 11, 2))

c_col1, c_col2, c_col3 = st.columns(3)
with c_col1:
    h2h_a_key = st.selectbox("Side A (Primary):", list(MASTER_DATABASE.keys()), index=list(MASTER_DATABASE.keys()).index(default_a))
with c_col2:
    h2h_b_key = st.selectbox("Side B (Opponent):", list(MASTER_DATABASE.keys()), index=list(MASTER_DATABASE.keys()).index(default_b))
with c_col3:
    h2h_game_date = st.date_input("Kickoff Date:", value=default_d, key="h2h_date_input")

ent_a = MASTER_DATABASE[h2h_a_key]
ent_b = MASTER_DATABASE[h2h_b_key]

# Side A Calculations
a_bdate = ent_a["birth_date"]
a_lp = compute_life_path(a_bdate, preserve_masters=True)
a_dob_red = reduce_digits(a_bdate.day, preserve_masters=True)
a_animal, a_elem, _ = get_chinese_profile(a_bdate.year)
a_base = reduce_digits(a_bdate.month + reduce_digits(a_bdate.day, preserve_masters=False), preserve_masters=False)

a_bday_yr = datetime.date(h2h_game_date.year, a_bdate.month, a_bdate.day)
a_flipped = h2h_game_date >= a_bday_yr
a_cyc = h2h_game_date.year if a_flipped else h2h_game_date.year - 1
a_py = reduce_digits(a_base + reduce_digits(a_cyc, preserve_masters=False), preserve_masters=False)
a_pm = reduce_digits(a_py + h2h_game_date.month, preserve_masters=False)
a_pd = reduce_digits(a_pm + reduce_digits(h2h_game_date.day, preserve_masters=False), preserve_masters=False)

# Side B Calculations
b_bdate = ent_b["birth_date"]
b_lp = compute_life_path(b_bdate, preserve_masters=True)
b_dob_red = reduce_digits(b_bdate.day, preserve_masters=True)
b_animal, b_elem, _ = get_chinese_profile(b_bdate.year)
b_base = reduce_digits(b_bdate.month + reduce_digits(b_bdate.day, preserve_masters=False), preserve_masters=False)

b_bday_yr = datetime.date(h2h_game_date.year, b_bdate.month, b_bdate.day)
b_flipped = h2h_game_date >= b_bday_yr
b_cyc = h2h_game_date.year if b_flipped else h2h_game_date.year - 1
b_py = reduce_digits(b_base + reduce_digits(b_cyc, preserve_masters=False), preserve_masters=False)
b_pm = reduce_digits(b_py + h2h_game_date.month, preserve_masters=False)
b_pd = reduce_digits(b_pm + reduce_digits(h2h_game_date.day, preserve_masters=False), preserve_masters=False)

# Kickoff Vibrations
g_power = reduce_digits(h2h_game_date.day, preserve_masters=True)
g_uy = reduce_digits(h2h_game_date.year, preserve_masters=False)
g_ud = reduce_digits(reduce_digits(g_uy + h2h_game_date.month, preserve_masters=False) + reduce_digits(h2h_game_date.day, preserve_masters=False), preserve_masters=False)
g_animal, g_elem, _ = get_chinese_profile(h2h_game_date.year)

a_aff = evaluate_affinity(a_animal, g_animal)
b_aff = evaluate_affinity(b_animal, g_animal)

st.markdown(f"#### 🛡️ Matchup Comparison: {ent_a['name']} vs. {ent_b['name']}")
h_col1, h_col2, h_col3 = st.columns([2, 1, 2])
with h_col1:
    st.markdown(f"##### 🔵 {ent_a['name']} ({ent_a['team']})")
    st.write(f"**Natal Life Path:** {a_lp} | **Day of Birth Reduced:** {a_dob_red}")
    st.write(f"**Chinese Sign:** {a_elem} {a_animal} ({a_aff})")
    st.metric("Personal Day (PD)", f"{a_pd}")
    st.metric("Personal Year (PY)", f"{a_py}")

with h_col2:
    st.markdown("##### ⚡ Game Kickoff")
    st.metric("Power#", f"{g_power}")
    st.metric("Universal Day (UD)", f"{g_ud}")
    st.write(f"**Year Animal:** {g_elem} {g_animal}")

with h_col3:
    st.markdown(f"##### 🔴 {ent_b['name']} ({ent_b['team']})")
    st.write(f"**Natal Life Path:** {b_lp} | **Day of Birth Reduced:** {b_dob_red}")
    st.write(f"**Chinese Sign:** {b_elem} {b_animal} ({b_aff})")
    st.metric("Personal Day (PD)", f"{b_pd}")
    st.metric("Personal Year (PY)", f"{b_py}")

# Edge Scoring Algorithm
st.markdown("---")
st.markdown("### 🏆 Pre-Game Metaphysical Advantage Scorecard")
a_score, b_score = 0, 0
reasons = []

if a_pd == g_power or a_pd == g_ud:
    a_score += 2
    reasons.append(f"🔵 **{ent_a['name']}** holds a direct Personal Day alignment with Kickoff ({a_pd}).")
if b_pd == g_power or b_pd == g_ud:
    b_score += 2
    reasons.append(f"🔴 **{ent_b['name']}** holds a direct Personal Day alignment with Kickoff ({b_pd}).")

if "San He" in a_aff or "Liu He" in a_aff:
    a_score += 2
    reasons.append(f"🔵 **{ent_a['name']}** operates in a harmonious Chinese astrological year ({a_aff}).")
elif "Chong" in a_aff or "Xing" in a_aff:
    a_score -= 2
    reasons.append(f"⚠️ **{ent_a['name']}** operates under astrological friction ({a_aff}).")

if "San He" in b_aff or "Liu He" in b_aff:
    b_score += 2
    reasons.append(f"🔴 **{ent_b['name']}** operates in a harmonious Chinese astrological year ({b_aff}).")
elif "Chong" in b_aff or "Xing" in b_aff:
    b_score -= 2
    reasons.append(f"⚠️ **{ent_b['name']}** operates under astrological friction ({b_aff}).")

if a_score > b_score:
    st.success(f"**Verdict:** Metaphysical Advantage favors **{ent_a['name']}** (Score: {a_score} vs. {b_score})")
elif b_score > a_score:
    st.error(f"**Verdict:** Metaphysical Advantage favors **{ent_b['name']}** (Score: {b_score} vs. {a_score})")
else:
    st.info(f"**Verdict:** Neutral / Balanced Metaphysical Equilibrium (Score: {a_score} vs. {b_score})")

for r in reasons:
    st.markdown(f"- {r}")