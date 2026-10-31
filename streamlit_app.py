import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Pure Cosmic Cycles: Complete Official Box Score Metrics, Dedicated Transits, Power#, & Cross-Resonance Scanner")

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
# 4. OFFICIAL VERIFIED 2026 & HISTORICAL DATA REPOSITORY
# ==============================================================================
BEARS_2026_SLATE = [
    {"Week": 1, "Date": datetime.date(2026, 9, 13), "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "@", "Venue": "Bank of America Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "59 - 37", "Result": "W", "Diff": "+22", "TotalOffYds": 552, "FirstDowns": 26, "TurnoverDiff": "+2", "ThirdDownEff": "10/14 (71.4%)"},
    {"Week": 2, "Date": datetime.date(2026, 9, 20), "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 9", "Result": "L", "Diff": "-6", "TotalOffYds": 248, "FirstDowns": 14, "TurnoverDiff": "-1", "ThirdDownEff": "3/13 (23.1%)"},
    {"Week": 3, "Date": datetime.date(2026, 9, 28), "DayOfWeek": "Mon", "Opp": "PHI", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "MNF", "Score": "27 - 7", "Result": "W", "Diff": "+20", "TotalOffYds": 374, "FirstDowns": 20, "TurnoverDiff": "+3", "ThirdDownEff": "6/14 (42.9%)"},
    {"Week": 4, "Date": datetime.date(2026, 10, 4), "DayOfWeek": "Sun", "Opp": "NYJ", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "23 - 12", "Result": "W", "Diff": "+11", "TotalOffYds": 492, "FirstDowns": 24, "TurnoverDiff": "+1", "ThirdDownEff": "7/15 (46.7%)"},
    {"Week": 5, "Date": datetime.date(2026, 10, 11), "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "@", "Venue": "Lambeau Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "7 - 31", "Result": "L", "Diff": "-24", "TotalOffYds": 238, "FirstDowns": 12, "TurnoverDiff": "-2", "ThirdDownEff": "2/11 (18.2%)"},
    {"Week": 6, "Date": datetime.date(2026, 10, 18), "DayOfWeek": "Sun", "Opp": "ATL", "HomeAway": "@", "Venue": "Mercedes-Benz Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "31 - 23", "Result": "W", "Diff": "+8", "TotalOffYds": 421, "FirstDowns": 23, "TurnoverDiff": "+1", "ThirdDownEff": "8/14 (57.1%)"},
    {"Week": 7, "Date": datetime.date(2026, 10, 22), "DayOfWeek": "Thu", "Opp": "NE", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "TNF", "Score": "30 - 24", "Result": "W", "Diff": "+6", "TotalOffYds": 405, "FirstDowns": 22, "TurnoverDiff": "0", "ThirdDownEff": "6/13 (46.2%)"},
    {"Week": 8, "Date": datetime.date(2026, 11, 2), "DayOfWeek": "Mon", "Opp": "SEA", "HomeAway": "@", "Venue": "Lumen Field", "Surface": "Turf", "GameTime": "MNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending", "TotalOffYds": 0, "FirstDowns": 0, "TurnoverDiff": "0", "ThirdDownEff": "Pending"},
    {"Week": 9, "Date": datetime.date(2026, 11, 8), "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "SNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending", "TotalOffYds": 0, "FirstDowns": 0, "TurnoverDiff": "0", "ThirdDownEff": "Pending"}
]

CALEB_2026_SLATE = [
    {
        "Week": 1, "Date": datetime.date(2026, 9, 13), "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "@",
        "Venue": "Bank of America Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "59 - 37", "Result": "W", "Diff": "+22",
        "CMP": 21, "ATT": 29, "CMP%": 72.4, "Pass Yds": 269, "Pass TD": 2, "Y/A": 9.3,
        "INT": 0, "SCK": 2, "Sack Yds Lost": 14, "Fumbles": 0, "Fumbles Lost": 0,
        "Passer Rating": 124.1, "QBR": 88.4,
        "Rush Att": 10, "Rush Yds": 65, "YPC": 6.5, "Rush TD": 2
    },
    {
        "Week": 2, "Date": datetime.date(2026, 9, 20), "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "vs",
        "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "3 - 9", "Result": "L", "Diff": "-6",
        "CMP": 15, "ATT": 26, "CMP%": 57.7, "Pass Yds": 138, "Pass TD": 0, "Y/A": 5.3,
        "INT": 1, "SCK": 3, "Sack Yds Lost": 21, "Fumbles": 1, "Fumbles Lost": 0,
        "Passer Rating": 56.2, "QBR": 38.1,
        "Rush Att": 5, "Rush Yds": 42, "YPC": 8.4, "Rush TD": 0
    },
    {
        "Week": 6, "Date": datetime.date(2026, 10, 18), "DayOfWeek": "Sun", "Opp": "ATL", "HomeAway": "@",
        "Venue": "Mercedes-Benz Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "31 - 23", "Result": "W", "Diff": "+8",
        "CMP": 30, "ATT": 36, "CMP%": 83.3, "Pass Yds": 305, "Pass TD": 1, "Y/A": 8.5,
        "INT": 0, "SCK": 4, "Sack Yds Lost": 26, "Fumbles": 1, "Fumbles Lost": 0,
        "Passer Rating": 111.2, "QBR": 79.5,
        "Rush Att": 4, "Rush Yds": 3, "YPC": 0.8, "Rush TD": 0
    },
    {
        "Week": 7, "Date": datetime.date(2026, 10, 22), "DayOfWeek": "Thu", "Opp": "NE", "HomeAway": "vs",
        "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "TNF", "Score": "30 - 24", "Result": "W", "Diff": "+6",
        "CMP": 22, "ATT": 33, "CMP%": 66.7, "Pass Yds": 308, "Pass TD": 2, "Y/A": 9.3,
        "INT": 0, "SCK": 3, "Sack Yds Lost": 19, "Fumbles": 0, "Fumbles Lost": 0,
        "Passer Rating": 116.7, "QBR": 84.2,
        "Rush Att": 5, "Rush Yds": 18, "YPC": 3.6, "Rush TD": 0
    },
    {
        "Week": 8, "Date": datetime.date(2026, 11, 2), "DayOfWeek": "Mon", "Opp": "SEA", "HomeAway": "@",
        "Venue": "Lumen Field", "Surface": "Turf", "GameTime": "MNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending",
        "CMP": 0, "ATT": 0, "CMP%": 0.0, "Pass Yds": 0, "Pass TD": 0, "Y/A": 0.0,
        "INT": 0, "SCK": 0, "Sack Yds Lost": 0, "Fumbles": 0, "Fumbles Lost": 0,
        "Passer Rating": 0.0, "QBR": 0.0,
        "Rush Att": 0, "Rush Yds": 0, "YPC": 0.0, "Rush TD": 0
    },
    {
        "Week": 9, "Date": datetime.date(2026, 11, 8), "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs",
        "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "SNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending",
        "CMP": 0, "ATT": 0, "CMP%": 0.0, "Pass Yds": 0, "Pass TD": 0, "Y/A": 0.0,
        "INT": 0, "SCK": 0, "Sack Yds Lost": 0, "Fumbles": 0, "Fumbles Lost": 0,
        "Passer Rating": 0.0, "QBR": 0.0,
        "Rush Att": 0, "Rush Yds": 0, "YPC": 0.0, "Rush TD": 0
    }
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
        "seasons": {2026: BEARS_2026_SLATE}
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
    },
    "Josh Allen (QB - BUF)": {
        "category": "QB", "name": "Josh Allen", "pos": "QB", "jersey": "#17",
        "birth_date": datetime.date(1996, 5, 21), "team": "BUF", "exp": "7th Season",
        "seasons": {
            2024: [
                {
                    "Week": 1, "Date": datetime.date(2024, 9, 8), "DayOfWeek": "Sun", "Opp": "ARI", "HomeAway": "vs",
                    "Venue": "Highmark Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "34 - 28", "Result": "W", "Diff": "+6",
                    "CMP": 18, "ATT": 23, "CMP%": 78.3, "Pass Yds": 232, "Pass TD": 2, "Y/A": 10.1,
                    "INT": 0, "SCK": 2, "Sack Yds Lost": 14, "Fumbles": 0, "Fumbles Lost": 0,
                    "Passer Rating": 137.7, "QBR": 86.4,
                    "Rush Att": 9, "Rush Yds": 39, "YPC": 4.3, "Rush TD": 2
                }
            ]
        }
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

p_bdate = entity_data["birth_date"]
natal_lp = compute_life_path(p_bdate, preserve_masters=True)
natal_dob_red = reduce_digits(p_bdate.day, preserve_masters=True)
natal_animal, natal_element, natal_polarity = get_chinese_profile(p_bdate.year)
birth_yr_red = reduce_digits(p_bdate.year, preserve_masters=False)
base_number = reduce_digits(p_bdate.month + reduce_digits(p_bdate.day, preserve_masters=False), preserve_masters=False)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Name", entity_data["name"])
c2.metric("Position / Role", entity_data["pos"])
c3.metric("Jersey / ID", entity_data["jersey"])
c4.metric("Birthdate / Inception", p_bdate.strftime("%B %d, %Y"))
c5.metric("Life Path Number", f"{natal_lp}")
c6.metric("Chinese Zodiac", f"{natal_element} {natal_animal}")

# ==============================================================================
# SECTION 2: MULTI-SEASON CAREER LEDGER (COMPLETE OFFICIAL BOX SCORE METRICS)
# ==============================================================================
st.markdown("---")
st.subheader(f"2. Career Ledger for {entity_data['name']}")

available_seasons = sorted(list(entity_data["seasons"].keys()), reverse=True)
if available_seasons:
    season_options = [str(s) for s in available_seasons] + ["All Career Seasons"]
    selected_season_choice = st.selectbox("Filter Season:", season_options, index=0)
else:
    selected_season_choice = st.selectbox("Filter Season:", ["No Seasons Loaded"], index=0)

if selected_season_choice == "All Career Seasons":
    target_seasons = available_seasons
elif selected_season_choice in [str(s) for s in available_seasons]:
    target_seasons = [int(selected_season_choice)]
else:
    target_seasons = []

raw_logs = []
for s in target_seasons:
    raw_logs.extend(entity_data["seasons"].get(s, []))

ledger_rows = []
for g in raw_logs:
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
    is_pending = g.get("Result") == "Pending"
    
    # PURE CROSS-RESONANCE (NO STAT REDUCTIONS)
    pd_power_match = (pd_val == power_num)
    pd_ud_match = (pd_val == ud)
    lp_match = (natal_lp == game_lp)
    
    if is_pending:
        match_str = "⏳ Kickoff Pending"
    elif pd_power_match and pd_ud_match:
        match_str = "⚡ DUAL MATCH (PD = Power# & UD)"
    elif pd_power_match:
        match_str = "⚡ POWER# RESONANCE (PD = Power#)"
    elif pd_ud_match:
        match_str = "🌐 UNIVERSAL HARMONY (PD = UD)"
    elif lp_match:
        match_str = "✨ LIFE PATH RESONANCE"
    else:
        match_str = "—"
        
    row = {
        "Season": g.get("Season", g_date.year), "Week": g.get("Week"), "Date": g_date.strftime("%Y-%m-%d"),
        "Day of Week": g.get("DayOfWeek"), "Opponent": g.get("Opp"), "Home/Away": g.get("HomeAway"),
        "Stadium / Venue": g.get("Venue"), "Surface": g.get("Surface"), "Game Time": g.get("GameTime"),
        "Final Score": g.get("Score"), "Result": g.get("Result"), "Point Diff": g.get("Diff"),
    }
    
    # Complete Official Box Score Metrics
    if cat == "QB":
        row.update({
            # Passing Volume
            "CMP": g.get("CMP") if not is_pending else "—",
            "ATT": g.get("ATT") if not is_pending else "—",
            "CMP%": f"{g.get('CMP%')}%" if not is_pending else "—",
            # Passing Production
            "Pass Yds": g.get("Pass Yds") if not is_pending else "—",
            "Pass TD": g.get("Pass TD") if not is_pending else "—",
            "Y/A": g.get("Y/A") if not is_pending else "—",
            # Negative & Turnover Metrics
            "INT": g.get("INT") if not is_pending else "—",
            "SCK": g.get("SCK") if not is_pending else "—",
            "Sack Yds Lost": g.get("Sack Yds Lost") if not is_pending else "—",
            "Fumbles": g.get("Fumbles") if not is_pending else "—",
            "Fumbles Lost": g.get("Fumbles Lost") if not is_pending else "—",
            # Efficiency
            "Passer Rating": g.get("Passer Rating") if not is_pending else "—",
            "QBR": g.get("QBR") if not is_pending else "—",
            # Rushing
            "Rush Att": g.get("Rush Att") if not is_pending else "—",
            "Rush Yds": g.get("Rush Yds") if not is_pending else "—",
            "YPC": g.get("YPC") if not is_pending else "—",
            "Rush TD": g.get("Rush TD") if not is_pending else "—",
        })
    elif cat == "FRANCHISE":
        row.update({
            "Total Offense Yds": g.get("TotalOffYds") if not is_pending else "—",
            "First Downs": g.get("FirstDowns") if not is_pending else "—",
            "Turnover Diff": g.get("TurnoverDiff") if not is_pending else "—",
            "3rd Down Eff": g.get("ThirdDownEff") if not is_pending else "—",
        })

    # Metaphysical Cycles & Alignment
    row.update({
        "Life Path Number": natal_lp, "Day of Birth Reduced": natal_dob_red,
        "Chinese Zodiac Animal": natal_animal, "Fixed / Heavenly Element": natal_element,
        "Yin / Yang Polarity": natal_polarity, "Birth Year Reduction": birth_yr_red,
        "Flip Status": "Flipped" if has_flipped else "Pre-Flip", "Game Day Life Path": game_lp,
        "Power#": power_num, "Game Year Animal & Element": f"{g_element} {g_animal}",
        "Affinity Status": affinity, "Universal Year (UY)": uy, "Universal Month (UM)": um,
        "Universal Day (UD)": ud, "Personal Year (PY)": py, "Personal Month (PM)": pm,
        "Personal Day (PD)": pd_val, "Cross-Resonance Match": match_str,
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
    })
    ledger_rows.append(row)

df = pd.DataFrame(ledger_rows)

if not df.empty:
    with st.expander("⚡ Pure Cross-Resonance Scanner & Filter Controls", expanded=True):
        f_c1, f_c2, f_c3, f_c4 = st.columns(4)
        with f_c1:
            scanner_match_type = st.selectbox(
                "Resonance Filter:",
                ["All Games", "Any Resonance Hit", "Dual Match (PD = Power# & UD)", "Power# Resonance", "Universal Harmony", "Life Path Resonance"]
            )
        with f_c2:
            all_powers = ["All"] + sorted([str(p) for p in df["Power#"].unique() if pd.notna(p)])
            selected_power = st.selectbox("Filter by Power#:", all_powers, index=0)
        with f_c3:
            all_affinities = ["All"] + sorted([str(a) for a in df["Affinity Status"].unique() if pd.notna(a)])
            selected_affinity = st.selectbox("Filter Chinese Affinity:", all_affinities, index=0)
        with f_c4:
            all_results = ["All", "W", "L", "Pending"]
            selected_result = st.selectbox("Filter Game Result:", all_results, index=0)

    filtered_df = df.copy()
    if scanner_match_type == "Any Resonance Hit":
        filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("MATCH|RESONANCE|HARMONY")]
    elif scanner_match_type == "Dual Match (PD = Power# & UD)":
        filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("DUAL MATCH")]
    elif scanner_match_type == "Power# Resonance":
        filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("POWER# RESONANCE")]
    elif scanner_match_type == "Universal Harmony":
        filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("UNIVERSAL HARMONY")]
    elif scanner_match_type == "Life Path Resonance":
        filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("LIFE PATH RESONANCE")]

    if selected_power != "All":
        filtered_df = filtered_df[filtered_df["Power#"].astype(str) == selected_power]
    if selected_affinity != "All":
        filtered_df = filtered_df[filtered_df["Affinity Status"] == selected_affinity]
    if selected_result != "All":
        filtered_df = filtered_df[filtered_df["Result"] == selected_result]

    def apply_visual_highlights(row):
        styles = [''] * len(row)
        m_val = str(row.get("Cross-Resonance Match", ""))
        if "DUAL MATCH" in m_val:
            match_idx = row.index.get_loc("Cross-Resonance Match")
            styles[match_idx] = 'background-color: #064e3b; color: #6ee7b7; font-weight: bold;'
        elif "RESONANCE" in m_val or "HARMONY" in m_val:
            match_idx = row.index.get_loc("Cross-Resonance Match")
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

    # Metrics Summary Bar
    st.markdown("### 📊 Correlation Overview")
    m1, m2, m3, m4 = st.columns(4)
    total_g = len(filtered_df)
    num_hits = len(filtered_df[filtered_df["Cross-Resonance Match"].str.contains("MATCH|RESONANCE|HARMONY")]) if total_g > 0 else 0
    pos_astrology = len(filtered_df[filtered_df["Affinity Status"].str.contains("San He|Liu He")]) if total_g > 0 else 0
    m1.metric("Games Displayed", f"{total_g}")
    m2.metric("Cross-Resonance Hits", f"{num_hits}")
    m3.metric("Favorable Astrology Cycles", f"{pos_astrology}")
    m4.metric("Resonance Hit Rate", f"{round(num_hits/total_g*100, 1) if total_g > 0 else 0}%")

    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Ledger to CSV",
        data=csv_data,
        file_name=f"{entity_data['name'].replace(' ', '_')}_Metaphysical_Ledger.csv",
        mime="text/csv",
    )
