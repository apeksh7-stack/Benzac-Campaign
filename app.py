import streamlit as st
import pandas as pd
import html

st.set_page_config(
    page_title="BENZAC | 24-Month Promotion Engine",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# DATA
# -----------------------------------------------------------------------------
CAMPAIGN_DATA = [
    {
        "id": "C1",
        "name": "First Pimple? Let's Talk.",
        "short": "FIRST PIMPLE",
        "icon": "✦",
        "ruler_phase": "TALK + TRY",
        "badge_class": "talk",
        "audience": "Teens & Gen-Z",
        "months": "M1 – M24",
        "start_m": 1,
        "end_m": 24,
        "goal": "Destigmatize acne conversations and turn first-pimple discovery into real trial.",
        "metrics": ["10M+ views", "150k trial packs", "25% engagement lift"],
        "accent": "#19A9D8",
        "evolution": {
            "TALK + TRY": ["Myth Busters", "30-Day Skin Series", "10-Min Relief"],
            "TRUST": ["Before & After Science", "Real Progress Logs", "Derm Tips"],
            "PREFERENCE": ["Campus Ambassador Reels", "Unfiltered Real Skin", "UGC Wall"],
            "HABIT": ["Routine Streak Reels", "Product Reorder Nudges", "Daily Cleanse"],
        },
        "activations": [
            {"phase": "TALK + TRY", "channel": "Instagram Reels / YouTube Shorts", "subtheme": "Myth Busters & 30-Day Series", "voices": "Taneesho, Agasthya Shah", "format": "Fast-paced myth breakdowns & unfiltered logs"},
            {"phase": "TRUST", "channel": "YouTube Shorts", "subtheme": "Real Progress Logs", "voices": "Tarini Shah & Student Ambassadors", "format": "30-day journey logs & honest check-ins"},
            {"phase": "PREFERENCE", "channel": "Instagram Reels", "subtheme": "Campus Ambassador Reels", "voices": "50+ Campus Ambassadors", "format": "Real skin wall submissions & student routines"},
            {"phase": "HABIT", "channel": "WhatsApp / Benzac App", "subtheme": "Routine Streak Reels", "voices": "Benzac Skin Coach", "format": "Gamified streak updates & auto-replenish prompts"},
        ],
    },
    {
        "id": "C2",
        "name": "Benzac Derm Board & Science Hub",
        "short": "DERM BOARD",
        "icon": "✚",
        "ruler_phase": "TRUST",
        "badge_class": "trust",
        "audience": "HCPs & Dermatologists",
        "months": "M4 – M24",
        "start_m": 4,
        "end_m": 24,
        "goal": "Establish medical credibility, doctor advocacy, and clinical confidence.",
        "metrics": ["500+ derm partners", "+35% trust lift", "80k clinic kits"],
        "accent": "#7651C8",
        "evolution": {
            "TALK + TRY": ["Rx Guidelines", "OTC Safety Factsheets"],
            "TRUST": ["Clinical Evidence Brief", "Patient Consultation Aids", "BP Deep-Dive"],
            "PREFERENCE": ["Derm Endorsed UGC", "Expert Reaction Shorts"],
            "HABIT": ["Long-Term Maintenance Plans", "Refill Protocols"],
        },
        "activations": [
            {"phase": "TALK + TRY", "channel": "Medical Portals", "subtheme": "OTC Safety Factsheets", "voices": "Galderma Medical Team", "format": "Digital clinical summaries"},
            {"phase": "TRUST", "channel": "Roundtables & CME Seminars", "subtheme": "Clinical Evidence Brief", "voices": "Dr. Rashmi Shetty, Dr. Aanchal Panth", "format": "Peer-to-peer trial breakdowns & clinic kits"},
            {"phase": "PREFERENCE", "channel": "Instagram / YouTube", "subtheme": "Derm Endorsed UGC", "voices": "Dr. Manasi Shirolikar", "format": "Expert commentary on viral acne trends"},
            {"phase": "HABIT", "channel": "Clinic POS & Rx Cards", "subtheme": "Long-Term Maintenance Plans", "voices": "Clinic Partners", "format": "Patient routine cards & repeat prescription slips"},
        ],
    },
    {
        "id": "C3",
        "name": "Clear Skin, Confident Parenting",
        "short": "PARENT CONFIDENCE",
        "icon": "◒",
        "ruler_phase": "TRUST",
        "badge_class": "trust",
        "audience": "Parents of Teens",
        "months": "M3 – M18",
        "start_m": 3,
        "end_m": 18,
        "goal": "Educate parents on safe acne care, removing household pushback and enabling trial.",
        "metrics": ["2.5M parent reach", "40k household packs", "30% repeat purchase"],
        "accent": "#7651C8",
        "evolution": {
            "TALK + TRY": ["Teen Acne vs Hygiene Myths", "First-Treatment Guides"],
            "TRUST": ["Pediatric & Derm Q&As", "Gentle Care Comparisons"],
            "PREFERENCE": ["Parent Community Reviews", "Family Skincare Bundles"],
            "HABIT": ["Monthly Subscription", "Back-to-School Stock-Up"],
        },
        "activations": [
            {"phase": "TALK + TRY", "channel": "Parent Blogs & Instagram", "subtheme": "Teen Acne vs Hygiene Myths", "voices": "Mom Micro-Influencers", "format": "Educational carousel posts & reassuring articles"},
            {"phase": "TRUST", "channel": "YouTube Long-form", "subtheme": "Pediatric & Derm Q&As", "voices": "Dermatologists & Doctors", "format": "Guided parent Q&A video series"},
            {"phase": "PREFERENCE", "channel": "WhatsApp Communities", "subtheme": "Parent Community Reviews", "voices": "Parent Ambassadors", "format": "Direct Q&A & trial pack links"},
            {"phase": "HABIT", "channel": "E-Commerce / CRM", "subtheme": "Monthly Subscription", "voices": "Benzac Care Team", "format": "Subscribe & save automated refills"},
        ],
    },
    {
        "id": "C4",
        "name": "Youth Spaces & Campus Pop-Ups",
        "short": "YOUTH SPACES",
        "icon": "◆",
        "ruler_phase": "PREFERENCE",
        "badge_class": "preference",
        "audience": "Teens & College Students",
        "months": "M6 – M18",
        "start_m": 6,
        "end_m": 18,
        "goal": "Drive experiential engagement through pop-up skin check stations and campus festivals.",
        "metrics": ["120 college activations", "85k sampling units", "40% QR scans"],
        "accent": "#F2A900",
        "evolution": {
            "TALK + TRY": ["School Derm Sessions", "Starter Kits Access"],
            "TRUST": ["Skin Check Stations", "Interactive Diagnostics"],
            "PREFERENCE": ["Real Skin Wall", "Anonymous Story Sharing"],
            "HABIT": ["Campus Routine League", "App Scan Rewards"],
        },
        "activations": [
            {"phase": "TALK + TRY", "channel": "School & College Events", "subtheme": "School Derm Sessions", "voices": "Youth Derm Panel", "format": "Derm-led myth vs fact Q&A"},
            {"phase": "TRUST", "channel": "Campus Pop-Up Booths", "subtheme": "Skin Check Stations", "voices": "Skin Experts & Student Reps", "format": "On-site skin check & sample distribution"},
            {"phase": "PREFERENCE", "channel": "Festival Real Skin Wall", "subtheme": "Real Skin Wall", "voices": "Students & Attendees", "format": "Sticky-note real stories turned into social UGC"},
            {"phase": "HABIT", "channel": "Benzac App", "subtheme": "Campus Routine League", "voices": "College Ambassadors", "format": "Inter-college routine streaks & rewards"},
        ],
    },
    {
        "id": "C5",
        "name": "3-Step Daily Routine Lock",
        "short": "ROUTINE LOCK",
        "icon": "↻",
        "ruler_phase": "HABIT",
        "badge_class": "habit",
        "audience": "Teens & Young Adults",
        "months": "M6 – M24",
        "start_m": 6,
        "end_m": 24,
        "goal": "Lock in the Wash–Treat–Moisturize 3-step routine for long-term retention.",
        "metrics": ["+42% repeat purchase", "120k active trackers", "4.8/5 app rating"],
        "accent": "#19A974",
        "evolution": {
            "TALK + TRY": ["Quick Routine Previews", "Trial Pack Teasers"],
            "TRUST": ["Skin Barrier Health Guides", "Derm Validations"],
            "PREFERENCE": ["AM/PM Routine Reviews", "Texture Demos"],
            "HABIT": ["ClearStreak 30 Challenge", "Auto-Replenish Rewards"],
        },
        "activations": [
            {"phase": "TALK + TRY", "channel": "Instagram Reels", "subtheme": "Quick Routine Previews", "voices": "SkinFluencers", "format": "15-second 3-step routine breakdowns"},
            {"phase": "TRUST", "channel": "YouTube Shorts", "subtheme": "Skin Barrier Health Guides", "voices": "Dermatologists", "format": "Acne treatment & skin barrier care"},
            {"phase": "PREFERENCE", "channel": "Instagram Stories / Reels", "subtheme": "AM/PM Routine Reviews", "voices": "College Brand Ambassadors", "format": "GRWM clips and texture demos"},
            {"phase": "HABIT", "channel": "Benzac App & WhatsApp", "subtheme": "ClearStreak 30 Challenge", "voices": "Benzac 30-Day Coach", "format": "Daily streak check-ins, reminders & discount unlocks"},
        ],
    },
]

PHASES = [
    ("TALK + TRY", 1, 6, "#1DA7D7", "#E8F7FC"),
    ("TRUST", 7, 12, "#7651C8", "#F0ECFB"),
    ("PREFERENCE", 13, 18, "#F2A900", "#FFF7E3"),
    ("HABIT", 19, 24, "#18A673", "#EAF8F1"),
]
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"] * 2
MONTH_LABELS = [f"{m}\n{'27' if i < 12 else '28'}" for i, m in enumerate(MONTHS)]


# -----------------------------------------------------------------------------
# PARALLEL SUB-THEME TIMING
# Campaign tracks run in parallel. Every sub-theme gets its own duration.
# Bar colour is determined by the campaign's strategic home, not by the month.
# -----------------------------------------------------------------------------
SUBTHEME_TIMING = {
    "First Pimple? Let's Talk.": {
        "Myth Busters": (1, 6), "30-Day Skin Series": (1, 8), "10-Min Relief": (2, 5),
        "Teen Review Shorts": (4, 24), "Real Progress Logs": (5, 16),
        "Derm Short-Form Videos": (7, 24), "Campus Ambassador Reels": (13, 24),
        "Unfiltered Real Skin": (13, 20), "UGC Wall": (14, 24),
        "Routine Streak Reels": (19, 24), "Product Reorder Nudges": (19, 24), "Daily Cleanse": (19, 24),
        "Before & After Science": (7, 14), "Derm Tips": (7, 18),
    },
    "Benzac Derm Board & Science Hub": {
        "Rx Guidelines": (4, 10), "OTC Safety Factsheets": (4, 10),
        "Clinical Evidence Brief": (7, 24), "Patient Consultation Aids": (7, 24), "BP Deep-Dive": (7, 16),
        "Derm Endorsed UGC": (13, 24), "Expert Reaction Shorts": (13, 24),
        "Long-Term Maintenance Plans": (19, 24), "Refill Protocols": (20, 24),
    },
    "Clear Skin, Confident Parenting": {
        "Teen Acne vs Hygiene Myths": (3, 8), "First-Treatment Guides": (3, 10),
        "Pediatric & Derm Q&As": (7, 18), "Gentle Care Comparisons": (7, 14),
        "Parent Community Reviews": (13, 24), "Family Skincare Bundles": (13, 24),
        "Monthly Subscription": (19, 24), "Back-to-School Stock-Up": (19, 24),
    },
    "Youth Spaces & Campus Pop-Ups": {
        "School Derm Sessions": (6, 12), "Starter Kits Access": (6, 12),
        "Skin Check Stations": (7, 18), "Interactive Diagnostics": (8, 18),
        "Real Skin Wall": (13, 20), "Anonymous Story Sharing": (13, 24),
        "Campus Ambassador Network": (13, 24), "Campus Routine League": (19, 24), "App Scan Rewards": (19, 24),
    },
    "3-Step Daily Routine Lock": {
        "Quick Routine Previews": (6, 12), "Trial Pack Teasers": (6, 10),
        "Skin Barrier Health Guides": (7, 18), "Derm Validations": (7, 20),
        "AM/PM Routine Reviews": (13, 24), "Texture Demos": (13, 20),
        "ClearStreak 30 Challenge": (19, 24), "Auto-Replenish Rewards": (19, 24),
    },
}

def get_subthemes(campaign):
    """Flatten campaign evolution into individually timed execution streams."""
    timing = SUBTHEME_TIMING.get(campaign["name"], {})
    seen = set()
    items = []
    for phase, themes in campaign["evolution"].items():
        for theme in themes:
            if theme in seen:
                continue
            seen.add(theme)
            start, end = timing.get(theme, (phase_meta(phase)[1], phase_meta(phase)[2]))
            items.append({"name": theme, "start": start, "end": end, "phase": phase})
    # Include deliberately persistent themes not present in the old evolution data.
    for theme, (start, end) in timing.items():
        if theme not in seen:
            items.append({"name": theme, "start": start, "end": end, "phase": campaign["ruler_phase"]})
    return sorted(items, key=lambda x: (x["start"], x["end"], x["name"]))

# -----------------------------------------------------------------------------
# CSS
# -----------------------------------------------------------------------------
CSS = r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
[data-testid="stAppViewContainer"] { background: #F5F7FB; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 1500px; padding: 1.25rem 2.25rem 3rem; }

/* HERO */
.hero {
    position: relative; overflow: hidden; min-height: 285px;
    background: linear-gradient(112deg, #071D36 0%, #102F55 46%, #1592C2 100%);
    border-radius: 26px; padding: 38px 46px; color: white; margin-bottom: 22px;
    box-shadow: 0 18px 40px rgba(10,31,55,.16);
}
.hero:after { content:""; position:absolute; width:420px; height:420px; border-radius:50%; right:-110px; top:-170px; border:55px solid rgba(255,255,255,.07); }
.hero:before { content:"24"; position:absolute; right:44px; bottom:-58px; font-size:260px; line-height:1; font-weight:800; color:rgba(255,255,255,.055); letter-spacing:-20px; }
.hero-kicker { position:relative; z-index:1; font-size:.74rem; letter-spacing:.2em; font-weight:800; color:#89D9F7; margin-bottom:22px; }
.hero h1 { position:relative; z-index:1; color:#fff!important; font-size:3rem; line-height:1.03; letter-spacing:-.05em; margin:0 0 16px; font-weight:800; max-width:900px; }
.hero p { position:relative; z-index:1; color:#D5E4F0!important; font-size:1.05rem; font-weight:500; max-width:830px; line-height:1.6; margin:0; }
.hero-stats { position:absolute; z-index:1; right:48px; bottom:36px; display:flex; gap:9px; }
.hero-stat { border:1px solid rgba(255,255,255,.18); background:rgba(255,255,255,.08); backdrop-filter: blur(6px); padding:10px 14px; border-radius:12px; text-align:center; min-width:86px; }
.hero-stat b { display:block; font-size:1rem; color:#fff; }.hero-stat span { font-size:.58rem; color:#BFD2E0; text-transform:uppercase; letter-spacing:.09em; }

/* TABS */
.stSegmentedControl [data-baseweb="button-group"] { gap:8px; background:transparent; }
.stSegmentedControl button { border-radius:12px!important; border:1px solid #DCE4EF!important; background:#fff!important; padding:.55rem 1.1rem!important; font-weight:700!important; }
.stSegmentedControl button[aria-checked="true"] { background:#0C2848!important; color:white!important; border-color:#0C2848!important; }

.section-title { font-size:2rem; font-weight:800; letter-spacing:-.035em; color:#13273F; margin:22px 0 4px; }
.section-sub { color:#708092; font-size:.93rem; margin-bottom:18px; }

/* OVERVIEW */
.journey { display:grid; grid-template-columns:repeat(4,1fr); gap:0; background:#fff; border:1px solid #E0E7F0; border-radius:22px; overflow:hidden; margin:18px 0 26px; }
.journey-step { min-height:132px; padding:18px 20px; position:relative; border-right:1px solid #E6EBF2; }
.journey-step:last-child{border-right:0}.journey-num{font-size:.65rem;font-weight:800;letter-spacing:.12em;color:#8593A3}.journey-name{font-size:1.05rem;font-weight:800;color:#162C47;margin-top:9px}.journey-desc{font-size:.75rem;color:#6A7786;line-height:1.45;margin-top:7px}.journey-accent{position:absolute;left:0;right:0;bottom:0;height:5px;}

.metric-strip { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:22px; }
.metric { background:#fff; border:1px solid #E0E7F0; border-radius:16px; padding:15px 17px; }.metric b{font-size:1.35rem;color:#122942;display:block}.metric span{font-size:.68rem;color:#788798;font-weight:700;text-transform:uppercase;letter-spacing:.08em}

.campaign-grid { display:grid; grid-template-columns:repeat(5,1fr); gap:14px; }
.campaign-card { min-height:330px; background:#fff; border:1px solid #E0E7F0; border-radius:22px; overflow:hidden; transition:.2s ease; position:relative; }
.campaign-card:hover { transform:translateY(-4px); box-shadow:0 14px 30px rgba(22,42,68,.1); }
.campaign-art { height:125px; position:relative; overflow:hidden; color:white; padding:18px; display:flex; flex-direction:column; justify-content:space-between; }
.campaign-art:after { content:""; position:absolute; width:145px;height:145px;border:20px solid rgba(255,255,255,.14);border-radius:50%;right:-35px;top:-42px; }
.campaign-icon { font-size:2rem; position:relative;z-index:1; }.campaign-art-label{font-size:.62rem;letter-spacing:.14em;font-weight:800;position:relative;z-index:1}
.campaign-body{padding:16px 17px 17px}.campaign-name{font-size:1rem;font-weight:800;line-height:1.22;color:#13273F;min-height:49px}.campaign-aud{font-size:.68rem;color:#718093;font-weight:700;margin:8px 0}.campaign-goal{font-size:.72rem;color:#64748B;line-height:1.55;min-height:65px}.mini-chip{display:inline-block;font-size:.61rem;font-weight:800;border-radius:999px;padding:5px 8px;margin:10px 3px 0 0}

/* CALENDAR */
.calendar-shell { background:#fff; border:1px solid #DDE5EF; border-radius:22px; padding:18px; box-shadow:0 10px 30px rgba(22,42,68,.05); overflow-x:auto; }
.calendar-board { min-width:1240px; }
.calendar-phase-head { display:grid; grid-template-columns:265px repeat(24, minmax(38px,1fr)); }
.phase-head-label { grid-column:1; background:#102943; color:#fff; border-radius:13px 0 0 0; padding:15px 17px; font-size:.75rem; font-weight:800; display:flex;align-items:center; }
.phase-head { padding:10px 5px 8px; text-align:center; font-weight:800; font-size:.72rem; color:white; border-left:1px solid rgba(255,255,255,.16); }
.phase-head small { display:block; font-size:.56rem; font-weight:700; opacity:.8; margin-top:4px; letter-spacing:.06em; }
.month-row { display:grid; grid-template-columns:265px repeat(24, minmax(38px,1fr)); }
.month-label { background:#F8FAFC; border-bottom:1px solid #E1E7EF; border-right:1px solid #EDF1F5; min-height:46px; display:flex; flex-direction:column; justify-content:center; align-items:center; font-size:.56rem; color:#738092; font-weight:800; letter-spacing:.04em; }
.month-label span { font-size:.52rem; color:#A0AAB6; margin-top:2px; }
.calendar-row { display:grid; grid-template-columns:265px 1fr; min-height:88px; }
.row-label { background:#fff; border-bottom:1px solid #E6EBF1; padding:13px 16px; display:flex; flex-direction:column; justify-content:center; gap:5px; }
.row-label b{font-size:.78rem;color:#172E48;line-height:1.25}.row-label span{font-size:.62rem;color:#748294;font-weight:700}.row-label em{font-style:normal;font-size:.56rem;font-weight:800;letter-spacing:.07em;text-transform:uppercase}
.row-track { display:grid; grid-template-columns:repeat(24, minmax(38px,1fr)); position:relative; min-height:88px; border-bottom:1px solid #E6EBF1; background-color:#fff; background-image:linear-gradient(to right,#EEF2F6 1px,transparent 1px); background-size:calc(100% / 24) 100%; }
.timeline-bar { align-self:center; margin:0 2px; height:42px; border-radius:9px; color:white; padding:7px 9px; display:flex; align-items:center; font-size:.61rem; font-weight:800; line-height:1.2; overflow:hidden; box-shadow:0 4px 8px rgba(15,23,42,.1); min-width:0; }
.bar-talk{background:#1DA7D7}.bar-trust{background:#7651C8}.bar-preference{background:#F2A900}.bar-habit{background:#18A673}
.legend { display:flex; flex-wrap:wrap; gap:10px; margin:15px 0 0; }.legend-item{display:flex;align-items:center;gap:6px;font-size:.68rem;color:#6B7786;font-weight:700}.legend-dot{width:10px;height:10px;border-radius:50%}

/* DETAILS */
.detail-hero { background:#fff; border:1px solid #E0E7F0; border-radius:24px; overflow:hidden; display:grid; grid-template-columns:1.35fr .65fr; margin:14px 0 20px; }
.detail-main { padding:28px 30px; }.detail-kicker{font-size:.64rem;letter-spacing:.13em;font-weight:800;margin-bottom:12px}.detail-main h2{font-size:2.2rem;letter-spacing:-.04em;color:#142A44;margin:0 0 12px}.detail-main p{font-size:.93rem;color:#607084;line-height:1.65;max-width:760px}.detail-art{position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;color:white}.detail-art .big-icon{font-size:7rem;position:relative;z-index:1}.detail-art:after{content:"";position:absolute;width:300px;height:300px;border:32px solid rgba(255,255,255,.14);border-radius:50%;right:-80px;top:-70px}.detail-art:before{content:"";position:absolute;width:220px;height:220px;border:25px solid rgba(255,255,255,.09);border-radius:50%;left:-90px;bottom:-95px}
.detail-stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:20px}.detail-stat{background:#F7F9FC;border:1px solid #E8EDF3;border-radius:14px;padding:12px}.detail-stat b{font-size:.9rem;color:#182F4A;display:block}.detail-stat span{font-size:.58rem;color:#8491A0;text-transform:uppercase;letter-spacing:.07em;font-weight:800}
.phase-detail-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:12px 0 24px}.phase-card{border-radius:18px;padding:16px;border:1px solid #E2E8F0;min-height:175px}.phase-card h4{font-size:.8rem;margin:0 0 10px;color:#17304C}.phase-card small{font-size:.6rem;font-weight:800;letter-spacing:.08em}.theme-pill{font-size:.66rem;padding:7px 8px;border-radius:8px;background:white;margin-top:6px;color:#435162;font-weight:700;border:1px solid rgba(0,0,0,.05)}
.exec-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.exec-card{background:#fff;border:1px solid #E1E7EF;border-radius:18px;padding:16px;min-height:210px}.exec-card .phase-mini{font-size:.58rem;font-weight:800;letter-spacing:.09em}.exec-card h4{font-size:.92rem;color:#172E48;margin:10px 0}.exec-line{font-size:.68rem;color:#6C7A8B;line-height:1.55;margin-top:7px}.exec-line b{color:#263B54}



/* PARALLEL SUB-THEME CALENDAR */
.campaign-group { display:grid; grid-template-columns:265px 1fr; border-bottom:1px solid #E1E7EF; background:#fff; }
.group-label { padding:18px 16px; border-right:1px solid #E6ECF2; display:flex; flex-direction:column; justify-content:flex-start; }
.group-label .group-name { font-size:.82rem; font-weight:800; color:#172E48; line-height:1.3; }
.group-label .group-aud { font-size:.62rem; color:#748294; font-weight:700; margin-top:6px; }
.group-label .group-meta { font-size:.56rem; font-weight:800; letter-spacing:.07em; margin-top:8px; text-transform:uppercase; }
.group-track { padding:7px 0; background-color:#fff; background-image:linear-gradient(to right,#EEF2F6 1px,transparent 1px); background-size:calc(100% / 24) 100%; }
.subtheme-row { display:grid; grid-template-columns:repeat(24,minmax(38px,1fr)); min-height:38px; align-items:center; }
.subtheme-bar { height:27px; margin:4px 2px; border-radius:8px; color:#fff; padding:0 8px; display:flex; align-items:center; font-size:.59rem; font-weight:800; line-height:1.1; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; box-shadow:0 3px 8px rgba(15,23,42,.12); min-width:0; }
.subtheme-bar:hover { filter:brightness(.94); }
.detail-theme-table { background:#fff; border:1px solid #E0E7F0; border-radius:18px; padding:14px; overflow-x:auto; }
.detail-theme-grid { min-width:1000px; }
.detail-theme-months,.detail-theme-row { display:grid; grid-template-columns:210px repeat(24,1fr); }
.detail-theme-month { min-height:38px; display:flex; align-items:center; justify-content:center; border-bottom:1px solid #E7EDF3; border-right:1px solid #EEF2F6; font-size:.54rem; color:#7A8796; font-weight:800; }
.detail-theme-name { display:flex; align-items:center; padding:0 10px; border-bottom:1px solid #E7EDF3; font-size:.66rem; font-weight:800; color:#31465D; }
.detail-subtheme-bar { height:27px; align-self:center; margin:5px 2px; border-radius:8px; color:#fff; padding:0 8px; display:flex; align-items:center; font-size:.57rem; font-weight:800; overflow:hidden; white-space:nowrap; text-overflow:ellipsis; }


/* SUB-THEME EXECUTION */
.subtheme-execution-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin:12px 0 6px}
.subtheme-execution-card{background:#fff;border:1px solid #E0E7F0;border-radius:18px;padding:17px 18px 16px;box-shadow:0 5px 16px rgba(15,23,42,.035)}
.subtheme-card-top{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:14px}
.subtheme-card-name{font-size:.92rem;font-weight:800;color:#172E48;line-height:1.25}
.subtheme-card-role{font-size:.72rem;color:#6B7A8C;line-height:1.45;margin-top:5px}
.subtheme-status{flex:0 0 auto;font-size:.58rem;font-weight:800;color:#526274;background:#F1F5F9;border:1px solid #E2E8F0;border-radius:999px;padding:5px 8px;white-space:nowrap}
.subtheme-meta{display:grid;grid-template-columns:1fr 1fr;gap:12px 16px;border-top:1px solid #EEF2F6;padding-top:12px}
.subtheme-meta-block:last-child{grid-column:1 / -1}
.subtheme-meta-label{font-size:.56rem;font-weight:800;letter-spacing:.09em;color:#94A3B8;margin-bottom:4px}
.subtheme-meta-value{font-size:.69rem;line-height:1.45;font-weight:600;color:#526274}

@media(max-width:1050px){.campaign-grid{grid-template-columns:repeat(2,1fr)}.detail-hero{grid-template-columns:1fr}.detail-art{min-height:160px}.phase-detail-grid,.exec-grid,.subtheme-execution-grid{grid-template-columns:repeat(2,1fr)}.hero h1{font-size:2.4rem}.hero-stats{display:none}}
</style>
'''
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def esc(v):
    return html.escape(str(v))


def phase_for_month(month):
    if month <= 6: return "TALK + TRY"
    if month <= 12: return "TRUST"
    if month <= 18: return "PREFERENCE"
    return "HABIT"


def phase_meta(phase):
    return next(x for x in PHASES if x[0] == phase)


def render_hero():
    st.markdown('''
    <div class="hero">
      <div class="hero-kicker">BENZAC BY GALDERMA • PROMOTION ARCHITECTURE</div>
      <h1>24-MONTH INTEGRATED<br>PROMOTION ENGINE</h1>
      <p>A connected growth system that moves teens, parents and dermatologists from first-pimple discovery to long-term skincare habit.</p>
      <div class="hero-stats">
        <div class="hero-stat"><b>24</b><span>Months</span></div>
        <div class="hero-stat"><b>5</b><span>Campaign tracks</span></div>
        <div class="hero-stat"><b>4</b><span>Lifecycle phases</span></div>
      </div>
    </div>
    ''', unsafe_allow_html=True)


def render_overview():
    st.markdown('<div class="section-title">The promotion journey, at a glance.</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">One integrated engine. Five campaign tracks running in parallel, with individual sub-themes entering and extending at different moments.</div>', unsafe_allow_html=True)

    journey = ''
    for i, (name, start, end, color, pale) in enumerate(PHASES, start=1):
        desc = {
            "TALK + TRY": "Make first-pimple conversations visible and lower the barrier to trial.",
            "TRUST": "Add science, expert reassurance and credible education.",
            "PREFERENCE": "Turn authentic experiences into social proof and brand pull.",
            "HABIT": "Reinforce routines, retention and repeat behaviour.",
        }[name]
        journey += f'''<div class="journey-step"><div class="journey-num">PHASE {i} • M{start}–M{end}</div><div class="journey-name">{name}</div><div class="journey-desc">{desc}</div><div class="journey-accent" style="background:{color}"></div></div>'''
    st.markdown(f'<div class="journey">{journey}</div>', unsafe_allow_html=True)

    st.markdown('''<div class="metric-strip">
      <div class="metric"><b>3</b><span>Priority audiences</span></div>
      <div class="metric"><b>5</b><span>Connected tracks</span></div>
      <div class="metric"><b>20+</b><span>Activation formats</span></div>
      <div class="metric"><b>24</b><span>Months mapped</span></div>
    </div>''', unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size:1.45rem">Campaign portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Each track has its own audience, strategic job and independently timed sub-themes.</div>', unsafe_allow_html=True)

    cards = ''
    for c in CAMPAIGN_DATA:
        phase_color = phase_meta(c["ruler_phase"])[3]
        chips = ''.join([f'<span class="mini-chip" style="background:{phase_meta(p)[4]};color:{phase_meta(p)[3]}">{p}</span>' for p in c["evolution"].keys()])
        cards += f'''
        <div class="campaign-card">
          <div class="campaign-art" style="background:linear-gradient(135deg,{c['accent']} 0%,#0E2946 120%)">
            <div class="campaign-art-label">{esc(c['months'])}</div>
            <div class="campaign-icon">{c['icon']}</div>
          </div>
          <div class="campaign-body">
            <div class="campaign-name">{esc(c['name'])}</div>
            <div class="campaign-aud">◉ {esc(c['audience'])}</div>
            <div class="campaign-goal">{esc(c['goal'])}</div>
            <div>{chips}</div>
          </div>
        </div>'''
    st.markdown(f'<div class="campaign-grid">{cards}</div>', unsafe_allow_html=True)
    st.caption("Use **Campaign Details** to inspect channels, voices, formats and sub-themes for each track.")


def render_calendar():
    st.markdown('<div class="section-title">Integrated campaign calendar</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">X-axis = months • Y-axis = campaign tracks • every sub-theme has its own bar and duration. Campaigns run in parallel.</div>', unsafe_allow_html=True)

    board = ['<div class="calendar-shell"><div class="calendar-board">']
    board.append('<div class="calendar-phase-head"><div class="phase-head-label">CAMPAIGN TRACK &amp; AUDIENCE</div>')
    for phase, start_m, end_m, color, pale in PHASES:
        board.append(f'<div class="phase-head" style="grid-column:span 6;background:{color}">{phase}<small>M{start_m}–M{end_m}</small></div>')
    board.append('</div>')

    board.append('<div class="month-row"><div class="month-label" style="align-items:flex-start;padding-left:16px"><span style="font-size:.58rem;color:#7B8794">MONTH</span></div>')
    for label in MONTH_LABELS:
        mon, yr = label.split("\n")
        board.append(f'<div class="month-label">{mon}<span>{yr}</span></div>')
    board.append('</div>')

    for c in CAMPAIGN_DATA:
        color = phase_meta(c["ruler_phase"])[3]
        cls = {"TALK + TRY":"talk", "TRUST":"trust", "PREFERENCE":"preference", "HABIT":"habit"}[c["ruler_phase"]]
        themes = get_subthemes(c)
        board.append('<div class="campaign-group">')
        board.append(f'''<div class="group-label">
            <div class="group-name">{esc(c["name"])}</div>
            <div class="group-aud">◉ {esc(c["audience"])}</div>
            <div class="group-meta" style="color:{color}">{esc(c["months"])} • {len(themes)} SUB-THEMES</div>
        </div>''')
        board.append('<div class="group-track">')
        for theme in themes:
            span = theme["end"] - theme["start"] + 1
            board.append('<div class="subtheme-row">')
            board.append(f'<div class="subtheme-bar bar-{cls}" style="grid-column:{theme["start"]} / span {span}" title="{esc(theme["name"])} • M{theme["start"]}–M{theme["end"]}">{esc(theme["name"])}</div>')
            board.append('</div>')
        board.append('</div></div>')

    board.append('</div>')
    board.append('''<div class="legend">
      <div class="legend-item"><span class="legend-dot" style="background:#1DA7D7"></span>Discovery &amp; trial campaign</div>
      <div class="legend-item"><span class="legend-dot" style="background:#7651C8"></span>Trust-building campaigns</div>
      <div class="legend-item"><span class="legend-dot" style="background:#F2A900"></span>Preference campaign</div>
      <div class="legend-item"><span class="legend-dot" style="background:#18A673"></span>Habit campaign</div>
    </div></div>''')
    st.markdown(''.join(board).lstrip(), unsafe_allow_html=True)
    st.caption("Phase headers show the strategic journey. Bar colour shows the strategic home of the campaign—so a blue or purple sub-theme can continue into later phases.")

    st.markdown('<div class="section-title" style="font-size:1.35rem">Campaign lens</div>', unsafe_allow_html=True)
    selected = st.selectbox("Inspect a campaign", [c["name"] for c in CAMPAIGN_DATA], label_visibility="collapsed")
    c = next(x for x in CAMPAIGN_DATA if x["name"] == selected)
    rows = [{"Sub-theme": t["name"], "Duration": f'M{t["start"]}–M{t["end"]}'} for t in get_subthemes(c)]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def human_timing_label(theme):
    """Exact timing belongs in the timeline; details use a concise strategic label."""
    duration = theme["end"] - theme["start"] + 1
    if theme["end"] == 24:
        return "Always-on"
    if duration >= 12:
        return "Sustained stream"
    if theme["start"] <= 6:
        return "Launch focus"
    return "Core stream"


def theme_execution(campaign, theme):
    """Return concise execution metadata for each sub-theme."""
    name = theme["name"]

    activation = next((a for a in campaign["activations"] if a["subtheme"] == name), None)

    if activation is None:
        activation = next(
            (a for a in campaign["activations"]
             if name in a["subtheme"] or a["subtheme"] in name),
            None
        )

    if activation is None:
        activation = next(
            (a for a in campaign["activations"] if a["phase"] == theme["phase"]),
            None
        )

    if activation:
        return {
            "role": f"{theme['phase'].title()} execution stream",
            "platforms": activation["channel"],
            "partners": activation["voices"],
            "content": activation["format"],
        }

    return {
        "role": f"{theme['phase'].title()} execution stream",
        "platforms": "Integrated campaign channels",
        "partners": "Relevant campaign partners",
        "content": "Content adapted to campaign objective",
    }

def render_details():
    st.markdown('<div class="section-title">Campaign detail explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Each campaign stays active as a strategic track; the detail view shows exactly which sub-themes run when and what each one contains.</div>', unsafe_allow_html=True)

    selected = st.selectbox("Campaign track", [c["name"] for c in CAMPAIGN_DATA], label_visibility="collapsed")
    c = next(x for x in CAMPAIGN_DATA if x["name"] == selected)
    color = phase_meta(c["ruler_phase"])[3]
    cls = {"TALK + TRY":"talk", "TRUST":"trust", "PREFERENCE":"preference", "HABIT":"habit"}[c["ruler_phase"]]
    themes = get_subthemes(c)

    stats = ''.join([f'<div class="detail-stat"><b>{esc(m)}</b><span>Target metric</span></div>' for m in c["metrics"]])
    st.markdown(f'''
    <div class="detail-hero">
      <div class="detail-main">
        <div class="detail-kicker" style="color:{color}">{c["ruler_phase"]} • {c["months"]} • {esc(c["audience"])}</div>
        <h2>{esc(c["name"])}</h2>
        <p>{esc(c["goal"])}</p>
        <div class="detail-stat-grid">{stats}</div>
      </div>
      <div class="detail-art" style="background:linear-gradient(135deg,{color},#0D2947)"><div class="big-icon">{c["icon"]}</div></div>
    </div>''', unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size:1.35rem">Sub-theme timeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">The campaign remains active; each bar below shows the independent duration of one execution stream.</div>', unsafe_allow_html=True)
    timeline = ['<div class="detail-theme-table"><div class="detail-theme-grid"><div class="detail-theme-months"><div class="detail-theme-month"></div>']
    for label in MONTH_LABELS:
        mon, yr = label.split("\n")
        timeline.append(f'<div class="detail-theme-month">{mon}<br>{yr}</div>')
    timeline.append('</div>')
    for theme in themes:
        span = theme["end"] - theme["start"] + 1
        timeline.append('<div class="detail-theme-row">')
        timeline.append(f'<div class="detail-theme-name">{esc(theme["name"])}</div>')
        timeline.append(f'<div class="detail-subtheme-bar bar-{cls}" style="grid-column:{theme["start"] + 1} / span {span}">M{theme["start"]}–M{theme["end"]} • {esc(theme["name"])}</div>')
        timeline.append('</div>')
    timeline.append('</div></div>')
    st.markdown(''.join(timeline).lstrip(), unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size:1.35rem">Sub-theme execution</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">A quick view of where each stream shows up, who helps deliver it and what content it creates. Exact timing stays in the timeline above.</div>',
        unsafe_allow_html=True
    )

    cards = ['<div class="subtheme-execution-grid">']
    for theme in themes:
        meta = theme_execution(c, theme)
        cards.append(
            f'<div class="subtheme-execution-card" style="border-left:4px solid {color}">'
            f'<div class="subtheme-card-top">'
            f'<div>'
            f'<div class="subtheme-card-name">{esc(theme["name"])}</div>'
            f'<div class="subtheme-card-role">{esc(meta["role"])}</div>'
            f'</div>'
            f'<div class="subtheme-status">{esc(human_timing_label(theme))}</div>'
            f'</div>'
            f'<div class="subtheme-meta">'
            f'<div class="subtheme-meta-block">'
            f'<div class="subtheme-meta-label">PLATFORM</div>'
            f'<div class="subtheme-meta-value">{esc(meta["platforms"])}</div>'
            f'</div>'
            f'<div class="subtheme-meta-block">'
            f'<div class="subtheme-meta-label">PARTNERS / VOICES</div>'
            f'<div class="subtheme-meta-value">{esc(meta["partners"])}</div>'
            f'</div>'
            f'<div class="subtheme-meta-block">'
            f'<div class="subtheme-meta-label">CONTENT</div>'
            f'<div class="subtheme-meta-value">{esc(meta["content"])}</div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
    cards.append('</div>')
    st.markdown(''.join(cards).lstrip(), unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# APP
# -----------------------------------------------------------------------------
render_hero()

selected_tab = st.segmented_control(
    "Navigation",
    options=["✦ Overview", "▦ Campaign Calendar", "⌕ Campaign Details"],
    default="✦ Overview",
    label_visibility="collapsed",
)

if selected_tab == "✦ Overview":
    render_overview()
elif selected_tab == "▦ Campaign Calendar":
    render_calendar()
else:
    render_details()
