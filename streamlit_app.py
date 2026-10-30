import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Historical Game Logs, Birthday-Flip Cycles, Numerology & Harmonic Correlator")

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

CHINESE_ZODIAC = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
CHINESE_ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

def get_chinese_zodiac(year: int):
    zodiac_idx = (year - 4) % 12
    element_idx = ((year - 4) // 2) % 5
    return CHINESE_ELEMENTS[element_idx], CHINESE_ZODIAC[zodiac_idx]

# --- 3. SAFE DATA PIPELINE ---
@st.cache_data(ttl=86400, show_spinner="Connecting to NFL Historical Player Database...")
def load_nfl_players():
    url = "https://github.com/nflverse/nflverse-data/releases/download/players/players.parquet"
    try:
        # Read without hardcoded column projection to prevent pyarrow.lib.ArrowInvalid crashes
        df = pd.read_parquet(url)
        
        # Dynamically identify name column
        name_col = "display_name" if "display_name" in df.columns else ("common_name" if "common_name" in df.columns else "name")
        bdate_col = "birth_date" if "birth_date" in df.columns else "birthdate"
        
        df = df.dropna(subset=[name_col, bdate_col]).copy()
        df["player_name_clean"] = df[name_col].astype(str)
        df["birth_date_dt"] = pd.to_datetime(df[bdate_col], errors="coerce")
        df = df.dropna(subset=["birth_date_dt"])
        
        pos_col = "position" if "position" in df.columns else "position_group"
        df["pos_clean"] = df[pos_col].fillna("N/A") if pos_col in df.columns else "N/A"
        
        team_col = "team_abbr" if "team_abbr" in df.columns else ("recent_team" if "recent_team" in df.columns else "team")
        df["team_clean"] = df[team_col].fillna("N/A") if team_col in df.columns else "N/A"
        
        id_col = "gsis_id" if "gsis_id" in df.columns else ("player_id" if "player_id" in df.columns else None)
        df["id_clean"] = df[id_col] if id_col else ""

        return df[["player_name_clean", "pos_clean", "team_clean", "birth_date_dt", "id_clean"]].drop_duplicates(subset=["player_name_clean"])
    except Exception as e:
        st.warning(f"Note on registry connection: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=86400, show_spinner="Loading Season Stats...")
def load_season_stats(season: int):
    # Load specific season parquet directly from nflverse stats
    url = f"https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats_{season}.parquet"
    try:
        df = pd.read_parquet(url)
        return df
    except Exception:
        # Fallback to master if single season is formatted differently
        try:
            alt_url = "https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats.parquet"
            master_df = pd.read_parquet(alt_url)
            return master_df[master_df["season"] == season]
        except Exception:
            return pd.DataFrame()

@st.cache_data(ttl=86400, show_spinner="Loading Schedules...")
def load_schedules():
    url = "https://github.com/nflverse/nfldata/raw/master/data/games.parquet"
    try:
        df = pd.read_parquet(url, columns=["season", "week", "home_team", "away_team", "gameday"])
        df["gameday"] = pd.to_datetime(df["gameday"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame()

players_df = load_nfl_players()
schedules_df = load_schedules()

# --- 4. PLAYER PROFILE SETUP ---
st.subheader("1. NFL Player & Profile Selection")

if not players_df.empty:
    player_names = sorted(players_df["player_name_clean"].unique().tolist())
    default_idx = player_names.index("Josh Allen") if "Josh Allen" in player_names else 0
    selected_player_name = st.selectbox("Search & Select Player:", player_names, index=default_idx)
    
    player_row = players_df[players_df["player_name_clean"] == selected_player_name].iloc[0]
    p_bdate = player_row["birth_date_dt"].date()
    p_pos = player_row["pos_clean"]
    p_team = player_row["team_clean"]
    p_id = player_row["id_clean"]
else:
    st.info("Operating in manual entry mode.")
    selected_player_name = st.text_input("Player Name", value="Josh Allen")
    p_bdate = datetime.date(1996, 5, 21)
    p_pos = "QB"
    p_team = "BUF"
    p_id = ""

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
        ["All Games", "High Production Only (250+ Pass Yds / 80+ Rush Yds / 18+ Fantasy Pts)", "Direct Harmonic Hits Only"]
    )

season_stats_df = load_season_stats(selected_season)

if not season_stats_df.empty:
    # Match player
    name_mask = pd.Series([False] * len(season_stats_df))
    if "player_display_name" in season_stats_df.columns:
        name_mask = name_mask | (season_stats_df["player_display_name"] == selected_player_name)
    if "player_name" in season_stats_df.columns:
        last_name = selected_player_name.split()[-1]
        name_mask = name_mask | (season_stats_df["player_name"].str.endswith(last_name, na=False))
    if p_id and "player_id" in season_stats_df.columns:
        name_mask = name_mask | (season_stats_df["player_id"] == p_id)
        
    p_games = season_stats_df[name_mask].copy()

    if not p_games.empty and not schedules_df.empty:
        # Match game dates via schedule
        sched_curr = schedules_df[schedules_df["season"] == selected_season]
        
        # Build ledger rows
        ledger_records = []
        for _, row in p_games.iterrows():
            wk = row.get("week")
            tm = row.get("recent_team", p_team)
            
            # Lookup date from schedule
            game_match = sched_curr[(sched_curr["week"] == wk) & ((sched_curr["home_team"] == tm) | (sched_curr["away_team"] == tm))]
            if not game_match.empty and pd.notna(game_match.iloc[0]["gameday"]):
                g_date = game_match.iloc[0]["gameday"].date()
                opp = game_match.iloc[0]["away_team"] if game_match.iloc[0]["home_team"] == tm else game_match.iloc[0]["home_team"]
            else:
                # Default approximate date if not matched
                g_date = datetime.date(selected_season, 9 + min(max((int(wk)-1)//4, 0), 3), 15)
                opp = row.get("opponent_team", "—")

            # Birthday-Flip Logic:
            bday_game_year = datetime.date(g_date.year, p_bdate.month, p_bdate.day)
            flipped = g_date >= bday_game_year
            cycle_yr = g_date.year if flipped else g_date.year - 1
            cycle_yr_red = reduce_digits(cycle_yr)

            py = reduce_digits(base_number + cycle_yr_red)
            pm = reduce_digits(py + g_date.month)
            pd_val = reduce_digits(pm + reduce_digits(g_date.day))
            ud_val = reduce_digits(reduce_digits(g_date.year) + g_date.month + g_date.day)

            # Yardage & Stats
            pass_yds = int(row.get("passing_yards", 0)) if pd.notna(row.get("passing_yards")) else 0
            rush_yds = int(row.get("rushing_yards", 0)) if pd.notna(row.get("rushing_yards")) else 0
            rec_yds = int(row.get("receiving_yards", 0)) if pd.notna(row.get("receiving_yards")) else 0
            total_yds = pass_yds if p_pos == "QB" else (rush_yds + rec_yds)

            tds = int(row.get("passing_tds", 0) + row.get("rushing_tds", 0) + row.get("receiving_tds", 0))
            fpts = round(float(row.get("fantasy_points_ppr", 0.0)), 1) if pd.notna(row.get("fantasy_points_ppr")) else 0.0

            stat_reduced = reduce_digits(total_yds) if total_yds > 0 else 0
            is_match = (stat_reduced == pd_val) or (stat_reduced == ud_val)

            ledger_records.append({
                "Season": selected_season,
                "Week": wk,
                "Game Date": g_date.strftime("%Y-%m-%d"),
                "Opp": opp,
                "Yards": total_yds,
                "TDs": tds,
                "Fantasy Pts": fpts,
                "Stat Red.": stat_reduced,
                "Flip Status": "Flipped" if flipped else "Pre-Flip",
                "PY": py,
                "PM": pm,
                "Personal Day": pd_val,
                "Universal Day": ud_val,
                "Harmonic Match": "⚡ MATCH" if is_match and total_yds > 0 else "—"
            })

        matched_df = pd.DataFrame(ledger_records)

        # Filters
        display_df = matched_df.copy()
        if "High Production" in stat_filter:
            display_df = display_df[(display_df["Yards"] >= 250) | (display_df["Fantasy Pts"] >= 18.0)]
        elif "Direct Harmonic Hits" in stat_filter:
            display_df = display_df[display_df["Harmonic Match"] == "⚡ MATCH"]

        st.dataframe(display_df, use_container_width=True)

        # Statistical Summary
        total_games = len(matched_df)
        total_hits = len(matched_df[matched_df["Harmonic Match"] == "⚡ MATCH"])
        hit_pct = round((total_hits / total_games * 100), 1) if total_games > 0 else 0

        st.markdown("### 📊 Correlation Overview")
        c1, c2, c3 = st.columns(3)
        c1.metric("Games Evaluated", f"{total_games}")
        c2.metric("Direct Harmonic Hits", f"{total_hits}")
        c3.metric("Match Frequency", f"{hit_pct}%")
    else:
        st.info(f"No game records found for {selected_player_name} in {selected_season}.")
else:
    st.info(f"Loading data for season {selected_season}...")