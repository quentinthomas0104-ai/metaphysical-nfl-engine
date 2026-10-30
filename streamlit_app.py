import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Historical Game Logs, Birthday-Flip Cycles, Numerology & Harmonic Statistical Correlator")

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

# --- 3. NFL DATA PIPELINE (PLAYERS & SCHEDULES) ---
@st.cache_data(show_spinner="Accessing NFL Historical Registry...")
def load_nfl_players():
    url = "https://github.com/nflverse/nflverse-data/releases/download/players/players.parquet"
    cols = ["display_name", "position", "birth_date", "recent_team", "draft_year", "draft_club", "gsis_id"]
    df = pd.read_parquet(url, columns=cols)
    df = df.dropna(subset=["display_name", "birth_date"]).copy()
    df["birth_date"] = pd.to_datetime(df["birth_date"], errors="coerce")
    df = df.dropna(subset=["birth_date"])
    df = df.sort_values(by="display_name").reset_index(drop=True)
    return df

@st.cache_data(show_spinner="Fetching Season Stats & Game Logs...")
def load_season_stats(season: int):
    url = f"https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats_{season}.parquet"
    try:
        df = pd.read_parquet(url)
        return df
    except Exception:
        return pd.DataFrame()

@st.cache_data(show_spinner="Accessing Game Schedules...")
def load_schedules():
    url = "https://github.com/nflverse/nfldata/raw/master/data/games.parquet"
    try:
        df = pd.read_parquet(url, columns=["game_id", "season", "week", "gameday", "home_team", "away_team"])
        df["gameday"] = pd.to_datetime(df["gameday"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame()

try:
    players_df = load_nfl_players()
    schedules_df = load_schedules()
    db_available = True
except Exception:
    db_available = False

# --- 4. PLAYER PROFILE SETUP ---
st.subheader("1. NFL Player & Profile Selection")

if db_available:
    player_names = players_df["display_name"].unique().tolist()
    default_idx = player_names.index("Josh Allen") if "Josh Allen" in player_names else 0
    selected_player_name = st.selectbox("Search & Select Player:", player_names, index=default_idx)
    
    player_row = players_df[players_df["display_name"] == selected_player_name].iloc[0]
    p_bdate = player_row["birth_date"].date()
    p_pos = player_row["position"] if pd.notna(player_row["position"]) else "N/A"
    p_team = player_row["recent_team"] if pd.notna(player_row["recent_team"]) else player_row["draft_club"]
    p_id = player_row["gsis_id"]
else:
    selected_player_name = st.text_input("Player Name", value="Josh Allen")
    p_bdate = datetime.date(1996, 5, 21)
    p_pos = "QB"
    p_team = "BUF"
    p_id = None

# Baseline Metaphysical Metrics
b_month = p_bdate.month
b_day_reduced = reduce_digits(p_bdate.day)
base_number = reduce_digits(b_month + b_day_reduced)
life_path = reduce_digits(base_number + reduce_digits(p_bdate.year))
western_sign, western_elem = get_western_sun_sign(p_bdate.month, p_bdate.day)
c_elem, c_animal = get_chinese_zodiac(p_bdate.year)

p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns(5)
p_col1.metric("Player", selected_player_name)
p_col2.metric("Position / Team", f"{p_pos} | {p_team}")
p_col3.metric("Life Path", f"{life_path}")
p_col4.metric("Western Sign", f"{western_sign} ({western_elem})")
p_col5.metric("Chinese Zodiac", f"{c_elem} {c_animal}")

# --- 5. SEASON & GAME LOG SELECTOR ---
st.markdown("---")
st.subheader("2. Career Game Logs & Metaphysical Audit Ledger")

col_opt1, col_opt2 = st.columns(2)
with col_opt1:
    selected_season = st.selectbox("Select Season to Analyze:", list(range(2025, 2017, -1)), index=1)
with col_opt2:
    stat_filter = st.selectbox(
        "Performance Filter:",
        ["All Games", "High Production Only (250+ Pass Yds / 80+ Rush/Rec Yds / 18+ Fantasy Pts)", "Direct Harmonic Hits Only"]
    )

# Pull and merge stats
stats_df = load_season_stats(selected_season)
matched_stats = pd.DataFrame()

if not stats_df.empty and db_available:
    # Filter stats for player
    if "player_display_name" in stats_df.columns:
        player_stats = stats_df[stats_df["player_display_name"] == selected_player_name].copy()
    elif "player_name" in stats_df.columns:
        player_stats = stats_df[stats_df["player_name"].str.contains(selected_player_name.split()[-1], na=False)].copy()
    else:
        player_stats = pd.DataFrame()
        
    if not player_stats.empty and not schedules_df.empty:
        # Merge with schedule to get exact game dates
        sched_season = schedules_df[schedules_df["season"] == selected_season]
        merged = pd.merge(player_stats, sched_season, on=["game_id", "week"], how="left")
        
        # Build ledger rows
        ledger_records = []
        for _, row in merged.iterrows():
            g_date = row.get("gameday")
            if pd.isna(g_date):
                continue
            g_date = g_date.date() if isinstance(g_date, pd.Timestamp) else g_date
            
            # Birthday-Flip Logic:
            bday_game_year = datetime.date(g_date.year, p_bdate.month, p_bdate.day)
            flipped = g_date >= bday_game_year
            cycle_yr = g_date.year if flipped else g_date.year - 1
            cycle_yr_red = reduce_digits(cycle_yr)
            
            py = reduce_digits(base_number + cycle_yr_red)
            pm = reduce_digits(py + g_date.month)
            pd_val = reduce_digits(pm + reduce_digits(g_date.day))
            ud_val = reduce_digits(reduce_digits(g_date.year) + g_date.month + g_date.day)
            
            # Stat metrics
            pass_yds = int(row.get("passing_yards", 0)) if pd.notna(row.get("passing_yards")) else 0
            rush_yds = int(row.get("rushing_yards", 0)) if pd.notna(row.get("rushing_yards")) else 0
            rec_yds = int(row.get("receiving_yards", 0)) if pd.notna(row.get("receiving_yards")) else 0
            total_yds = pass_yds if p_pos == "QB" else (rush_yds + rec_yds)
            
            tds = int(row.get("passing_tds", 0) + row.get("rushing_tds", 0) + row.get("receiving_tds", 0))
            fpts = round(float(row.get("fantasy_points_ppr", 0.0)), 1) if pd.notna(row.get("fantasy_points_ppr")) else 0.0
            
            stat_reduced = reduce_digits(total_yds) if total_yds > 0 else 0
            is_match = (stat_reduced == pd_val) or (stat_reduced == ud_val)
            
            opp = row.get("away_team") if row.get("home_team") == p_team else row.get("home_team")
            
            ledger_records.append({
                "Week": row.get("week"),
                "Game Date": g_date.strftime("%Y-%m-%d"),
                "Opponent": opp,
                "Yards (Pass/Tot)": total_yds,
                "TDs": tds,
                "Fantasy Pts": fpts,
                "Stat Reduced": stat_reduced,
                "Flip Status": "Flipped" if flipped else "Pre-Flip",
                "PY": py,
                "PM": pm,
                "Personal Day": pd_val,
                "Universal Day": ud_val,
                "Harmonic Match": "⚡ MATCH" if is_match and total_yds > 0 else "—"
            })
            
        matched_stats = pd.DataFrame(ledger_records)

if not matched_stats.empty:
    # Apply user filter
    display_df = matched_stats.copy()
    if "High Production" in stat_filter:
        display_df = display_df[(display_df["Yards (Pass/Tot)"] >= 250) | (display_df["Fantasy Pts"] >= 18.0)]
    elif "Direct Harmonic Hits" in stat_filter:
        display_df = display_df[display_df["Harmonic Match"] == "⚡ MATCH"]
        
    st.dataframe(display_df, use_container_width=True)
    
    # Statistical Insights Summary
    total_games = len(matched_stats)
    total_hits = len(matched_stats[matched_stats["Harmonic Match"] == "⚡ MATCH"])
    hit_pct = round((total_hits / total_games * 100), 1) if total_games > 0 else 0
    
    st.markdown("### 📊 Correlation Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Games Evaluated", f"{total_games}")
    c2.metric("Direct Harmonic Hits", f"{total_hits}")
    c3.metric("Match Frequency", f"{hit_pct}%")
else:
    st.info("No active game log records found for this player/season selection.")