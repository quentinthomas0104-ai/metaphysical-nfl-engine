import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Historical Game Logs, Full Seasons, Birthday-Flip Cycles & Statistical Correlations")

# --- 1. CORE NUMEROLOGY & REDUCTION FUNCTIONS ---
def reduce_digits(n: int, preserve_masters: bool = False) -> int:
    """Reduces an integer to a single digit (1-9), optionally preserving master numbers 11, 22, 33."""
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
    return "Capricorn", "Earth"

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

# --- 3. COMPREHENSIVE 2024 GAME LOG DATA (FULL 17 WEEKS) ---
COMPLETE_2024_LOGS = {
    "Patrick Mahomes (QB - KC)": [
        {"Week": 1, "Date": datetime.date(2024, 9, 5), "Opp": "BAL", "PassYds": 291, "RushYds": 3, "TDs": 1, "FPts": 16.9},
        {"Week": 2, "Date": datetime.date(2024, 9, 15), "Opp": "CIN", "PassYds": 151, "RushYds": 29, "TDs": 2, "FPts": 13.9},
        {"Week": 3, "Date": datetime.date(2024, 9, 22), "Opp": "ATL", "PassYds": 217, "RushYds": 17, "TDs": 2, "FPts": 16.4},
        {"Week": 4, "Date": datetime.date(2024, 9, 29), "Opp": "LAC", "PassYds": 245, "RushYds": 12, "TDs": 1, "FPts": 14.0},
        {"Week": 5, "Date": datetime.date(2024, 10, 7), "Opp": "NO", "PassYds": 331, "RushYds": 22, "TDs": 0, "FPts": 15.4},
        {"Week": 7, "Date": datetime.date(2024, 10, 20), "Opp": "SF", "PassYds": 154, "RushYds": 39, "TDs": 1, "FPts": 11.1},
        {"Week": 8, "Date": datetime.date(2024, 10, 27), "Opp": "LV", "PassYds": 262, "RushYds": 17, "TDs": 2, "FPts": 18.2},
        {"Week": 9, "Date": datetime.date(2024, 11, 4), "Opp": "TB", "PassYds": 291, "RushYds": 9, "TDs": 3, "FPts": 24.5},
        {"Week": 10, "Date": datetime.date(2024, 11, 10), "Opp": "DEN", "PassYds": 266, "RushYds": 19, "TDs": 1, "FPts": 16.5},
        {"Week": 11, "Date": datetime.date(2024, 11, 17), "Opp": "BUF", "PassYds": 196, "RushYds": 9, "TDs": 3, "FPts": 17.7},
        {"Week": 12, "Date": datetime.date(2024, 11, 24), "Opp": "CAR", "PassYds": 269, "RushYds": 60, "TDs": 3, "FPts": 28.8},
        {"Week": 13, "Date": datetime.date(2024, 11, 29), "Opp": "LV", "PassYds": 306, "RushYds": 11, "TDs": 1, "FPts": 17.3},
        {"Week": 14, "Date": datetime.date(2024, 12, 8), "Opp": "LAC", "PassYds": 210, "RushYds": 14, "TDs": 1, "FPts": 13.8},
        {"Week": 15, "Date": datetime.date(2024, 12, 15), "Opp": "CLE", "PassYds": 159, "RushYds": 33, "TDs": 2, "FPts": 17.7},
        {"Week": 16, "Date": datetime.date(2024, 12, 21), "Opp": "HOU", "PassYds": 260, "RushYds": 11, "TDs": 1, "FPts": 15.5},
        {"Week": 17, "Date": datetime.date(2024, 12, 25), "Opp": "PIT", "PassYds": 238, "RushYds": 15, "TDs": 3, "FPts": 23.0},
    ],
    "Lamar Jackson (QB - BAL)": [
        {"Week": 1, "Date": datetime.date(2024, 9, 5), "Opp": "KC", "PassYds": 273, "RushYds": 122, "TDs": 1, "FPts": 25.1},
        {"Week": 2, "Date": datetime.date(2024, 9, 15), "Opp": "LV", "PassYds": 247, "RushYds": 45, "TDs": 1, "FPts": 18.4},
        {"Week": 3, "Date": datetime.date(2024, 9, 22), "Opp": "DAL", "PassYds": 182, "RushYds": 87, "TDs": 2, "FPts": 22.0},
        {"Week": 4, "Date": datetime.date(2024, 9, 29), "Opp": "BUF", "PassYds": 156, "RushYds": 54, "TDs": 3, "FPts": 23.6},
        {"Week": 5, "Date": datetime.date(2024, 10, 6), "Opp": "CIN", "PassYds": 348, "RushYds": 55, "TDs": 4, "FPts": 33.4},
        {"Week": 6, "Date": datetime.date(2024, 10, 13), "Opp": "WAS", "PassYds": 323, "RushYds": 40, "TDs": 1, "FPts": 20.9},
        {"Week": 7, "Date": datetime.date(2024, 10, 21), "Opp": "TB", "PassYds": 281, "RushYds": 52, "TDs": 5, "FPts": 35.4},
        {"Week": 8, "Date": datetime.date(2024, 10, 27), "Opp": "CLE", "PassYds": 289, "RushYds": 46, "TDs": 2, "FPts": 22.2},
        {"Week": 9, "Date": datetime.date(2024, 11, 3), "Opp": "DEN", "PassYds": 280, "RushYds": 4, "TDs": 3, "FPts": 25.6},
        {"Week": 10, "Date": datetime.date(2024, 11, 7), "Opp": "CIN", "PassYds": 290, "RushYds": 33, "TDs": 4, "FPts": 30.9},
        {"Week": 11, "Date": datetime.date(2024, 11, 17), "Opp": "PIT", "PassYds": 207, "RushYds": 46, "TDs": 1, "FPts": 14.9},
        {"Week": 12, "Date": datetime.date(2024, 11, 25), "Opp": "LAC", "PassYds": 177, "RushYds": 15, "TDs": 2, "FPts": 16.6},
        {"Week": 13, "Date": datetime.date(2024, 12, 1), "Opp": "PHI", "PassYds": 237, "RushYds": 79, "TDs": 2, "FPts": 23.4},
        {"Week": 15, "Date": datetime.date(2024, 12, 15), "Opp": "NYG", "PassYds": 290, "RushYds": 65, "TDs": 5, "FPts": 38.1},
        {"Week": 16, "Date": datetime.date(2024, 12, 21), "Opp": "PIT", "PassYds": 217, "RushYds": 43, "TDs": 1, "FPts": 17.0},
        {"Week": 17, "Date": datetime.date(2024, 12, 25), "Opp": "HOU", "PassYds": 167, "RushYds": 87, "TDs": 3, "FPts": 27.4},
    ],
    "Josh Allen (QB - BUF)": [
        {"Week": 1, "Date": datetime.date(2024, 9, 8), "Opp": "ARI", "PassYds": 232, "RushYds": 39, "TDs": 4, "FPts": 31.2},
        {"Week": 2, "Date": datetime.date(2024, 9, 12), "Opp": "MIA", "PassYds": 139, "RushYds": 2, "TDs": 1, "FPts": 11.8},
        {"Week": 3, "Date": datetime.date(2024, 9, 23), "Opp": "JAX", "PassYds": 263, "RushYds": 44, "TDs": 4, "FPts": 30.9},
        {"Week": 4, "Date": datetime.date(2024, 9, 29), "Opp": "BAL", "PassYds": 180, "RushYds": 21, "TDs": 0, "FPts": 9.3},
        {"Week": 5, "Date": datetime.date(2024, 10, 6), "Opp": "HOU", "PassYds": 131, "RushYds": 54, "TDs": 1, "FPts": 14.6},
        {"Week": 6, "Date": datetime.date(2024, 10, 14), "Opp": "NYJ", "PassYds": 215, "RushYds": 18, "TDs": 3, "FPts": 24.4},
        {"Week": 7, "Date": datetime.date(2024, 10, 20), "Opp": "TEN", "PassYds": 323, "RushYds": 1, "TDs": 2, "FPts": 21.0},
        {"Week": 8, "Date": datetime.date(2024, 10, 27), "Opp": "SEA", "PassYds": 283, "RushYds": 25, "TDs": 2, "FPts": 21.8},
        {"Week": 9, "Date": datetime.date(2024, 11, 3), "Opp": "MIA", "PassYds": 235, "RushYds": 7, "TDs": 3, "FPts": 22.1},
        {"Week": 10, "Date": datetime.date(2024, 11, 10), "Opp": "IND", "PassYds": 280, "RushYds": 50, "TDs": 1, "FPts": 20.2},
        {"Week": 11, "Date": datetime.date(2024, 11, 17), "Opp": "KC", "PassYds": 262, "RushYds": 55, "TDs": 2, "FPts": 24.0},
        {"Week": 13, "Date": datetime.date(2024, 12, 1), "Opp": "SF", "PassYds": 208, "RushYds": 18, "TDs": 3, "FPts": 26.1},
        {"Week": 14, "Date": datetime.date(2024, 12, 8), "Opp": "LAR", "PassYds": 342, "RushYds": 82, "TDs": 6, "FPts": 43.9},
        {"Week": 15, "Date": datetime.date(2024, 12, 15), "Opp": "DET", "PassYds": 362, "RushYds": 44, "TDs": 4, "FPts": 32.9},
        {"Week": 16, "Date": datetime.date(2024, 12, 22), "Opp": "NE", "PassYds": 154, "RushYds": 36, "TDs": 2, "FPts": 17.8},
        {"Week": 17, "Date": datetime.date(2024, 12, 29), "Opp": "NYJ", "PassYds": 124, "RushYds": 43, "TDs": 3, "FPts": 21.3},
    ],
    "Caleb Williams (QB - CHI)": [
        {"Week": 1, "Date": datetime.date(2024, 9, 8), "Opp": "TEN", "PassYds": 93, "RushYds": 15, "TDs": 0, "FPts": 5.2},
        {"Week": 2, "Date": datetime.date(2024, 9, 15), "Opp": "HOU", "PassYds": 174, "RushYds": 44, "TDs": 0, "FPts": 7.4},
        {"Week": 3, "Date": datetime.date(2024, 9, 22), "Opp": "IND", "PassYds": 363, "RushYds": 8, "TDs": 2, "FPts": 17.3},
        {"Week": 4, "Date": datetime.date(2024, 9, 29), "Opp": "LAR", "PassYds": 157, "RushYds": 12, "TDs": 1, "FPts": 11.5},
        {"Week": 5, "Date": datetime.date(2024, 10, 6), "Opp": "CAR", "PassYds": 304, "RushYds": 34, "TDs": 2, "FPts": 23.6},
        {"Week": 6, "Date": datetime.date(2024, 10, 13), "Opp": "JAX", "PassYds": 226, "RushYds": 56, "TDs": 4, "FPts": 28.6},
        {"Week": 8, "Date": datetime.date(2024, 10, 27), "Opp": "WAS", "PassYds": 131, "RushYds": 41, "TDs": 0, "FPts": 9.3},
        {"Week": 9, "Date": datetime.date(2024, 11, 3), "Opp": "ARI", "PassYds": 217, "RushYds": 0, "TDs": 0, "FPts": 8.7},
        {"Week": 10, "Date": datetime.date(2024, 11, 10), "Opp": "NE", "PassYds": 120, "RushYds": 15, "TDs": 0, "FPts": 6.3},
        {"Week": 11, "Date": datetime.date(2024, 11, 17), "Opp": "GB", "PassYds": 231, "RushYds": 70, "TDs": 0, "FPts": 16.2},
        {"Week": 12, "Date": datetime.date(2024, 11, 24), "Opp": "MIN", "PassYds": 340, "RushYds": 33, "TDs": 2, "FPts": 22.9},
        {"Week": 13, "Date": datetime.date(2024, 11, 28), "Opp": "DET", "PassYds": 256, "RushYds": 8, "TDs": 3, "FPts": 23.0},
        {"Week": 14, "Date": datetime.date(2024, 12, 8), "Opp": "SF", "PassYds": 134, "RushYds": 16, "TDs": 2, "FPts": 15.0},
        {"Week": 15, "Date": datetime.date(2024, 12, 16), "Opp": "MIN", "PassYds": 168, "RushYds": 18, "TDs": 1, "FPts": 12.5},
        {"Week": 16, "Date": datetime.date(2024, 12, 22), "Opp": "DET", "PassYds": 334, "RushYds": 42, "TDs": 3, "FPts": 27.6},
        {"Week": 17, "Date": datetime.date(2024, 12, 26), "Opp": "SEA", "PassYds": 204, "RushYds": 26, "TDs": 2, "FPts": 18.8},
    ]
}

