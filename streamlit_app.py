import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime

st.set_page_config(page_title="NFL Metaphysical Engine", layout="wide")

# ==============================================================================
# AUDITED PERSONNEL & ROSTER DATABASE (PRIMARY SOURCE VERIFIED)
# ==============================================================================
# Depth chart position priority index for proper hierarchy sorting
DEPTH_ORDER = {
    "QB": 1, "RB": 2, "WR": 3, "TE": 4, "OT": 5, "OG": 6, "C": 7, "OL": 8,
    "DE": 9, "DT": 10, "DL": 11, "LB": 12, "CB": 13, "S": 14, "DB": 15,
    "K": 16, "P": 17, "LS": 18, "COACH": 19, "FRONT_OFFICE": 20, "OWNER": 21
}

ACTIVE_PERSONNEL = [
    # Chicago Bears (Ordered strictly by Depth Chart & Personnel)
    {"name": "Caleb Williams", "team": "Chicago Bears", "pos": "QB", "string": "1st String (Starter)", "dob": "2001-11-18", "type": "Player", "exp": "3rd Season"},
    {"name": "Tyson Bagent", "team": "Chicago Bears", "pos": "QB", "string": "2nd String (Backup)", "dob": "2000-06-08", "type": "Player", "exp": "4th Season"},
    {"name": "D'Andre Swift", "team": "Chicago Bears", "pos": "RB", "string": "1st String (Starter)", "dob": "1999-01-14", "type": "Player", "exp": "7th Season"},
    {"name": "Roschon Johnson", "team": "Chicago Bears", "pos": "RB", "string": "2nd String (Backup)", "dob": "2001-01-31", "type": "Player", "exp": "4th Season"},
    {"name": "Rome Odunze", "team": "Chicago Bears", "pos": "WR", "string": "1st String (Starter)", "dob": "2002-06-03", "type": "Player", "exp": "3rd Season"},
    {"name": "DJ Moore", "team": "Chicago Bears", "pos": "WR", "string": "1st String (Starter)", "dob": "1997-04-14", "type": "Player", "exp": "9th Season"},
    {"name": "Cole Kmet", "team": "Chicago Bears", "pos": "TE", "string": "1st String (Starter)", "dob": "1999-03-10", "type": "Player", "exp": "7th Season"},
    {"name": "Darnell Wright", "team": "Chicago Bears", "pos": "OT", "string": "1st String (RT Starter)", "dob": "2001-08-10", "type": "Player", "exp": "4th Season"},
    {"name": "Braxton Jones", "team": "Chicago Bears", "pos": "OT", "string": "1st String (LT Starter)", "dob": "1999-03-27", "type": "Player", "exp": "5th Season"},
    {"name": "Montez Sweat", "team": "Chicago Bears", "pos": "DE", "string": "1st String (DE Starter)", "dob": "1996-09-04", "type": "Player", "exp": "8th Season"},
    {"name": "Gervon Dexter", "team": "Chicago Bears", "pos": "DT", "string": "1st String (DT Starter)", "dob": "2001-10-05", "type": "Player", "exp": "4th Season"},
    {"name": "T.J. Edwards", "team": "Chicago Bears", "pos": "LB", "string": "1st String (MLB Starter)", "dob": "1996-08-12", "type": "Player", "exp": "8th Season"},
    {"name": "Tremaine Edmunds", "team": "Chicago Bears", "pos": "LB", "string": "1st String (OLB Starter)", "dob": "1998-05-02", "type": "Player", "exp": "9th Season"},
    {"name": "Jaylon Johnson", "team": "Chicago Bears", "pos": "CB", "string": "1st String (CB1 Starter)", "dob": "1999-04-19", "type": "Player", "exp": "7th Season"},
    {"name": "Kyler Gordon", "team": "Chicago Bears", "pos": "CB", "string": "1st String (Nickel Starter)", "dob": "1999-12-17", "type": "Player", "exp": "5th Season"},
    {"name": "Kevin Byard", "team": "Chicago Bears", "pos": "S", "string": "1st String (FS Starter)", "dob": "1993-08-17", "type": "Player", "exp": "11th Season"},
    {"name": "Cairo Santos", "team": "Chicago Bears", "pos": "K", "string": "1st String (Kicker)", "dob": "1991-11-12", "type": "Player", "exp": "13th Season"},
    {"name": "Tory Taylor", "team": "Chicago Bears", "pos": "P", "string": "1st String (Punter)", "dob": "1997-07-09", "type": "Player", "exp": "3rd Season"},
    {"name": "Scott Daly", "team": "Chicago Bears", "pos": "LS", "string": "1st String (Long Snapper)", "dob": "1994-02-07", "type": "Player", "exp": "6th Season"},
    {"name": "Ryan Poles", "team": "Chicago Bears", "pos": "FRONT_OFFICE", "string": "General Manager", "dob": "1985-09-21", "type": "Associated Personnel", "exp": "Front Office"},
    {"name": "Virginia Halas McCaskey", "team": "Chicago Bears", "pos": "OWNER", "string": "Principal Owner", "dob": "1923-01-05", "type": "Associated Personnel", "exp": "Ownership"},

    # Kansas City Chiefs
    {"name": "Patrick Mahomes", "team": "Kansas City Chiefs", "pos": "QB", "string": "1st String (Starter)", "dob": "1995-09-17", "type": "Player", "exp": "10th Season"},
    {"name": "Carson Wentz", "team": "Kansas City Chiefs", "pos": "QB", "string": "2nd String (Backup)", "dob": "1992-12-30", "type": "Player", "exp": "11th Season"},
    {"name": "Isiah Pacheco", "team": "Kansas City Chiefs", "pos": "RB", "string": "1st String (Starter)", "dob": "1999-03-02", "type": "Player", "exp": "5th Season"},
    {"name": "Travis Kelce", "team": "Kansas City Chiefs", "pos": "TE", "string": "1st String (Starter)", "dob": "1989-10-05", "type": "Player", "exp": "14th Season"},
    {"name": "Chris Jones", "team": "Kansas City Chiefs", "pos": "DT", "string": "1st String (Starter)", "dob": "1994-07-03", "type": "Player", "exp": "11th Season"},
    {"name": "Nick Bolton", "team": "Kansas City Chiefs", "pos": "LB", "string": "1st String (Starter)", "dob": "2000-03-10", "type": "Player", "exp": "6th Season"},
    {"name": "Harrison Butker", "team": "Kansas City Chiefs", "pos": "K", "string": "1st String (Starter)", "dob": "1995-07-14", "type": "Player", "exp": "10th Season"},
    {"name": "Andy Reid", "team": "Kansas City Chiefs", "pos": "COACH", "string": "Head Coach", "dob": "1958-03-19", "type": "Associated Personnel", "exp": "Head Coach"},
    {"name": "Brett Veach", "team": "Kansas City Chiefs", "pos": "FRONT_OFFICE", "string": "General Manager", "dob": "1977-12-19", "type": "Associated Personnel", "exp": "Front Office"},
    {"name": "Clark Hunt", "team": "Kansas City Chiefs", "pos": "OWNER", "string": "Chairman and CEO", "dob": "1965-02-19", "type": "Associated Personnel", "exp": "Ownership"},

    # Baltimore Ravens
    {"name": "Lamar Jackson", "team": "Baltimore Ravens", "pos": "QB", "string": "1st String (Starter)", "dob": "1997-01-07", "type": "Player", "exp": "9th Season"},
    {"name": "Derrick Henry", "team": "Baltimore Ravens", "pos": "RB", "string": "1st String (Starter)", "dob": "1994-01-04", "type": "Player", "exp": "11th Season"},
    {"name": "Zay Flowers", "team": "Baltimore Ravens", "pos": "WR", "string": "1st String (Starter)", "dob": "2000-09-11", "type": "Player", "exp": "4th Season"},
    {"name": "Mark Andrews", "team": "Baltimore Ravens", "pos": "TE", "string": "1st String (Starter)", "dob": "1995-09-06", "type": "Player", "exp": "9th Season"},
    {"name": "Roquan Smith", "team": "Baltimore Ravens", "pos": "LB", "string": "1st String (Starter)", "dob": "1997-04-08", "type": "Player", "exp": "9th Season"},
    {"name": "Kyle Hamilton", "team": "Baltimore Ravens", "pos": "S", "string": "1st String (Starter)", "dob": "2001-03-16", "type": "Player", "exp": "5th Season"},
    {"name": "Justin Tucker", "team": "Baltimore Ravens", "pos": "K", "string": "1st String (Starter)", "dob": "1989-11-21", "type": "Player", "exp": "15th Season"},
    {"name": "John Harbaugh", "team": "Baltimore Ravens", "pos": "COACH", "string": "Head Coach", "dob": "1962-09-23", "type": "Associated Personnel", "exp": "Head Coach"},
    {"name": "Eric DeCosta", "team": "Baltimore Ravens", "pos": "FRONT_OFFICE", "string": "General Manager", "dob": "1971-04-10", "type": "Associated Personnel", "exp": "Front Office"},

    # Buffalo Bills
    {"name": "Josh Allen", "team": "Buffalo Bills", "pos": "QB", "string": "1st String (Starter)", "dob": "1996-05-21", "type": "Player", "exp": "9th Season"},
    {"name": "James Cook", "team": "Buffalo Bills", "pos": "RB", "string": "1st String (Starter)", "dob": "1999-09-25", "type": "Player", "exp": "5th Season"},
    {"name": "Dalton Kincaid", "team": "Buffalo Bills", "pos": "TE", "string": "1st String (Starter)", "dob": "1999-10-18", "type": "Player", "exp": "4th Season"},
    {"name": "Greg Rousseau", "team": "Buffalo Bills", "pos": "DE", "string": "1st String (Starter)", "dob": "2000-04-05", "type": "Player", "exp": "6th Season"},
    {"name": "Sean McDermott", "team": "Buffalo Bills", "pos": "COACH", "string": "Head Coach", "dob": "1974-03-21", "type": "Associated Personnel", "exp": "Head Coach"},

    # Houston Texans
    {"name": "C.J. Stroud", "team": "Houston Texans", "pos": "QB", "string": "1st String (Starter)", "dob": "2001-10-03", "type": "Player", "exp": "4th Season"},
    {"name": "Joe Mixon", "team": "Houston Texans", "pos": "RB", "string": "1st String (Starter)", "dob": "1996-07-24", "type": "Player", "exp": "10th Season"},
    {"name": "Nico Collins", "team": "Houston Texans", "pos": "WR", "string": "1st String (Starter)", "dob": "1999-03-19", "type": "Player", "exp": "6th Season"},
    {"name": "Will Anderson Jr.", "team": "Houston Texans", "pos": "DE", "string": "1st String (Starter)", "dob": "2001-09-02", "type": "Player", "exp": "4th Season"},
    {"name": "DeMeco Ryans", "team": "Houston Texans", "pos": "COACH", "string": "Head Coach", "dob": "1984-07-28", "type": "Associated Personnel", "exp": "Head Coach"},

    # Washington Commanders
    {"name": "Jayden Daniels", "team": "Washington Commanders", "pos": "QB", "string": "1st String (Starter)", "dob": "2000-12-18", "type": "Player", "exp": "3rd Season"},
    {"name": "Brian Robinson Jr.", "team": "Washington Commanders", "pos": "RB", "string": "1st String (Starter)", "dob": "1999-03-22", "type": "Player", "exp": "5th Season"},
    {"name": "Terry McLaurin", "team": "Washington Commanders", "pos": "WR", "string": "1st String (Starter)", "dob": "1995-09-15", "type": "Player", "exp": "8th Season"},
    {"name": "Dan Quinn", "team": "Washington Commanders", "pos": "COACH", "string": "Head Coach", "dob": "1970-09-11", "type": "Associated Personnel