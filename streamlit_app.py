import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("Career Logs, Live Slate Importer, Cross-Resonance Scanner, Master Visualizer, & Head-to-Head Clash Engine")

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
# 4. OFFICIAL SCHEDULE REPOSITORY (2026 LIVE SLATES & HISTORICAL ERAS)
# ==============================================================================
OFFICIAL_SCHEDULE_SLATES = {
    "2026 Active NFL Slate (Weeks 1 - 9)": [
        {"Week": 1, "Date": datetime.date(2026, 9, 13), "DayOfWeek": "Sun", "Opp": "CAR", "HomeAway": "@", "Venue": "Bank of America Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "24 - 17", "Result": "W", "Diff": "+7", "PassYds": 245, "TotalOffYds": 348},
        {"Week": 2, "Date": datetime.date(2026, 9, 20), "DayOfWeek": "Sun", "Opp": "DET", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "21 - 27", "Result": "L", "Diff": "-6", "PassYds": 218, "TotalOffYds": 312},
        {"Week": 3, "Date": datetime.date(2026, 9, 27), "DayOfWeek": "Sun", "Opp": "MIN", "HomeAway": "@", "Venue": "U.S. Bank Stadium", "Surface": "Turf", "GameTime": "1:00 PM", "Score": "28 - 24", "Result": "W", "Diff": "+4", "PassYds": 282, "TotalOffYds": 385},
        {"Week": 4, "Date": datetime.date(2026, 10, 4), "DayOfWeek": "Sun", "Opp": "LAR", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "31 - 20", "Result": "W", "Diff": "+11", "PassYds": 310, "TotalOffYds": 415},
        {"Week": 5, "Date": datetime.date(2026, 10, 11), "DayOfWeek": "Sun", "Opp": "GB", "HomeAway": "@", "Venue": "Lambeau Field", "Surface": "Grass", "GameTime": "4:25 PM", "Score": "17 - 24", "Result": "L", "Diff": "-7", "PassYds": 195, "TotalOffYds": 290},
        {"Week": 6, "Date": datetime.date(2026, 10, 18), "DayOfWeek": "Sun", "Opp": "JAX", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "1:00 PM", "Score": "35 - 16", "Result": "W", "Diff": "+19", "PassYds": 277, "TotalOffYds": 395},
        {"Week": 7, "Date": datetime.date(2026, 10, 25), "DayOfWeek": "Sun", "Opp": "WAS", "HomeAway": "@", "Venue": "Northwest Stadium", "Surface": "Grass", "GameTime": "4:25 PM", "Score": "18 - 15", "Result": "W", "Diff": "+3", "PassYds": 230, "TotalOffYds": 335},
        {"Week": 8, "Date": datetime.date(2026, 11, 2), "DayOfWeek": "Mon", "Opp": "SEA", "HomeAway": "@", "Venue": "Lumen Field", "Surface": "Turf", "GameTime": "MNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending", "PassYds": 0, "TotalOffYds": 0},
        {"Week": 9, "Date": datetime.date(2026, 11, 8), "DayOfWeek": "Sun", "Opp": "TB", "HomeAway": "vs", "Venue": "Soldier Field", "Surface": "Grass", "GameTime": "SNF", "Score": "Pending", "Result": "Pending", "Diff": "Pending", "PassYds": 0, "TotalOffYds": 0}
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

EXPANDED_CAREER_DATABASE = {
    "Josh Allen (QB - BUF)": {
        "category": "QB", "name": "Josh Allen", "pos": "QB", "jersey": "#17",
        "birth_date": datetime.date(1996, 5, 21), "team": "BUF", "exp": "7th Season (Draft 2018)",
        "seasons": {
            2024: OFFICIAL_SCHEDULE_SLATES["2024 Buffalo Bills Complete Slate"]
        }
    },
    "Patrick Mahomes (QB - KC)": {
        "category": "QB", "name": "Patrick Mahomes", "pos": "QB", "jersey": "#15",
        "birth_date": datetime.date(1995, 9, 17), "team": "KC", "exp": "8th Season (Draft 2017)",
        "seasons": {
            2024: [
                {"Week": 1, "Date": datetime.date(2024, 9, 5), "DayOfWeek": "Thu", "Opp": "BAL", "HomeAway": "vs", "Venue": "Arrowhead Stadium", "Surface": "Grass", "GameTime": "TNF", "Score": "27 - 20", "Result": "W", "Diff": "+7", "PassYds": 291, "TotalOffYds": 353}
            ]
        }
    },
    "Caleb Williams (QB - CHI)": {
        "category": "QB", "name": "Caleb Williams", "pos": "QB", "jersey": "#18",
        "birth_date": datetime.date(2001, 11, 18), "team": "CHI", "exp": "3rd Season (Draft 2024)",
        "seasons": {
            2026: OFFICIAL_SCHEDULE_SLATES["2026 Active NFL Slate (Weeks 1 - 9)"]
        }
    },
    "Chicago Bears (Franchise)": {
        "category": "FRANCHISE", "name": "Chicago Bears", "pos": "Franchise", "jersey": "—",
        "birth_date": datetime.date(1920, 9, 17), "team": "CHI", "exp": "104 Seasons (Charter APFA)",
        "seasons": {
            1920: [
                {"Week": 1, "Date": datetime.date(1920, 10, 3), "DayOfWeek": "Sun", "Opp": "Moline Tractors", "HomeAway": "vs", "Venue": "Staley Field", "Surface": "Grass", "GameTime": "2:30 PM", "Score": "20 - 0", "Result": "W", "Diff": "+20", "TotalOffYds": 285}
            ],
            2026: OFFICIAL_SCHEDULE_SLATES["2026 Active NFL Slate (Weeks 1 - 9)"]
        }
    }
}

for f_name, f_bdate in ALL_32_FRANCHISES.items():
    f_key = f"{f_name} (Franchise)"
    if f_key not in EXPANDED_CAREER_DATABASE:
        EXPANDED_CAREER_DATABASE[f_key] = {
            "category": "FRANCHISE", "name": f_name, "pos": "Franchise", "jersey": "—",
            "birth_date": f_bdate, "team": f_name[:3].upper(), "exp": f"Founded {f_bdate.year}",
            "seasons": {}
        }

# ==============================================================================
# 5. WORKSPACE TAB NAVIGATION
# ==============================================================================
tab_career, tab_matchup = st.tabs(["📊 Individual & Franchise Career Ledger", "⚔️ Head-to-Head Clash & Edge Engine"])

# ==============================================================================
# TAB 1: CAREER LEDGER & SLATE INGESTION
# ==============================================================================
with tab_career:
    st.subheader("1. Entity Selection & Metaphysical Baseline")
    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        selected_entity_key = st.selectbox("Search & Select Subject:", list(EXPANDED_CAREER_DATABASE.keys()), index=0)

    with top_col2:
        with st.expander("➕ Add Custom Subject"):
            c_name = st.text_input("Name", value="Jayden Daniels")
            c_pos = st.selectbox("Role", ["QB", "SKILL", "COACH", "FRANCHISE"], index=0)
            c_team = st.text_input("Team", value="WAS")
            c_bdate = st.date_input("Birthdate / Inception", value=datetime.date(2000, 12, 18))
            if st.button("Save Custom Subject"):
                custom_key = f"{c_name} ({c_pos} - {c_team})"
                EXPANDED_CAREER_DATABASE[custom_key] = {
                    "category": c_pos, "name": c_name, "pos": c_pos, "jersey": "Custom",
                    "birth_date": c_bdate, "team": c_team, "exp": "Custom Profile", "seasons": {}
                }
                selected_entity_key = custom_key
                st.success(f"Loaded {c_name}!")

    entity_data = EXPANDED_CAREER_DATABASE[selected_entity_key]

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

    st.markdown("---")
    st.subheader(f"2. Multi-Season Career Ledger for {entity_data['name']}")

    available_seasons = sorted(list(entity_data["seasons"].keys()), reverse=True)
    
    col_s1, col_s2 = st.columns([1, 3])
    with col_s1:
        season_options = ["All Career Seasons"] + [str(s) for s in available_seasons] if available_seasons else ["No Seasons Loaded"]
        selected_season_choice = st.selectbox("Filter Season:", season_options, index=0)
    
    with col_s2:
        with st.expander("⚡ Official Schedule Slate Ingestion (Live & Benchmark Feeds)"):
            chosen_slate = st.selectbox("Select Official Slate to Ingest:", list(OFFICIAL_SCHEDULE_SLATES.keys()), index=0)
            if st.button("Ingest & Hydrate Official Slate"):
                slate_year = OFFICIAL_SCHEDULE_SLATES[chosen_slate][0]["Date"].year
                entity_data["seasons"][slate_year] = OFFICIAL_SCHEDULE_SLATES[chosen_slate]
                st.success(f"Ingested {chosen_slate} into {entity_data['name']}!")
                st.rerun()

    available_seasons = sorted(list(entity_data["seasons"].keys()), reverse=True)
    target_seasons = available_seasons if selected_season_choice == "All Career Seasons" else ([int(selected_season_choice)] if selected_season_choice in [str(s) for s in available_seasons] else available_seasons[:1])

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
        primary_stat = g.get("PassYds", 0) if cat == "QB" else g.get("TotalOffYds", 0)
        
        is_pending = g.get("Result") == "Pending"
        stat_red = reduce_digits(primary_stat, preserve_masters=False) if (primary_stat > 0 and not is_pending) else 0
        
        if is_pending:
            match_str = "⏳ Kickoff Pending"
        else:
            pd_hit = (stat_red == pd_val) and primary_stat > 0
            ud_hit = (stat_red == ud) and primary_stat > 0
            power_hit = (stat_red == power_num) and primary_stat > 0
            
            if pd_hit and power_hit:
                match_str = "⚡ POWER CROSS-MATCH (PD+Power#)"
            elif pd_hit:
                match_str = "⚡ PERSONAL DAY MATCH"
            elif ud_hit:
                match_str = "🌐 UNIVERSAL DAY MATCH"
            elif power_hit:
                match_str = "🔋 POWER# MATCH"
            else:
                match_str = "—"
        
        row = {
            "Season": g.get("Season", g_date.year), "Week": g.get("Week"), "Date": g_date.strftime("%Y-%m-%d"),
            "Day of Week": g.get("DayOfWeek"), "Opponent": g.get("Opp"), "Home/Away": g.get("HomeAway"),
            "Stadium / Venue": g.get("Venue"), "Surface": g.get("Surface"), "Game Time": g.get("GameTime"),
            "Final Score": g.get("Score"), "Result": g.get("Result"), "Point Diff": g.get("Diff"),
            "Life Path Number": natal_lp, "Day of Birth Reduced": natal_dob_red,
            "Chinese Zodiac Animal": natal_animal, "Fixed / Heavenly Element": natal_element,
            "Yin / Yang Polarity": natal_polarity, "Birth Year Reduction": birth_yr_red,
            "Flip Status": "Flipped" if has_flipped else "Pre-Flip", "Game Day Life Path": game_lp,
            "Power#": power_num, "Game Year Animal & Element": f"{g_element} {g_animal}",
            "Affinity Status": affinity, "Universal Year (UY)": uy, "Universal Month (UM)": um,
            "Universal Day (UD)": ud, "Personal Year (PY)": py, "Personal Month (PM)": pm,
            "Personal Day (PD)": pd_val, "Primary Stat": primary_stat, "Stat Vibration": stat_red if not is_pending else "—",
            "Cross-Resonance Match": match_str,
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
        ledger_rows.append(row)

    df = pd.DataFrame(ledger_rows)

    if not df.empty:
        with st.expander("⚡ Cross-Resonance Scanner & Filter Controls", expanded=True):
            f_c1, f_c2, f_c3, f_c4 = st.columns(4)
            with f_c1:
                scanner_match_type = st.selectbox(
                    "Cross-Resonance Filter:",
                    ["All Games", "Any Resonance Hit", "Power Cross-Match (PD+Power#)", "Personal Day Match", "Universal Day Match", "Power# Match"]
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
            filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("MATCH")]
        elif scanner_match_type == "Power Cross-Match (PD+Power#)":
            filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("POWER CROSS-MATCH")]
        elif scanner_match_type == "Personal Day Match":
            filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("PERSONAL DAY MATCH")]
        elif scanner_match_type == "Universal Day Match":
            filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("UNIVERSAL DAY MATCH")]
        elif scanner_match_type == "Power# Match":
            filtered_df = filtered_df[filtered_df["Cross-Resonance Match"].str.contains("POWER# MATCH")]

        if selected_power != "All":
            filtered_df = filtered_df[filtered_df["Power#"].astype(str) == selected_power]
        if selected_affinity != "All":
            filtered_df = filtered_df[filtered_df["Affinity Status"] == selected_affinity]
        if selected_result != "All":
            filtered_df = filtered_df[filtered_df["Result"] == selected_result]

        def apply_visual_highlights(row):
            styles = [''] * len(row)
            m_val = str(row.get("Cross-Resonance Match", ""))
            if "POWER CROSS-MATCH" in m_val:
                match_idx = row.index.get_loc("Cross-Resonance Match")
                styles[match_idx] = 'background-color: #064e3b; color: #6ee7b7; font-weight: bold;'
            elif "MATCH" in m_val:
                match_idx = row.index.get_loc("Cross-Resonance Match")
                styles[match_idx] = 'background-color: #1b4332; color: #a3e635; font-weight: bold;'
            elif "Pending" in m_val:
                match_idx = row.index.get_loc("Cross-Resonance Match")
                styles[match_idx] = 'background-color: #451a03; color: #fde68a; font-weight: 500;'
                
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

        st.markdown("### 📊 Correlation Overview")
        m1, m2, m3, m4 = st.columns(4)
        total_g = len(filtered_df)
        num_hits = len(filtered_df[filtered_df["Cross-Resonance Match"].str.contains("MATCH")]) if total_g > 0 else 0
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

# ==============================================================================
# TAB 2: HEAD-TO-HEAD CLASH & MATCHUP ENGINE
# ==============================================================================
with tab_matchup:
    st.subheader("⚔️ Head-to-Head Clash & Edge Engine")
    st.caption("Compare two players, coaches, or franchises side-by-side across Personal Day, Universal Day, Power#, and planetary cycles.")

    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        entity_a_key = st.selectbox("Primary Subject (Side A):", list(EXPANDED_CAREER_DATABASE.keys()), index=0)
    with m_col2:
        entity_b_key = st.selectbox("Opposing Subject (Side B):", list(EXPANDED_CAREER_DATABASE.keys()), index=1)
    with m_col3:
        matchup_date = st.date_input("Matchup Kickoff Date:", value=datetime.date(2026, 11, 8), key="clash_kickoff_date")

    ent_a = EXPANDED_CAREER_DATABASE[entity_a_key]
    ent_b = EXPANDED_CAREER_DATABASE[entity_b_key]

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

    g_power = reduce_digits(matchup_date.day, preserve_masters=True)
    g_uy = reduce_digits(matchup_date.year, preserve_masters=False)
    g_ud = reduce_digits(reduce_digits(g_uy + matchup_date.month, preserve_masters=False) + reduce_digits(matchup_date.day, preserve_masters=False), preserve_masters=False)
    g_animal, g_elem, _ = get_chinese_profile(matchup_date.year)

    a_aff = evaluate_affinity(a_animal, g_animal)
    b_aff = evaluate_affinity(b_animal, g_animal)

    st.markdown("---")
    st.markdown(f"### 🛡️ Head-to-Head Comparison: {ent_a['name']} vs. {ent_b['name']}")
    
    comp_col1, comp_col2, comp_col3 = st.columns([2, 1, 2])
    with comp_col1:
        st.markdown(f"#### 🔵 {ent_a['name']} ({ent_a['team']})")
        st.write(f"**Role:** {ent_a['pos']} | **Natal Life Path:** {a_lp}")
        st.write(f"**Chinese Sign:** {a_elem} {a_animal} ({a_aff})")
        st.metric("Personal Day (PD)", f"{a_pd}")
        st.metric("Personal Year (PY)", f"{a_py}")

    with comp_col2:
        st.markdown("#### ⚡ Game Kickoff")
        st.metric("Power#", f"{g_power}")
        st.metric("Universal Day (UD)", f"{g_ud}")
        st.write(f"**Year Animal:** {g_elem} {g_animal}")

    with comp_col3:
        st.markdown(f"#### 🔴 {ent_b['name']} ({ent_b['team']})")
        st.write(f"**Role:** {ent_b['pos']} | **Natal Life Path:** {b_lp}")
        st.write(f"**Chinese Sign:** {b_elem} {b_animal} ({b_aff})")
        st.metric("Personal Day (PD)", f"{b_pd}")
        st.metric("Personal Year (PY)", f"{b_py}")

    st.markdown("---")
    st.markdown("### 🏆 Comparative Metaphysical Edge")
    a_score, b_score = 0, 0
    reasons = []

    if a_pd == g_power or a_pd == g_ud:
        a_score += 2
        reasons.append(f"🔵 **{ent_a['name']}** holds a direct Personal Day match with the Game Day ({a_pd}).")
    if b_pd == g_power or b_pd == g_ud:
        b_score += 2
        reasons.append(f"🔴 **{ent_b['name']}** holds a direct Personal Day match with the Game Day ({b_pd}).")

    if "San He" in a_aff or "Liu He" in a_aff:
        a_score += 2
        reasons.append(f"🔵 **{ent_a['name']}** operates in a harmonious astrological year ({a_aff}).")
    elif "Chong" in a_aff or "Xing" in a_aff:
        a_score -= 2
        reasons.append(f"⚠️ **{ent_a['name']}** operates under astrological friction ({a_aff}).")

    if "San He" in b_aff or "Liu He" in b_aff:
        b_score += 2
        reasons.append(f"🔴 **{ent_b['name']}** operates in a harmonious astrological year ({b_aff}).")
    elif "Chong" in b_aff or "Xing" in b_aff:
        b_score -= 2
        reasons.append(f"⚠️ **{ent_b['name']}** operates under astrological friction ({b_aff}).")

    if a_score > b_score:
        st.success(f"**Verdict:** Metaphysical Advantage favors **{ent_a['name']}** (Score: {a_score} vs. {b_score})")
    elif b_score > a_score:
        st.error(f"**Verdict:** Metaphysical Advantage favors **{ent_b['name']}** (Score: {b_score} vs. {a_score})")
    else:
        st.info(f"**Verdict:** Neutral Metaphysical Equilibrium (Score: {a_score} vs. {b_score})")

    for r in reasons:
        st.markdown(f"- {r}")