import streamlit as st
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("3-Step Protocol: Birthday-Flips, Numerology Cycles & Box-Score Correlator")

# --- 1. CORE MATHEMATICAL & REDUCTION FUNCTIONS ---
def reduce_digits(n: int, preserve_masters: bool = False) -> int:
    """Reduces an integer to a single digit (1-9), optionally preserving master numbers."""
    if preserve_masters and n in [11, 22, 33]:
        return n
    while n > 9:
        if preserve_masters and n in [11, 22, 33]:
            return n
        n = sum(int(d) for d in str(n))
    return n

CHINESE_ZODIAC = ["Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat", "Monkey", "Rooster", "Dog", "Pig"]
ELEMENTS = ["Wood", "Fire", "Earth", "Metal", "Water"]

def get_chinese_zodiac(year: int):
    zodiac_idx = (year - 4) % 12
    element_idx = ((year - 4) // 2) % 5
    return ELEMENTS[element_idx], CHINESE_ZODIAC[zodiac_idx]

# --- 2. INPUT SECTIONS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Subject Profile")
    subject_name = st.text_input("Player / Team Name", value="Chicago Bears")
    birth_date = st.date_input(
        "Birthdate / Inception Date",
        value=datetime.date(1920, 9, 17),
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date(2030, 12, 31)
    )

with col2:
    st.subheader("2. Event & Game Setup")
    game_date = st.date_input(
        "Game Date",
        value=datetime.date(2026, 11, 1),
        min_value=datetime.date(1920, 1, 1),
        max_value=datetime.date(2030, 12, 31)
    )
    opponent_name = st.text_input("Opponent (Optional)", value="Green Bay Packers")

# --- 3. BOX-SCORE & STAT TRACKER INPUTS ---
st.markdown("---")
st.subheader("📊 Box-Score & Game Stats Correlator")
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    stat_type = st.selectbox("Primary Role / Stat Set", ["Offensive (Skill)", "Quarterback", "Defensive (IDP)", "Kicker / Special Teams"])

with stat_col2:
    if stat_type == "Quarterback":
        primary_stat = st.number_input("Pass Yards", min_value=0, value=245, step=1)
        secondary_stat = st.number_input("Pass TDs", min_value=0, value=2, step=1)
    elif stat_type == "Offensive (Skill)":
        primary_stat = st.number_input("Total Rush/Rec Yards", min_value=0, value=94, step=1)
        secondary_stat = st.number_input("Total Touchdowns", min_value=0, value=1, step=1)
    elif stat_type == "Defensive (IDP)":
        primary_stat = st.number_input("Total Tackles", min_value=0, value=8, step=1)
        secondary_stat = st.number_input("Sacks / TFL", min_value=0.0, value=1.5, step=0.5)
    else:
        primary_stat = st.number_input("Field Goals Made", min_value=0, value=3, step=1)
        secondary_stat = st.number_input("Total Kicking Points", min_value=0, value=11, step=1)

with stat_col3:
    fantasy_points = st.number_input("PPR / Fantasy Points", min_value=0.0, value=18.4, step=0.1)

with stat_col4:
    stat_reduced = reduce_digits(int(primary_stat))
    st.metric("Primary Stat Reduction", f"{int(primary_stat)} -> {stat_reduced}")
    st.caption("Single-digit vibration of primary yardage/production.")

# --- 4. AUDIT & NUMEROLOGY ENGINE CALCULATIONS ---
b_month = birth_date.month
b_day_reduced = reduce_digits(birth_date.day)
base_number = reduce_digits(b_month + b_day_reduced)

# Precise Calendar Birthday-Flip Logic:
# If game date is on or after the birthday in that calendar year -> Cycle Year = Game Year
# If game date is before the birthday in that calendar year -> Cycle Year = Game Year - 1
birthday_this_year = datetime.date(game_date.year, birth_date.month, birth_date.day)
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

# Universal Day Calculation
univ_day = reduce_digits(reduce_digits(game_date.year) + game_date.month + game_date.day)

# Chinese Zodiac Profiles
sub_elem, sub_animal = get_chinese_zodiac(birth_date.year)
game_elem, game_animal = get_chinese_zodiac(game_date.year)

# Stat-to-Cycle Harmony Check
is_direct_hit = (stat_reduced == personal_day) or (stat_reduced == univ_day)

# --- 5. RESULTS LEDGER & CORRELATION DASHBOARD ---
st.markdown("---")
st.subheader("3. Audit Results & Metaphysical Ledger")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Cycle Year", f"{cycle_year} (Reduces to {cycle_yr_reduced})")
m2.metric("Personal Year (PY)", f"{personal_year}")
m3.metric("Personal Month (PM)", f"{personal_month}")
m4.metric("Personal Day (PD)", f"{personal_day}")

st.markdown("### Step-by-Step Mathematical Verification")
st.write(f"- **Birthday Flip Check:** Game `{game_date.strftime('%B %d')}` vs Birthday `{birth_date.strftime('%B %d')}` -> **{'Flipped (Game Year)' if has_flipped else 'Not Flipped Yet (Game Year - 1)'}**")
st.write(f"- **Base (Month + Day):** `{b_month} + {b_day_reduced}` -> **{base_number}**")
st.write(f"- **Personal Year Math:** Base `{base_number}` + Cycle Year `{cycle_yr_reduced}` -> **{personal_year}**")
st.write(f"- **Personal Month Math:** PY `{personal_year}` + Game Month `{game_month}` -> **{personal_month}**")
st.write(f"- **Personal Day Math:** PM `{personal_month}` + Game Day `{game_day_reduced}` -> **{personal_day}**")
st.write(f"- **Universal Day:** `{game_date.strftime('%Y-%m-%d')}` -> **{univ_day}**")
st.write(f"- **Astrological Profiles:** Subject is **{sub_elem} {sub_animal}**, Game Year is **{game_elem} {game_animal}**")

# Correlation Alert
st.markdown("### 🔍 Cycle-to-Performance Correlation")
if is_direct_hit:
    st.success(f"⚡ Direct Harmonic Match: Primary Stat reduction ({stat_reduced}) matches Personal Day ({personal_day}) or Universal Day ({univ_day})!")
else:
    st.info(f"Vibrational Spread: Stat reduced to {stat_reduced} against Personal Day {personal_day} and Universal Day {univ_day}.")