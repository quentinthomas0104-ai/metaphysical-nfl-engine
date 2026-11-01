import streamlit as st  # type: ignore
import pandas as pd     # type: ignore
import datetime

st.set_page_config(page_title="Ourlads NFL Depth Charts", layout="wide")

# ==============================================================================
# OURLADS DENSE EXCEL STYLING (HIGH DENSITY, CRISP BORDERS, COMPACT ROWS)
# ==============================================================================
st.markdown("""
    <style>
    /* Compact, dense spreadsheet typography */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* Top-left horizontal bar container */
    .top-nav-bar {
        background-color: #0d1117;
        padding: 6px 12px;
        border-radius: 4px;
        border: 1px solid #30363d;
        display: inline-flex;
        gap: 10px;
        align-items: center;
        margin-bottom: 12px;
    }
    
    /* Ourlads dense table styling */
    .ourlads-header {
        background-color: #161b22;
        color: #58a6ff;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        padding: 4px 8px;
        border-left: 3px solid #1f6feb;
        margin-top: 14px;
        margin-bottom: 6px;
    }
    
    .dense-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
        margin-bottom: 12px;
    }
    .dense-table th {
        background-color: #21262d;
        color: #c9d1d9;
        font-weight: 600;
        text-align: left;
        padding: 4px 8px;
        border: 1px solid #30363d;
        white-space: nowrap;
    }
    .dense-table td {
        padding: 3px 8px;
        border: 1px solid #30363d;
        color: #e6edf3;
        white-space: nowrap;
    }
    .dense-table tr:nth-child(even) {
        background-color: #0d1117;
    }
    .dense-table tr:nth-child(odd) {
        background-color: #161b22;
    }
    .pos-cell {
        font-weight: 700;
        color: #f0883e;
        width: 60px;
    }
    .dob-tag {
        color: #8b949e;
        font-size: 11px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# AUDITED PERSONNEL & DEPTH CHART SLATE
# ==============================================================================
# Exact Ourlads depth chart layout by unit
OURLADS_ROSTERS = {
    "Chicago Bears": {
        "Offense": [
            {"pos": "QB", "st1": "Caleb Williams (11/18/01)", "st2": "Tyson Bagent (06/08/00)", "st3": "Brett Rypien (07/09/96)", "st4": "Austin Reed (02/22/00)"},
            {"pos": "RB", "st1": "D'Andre Swift (01/14/99)", "st2": "Roschon Johnson (01/31/01)", "st3": "Khalil Herbert (04/21/98)", "st4": "Travis Homer (08/07/98)"},
            {"pos": "WR", "st1": "DJ Moore (04/14/97)", "st2": "Tyler Scott (10/12/01)", "st3": "Velus Jones Jr. (05/11/97)", "st4": "Collin Johnson (09/23/97)"},
            {"pos": "WR", "st1": "Rome Odunze (06/03/02)", "st2": "DeAndre Carter (04/10/93)", "st3": "Miles Boykin (10/12/96)", "st4": "—"},
            {"pos": "TE", "st1": "Cole Kmet (03/10/99)", "st2": "Gerald Everett (06/25/94)", "st3": "Marcedes Lewis (05/19/84)", "st4": "Tommy Sweeney (07/01/95)"},
            {"pos": "LT", "st1": "Braxton Jones (03/27/99)", "st2": "Kiran Amegadjie (02/01/02)", "st3": "Larry Borom (03/30/99)", "st4": "—"},
            {"pos": "LG", "st1": "Teven Jenkins (03/03/98)", "st2": "Bill Murray (07/18/97)", "st3": "—", "st4": "—"},
            {"pos": "C",  "st1": "Coleman Shelton (07/28/95)", "st2": "Ryan Bates (02/14/97)", "st3": "Doug Kramer Jr. (06/04/98)", "st4": "—"},
            {"pos": "RG", "st1": "Matt Pryor (12/16/94)", "st2": "Nate Davis (09/23/96)", "st3": "—", "st4": "—"},
            {"pos": "RT", "st1": "Darnell Wright (08/10/01)", "st2": "Jake Curhan (02/09/98)", "st3": "—", "st4": "—"}
        ],
        "Defense": [
            {"pos": "LDE", "st1": "Montez Sweat (09/04/96)", "st2": "Austin Booker (12/10/02)", "st3": "Daniel Hardy (12/15/98)", "st4": "—"},
            {"pos": "NT",  "st1": "Andrew Billings (03/06/95)", "st2": "Zacch Pickens (03/06/00)", "st3": "Byron Cowart (05/20/96)", "st4": "—"},
            {"pos": "DT",  "st1": "Gervon Dexter (10/05/01)", "st2": "Chris Williams (06/19/98)", "st3": "—", "st4": "—"},
            {"pos": "RDE", "st1": "DeMarcus Walker (09/30/94)", "st2": "Darrell Taylor (03/24/97)", "st3": "Dominique Robinson (05/02/00)", "st4": "—"},
            {"pos": "WLB", "st1": "T.J. Edwards (08/12/96)", "st2": "Jack Sanborn (07/29/00)", "st3": "Carl Jones Jr. (03/10/01)", "st4": "—"},
            {"pos": "MLB", "st1": "Tremaine Edmunds (05/02/98)", "st2": "Amen Ogbongbemiga (09/04/98)", "st3": "—", "st4": "—"},
            {"pos": "CB",  "st1": "Jaylon Johnson (04/19/99)", "st2": "Terell Smith (07/28/99)", "st3": "Jaylon Jones (05/14/98)", "st4": "—"},
            {"pos": "CB",  "st1": "Tyrique Stevenson (05/26/00)", "st2": "Ameer Speed (10/11/99)", "st3": "Reddy Steward (05/04/01)", "st4": "—"},
            {"pos": "NB",  "st1": "Kyler Gordon (12/17/99)", "st2": "Josh Blackwell (04/09/99)", "st3": "—", "st4": "—"},
            {"pos": "SS",  "st1": "Jaquan Brisker (04/20/99)", "st2": "Elijah Hicks (10/16/99)", "st3": "Jonathan Owens (07/22/95)", "st4": "—"},
            {"pos": "FS",  "st1": "Kevin Byard (08/17/93)", "st2": "Tarvarius Moore (08/16/96)", "st3": "—", "st4": "—"}
        ],
        "Specialists": [
            {"pos": "PK",  "st1": "Cairo Santos (11/12/91)", "st2": "—", "st3": "—", "st4": "—"},
            {"pos": "P",   "st1": "Tory Taylor (07/09/97)", "st2": "—", "st3": "—", "st4": "—"},
            {"pos": "LS",  "st1": "Scott Daly (02/07/94)", "st2": "—", "st3": "—", "st4": "—"},
            {"pos": "H",   "st1": "Tory Taylor (07/09/97)", "st2": "—", "st3": "—", "st4": "—"},
            {"pos": "PR",  "st1": "DeAndre Carter (04/10/93)", "st2": "Tyler Scott (10/12/01)", "st3": "Rome Odunze (06/03/02)", "st4": "—"},
            {"pos": "KR",  "st1": "DeAndre Carter (04/10/93)", "st2": "Tyler Scott (10/12/01)", "st3": "Velus Jones Jr. (05/11/97)", "st4": "—"}
        ],
        "Personnel": [
            {"title": "Head Coach", "name": "Matt Eberflus", "dob": "1970-05-17"},
            {"title": "General Manager", "name": "Ryan Poles", "dob": "1985-09-21"},
            {"title": "Principal Owner", "name": "Virginia Halas McCaskey", "dob": "1923-01-05"},
            {"title": "Chairman", "name": "George H. McCaskey", "dob": "1956-09-04"},
            {"title": "President & CEO", "name": "Kevin Warren", "dob": "1963-09-24"}
        ]
    },
    "Kansas City Chiefs": {
        "Offense": [
            {"pos": "QB", "st1": "Patrick Mahomes (09/17/95)", "st2": "Carson Wentz (12/30/92)", "st3": "Chris Oladokun (09/03/97)", "st4": "—"},
            {"pos": "RB", "st1": "Isiah Pacheco (03/02/99)", "st2": "Kareem Hunt (08/06/95)", "st3": "Samaje Perine (09/16/95)", "st4": "Clyde Edwards-Helaire (04/11/99)"},
            {"pos": "WR", "st1": "DeAndre Hopkins (06/06/92)", "st2": "Xavier Worthy (04/27/03)", "st3": "Justin Watson (04/04/96)", "st4": "Mecole Hardman (05/08/98)"},
            {"pos": "TE", "st1": "Travis Kelce (10/05/89)", "st2": "Noah Gray (04/30/99)", "st3": "Peyton Hendershot (04/23/99)", "st4": "Jared Wiley (11/02/00)"},
            {"pos": "LT", "st1": "Wanya Morris (10/10/00)", "st2": "Kingsley Suamataia (01/18/03)", "st3": "—", "st4": "—"},
            {"pos": "C",  "st1": "Creed Humphrey (06/28/99)", "st2": "Hunter Nourzad (11/26/00)", "st3": "—", "st4": "—"}
        ],
        "Defense": [
            {"pos": "LDE", "st1": "George Karlaftis (04/03/01)", "st2": "Felix Anudike-Uzomah (01/24/02)", "st3": "Malik Herring (11/09/97)", "st4": "—"},
            {"pos": "DT",  "st1": "Chris Jones (07/03/94)", "st2": "Tershawn Wharton (06/25/98)", "st3": "Mike Pennel (05/09/91)", "st4": "—"},
            {"pos": "MLB", "st1": "Nick Bolton (03/10/00)", "st2": "Drue Tranquill (08/15/95)", "st3": "Leo Chenal (10/26/00)", "st4": "—"},
            {"pos": "CB",  "st1": "Trent McDuffie (09/13/00)", "st2": "Joshua Williams (10/17/99)", "st3": "Nazeeh Johnson (07/17/98)", "st4": "—"},
            {"pos": "FS",  "st1": "Justin Reid (02/15/97)", "st2": "Chamarri Conner (07/11/00)", "st3": "Jaden Hicks (08/16/02)", "st4": "—"}
        ],
        "Specialists": [
            {"pos": "PK",  "st1": "Harrison Butker (07/14/95)", "st2": "—", "st3": "—", "st4": "—"},
            {"pos": "P",   "st1": "Matt Araiza (05/16/00)", "st2": "—", "st3": "—", "st4": "—"},
            {"pos": "LS",  "st1": "James Winchester (08/06/89)", "st2": "—", "st3": "—", "st4": "—"}
        ],
        "Personnel": [
            {"title": "Head Coach", "name": "Andy Reid", "dob": "1958-03-19"},
            {"title": "General Manager", "name": "Brett Veach", "dob": "1977-12-19"},
            {"title": "Chairman & CEO", "name": "Clark Hunt", "dob": "1965-02-19"}
        ]
    }
}

# Master list of individual active players for Position Index
FLAT_ACTIVE_PLAYERS = [
    {"name": "Caleb Williams", "team": "Chicago Bears", "pos": "QB", "string": "1st String", "dob": "2001-11-18"},
    {"name": "Tyson Bagent", "team": "Chicago Bears", "pos": "QB", "string": "2nd String", "dob": "2000-06-08"},
    {"name": "Patrick Mahomes", "team": "Kansas City Chiefs", "pos": "QB", "string": "1st String", "dob": "1995-09-17"},
    {"name": "Carson Wentz", "team": "Kansas City Chiefs", "pos": "QB", "string": "2nd String", "dob": "1992-12-30"},
    {"name": "Josh Allen", "team": "Buffalo Bills", "pos": "QB", "string": "1st String", "dob": "1996-05-21"},
    {"name": "Lamar Jackson", "team": "Baltimore Ravens", "pos": "QB", "string": "1st String", "dob": "1997-01-07"},
    {"name": "C.J. Stroud", "team": "Houston Texans", "pos": "QB", "string": "1st String", "dob": "2001-10-03"},
    {"name": "Jayden Daniels", "team": "Washington Commanders", "pos": "QB", "string": "1st String", "dob": "2000-12-18"},
    {"name": "D'Andre Swift", "team": "Chicago Bears", "pos": "RB", "string": "1st String", "dob": "1999-01-14"},
    {"name": "Roschon Johnson", "team": "Chicago Bears", "pos": "RB", "string": "2nd String", "dob": "2001-01-31"},
    {"name": "Isiah Pacheco", "team": "Kansas City Chiefs", "pos": "RB", "string": "1st String", "dob": "1999-03-02"},
    {"name": "Derrick Henry", "team": "Baltimore Ravens", "pos": "RB", "string": "1st String", "dob": "1994-01-04"},
    {"name": "James Cook", "team": "Buffalo Bills", "pos": "RB", "string": "1st String", "dob": "1999-09-25"},
    {"name": "Joe Mixon", "team": "Houston Texans", "pos": "RB", "string": "1st String", "dob": "1996-07-24"},
    {"name": "Rome Odunze", "team": "Chicago Bears", "pos": "WR", "string": "1st String", "dob": "2002-06-03"},
    {"name": "DJ Moore", "team": "Chicago Bears", "pos": "WR", "string": "1st String", "dob": "1997-04-14"},
    {"name": "DeAndre Hopkins", "team": "Kansas City Chiefs", "pos": "WR", "string": "1st String", "dob": "1992-06-06"},
    {"name": "Zay Flowers", "team": "Baltimore Ravens", "pos": "WR", "string": "1st String", "dob": "2000-09-11"},
    {"name": "Terry McLaurin", "team": "Washington Commanders", "pos": "WR", "string": "1st String", "dob": "1995-09-15"},
    {"name": "Cole Kmet", "team": "Chicago Bears", "pos": "TE", "string": "1st String", "dob": "1999-03-10"},
    {"name": "Travis Kelce", "team": "Kansas City Chiefs", "pos": "TE", "string": "1st String", "dob": "1989-10-05"},
    {"name": "Mark Andrews", "team": "Baltimore Ravens", "pos": "TE", "string": "1st String", "dob": "1995-09-06"},
    {"name": "Montez Sweat", "team": "Chicago Bears", "pos": "DE", "string": "1st String", "dob": "1996-09-04"},
    {"name": "Chris Jones", "team": "Kansas City Chiefs", "pos": "DT", "string": "1st String", "dob": "1994-07-03"},
    {"name": "T.J. Edwards", "team": "Chicago Bears", "pos": "LB", "string": "1st String", "dob": "1996-08-12"},
    {"name": "Tremaine Edmunds", "team": "Chicago Bears", "pos": "LB", "string": "1st String", "dob": "1998-05-02"},
    {"name": "Roquan Smith", "team": "Baltimore Ravens", "pos": "LB", "string": "1st String", "dob": "1997-04-08"},
    {"name": "Jaylon Johnson", "team": "Chicago Bears", "pos": "CB", "string": "1st String", "dob": "1999-04-19"},
    {"name": "Kyler Gordon", "team": "Chicago Bears", "pos": "CB", "string": "1st String", "dob": "1999-12-17"},
    {"name": "Kevin Byard", "team": "Chicago Bears", "pos": "S", "string": "1st String", "dob": "1993-08-17"},
    {"name": "Cairo Santos", "team": "Chicago Bears", "pos": "PK", "string": "1st String", "dob": "1991-11-12"},
    {"name": "Tory Taylor", "team": "Chicago Bears", "pos": "P", "string": "1st String", "dob": "1997-07-09"}
]

NON_ACTIVE_PERSONNEL = [
    {"name": "Walter Payton", "team": "Chicago Bears", "role": "Hall of Fame RB (#34)", "dob": "1954-07-25", "era": "1975–1987"},
    {"name": "Mike Ditka", "team": "Chicago Bears", "role": "Hall of Fame TE / HC", "dob": "1939-10-18", "era": "1961–1992"},
    {"name": "George Halas", "team": "Chicago Bears", "role": "Franchise Founder / HC", "dob": "1895-02-02", "era": "1920–1983"},
    {"name": "Dick Butkus", "team": "Chicago Bears", "role": "Hall of Fame MLB (#51)", "dob": "1942-12-09", "era": "1965–1973"},
    {"name": "Jim McMahon", "team": "Chicago Bears", "role": "Super Bowl XX Champion QB", "dob": "1959-08-21", "era": "1982–1996"},
    {"name": "Matt Eberflus", "team": "Chicago Bears", "role": "Former Head Coach", "dob": "1970-05-17", "era": "2022–2024"},
    {"name": "Tom Brady", "team": "New England Patriots", "role": "7x Super Bowl Champion QB", "dob": "1977-08-03", "era": "2000–2022"},
    {"name": "Peyton Manning", "team": "Indianapolis Colts", "role": "Hall of Fame QB", "dob": "1976-03-24", "era": "1998–2015"},
    {"name": "Bill Belichick", "team": "New England Patriots", "role": "6x Super Bowl Champion HC", "dob": "1952-04-16", "era": "1975–2023"},
    {"name": "Vince Lombardi", "team": "Green Bay Packers", "role": "Hall of Fame HC", "dob": "1913-06-11", "era": "1959–1969"}
]

# ==============================================================================
# TOP-LEFT HORIZONTAL NAVIGATION BAR
# ==============================================================================
bar_col1, bar_col2 = st.columns([2.5, 3.5])

with bar_col1:
    main_status = st.radio(
        "NFL Status",
        options=["ACTIVE", "NON-ACTIVE / RETIRED"],
        horizontal=True,
        label_visibility="collapsed"
    )

with bar_col2:
    st.caption("OURLADS OFFICIAL DEPTH CHART & METAPHYSICAL PERSONNEL ENGINE")

st.markdown("---")

# ==============================================================================
# VIEW 1: ACTIVE (OURLADS MULTI-COLUMN SPREADSHEET FORMAT)
# ==============================================================================
if main_status == "ACTIVE":
    sub_col1, sub_col2 = st.columns([1.5, 4])
    with sub_col1:
        view_type = st.radio(
            "View Mode",
            options=["By Team Depth Chart", "By Position (All Players)"],
            horizontal=True,
            label_visibility="collapsed"
        )
    
    if view_type == "By Team Depth Chart":
        avail_teams = list(OURLADS_ROSTERS.keys())
        selected_team = st.selectbox("Select Team:", avail_teams, index=0)
        team_data = OURLADS_ROSTERS[selected_team]
        
        # OFFENSE
        st.markdown('<div class="ourlads-header">OFFENSE</div>', unsafe_allow_html=True)
        off_html = ['<table class="dense-table"><thead><tr><th>POS</th><th>1ST STRING</th><th>2ND STRING</th><th>3RD STRING</th><th>4TH STRING</th></tr></thead><tbody>']
        for r in team_data["Offense"]:
            off_html.append(f'<tr><td class="pos-cell">{r["pos"]}</td><td>{r["st1"]}</td><td>{r["st2"]}</td><td>{r["st3"]}</td><td>{r["st4"]}</td></tr>')
        off_html.append('</tbody></table>')
        st.markdown("".join(off_html), unsafe_allow_html=True)
        
        # DEFENSE
        st.markdown('<div class="ourlads-header">DEFENSE</div>', unsafe_allow_html=True)
        def_html = ['<table class="dense-table"><thead><tr><th>POS</th><th>1ST STRING</th><th>2ND STRING</th><th>3RD STRING</th><th>4TH STRING</th></tr></thead><tbody>']
        for r in team_data["Defense"]:
            def_html.append(f'<tr><td class="pos-cell">{r["pos"]}</td><td>{r["st1"]}</td><td>{r["st2"]}</td><td>{r["st3"]}</td><td>{r["st4"]}</td></tr>')
        def_html.append('</tbody></table>')
        st.markdown("".join(def_html), unsafe_allow_html=True)
        
        # SPECIALISTS
        st.markdown('<div class="ourlads-header">SPECIAL TEAMS</div>', unsafe_allow_html=True)
        sp_html = ['<table class="dense-table"><thead><tr><th>POS</th><th>1ST STRING</th><th>2ND STRING</th><th>3RD STRING</th><th>4TH STRING</th></tr></thead><tbody>']
        for r in team_data["Specialists"]:
            sp_html.append(f'<tr><td class="pos-cell">{r["pos"]}</td><td>{r["st1"]}</td><td>{r["st2"]}</td><td>{r["st3"]}</td><td>{r["st4"]}</td></tr>')
        sp_html.append('</tbody></table>')
        st.markdown("".join(sp_html), unsafe_allow_html=True)
        
        # COACHES & EXECUTIVES
        st.markdown('<div class="ourlads-header">COACHES & ASSOCIATED PERSONNEL</div>', unsafe_allow_html=True)
        staff_html = ['<table class="dense-table"><thead><tr><th>ASSIGNMENT / TITLE</th><th>NAME</th><th>DATE OF BIRTH</th></tr></thead><tbody>']
        for s in team_data["Personnel"]:
            staff_html.append(f'<tr><td class="pos-cell" style="width:200px;">{s["title"]}</td><td>{s["name"]}</td><td>{s["dob"]}</td></tr>')
        staff_html.append('</tbody></table>')
        st.markdown("".join(staff_html), unsafe_allow_html=True)
        
    else:
        # BY POSITION SPREADSHEET
        pos_list = sorted(list(set(p["pos"] for p in FLAT_ACTIVE_PLAYERS)))
        sel_pos = st.selectbox("Select Position:", pos_list, index=0)
        
        filtered_players = [p for p in FLAT_ACTIVE_PLAYERS if p["pos"] == sel_pos]
        st.markdown(f'<div class="ourlads-header">ACTIVE {sel_pos} POSITION INDEX</div>', unsafe_allow_html=True)
        
        pos_html = ['<table class="dense-table"><thead><tr><th>PLAYER NAME</th><th>NFL TEAM</th><th>POSITION</th><th>DEPTH STATUS</th><th>DATE OF BIRTH</th></tr></thead><tbody>']
        for p in filtered_players:
            pos_html.append(f'<tr><td>{p["name"]}</td><td>{p["team"]}</td><td class="pos-cell">{p["pos"]}</td><td>{p["string"]}</td><td>{p["dob"]}</td></tr>')
        pos_html.append('</tbody></table>')
        st.markdown("".join(pos_html), unsafe_allow_html=True)

# ==============================================================================
# VIEW 2: NON-ACTIVE / RETIRED
# ==============================================================================
else:
    st.markdown('<div class="ourlads-header">HISTORICAL NFL LEGENDS & ASSOCIATED PERSONNEL</div>', unsafe_allow_html=True)
    
    ret_html = ['<table class="dense-table"><thead><tr><th>NAME</th><th>PRIMARY FRANCHISE</th><th>HISTORICAL ROLE / POSITION</th><th>ERA</th><th>DATE OF BIRTH</th></tr></thead><tbody>']
    for n in NON_ACTIVE_PERSONNEL:
        ret_html.append(f'<tr><td>{n["name"]}</td><td>{n["team"]}</td><td>{n["role"]}</td><td>{n["era"]}</td><td>{n["dob"]}</td></tr>')
    ret_html.append('</tbody></table>')
    st.markdown("".join(ret_html), unsafe_allow_html=True)