else:
    st.info("No season loaded for this entity.")

# ==============================================================================
# SECTION 3: HEAD-TO-HEAD CLASH & EDGE ENGINE
# ==============================================================================
st.markdown("---")
st.subheader("3. ⚔️ Head-to-Head Clash & Edge Engine")
st.caption("Compare two teams, coaches, or quarterbacks side-by-side to evaluate the metaphysical edge.")

col_c1, col_c2, col_c3 = st.columns(3)
with col_c1:
    ent_a_key = st.selectbox("Primary Subject (Side A):", list(MASTER_DATABASE.keys()), index=0, key="clash_a")
with col_c2:
    default_b_idx = list(MASTER_DATABASE.keys()).index("Seattle Seahawks (Franchise)") if "Seattle Seahawks (Franchise)" in MASTER_DATABASE else 1
    ent_b_key = st.selectbox("Opposing Subject (Side B):", list(MASTER_DATABASE.keys()), index=default_b_idx, key="clash_b")
with col_c3:
    matchup_date = st.date_input("Matchup Kickoff Date:", value=datetime.date(2026, 11, 2), key="clash_date_picker")

ent_a = MASTER_DATABASE[ent_a_key]
ent_b = MASTER_DATABASE[ent_b_key]

# Side A Calculations
a_bdate = ent_a["birth_date"]
a_lp = compute_life_path(a_bdate, preserve_masters=True)
a_animal, a_elem, _ = get_chinese_profile(a_bdate.year)
a_base = reduce_digits(a_bdate.month + reduce_digits(a_bdate.day, preserve_masters=False), preserve_masters=False)

