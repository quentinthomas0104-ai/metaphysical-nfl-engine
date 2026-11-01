import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime

st.set_page_config(page_title="Metaphysical NFL Spreadsheet", layout="wide")

st.title("📊 Metaphysical NFL Analytics Spreadsheet")
st.caption("Excel-style metaphysical calculator: Look up any entity, test any date, and isolate patterns.")

# ==============================================================================
# CALCULATION ENGINES
# ==============================================================================
def reduce_num(n: int, preserve_masters: bool = True) -> int:
    if not n:
        return 0
    n = abs(int(n))
    if preserve_masters and n in [11, 22, 33]:
        return n
    while n > 9:
        if preserve_masters and n in [11, 22, 33]:
            return n
        n = sum(int(d) for d in str(n))
    return n

def get_life_path(d: datetime.date) -> int:
    m = reduce_num(d.month, False)
    day = reduce_num(d.day, True)
    y = reduce_num(d.year, False)
    return reduce_num(m + day + y, True)

CHINESE_ZODIAC = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
CHINESE_ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

SAN_HE = {
    "Rat": ["Dragon", "Monkey"], "Dragon": ["Rat", "Monkey"], "Monkey": ["Rat", "Dragon"],
    "Ox": ["Snake", "Rooster"], "Snake": ["Ox", "Rooster"], "Rooster": ["Ox", "Snake"],
    "Tiger": ["Horse", "Dog"], "Horse": ["Tiger", "Dog"], "Dog": ["Tiger", "Horse"],
    "Rabbit": ["Goat", "Pig"], "Goat": ["Rabbit", "Pig"], "Pig": ["Rabbit", "Goat"]
}
LIU_HE = {
    "Rat": "Ox", "Ox": "Rat", "Tiger": "Pig", "Pig": "Tiger",
    "Rabbit": "Dog", "Dog": "Rabbit", "Dragon": "Rooster", "Rooster": "Dragon",
    "Snake": "Monkey", "Monkey": "Snake", "Horse": "Goat", "Goat": "Horse"
}
CHONG = {
    "Rat": "Horse", "Horse": "Rat", "Ox": "Goat", "Goat": "Ox",
    "Tiger": "Monkey", "Monkey": "Tiger", "Rabbit": "Rooster", "Rooster": "Rabbit",
    "Dragon": "Dog", "Dog": "Dragon", "Snake": "Pig", "Pig": "Snake"
}

