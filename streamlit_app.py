import streamlit as st
import pandas as pd
import datetime
import math

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Automated NFL Player Registry, Birthday-Flip Cycles, Numerology & Planetary Transits")

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

# --- 2. WESTERN ASTROLOGY & PLANETARY CALCULATOR ---
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
    """Calculates approximate ecliptic longitude of Sun (0-360 deg) for transits/aspects."""
    day_of_year = d.timetuple().tm_yday
    # Vernal Equinox approx March 20 (Day 79)
    deg = ((day_of_year - 79) * 360 / 365.25) % 360
    return deg

def get_aspect(deg1: float, deg2: float):
    diff = abs(deg1 - deg2) % 360
    if diff > 180:
        diff = 360 - diff
    orb = 8.0  # standard transit orb
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

# --- 3. LOAD HISTORICAL NFL PLAYER DATABASE (CACHED) ---
@st.cache_data(show_spinner="Connecting to NFL Historical Player Database...")
def load_nfl_players():
    url = "https://github.com/nflverse/nflverse-data/releases/download/players/players.parquet"
    cols = ["display_name", "position", "birth_date", "recent_team", "draft_year", "draft_club"]
    df = pd.read_parquet(url, columns=cols)
    df = df.dropna(subset=["display_name", "birth_date"]).copy()
    df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
    df = df.dropna(subset=["birth_date"])
    df = df.sort_values(by="display_name").reset_index(drop=True)
    return df

try:
    players_df = load_nfl_players()
    db_available = True
except Exception:
    db_available = False

# --- 4. AUTO-COMPLETE SEARCH & SELECTION ---
st.subheader("1. NFL Player & Entity Lookup")

if db_available:
    player_names = players_df["display_name"].unique().tolist()
    default_idx = player_names.index("Josh Allen") if "Josh Allen" in player_names else 0
    selected_player_name = st.selectbox("Search & Select Player (Auto-Populates):", player_names, index=default_idx)
    
    player_row = players_df[players_df["display_name"] == selected_player_name].iloc[0]
    p_bdate = player_row["birth_date"].date()
    p_pos = player_row["position"] if pd.notna(player_row["position"]) else "N/A"
    p_team = player_row["recent_team"] if pd.notna(player_row["recent_team"]) else player_row["draft_club"]
else:
    st.warning("Operating in manual fallback mode.")
    selected_player_name = st.text_input("Player Name", value="Josh Allen")
    p_bdate = datetime.date(1996, 5, 21)
    p_pos = "QB"
    p_team = "BUF"

info_col1, info_col2, info_col3, info_col4 = st.columns(4)
info_col1.metric("Player", selected_player_name)
info_col2.metric("Position", str(p_pos))
info_col3.metric("Team", str(p_team))
info_col4.metric("Birthdate", p_bdate.strftime("%B %d, %Y"))

# --- 5. TARGET GAME DATE ---
st.markdown("---")
st.subheader("2. Target Game & Matchup Setup")
g_col1, g_col2 = st.columns(2)

with g_col1:
    game_date = st.date_input(
        "Select Game Date",
        value=datetime.date(2026, 11, 1),
        min_value=datetime.date(1920, 1, 1),
        max_value=datetime.date(2030, 12, 31)
    )

with g_col2:
    opponent_name = st.text_input("Opponent (Optional)", value="Kansas City Chiefs")

# --- 6. AUDIT & METAPHYSICAL CALCULATIONS ---
b_month = p_bdate.month
b_day_reduced = reduce_digits(p_bdate.day)
base_number = reduce_digits(b_month + b_day_reduced)

y_reduced = reduce_digits(p_bdate.year)
life_path = reduce_digits(base_number + y_reduced)

# Precise Calendar Birthday-Flip Logic:
birthday_this_year = datetime.date(game_date.year, p_bdate.month, p_bdate.day)
has_flipped = game_date >= birthday_this_year

if has_flipped:
    cycle_year = game_date.year
else:
    cycle_year = game_date.year - 1

cycle_yr_reduced = reduce_digits(cycle_year)
personal_year = reduce_digits(base_number + cycle_yr_reduced)

game_month = game_date.month
personal_month = reduce_digits(personal_year + game_month)

game_day_reduced = reduce_digits(game_date.day)
personal_day = reduce_digits(personal_month + game_day_reduced)

univ_day = reduce_digits(reduce_digits(game_date.year) + game_date.month + game_date.day)

# Western & Chinese Astrology
western_sign, western_elem = get_western_sun_sign(p_bdate.month, p_bdate.day)
game_sign, game_elem = get_western_sun_sign(game_date.month, game_date.day)
p_c_elem, p_c_animal = get_chinese_zodiac(p_bdate.year)
g_c_elem, g_c_animal = get_chinese_zodiac(game_date.year)

# Solar Transit & Aspect Check
natal_sun_long = approximate_sun_longitude(p_bdate)
transit_sun_long = approximate_sun_longitude(game_date)
sun_transit_aspect = get_aspect(natal_sun_long, transit_sun_long)

# --- 7. AUDIT LEDGER & METRICS ---
st.markdown("---")
st.subheader("3. Numerological Cycles & Planetary Transit Ledger")

n1, n2, n3, n4, n5 = st.columns(5)
n1.metric("Life Path", f"{life_path}")
n2.metric("Cycle Year", f"{cycle_year} (-> {cycle_yr_reduced})")
n3.metric("Personal Year (PY)", f"{personal_year}")
n4.metric("Personal Month (PM)", f"{personal_month}")
n5.metric("Personal Day (PD)", f"{personal_day}")

a1, a2, a3, a4 = st.columns(4)
a1.metric("Western Sun Sign", f"{western_sign} ({western_elem})")
a2.metric("Game Sun Sign", f"{game_sign} ({game_elem})")
a3.metric("Chinese Zodiac", f"{p_c_elem} {p_c_animal}")
a4.metric("Solar Transit Aspect", f"{sun_transit_aspect}")

st.markdown("### Step-by-Step Verification & Astrological Alignment")
st.write(f"- **Birthday Flip Audit:** Game `{game_date.strftime('%B %d')}` vs Birthday `{p_bdate.strftime('%B %d')}` -> **{'Flipped (Game Year)' if has_flipped else 'Not Flipped Yet (Game Year - 1)'}**")
st.write(f"- **Universal Day:** `{game_date.strftime('%Y-%m-%d')}` -> **{univ_day}**")
st.write(f"- **Western Astrology:** Natal Sun in **{western_sign} ({western_elem})** at ~`{natal_sun_long:.1f}°` | Game Sun in **{game_sign} ({game_elem})** at ~`{transit_sun_long:.1f}°`")
st.write(f"- **Transit Aspect to Natal Sun:** **{sun_transit_aspect}**")
st.write(f"- **Chinese Astrology:** Player born in the Year of the **{p_c_elem} {p_c_animal}**; Game played in the Year of the **{g_c_elem} {g_c_animal}**")