PLAYERS_METADATA = {
    "Patrick Mahomes (QB - KC)": {"name": "Patrick Mahomes", "bdate": datetime.date(1995, 9, 17), "pos": "QB", "team": "KC"},
    "Lamar Jackson (QB - BAL)": {"name": "Lamar Jackson", "bdate": datetime.date(1997, 1, 7), "pos": "QB", "team": "BAL"},
    "Josh Allen (QB - BUF)": {"name": "Josh Allen", "bdate": datetime.date(1996, 5, 21), "pos": "QB", "team": "BUF"},
    "Caleb Williams (QB - CHI)": {"name": "Caleb Williams", "bdate": datetime.date(2001, 11, 18), "pos": "QB", "team": "CHI"},
}

# --- 4. STREAMLIT UI ---
st.subheader("1. Player Selection & Astrological Profile")
selected_key = st.selectbox("Select Player:", list(PLAYERS_METADATA.keys()), index=0)
p_meta = PLAYERS_METADATA[selected_key]

p_bdate = p_meta["bdate"]
b_month = p_bdate.month
b_day_red = reduce_digits(p_bdate.day)
base_number = reduce_digits(b_month + b_day_red)
life_path = reduce_digits(base_number + reduce_digits(p_bdate.year))
w_sign, w_elem = get_western_sun_sign(p_bdate.month, p_bdate.day)
c_elem, c_animal = get_chinese_zodiac(p_bdate.year)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Player", p_meta["name"])
c2.metric("Team / Pos", f"{p_meta['team']} | {p_meta['pos']}")
c3.metric("Life Path", f"{life_path}")
c4.metric("Western Sign", f"{w_sign} ({w_elem})")
c5.metric("Chinese Zodiac", f"{c_elem} {c_animal}")