a_bday_yr = datetime.date(matchup_date.year, a_bdate.month, a_bdate.day)
a_flipped = matchup_date >= a_bday_yr
a_cyc = matchup_date.year if a_flipped else matchup_date.year - 1
a_py = reduce_digits(a_base + reduce_digits(a_cyc, preserve_masters=False), preserve_masters=False)
a_pm = reduce_digits(a_py + matchup_date.month, preserve_masters=False)
a_pd = reduce_digits(a_pm + reduce_digits(matchup_date.day, preserve_masters=False), preserve_masters=False)

# Side B Calculations
b_bdate = ent_b["birth_date"]
b_lp = compute_life_path(b_bdate, preserve_masters=True)
b_animal, b_elem, _ = get_chinese_profile(b_bdate.year)
b_base = reduce_digits(b_bdate.month + reduce_digits(b_bdate.day, preserve_masters=False), preserve_masters=False)

b_bday_yr = datetime.date(matchup_date.year, b_bdate.month, b_bdate.day)
b_flipped = matchup_date >= b_bday_yr
b_cyc = matchup_date.year if b_flipped else matchup_date.year - 1
b_py = reduce_digits(b_base + reduce_digits(b_cyc, preserve_masters=False), preserve_masters=False)
b_pm = reduce_digits(b_py + matchup_date.month, preserve_masters=False)
b_pd = reduce_digits(b_pm + reduce_digits(matchup_date.day, preserve_masters=False), preserve_masters=False)

