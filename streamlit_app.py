import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Historical Game Logs, Birthday-Flip Cycles, Numerology & Planetary Transits")

# --- 1. CORE NUMEROLOGY & REDUCTION FUNCTIONS ---
def reduce_digits(n: int, preserve_masters: bool = False) -> int:
    """Reduces an integer to a single digit (1-9), optionally preserving master numbers."""
    if preserve_masters and n in [11, 22, 33]:
        return n
    while n > 9:
        if preserve_masters and n in [11, 22, 33]:
            return n
        n = sum(int(d) for d in str(n))
    return n

# --- 2. WESTERN & CHINESE ASTROLOGY CALCULATORS ---
ZODIAC_SIGNS = [
    ("Capricorn", (1, 1), (1, 19), "Earth"),
    ("Aquarius", (1, 20), (2, 18), "Air"),
    ("Pisces", (2, 19), (3, 20), "Water"),
    ("Aries", (3, 21), (4, 19), "Fire"),
    ("Taurus", (4, 20), (5, 20), "Earth"),
    ("Gemini", (5, 21), (6, 20), "Air"),
    ("Cancer", (6, 21), (7, 22), "Water"),
    ("Leo", (7, 23), (8, 22), "Fire"),
    ("Virgo", (8, 23), (9, 22), "Earth"),
    ("Libra", (9, 23), (10, 22), "Air"),
    ("Scorpio", (10, 23), (11, 21), "Water"),
    ("Sagittarius", (11, 22), (12, 21), "Fire"),
    ("Capricorn", (12, 22), (12, 31), "Earth"),
]

def get_western_sun_sign(month: int, day: int):
    for sign, start, end, element in ZODIAC_SIGNS:
        if (month == start[0] and day >= start[1]) or (month == end[0] and day <= end[1]):
            return sign, element
    return "Gemini", "Air"

def approximate_sun_longitude(d: datetime.date) -> float:
    day_of_year = d.timetuple().tm_yday
    return ((day_of_year - 79) * 360 / 365.25) % 360

def get_aspect(deg1: float, deg2: float):
    diff = abs(deg1 - deg2) % 360
    if diff > 180:
        diff = 360 - diff
    orb = 8.0
    if abs(diff - 0) <= orb:
        return "Conjunction (0°)"
    elif abs(diff - 60) <= orb:
        return "Sextile (60°)"
    elif abs(diff - 90) <= orb:
        return "Square (90°)"
    elif abs(diff - 120) <= orb:
        return "Trine (120°)"
    elif abs(diff - 180) <= orb:
        return "Opposition (180°)"
    return "No Major Aspect"

CHINESE_ZODIAC = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
CHINESE_ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