# --- 5. FULL SEASON LEDGER WITH CYCLE MATH ---
st.markdown("---")
st.subheader(f"2. Complete 2024 Game Logs & Metaphysical Ledger for {p_meta['name']}")

raw_logs = COMPLETE_2024_LOGS.get(selected_key, [])
ledger_rows = []

for g in raw_logs:
    g_date = g["Date"]
    
    # Birthday-Flip Logic:
    bday_game_year = datetime.date(g_date.year, p_bdate.month, p_bdate.day)
    flipped = g_date >= bday_game_year
    cycle_yr = g_date.year if flipped else g_date.year - 1
    cycle_yr_red = reduce_digits(cycle_yr)

    py = reduce_digits(base_number + cycle_yr_red)
    pm = reduce_digits(py + g_date.month)
    pd_val = reduce_digits(pm + reduce_digits(g_date.day))
    ud_val = reduce_digits(reduce_digits(g_date.year) + g_date.month + g_date.day)

    tot_yds = g["PassYds"] if p_meta["pos"] == "QB" else g["RushYds"]
    stat_red = reduce_digits(tot_yds) if tot_yds > 0 else 0
    is_match = (stat_red == pd_val) or (stat_red == ud_val)

    natal_sun = approximate_sun_longitude(p_bdate)
    trans_sun = approximate_sun_longitude(g_date)
    aspect = get_aspect(natal_sun, trans_sun)

    ledger_rows.append({
        "Week": g["Week"],
        "Game Date": g_date.strftime("%Y-%m-%d"),
        "Opp": g["Opp"],
        "Pass Yds": g["PassYds"],
        "Rush Yds": g["RushYds"],
        "TDs": g["TDs"],
        "Fantasy Pts": g["FPts"],
        "Stat Red.": stat_red,
        "Flip Status": "Flipped" if flipped else "Pre-Flip",
        "PY": py,
        "PM": pm,
        "Personal Day": pd_val,
        "Universal Day": ud_val,
        "Sun Transit": aspect,
        "Harmonic Match": "⚡ MATCH" if is_match else "—"
    })

df = pd.DataFrame(ledger_rows)
st.dataframe(df, use_container_width=True)

if not df.empty:
    tot_g = len(df)
    tot_hits = len(df[df["Harmonic Match"] == "⚡ MATCH"])
    hit_rate = round((tot_hits / tot_g * 100), 1) if tot_g > 0 else 0
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Total 2024 Games", f"{tot_g}")
    sc2.metric("Direct Harmonic Matches", f"{tot_hits}")
    sc3.metric("Match Frequency", f"{hit_rate}%")