# Kickoff Cycles
g_power = reduce_digits(matchup_date.day, preserve_masters=True)
g_uy = reduce_digits(matchup_date.year, preserve_masters=False)
g_ud = reduce_digits(reduce_digits(g_uy + matchup_date.month, preserve_masters=False) + reduce_digits(matchup_date.day, preserve_masters=False), preserve_masters=False)
g_animal, g_elem, _ = get_chinese_profile(matchup_date.year)

a_aff = evaluate_affinity(a_animal, g_animal)
b_aff = evaluate_affinity(b_animal, g_animal)

st.markdown(f"#### 🛡️ Matchup Comparison: {ent_a['name']} vs. {ent_b['name']}")
comp_c1, comp_c2, comp_c3 = st.columns([2, 1, 2])
with comp_c1:
    st.markdown(f"##### 🔵 {ent_a['name']} ({ent_a['team']})")
    st.write(f"**Natal Life Path:** {a_lp} | **Chinese Sign:** {a_elem} {a_animal}")
    st.write(f"**Season Alignment:** {a_aff}")
    st.metric("Personal Day (PD)", f"{a_pd}")
    st.metric("Personal Year (PY)", f"{a_py}")

with comp_c2:
    st.markdown("##### ⚡ Game Kickoff")
    st.metric("Power#", f"{g_power}")
    st.metric("Universal Day (UD)", f"{g_ud}")
    st.write(f"**Year Animal:** {g_elem} {g_animal}")

