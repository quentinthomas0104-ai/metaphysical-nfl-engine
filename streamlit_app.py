import streamlit as st
import datetime

st.set_page_config(page_title="Metaphysical Analytics Engine", layout="wide")

st.title("🏈 Metaphysical Analytics Engine")
st.caption("3-Step Protocol: Precise Calendar Birthday-Flips, Numerology & Chinese Astrology")

# --- 1. BASELINE CONFIGURATION & REDUCTION FUNCTIONS ---
def reduce_digits(n: int, preserve_masters: bool = False) -> int:
    """Reduces an integer to a single digit (1-9), optionally preserving 11, 22, 33."""
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
    # Base year 1924 = Wood Rat (Rat index 0, Wood index 0)
    zodiac_idx = (year - 4) % 12
    element_idx = ((year - 4) // 2) % 5
    return ELEMENTS[element_idx], CHINESE_ZODIAC[zodiac_idx]

# --- 2. USER INPUTS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Subject Profile")
    subject_name = st.text_input("Name / Entity", value="Chicago Bears")
    birth_date = st.date_input(
        "Birthdate / Inception Date",
        value=datetime.date(1920, 9, 17),
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date(2030, 12, 31)
    )

with col2:
    st.subheader("2. Event / Game Date")
    game_date = st.date_input(
        "Game Date",
        value=datetime.date(2026, 11, 1),
        min_value=datetime.date(1920, 1, 1),
        max_value=datetime.date(2030, 12, 31)
    )

# --- 3. AUDIT & ENGINE CALCULATIONS ---
# Base Calculations (Birth Month + Birth Day)
b_month = birth_date.month
b_day_reduced = reduce_digits(birth_date.day)
base_number = reduce_digits(b_month + b_day_reduced)

# Precise Calendar Birthday-Flip Logic:
# If game is on or after the birthday in that calendar year -> Cycle Year = Game Year
# If game is before the birthday in that calendar year -> Cycle Year = Game Year - 1
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

# Chinese Zodiac & Harmony
sub_elem, sub_animal = get_chinese_zodiac(birth_date.year)
game_elem, game_animal = get_chinese_zodiac(game_date.year)

# Harmony Matrix for Rat/Monkey/Ox comparisons
st.markdown("---")
st.subheader("3. Audit Results & Mathematical Ledger")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Cycle Year", f"{cycle_year} (Reduces to {cycle_yr_reduced})")
m2.metric("Personal Year (PY)", f"{personal_year}")
m3.metric("Personal Month (PM)", f"{personal_month}")
m4.metric("Personal Day (PD)", f"{personal_day}")

st.markdown("### Step-by-Step Mathematical Verification")
st.write(f"- **Birthday Flip Check:** Game Date `{game_date.strftime('%B %d')}` vs Birthday `{birth_date.strftime('%B %d')}` -> **{'Flipped (Game Year)' if has_flipped else 'Not Flipped Yet (Game Year - 1)'}**")
st.write(f"- **Base (Month + Day):** `{b_month} + {b_day_reduced} = {b_month + b_day_reduced}` -> **{base_number}**")
st.write(f"- **Personal Year Math:** Base `{base_number}` + Cycle Year `{cycle_yr_reduced}` -> **{personal_year}**")
st.write(f"- **Personal Month Math:** PY `{personal_year}` + Game Month `{game_month}` -> **{personal_month}**")
st.write(f"- **Personal Day Math:** PM `{personal_month}` + Game Day `{game_day_reduced}` -> **{personal_day}**")
st.write(f"- **Universal Day:** `{game_date.strftime('%Y-%m-%d')}` -> **{univ_day}**")
st.write(f"- **Astrological Profiles:** Subject is **{sub_elem} {sub_animal}**, Game Year is **{game_elem} {game_animal}**")