def get_chinese_zodiac(year: int):
    zodiac_idx = (year - 4) % 12
    element_idx = ((year - 4) // 2) % 5
    return CHINESE_ELEMENTS[element_idx], CHINESE_ZODIAC[zodiac_idx]

# --- 3. VERIFIED PROFILES & INSTANT STATS LEDGER ---
VERIFIED_PLAYERS = {
    "Josh Allen (QB - BUF)": {
        "name": "Josh Allen",
        "birth_date": datetime.date(1996, 5, 21),
        "position": "QB",
        "team": "BUF",
        "logs": [
            {"Season": 2024, "Week": 1, "Date": datetime.date(2024, 9, 8), "Opp": "ARI", "PassYds": 232, "RushYds": 39, "TDs": 4, "FPts": 31.2},
            {"Season": 2024, "Week": 2, "Date": datetime.date(2024, 9, 12), "Opp": "MIA", "PassYds": 139, "RushYds": 2, "TDs": 1, "FPts": 11.8},
            {"Season": 2024, "Week": 3, "Date": datetime.date(2024, 9, 23), "Opp": "JAX", "PassYds": 263, "RushYds": 44, "TDs": 4, "FPts": 30.9},
            {"Season": 2024, "Week": 4, "Date": datetime.date(2024, 9, 29), "Opp": "BAL", "PassYds": 180, "RushYds": 21, "TDs": 0, "FPts": 9.3},
            {"Season": 2024, "Week": 5, "Date": datetime.date(2024, 10, 6), "Opp": "HOU", "PassYds": 131, "RushYds": 54, "TDs": 1, "FPts": 14.6},
            {"Season": 2024, "Week": 6, "Date": datetime.date(2024, 10, 14), "Opp": "NYJ", "PassYds": 215, "RushYds": 18, "TDs": 3, "FPts": 24.4},
            {"Season": 2024, "Week": 7, "Date": datetime.date(2024, 10, 20), "Opp": "TEN", "PassYds": 323, "RushYds": 1, "TDs": 2, "FPts": 21.0},
            {"Season": 2024, "Week": 8, "Date": datetime.date(2024, 10, 27), "Opp": "SEA", "PassYds": 283, "RushYds": 25, "TDs": 2, "FPts": 21.8},
            {"Season": 2024, "Week": 9, "Date": datetime.date(2024, 11, 3), "Opp": "MIA", "PassYds": 235, "RushYds": 7, "TDs": 3, "FPts": 22.1},
            {"Season": 2024, "Week": 10, "Date": datetime.date(2024, 11, 10), "Opp": "IND", "PassYds": 280, "RushYds": 50, "TDs": 1, "FPts": 20.2},
            {"Season": 2024, "Week": 11, "Date": datetime.date(2024, 11, 17), "Opp": "KC", "PassYds": 262, "RushYds": 55, "TDs": 2, "FPts": 24.0},
            {"Season": 2024, "Week": 13, "Date": datetime.date(2024, 12, 1), "Opp": "SF", "PassYds": 208, "RushYds": 18, "TDs": 3, "FPts": 26.1},
            {"Season": 2024, "Week": 14, "Date": datetime.date(2024, 12, 8), "Opp": "LAR", "PassYds": 342, "RushYds": 82, "TDs": 6, "FPts": 43.9},
            {"Season": 2024, "Week": 15, "Date": datetime.date(2024, 12, 15), "Opp": "DET", "PassYds": 362, "RushYds": 44, "TDs": 4, "FPts": 32.9},
            {"Season": 2024, "Week": 16, "Date": datetime.date(2024, 12, 22), "Opp": "NE", "PassYds": 154, "RushYds": 36, "TDs": 2, "FPts": 17.8},
            {"Season": 2024, "Week": 17, "Date": datetime.date(2024, 12, 29), "Opp": "NYJ", "PassYds": 124, "RushYds": 43, "TDs": 3, "FPts": 21.3},
        ]
    },
    "Patrick Mahomes (QB - KC)": {
        "name": "Patrick Mahomes",
        "birth_date": datetime.date(1995, 9, 17),
        "position": "QB",
        "team": "KC",
        "logs": [
            {"Season": 2024, "Week": 1, "Date": datetime.date(2024, 9, 5), "Opp": "BAL", "PassYds": 291, "RushYds": 3, "TDs": 1, "FPts": 16.9},
            {"Season": 2024, "Week": 2, "Date": datetime.date(2024, 9, 15), "Opp": "CIN", "PassYds": 151, "RushYds": 29, "TDs": 2, "FPts": 13.9},
            {"Season": 2024, "Week": 3, "Date": datetime.date(2024, 9, 22), "Opp": "ATL", "PassYds": 217, "RushYds": 17, "TDs": 2, "FPts": 16.4},
            {"Season": 2024, "Week": 4, "Date": datetime.date(2024, 9, 29), "Opp": "LAC", "PassYds": 245, "RushYds": 12, "TDs": 1, "FPts": 14.0},
        ]
    },
    "Lamar Jackson (QB - BAL)": {
        "name": "Lamar Jackson",
        "birth_date": datetime.date(1997, 1, 7),
        "position": "QB",
        "team": "BAL",
        "logs": [
            {"Season": 2024, "Week": 1, "Date": datetime.date(2024, 9, 5), "Opp": "KC", "PassYds": 273, "RushYds": 122, "TDs": 1, "FPts": 25.1},
            {"Season": 2024, "Week": 2, "Date": datetime.date(2024, 9, 15), "Opp": "LV", "PassYds": 247, "RushYds": 45, "TDs": 1, "FPts": 18.4},
        ]
    }
}

# --- 4. PLAYER PROFILE SETUP ---
st.subheader("1. NFL Player & Profile Selection")

player_choice = st.selectbox("Search & Select Player:", list(VERIFIED_PLAYERS.keys()), index=0)
player_data = VERIFIED_PLAYERS[player_choice]

p_name = player_data["name"]
p_bdate = player_data["birth_date"]
p_pos = player_data["position"]
p_team = player_data["team"]

# Baseline Calculations
b_month = p_bdate.month
b_day_reduced = reduce_digits(p_bdate.day)
base_number = reduce_digits(b_month + b_day_reduced)
b_yr_red = reduce_digits(p_bdate.year)
life_path = reduce_digits(base_number + b_yr_red)
western_sign, western_elem = get_western_sun_sign(p_bdate.month, p_bdate.day)
c_elem, c_animal = get_chinese_zodiac(p_bdate.year)

p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns(5)
p_col1.metric("Player", p_name)
p_col2.metric("Position / Team", f"{p_pos} | {p_team}")
p_col3.metric("Life Path", f"{life_path}")
p_col4.metric("Western Sign", f"{western_sign} ({western_elem})")
p_col5.metric("Chinese Zodiac", f"{c_elem} {c_animal}")

# --- 5. GAME LOGS & METAPHYSICAL AUDIT LEDGER ---
st.markdown("---")
st.subheader("2. Career Game Logs & Metaphysical Audit Ledger")

col_opt1, col_opt2 = st.columns(2)
with col_opt1:
    selected_season = st.selectbox("Select Season to Analyze:", [2024], index=0)
with col_opt2:
    stat_filter = st.selectbox(
        "Performance Filter:",
        ["All Games", "High Production Only (250+ Pass Yds / 20+ Fantasy Pts)", "Direct Harmonic Hits Only"]
    )

ledger_records = []
for row in player_data["logs"]:
    if row["Season"] != selected_season:
        continue
        
    g_date = row["Date"]
    
    # Birthday-Flip Logic:
    bday_game_year = datetime.date(g_date.year, p_bdate.month, p_bdate.day)
    flipped = g_date >= bday_game_year
    cycle_yr = g_date.year if flipped else g_date.year - 1
    cycle_yr_red = reduce_digits(cycle_yr)

    py = reduce_digits(base_number + cycle_yr_red)
    pm = reduce_digits(py + g_date.month)
    pd_val = reduce_digits(pm + reduce_digits(g_date.day))
    ud_val = reduce_digits(reduce_digits(g_date.year) + g_date.month + g_date.day)

    total_yds = row["PassYds"] if p_pos == "QB" else (row["RushYds"])
    stat_reduced = reduce_digits(total_yds) if total_yds > 0 else 0
    is_match = (stat_reduced == pd_val) or (stat_reduced == ud_val)

    # Transit Aspect to Natal Sun
    natal_sun = approximate_sun_longitude(p_bdate)
    trans_sun = approximate_sun_longitude(g_date)
    aspect = get_aspect(natal_sun, trans_sun)

    ledger_records.append({
        "Season": row["Season"],
        "Week": row["Week"],
        "Game Date": g_date.strftime("%Y-%m-%d"),
        "Opp": row["Opp"],
        "Pass Yds": row["PassYds"],
        "Rush Yds": row["RushYds"],
        "TDs": row["TDs"],
        "Fantasy Pts": row["FPts"],
        "Stat Red.": stat_reduced,
        "Flip Status": "Flipped" if flipped else "Pre-Flip",
        "PY": py,
        "PM": pm,
        "Personal Day": pd_val,
        "Universal Day": ud_val,
        "Sun Transit": aspect,
        "Harmonic Match": "⚡ MATCH" if is_match else "—"
    })

matched_df = pd.DataFrame(ledger_records)

# Filter
display_df = matched_df.copy()
if "High Production" in stat_filter:
    display_df = display_df[(display_df["Pass Yds"] >= 250) | (display_df["Fantasy Pts"] >= 20.0)]
elif "Direct Harmonic Hits" in stat_filter:
    display_df = display_df[display_df["Harmonic Match"] == "⚡ MATCH"]

st.dataframe(display_df, use_container_width=True)

# Overview Metrics
total_games = len(matched_df)
total_hits = len(matched_df[matched_df["Harmonic Match"] == "⚡ MATCH"])
hit_pct = round((total_hits / total_games * 100), 1) if total_games > 0 else 0

st.markdown("### 📊 Correlation Overview")
c1, c2, c3 = st.columns(3)
c1.metric("Games Evaluated", f"{total_games}")
c2.metric("Direct Harmonic Hits", f"{total_hits}")
c3.metric("Match Frequency", f"{hit_pct}%")