with comp_c3:
    st.markdown(f"##### 🔴 {ent_b['name']} ({ent_b['team']})")
    st.write(f"**Natal Life Path:** {b_lp} | **Chinese Sign:** {b_elem} {b_animal}")
    st.write(f"**Season Alignment:** {b_aff}")
    st.metric("Personal Day (PD)", f"{b_pd}")
    st.metric("Personal Year (PY)", f"{b_py}")

# Edge Scoring
st.markdown("---")
st.markdown("### 🏆 Pre-Game Metaphysical Advantage Verdict")
a_score, b_score = 0, 0
reasons = []

if a_pd == g_power or a_pd == g_ud:
    a_score += 2
    reasons.append(f"🔵 **{ent_a['name']}** holds a direct Personal Day alignment with the Kickoff Day ({a_pd}).")
if b_pd == g_power or b_pd == g_ud:
    b_score += 2
    reasons.append(f"🔴 **{ent_b['name']}** holds a direct Personal Day alignment with the Kickoff Day ({b_pd}).")

if "San He" in a_aff or "Liu He" in a_aff:
    a_score += 2
    reasons.append(f"🔵 **{ent_a['name']}** benefits from a harmonious Chinese astrological year ({a_aff}).")
elif "Chong" in a_aff or "Xing" in a_aff:
    a_score -= 2
    reasons.append(f"⚠️ **{ent_a['name']}** operates under astrological friction ({a_aff}).")

if "San He" in b_aff or "Liu He" in b_aff:
    b_score += 2
    reasons.append(f"🔴 **{ent_b['name']}** benefits from a harmonious Chinese astrological year ({b_aff}).")
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