def get_chinese(year: int):
    z = CHINESE_ZODIAC[(year - 4) % 12]
    e = CHINESE_ELEMENTS[((year - 4) // 2) % 5]
    pol = "Yang" if (year % 2 == 0) else "Yin"
    return z, e, pol

def get_affinity(natal_z: str, target_z: str) -> str:
    if target_z in SAN_HE.get(natal_z, []):
        return "San He (Harmony)"
    if LIU_HE.get(natal_z) == target_z:
        return "Liu He (Secret Friend)"
    if CHONG.get(natal_z) == target_z:
        return "Chong (Clash)"
    return "Neutral"

PLANET_PERIODS = {
    "Sun": 365.256, "Moon": 27.321, "Mercury": 87.969, "Venus": 224.701,
    "Mars": 686.980, "Jupiter": 4332.589, "Saturn": 10759.22
}
J2000_LONGS = {
    "Sun": 280.46, "Moon": 218.32, "Mercury": 252.25, "Venus": 181.98,
    "Mars": 355.43, "Jupiter": 34.35, "Saturn": 50.44
}
ZODIAC_SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

def get_planet_pos(planet: str, d: datetime.date):
    days = (d - datetime.date(2000, 1, 1)).days
    deg = (J2000_LONGS[planet] + (days * (360.0 / PLANET_PERIODS[planet]))) % 360.0
    return deg, ZODIAC_SIGNS[int(deg // 30)]

def get_transit_aspect(p1: str, p2: str, t_date: datetime.date, n_date: datetime.date) -> str:
    d1, s1 = get_planet_pos(p1, t_date)
    d2, s2 = get_planet_pos(p2, n_date)
    diff = abs(d1 - d2) % 360
    if diff > 180:
        diff = 360 - diff
    if diff <= 8.0:
        return f"{p1} in {s1} Conj (0°) {p2} in {s2}"
    if abs(diff - 120.0) <= 8.0:
        return f"{p1} in {s1} Trine (120°) {p2} in {s2}"
    if abs(diff - 90.0) <= 7.0:
        return f"{p1} in {s1} Square (90°) {p2} in {s2}"
    if abs(diff - 180.0) <= 8.0:
        return f"{p1} in {s1} Opp (180°) {p2} in {s2}"
    return "—"

# ==============================================================================
# PRELOADED REGISTRY (IN-MEMORY, NO EXTERNAL JSON FILES)
# ==============================================================================
PRELOADED = {
    "Caleb Williams (QB - CHI)": datetime.date(2001, 11, 18),
    "Chicago Bears (Franchise)": datetime.date(1920, 9, 17),
    "Patrick Mahomes (QB - KC)": datetime.date(1995, 9, 17),
    "Josh Allen (QB - BUF)": datetime.date(1996, 5, 21),
    "Lamar Jackson (QB - BAL)": datetime.date(1997, 1, 7),
    "Jayden Daniels (QB - WAS)": datetime.date(2000, 12, 18),
    "C.J. Stroud (QB - HOU)": datetime.date(2001, 10, 3),
    "Mike Ditka (Coach - CHI)": datetime.date(1939, 10, 18),
    "Andy Reid (Coach - KC)": datetime.date(1958, 3, 19),
    "Matt Eberflus (Coach - CHI)": datetime.date(1970, 5, 17),
    "George Halas (Owner/Founder - CHI)": datetime.date(1895, 2, 2),
    "Walter Payton (RB - CHI)": datetime.date(1954, 7, 25),
    "Kansas City Chiefs (Franchise)": datetime.date(1959, 8, 14),
    "Green Bay Packers (Franchise)": datetime.date(1919, 8, 11),
    "Seattle Seahawks (Franchise)": datetime.date(1974, 6, 4),
    "Dallas Cowboys (Franchise)": datetime.date(1960, 1, 28)
}

# Preloaded Bears 2024 & 2026 game schedule dates
DEFAULT_GAME_DATES = [
    datetime.date(2024, 9, 8), datetime.date(2024, 9, 15), datetime.date(2024, 9, 22),
    datetime.date(2024, 9, 29), datetime.date(2024, 10, 6), datetime.date(2024, 10, 13),
    datetime.date(2024, 10, 27), datetime.date(2024, 11, 3), datetime.date(2024, 11, 10),
    datetime.date(2024, 11, 17), datetime.date(2024, 11, 24), datetime.date(2024, 11, 28),
    datetime.date(2024, 12, 8), datetime.date(2024, 12, 16), datetime.date(2024, 12, 22),
    datetime.date(2024, 12, 26), datetime.date(2025, 1, 5), datetime.date(2026, 9, 13),
    datetime.date(2026, 9, 20), datetime.date(2026, 9, 28), datetime.date(2026, 10, 4),
    datetime.date(2026, 10, 11), datetime.date(2026, 10, 18), datetime.date(2026, 10, 22),
    datetime.date(2026, 11, 2), datetime.date(2026, 11, 8), datetime.date(2026, 11, 15)
]

# ==============================================================================
# TOP CONTROLS: CHOOSE ENTITY & DATES
# ==============================================================================
c1, c2, c3 = st.columns([2, 1, 1])

with c1:
    selection_mode = st.radio("Entity Input Method:", ["Select from Registry", "Type Any Custom Name"], horizontal=True)
    if selection_mode == "Select from Registry":
        selected_name = st.selectbox("Choose Entity:", list(PRELOADED.keys()), index=0)
        birthdate = PRELOADED[selected_name]
    else:
        selected_name = st.text_input("Enter Full Name / Franchise Name:", value="Jim McMahon")
        birthdate = st.date_input("Birthdate / Founding Date:", value=datetime.date(1959, 8, 21))

natal_lp = get_life_path(birthdate)
natal_dob_red = reduce_num(birthdate.day, True)
natal_z, natal_elem, natal_pol = get_chinese(birthdate.year)
base_number = reduce_num(birthdate.month + reduce_num(birthdate.day, False), False)

with c2:
    st.metric("Life Path", f"{natal_lp}")
    st.metric("Day of Birth Red", f"{natal_dob_red}")

with c3:
    st.metric("Chinese Zodiac", f"{natal_elem} {natal_z} ({natal_pol})")
    st.metric("Birthdate", birthdate.strftime("%b %d, %Y"))

# ==============================================================================
# SPREADSHEET ROW BUILDER
# ==============================================================================
st.markdown("---")
st.subheader("📋 Metaphysical Game / Date Spreadsheet")

row_ctrl1, row_ctrl2 = st.columns([2, 2])
with row_ctrl1:
    date_preset = st.radio("Dates to Show:", ["Bears Game Schedule (2024–2026)", "Pick a Single Specific Date"], horizontal=True)

if date_preset == "Pick a Single Specific Date":
    with row_ctrl2:
        single_date = st.date_input("Select Any Date to Calculate:", value=datetime.date(2026, 11, 2))
    dates_to_run = [single_date]
else:
    dates_to_run = DEFAULT_GAME_DATES

rows = []
for target_d in dates_to_run:
    # Birthday flip check
    bday_target_year = datetime.date(target_d.year, birthdate.month, birthdate.day)
    has_flipped = (target_d >= bday_target_year)
    active_year = target_d.year if has_flipped else (target_d.year - 1)
    
    # Numerology
    py = reduce_num(base_number + reduce_num(active_year, False), False)
    pm = reduce_num(py + target_d.month, False)
    pd_val = reduce_num(pm + reduce_num(target_d.day, False), False)
    power_num = reduce_num(target_d.day, True)
    
    uy = reduce_num(target_d.year, False)
    um = reduce_num(uy + target_d.month, False)
    ud = reduce_num(um + reduce_num(target_d.day, False), False)
    game_lp = get_life_path(target_d)
    
    # Chinese
    t_z, t_elem, _ = get_chinese(target_d.year)
    aff = get_affinity(natal_z, t_z)
    
    # Matches
    is_power_match = "MATCH (PD=Power#)" if (pd_val == power_num) else "—"
    is_ud_match = "MATCH (PD=UD)" if (pd_val == ud) else "—"
    
    # Western
    mars_tr = get_transit_aspect("Mars", "Sun", target_d, birthdate)
    jup_tr = get_transit_aspect("Jupiter", "Sun", target_d, birthdate)
    sat_tr = get_transit_aspect("Saturn", "Sun", target_d, birthdate)

    rows.append({
        "Date": target_d.strftime("%Y-%m-%d"),
        "Day": target_d.strftime("%a"),
        "Personal Day (PD)": pd_val,
        "Power#": power_num,
        "Universal Day (UD)": ud,
        "PD vs Power#": is_power_match,
        "PD vs UD": is_ud_match,
        "Personal Year (PY)": py,
        "Flip Status": "Flipped" if has_flipped else "Pre-Flip",
        "Personal Month (PM)": pm,
        "Game Life Path": game_lp,
        "Year Animal & Element": f"{t_elem} {t_z}",
        "Year Affinity": aff,
        "Mars Transit (to Sun)": mars_tr,
        "Jupiter Transit (to Sun)": jup_tr,
        "Saturn Transit (to Sun)": sat_tr
    })

df = pd.DataFrame(rows)

# Filter Bar (like Excel column filters)
with st.expander("🔎 Quick Filters", expanded=False):
    f1, f2, f3 = st.columns(3)
    with f1:
        pd_filter = st.multiselect("Filter by Personal Day (PD):", options=sorted(df["Personal Day (PD)"].unique()))
    with f2:
        power_filter = st.multiselect("Filter by Power#:", options=sorted(df["Power#"].unique()))
    with f3:
        match_only = st.checkbox("Show Only Power# or UD Matches")

filtered_df = df.copy()
if pd_filter:
    filtered_df = filtered_df[filtered_df["Personal Day (PD)"].isin(pd_filter)]
if power_filter:
    filtered_df = filtered_df[filtered_df["Power#"].isin(power_filter)]
if match_only:
    filtered_df = filtered_df[(filtered_df["PD vs Power#"] != "—") | (filtered_df["PD vs UD"] != "—")]

st.dataframe(filtered_df, use_container_width=True, hide_index=True)

st.download_button(
    label="📥 Download This Table as CSV (Excel)",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name=f"{selected_name.replace(' ', '_')}_metaphysical_sheet.csv",
    mime="text/csv"
)