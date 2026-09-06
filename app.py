import base64
import html

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="BENZAC | 24-Month Promotion Engine",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =============================================================================
# BRAND SYSTEM  —  Benzac by Galderma
# Blue-led, clinical-but-warm. One family, four steps of depth.
# =============================================================================
INK = "#0A1E3C"
NAVY = "#0B2A8C"
BLUE = "#1E63D8"
SKY = "#35AEE6"
VIOLET = "#6B4FE0"
MIST = "#F4F8FD"
LINE = "#DCE7F5"
MUTED = "#64748B"

PHASES = [
    ("TALK + TRY", 1, 6, SKY, "#E6F6FD", "Make the first-pimple moment visible and lower the barrier to trial."),
    ("TRUST", 7, 12, BLUE, "#E8F0FE", "Add science, expert reassurance and credible education."),
    ("PREFERENCE", 13, 18, VIOLET, "#EFEBFD", "Turn authentic experiences into social proof and brand pull."),
    ("HABIT", 19, 24, NAVY, "#E7EBF7", "Reinforce routine, retention and repeat behaviour."),
]
PHASE_CLASS = {"TALK + TRY": "talk", "TRUST": "trust", "PREFERENCE": "pref", "HABIT": "habit"}

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"] * 2
MONTH_LABELS = [(m, "Y1" if i < 12 else "Y2") for i, m in enumerate(MONTHS)]

# Indian calendar moments the plan is timed against (from listening + category behaviour)
SEASON_MARKERS = [
    (3, 6, "Post-board reset · Mar–Jun"),
    (9, 11, "Wedding & festival season · Sep–Nov"),
    (15, 18, "Post-board reset · Y2"),
    (21, 23, "Festival season · Y2"),
]


# =============================================================================
# INLINE SVG ART  (no external image calls — renders anywhere)
# =============================================================================
def svg(markup: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(markup.encode()).decode()


def _wrap(inner, w=520, h=260):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
        f"{inner}</svg>"
    )


ART_TEEN = svg(_wrap('''
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#35AEE6"/><stop offset="1" stop-color="#0B2A8C"/></linearGradient></defs>
<rect width="520" height="260" fill="url(#g)"/>
<circle cx="440" cy="40" r="96" fill="none" stroke="#fff" stroke-opacity=".13" stroke-width="26"/>
<circle cx="70" cy="235" r="66" fill="none" stroke="#fff" stroke-opacity=".10" stroke-width="20"/>
<rect x="196" y="42" width="128" height="200" rx="20" fill="#fff" fill-opacity=".95"/>
<rect x="206" y="52" width="108" height="150" rx="12" fill="#0B2A8C" fill-opacity=".14"/>
<circle cx="260" cy="112" r="30" fill="#0B2A8C" fill-opacity=".28"/>
<rect x="222" y="160" width="76" height="7" rx="3.5" fill="#0B2A8C" fill-opacity=".35"/>
<rect x="222" y="175" width="52" height="7" rx="3.5" fill="#0B2A8C" fill-opacity=".22"/>
<circle cx="260" cy="222" r="10" fill="#35AEE6"/>
'''))

ART_DERM = svg(_wrap('''
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#1E63D8"/><stop offset="1" stop-color="#081C48"/></linearGradient></defs>
<rect width="520" height="260" fill="url(#g)"/>
<circle cx="450" cy="210" r="94" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="24"/>
<rect x="176" y="40" width="168" height="180" rx="14" fill="#fff" fill-opacity=".95"/>
<rect x="196" y="66" width="128" height="9" rx="4.5" fill="#1E63D8" fill-opacity=".55"/>
<rect x="196" y="88" width="104" height="7" rx="3.5" fill="#0B2A8C" fill-opacity=".22"/>
<rect x="196" y="104" width="118" height="7" rx="3.5" fill="#0B2A8C" fill-opacity=".22"/>
<rect x="196" y="120" width="88" height="7" rx="3.5" fill="#0B2A8C" fill-opacity=".22"/>
<rect x="238" y="150" width="44" height="14" rx="7" fill="#1E63D8"/>
<rect x="252" y="136" width="16" height="42" rx="8" fill="#1E63D8"/>
<rect x="196" y="192" width="128" height="7" rx="3.5" fill="#0B2A8C" fill-opacity=".16"/>
'''))

ART_PARENT = svg(_wrap('''
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#6B4FE0"/><stop offset="1" stop-color="#12225E"/></linearGradient></defs>
<rect width="520" height="260" fill="url(#g)"/>
<circle cx="60" cy="40" r="82" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="22"/>
<circle cx="216" cy="122" r="46" fill="#fff" fill-opacity=".92"/>
<circle cx="216" cy="104" r="17" fill="#6B4FE0" fill-opacity=".45"/>
<path d="M188 148c4-18 14-27 28-27s24 9 28 27z" fill="#6B4FE0" fill-opacity=".45"/>
<circle cx="304" cy="140" r="36" fill="#fff" fill-opacity=".92"/>
<circle cx="304" cy="127" r="13" fill="#6B4FE0" fill-opacity=".45"/>
<path d="M283 161c3-14 11-21 21-21s18 7 21 21z" fill="#6B4FE0" fill-opacity=".45"/>
<path d="M368 92c9-11 27-4 27 10 0 13-19 24-27 30-8-6-27-17-27-30 0-14 18-21 27-10z" fill="#fff" fill-opacity=".55"/>
'''))

ART_CAMPUS = svg(_wrap('''
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#2E86E0"/><stop offset="1" stop-color="#0B2A8C"/></linearGradient></defs>
<rect width="520" height="260" fill="url(#g)"/>
<circle cx="452" cy="52" r="90" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width="24"/>
<path d="M140 96h240l-22-40H162z" fill="#fff" fill-opacity=".9"/>
<rect x="152" y="96" width="216" height="120" rx="10" fill="#fff" fill-opacity=".95"/>
<rect x="172" y="120" width="72" height="60" rx="8" fill="#0B2A8C" fill-opacity=".16"/>
<rect x="256" y="120" width="40" height="40" rx="6" fill="#35AEE6" fill-opacity=".65"/>
<rect x="304" y="120" width="40" height="40" rx="6" fill="#6B4FE0" fill-opacity=".55"/>
<rect x="256" y="168" width="40" height="40" rx="6" fill="#6B4FE0" fill-opacity=".4"/>
<rect x="304" y="168" width="40" height="40" rx="6" fill="#35AEE6" fill-opacity=".45"/>
<rect x="172" y="190" width="72" height="8" rx="4" fill="#0B2A8C" fill-opacity=".22"/>
'''))

ART_ROUTINE = svg(_wrap('''
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#0B2A8C"/><stop offset="1" stop-color="#1E63D8"/></linearGradient></defs>
<rect width="520" height="260" fill="url(#g)"/>
<circle cx="70" cy="220" r="80" fill="none" stroke="#fff" stroke-opacity=".11" stroke-width="22"/>
<rect x="168" y="96" width="46" height="112" rx="10" fill="#fff" fill-opacity=".95"/>
<rect x="176" y="80" width="30" height="20" rx="5" fill="#fff" fill-opacity=".7"/>
<rect x="226" y="80" width="52" height="128" rx="11" fill="#fff" fill-opacity=".95"/>
<rect x="236" y="62" width="32" height="22" rx="5" fill="#fff" fill-opacity=".7"/>
<rect x="290" y="104" width="44" height="104" rx="10" fill="#fff" fill-opacity=".95"/>
<rect x="298" y="88" width="28" height="20" rx="5" fill="#fff" fill-opacity=".7"/>
<circle cx="410" cy="130" r="52" fill="none" stroke="#fff" stroke-opacity=".28" stroke-width="14"/>
<path d="M410 78a52 52 0 0 1 43 81" fill="none" stroke="#35AEE6" stroke-width="14" stroke-linecap="round"/>
<rect x="176" y="150" width="30" height="6" rx="3" fill="#1E63D8" fill-opacity=".35"/>
<rect x="236" y="140" width="32" height="6" rx="3" fill="#1E63D8" fill-opacity=".35"/>
<rect x="298" y="156" width="28" height="6" rx="3" fill="#1E63D8" fill-opacity=".35"/>
'''))

ART_HERO = svg(_wrap('''
<defs><linearGradient id="b" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#ffffff" stop-opacity=".22"/><stop offset="1" stop-color="#ffffff" stop-opacity=".04"/></linearGradient></defs>
<circle cx="230" cy="130" r="118" fill="none" stroke="#fff" stroke-opacity=".16" stroke-width="30"/>
<rect x="176" y="66" width="60" height="150" rx="14" fill="url(#b)" stroke="#fff" stroke-opacity=".35"/>
<rect x="186" y="46" width="40" height="24" rx="6" fill="#fff" fill-opacity=".3"/>
<rect x="252" y="92" width="52" height="124" rx="12" fill="url(#b)" stroke="#fff" stroke-opacity=".3"/>
<rect x="260" y="74" width="36" height="20" rx="5" fill="#fff" fill-opacity=".25"/>
<circle cx="376" cy="150" r="46" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="12"/>
<path d="M376 104a46 46 0 0 1 36 74" fill="none" stroke="#8AD6F5" stroke-width="12" stroke-linecap="round"/>
''', 520, 280))

TAB_ART = {
    "overview": ART_HERO,
    "calendar": ART_CAMPUS,
    "details": ART_DERM,
}


# =============================================================================
# CONSUMER SIGNALS  (from the digital listening dataset — 36 insights)
# =============================================================================
SIGNALS = [
    ("“acnestar”", "Category search in India autocompletes to a rival benzoyl peroxide brand. Benzac has no default recall at the counter.", "Buy symptom + ingredient search. Build name recall at pharmacy."),
    ("“pimple kaise hataye”", "Acne is searched in Hinglish, not clinical English.", "Hinglish creative, Hinglish app copy, clinical English only for HCPs."),
    ("Day 1 – 7", "Redness and purge-or-react confusion in week one decides whether BPO is kept or dropped.", "Own onboarding. Tolerability guidance from first use, not month six."),
    ("“before it leaves scars”", "Scar fear, not the pimple, is what finally converts to treatment.", "Lead with early treatment as scar prevention."),
    ("Parent holds the wallet", "Teens post asking how to convince a parent to buy skincare; parents blame hygiene and diet.", "A parent-facing myth-bust and a derm-recommended claim on pack."),
    ("Proof = a timeline", "Highest-engagement content is a real person's multi-month journey. Paid endorsement reads as evidence against.", "Unretouched Day 0/14/30 stories from named real users."),
]

CHANNEL_MIX = {
    "First Pimple? Let's Talk.": [("Instagram", 30), ("YouTube", 26), ("Search", 16), ("Benzac App", 14), ("Reddit / communities", 8), ("Quick-commerce", 6)],
    "Benzac Derm Board & Science Hub": [("HCP portals / CME", 34), ("Clinic materials", 26), ("Webinars", 18), ("YouTube", 12), ("LinkedIn", 10)],
    "Clear Skin, Confident Parenting": [("YouTube", 26), ("Facebook", 22), ("Search", 20), ("WhatsApp", 16), ("Pharmacy", 16)],
    "Youth Spaces & Campus Pop-Ups": [("Campus / school", 38), ("Instagram", 26), ("Benzac App", 16), ("Pharmacy", 12), ("Snapchat", 8)],
    "3-Step Daily Routine Lock": [("Benzac App", 32), ("Instagram", 22), ("Quick-commerce", 18), ("CRM / WhatsApp", 16), ("Pharmacy", 12)],
}

PARTNER_ROSTER = {
    "First Pimple? Let's Talk.": {
        "Creator voices": "Agasthya Shah · Tarini Shah · Taneesho · Raw & Real campus creators",
        "Expert voices": "Dr. Aanchal Panth · Dr. Manasi Shirolikar",
        "Platform partners": "Instagram Reels · YouTube Shorts · Snapchat · Google Search",
        "Commerce partners": "Blinkit · Zepto · Nykaa",
    },
    "Benzac Derm Board & Science Hub": {
        "Creator voices": "Clinic-led creators · Resident doctor accounts",
        "Expert voices": "Dr. Rashmi Shetty · Dr. Aanchal Panth · Dr. Manasi Shirolikar · IADVL faculty",
        "Platform partners": "CME hubs · HCP portals · LinkedIn · YouTube",
        "Commerce partners": "Clinic dispensing · Apollo Pharmacy · MedPlus",
    },
    "Clear Skin, Confident Parenting": {
        "Creator voices": "Parent creators · Family health pages · School parent networks",
        "Expert voices": "Paediatric dermatologists · Family physicians · Pharmacist educators",
        "Platform partners": "YouTube · Facebook · Google Search · WhatsApp communities",
        "Commerce partners": "Apollo · PharmEasy · Netmeds · Modern trade",
    },
    "Youth Spaces & Campus Pop-Ups": {
        "Creator voices": "Campus ambassadors · College media pages · Student societies",
        "Expert voices": "Youth derm panel · Campus wellness cells",
        "Platform partners": "College fests · School wellness programmes · Instagram · Snapchat",
        "Commerce partners": "Campus pharmacy tie-ups · Blinkit · Zepto",
    },
    "3-Step Daily Routine Lock": {
        "Creator voices": "Routine creators · Skincare educators · Habit community leads",
        "Expert voices": "Dermatologists · Pharmacist creators",
        "Platform partners": "Benzac App · Instagram Reels · WhatsApp · CRM",
        "Commerce partners": "Nykaa · Amazon · Blinkit · Zepto · Pharmacy chains",
    },
}


# =============================================================================
# CAMPAIGN TRACKS
# =============================================================================
CAMPAIGN_DATA = [
    {
        "id": "C1",
        "name": "First Pimple? Let's Talk.",
        "short": "FIRST PIMPLE",
        "icon": "✦",
        "ruler_phase": "TALK + TRY",
        "audience": "Teens & Gen-Z (13–18)",
        "months": "M1 – M24",
        "start_m": 1,
        "end_m": 24,
        "accent": SKY,
        "art": ART_TEEN,
        "goal": "Make the first-pimple moment easier to talk about, easier to understand and easier to act on — then keep real peer progress visible over time.",
        "listening": "Teens already talk about acne publicly and reject brand polish. Shame, event panic and distrust of sponsored content are the recurring tensions.",
        "metrics": ["10M+ views", "150k trial packs", "25% engagement lift"],
    },
    {
        "id": "C2",
        "name": "Benzac Derm Board & Science Hub",
        "short": "DERM BOARD",
        "icon": "✚",
        "ruler_phase": "TRUST",
        "audience": "HCPs & Dermatologists",
        "months": "M4 – M24",
        "start_m": 4,
        "end_m": 24,
        "accent": BLUE,
        "art": ART_DERM,
        "goal": "Turn clinical evidence into practical confidence — equipping dermatologists to explain, recommend and reinforce appropriate acne care.",
        "listening": "Demand for expert access is real but blocked by price, not belief — the top community advice is to use government hospital derms. Sell access and openness, not authority.",
        "metrics": ["500+ derm partners", "+35% trust lift", "80k clinic kits"],
    },
    {
        "id": "C3",
        "name": "Clear Skin, Confident Parenting",
        "short": "PARENT CONFIDENCE",
        "icon": "◒",
        "ruler_phase": "TRUST",
        "audience": "Parents of Teens",
        "months": "M3 – M24",
        "start_m": 3,
        "end_m": 24,
        "accent": VIOLET,
        "art": ART_PARENT,
        "goal": "Replace household myths and treatment hesitation with calm, credible guidance that helps parents support teen acne care from first concern to routine.",
        "listening": "The parent controls the wallet and repeats the myths — hygiene blame, diet blame, home remedies. This audience needs its own myth-bust, not teen creative trickled down.",
        "metrics": ["2.5M parent reach", "40k household packs", "30% repeat purchase"],
    },
    {
        "id": "C4",
        "name": "Youth Spaces & Campus Pop-Ups",
        "short": "YOUTH SPACES",
        "icon": "◆",
        "ruler_phase": "PREFERENCE",
        "audience": "Teens & College Students",
        "months": "M3 – M24",
        "start_m": 3,
        "end_m": 24,
        "accent": "#2E86E0",
        "art": ART_CAMPUS,
        "goal": "Take Benzac into the spaces where young people already gather, turning real skin conversations into participation, trial and community-led advocacy.",
        "listening": "College entry and the post-board window are self-declared reset moments, and the first cart is usually curated by a friend. Timing matters more than scale here.",
        "metrics": ["120 college activations", "85k sampling units", "40% QR scans"],
    },
    {
        "id": "C5",
        "name": "3-Step Daily Routine Lock",
        "short": "ROUTINE LOCK",
        "icon": "↻",
        "ruler_phase": "HABIT",
        "audience": "Teens & Young Adults",
        "months": "M1 – M24",
        "start_m": 1,
        "end_m": 24,
        "accent": NAVY,
        "art": ART_ROUTINE,
        "goal": "Move Benzac from a one-off treatment into a repeatable Wash–Treat–Moisturize routine, supported from day one by the Benzac app, reminders, rewards and real-life proof.",
        "listening": "Carries the most listening evidence of any track. Irritation and purge confusion happen at first use — so this track runs from M1, alongside trial, not six months after it.",
        "metrics": ["+42% repeat purchase", "120k active trackers", "4.8/5 app rating"],
    },
]

# -----------------------------------------------------------------------------
# SUB-THEME TIMING  (parallel streams; timed to Indian calendar moments)
# -----------------------------------------------------------------------------
SUBTHEMES = {
    "First Pimple? Let's Talk.": [
        ("Myth Busters: What Nobody Told You", 1, 8, "TALK + TRY"),
        ("10-Min Relief: First-Pimple Fix", 1, 6, "TALK + TRY"),
        ("30-Day Real Skin Series", 2, 10, "TALK + TRY"),
        ("Festival & Function Ready", 9, 11, "TRUST"),
        ("Before & After, With the Science", 7, 15, "TRUST"),
        ("Real Progress: 30-Day Check-Ins", 5, 18, "TRUST"),
        ("Derm Reacts: Acne, Unfiltered", 7, 24, "TRUST"),
        ("Unfiltered Real Skin Stories", 13, 21, "PREFERENCE"),
        ("The Real Skin Wall", 14, 24, "PREFERENCE"),
        ("Routine Streak Reels", 19, 24, "HABIT"),
    ],
    "Benzac Derm Board & Science Hub": [
        ("OTC Acne Care: Safety in Practice", 4, 11, "TALK + TRY"),
        ("First-Visit Conversation Guides", 4, 13, "TALK + TRY"),
        ("Benzoyl Peroxide: The Deep Dive", 7, 17, "TRUST"),
        ("Clinical Evidence, Made Practical", 7, 24, "TRUST"),
        ("Better Patient Conversations", 8, 24, "TRUST"),
        ("Expert Reacts: Acne Online", 13, 24, "PREFERENCE"),
        ("Derm-Backed Real Skin Stories", 13, 24, "PREFERENCE"),
        ("Access Clinics & Camp Days", 10, 22, "PREFERENCE"),
        ("Long-Term Maintenance Plans", 19, 24, "HABIT"),
    ],
    "Clear Skin, Confident Parenting": [
        ("Acne Isn't a Hygiene Failure", 3, 10, "TALK + TRY"),
        ("Your Teen's First Treatment Guide", 3, 12, "TALK + TRY"),
        ("It's Not the Oily Food", 5, 14, "TRUST"),
        ("Ask the Derm, Ask the Paediatrician", 7, 19, "TRUST"),
        ("Gentle Care: What to Compare", 8, 15, "TRUST"),
        ("Parents Who've Been Through It", 13, 24, "PREFERENCE"),
        ("The Family Acne-Care Shelf", 13, 24, "PREFERENCE"),
        ("School-Term Stock-Up", 5, 7, "HABIT"),
        ("Care Routine & Refill Reminders", 17, 24, "HABIT"),
    ],
    "Youth Spaces & Campus Pop-Ups": [
        ("Post-Board Campus Sessions", 3, 7, "TALK + TRY"),
        ("Try-It-Here Starter Access", 3, 9, "TALK + TRY"),
        ("Know Your Skin Stations", 7, 18, "TRUST"),
        ("Interactive Acne Check-Ins", 8, 18, "TRUST"),
        ("Admission-Month Freshers Drive", 6, 8, "TRUST"),
        ("The Real Skin Wall", 13, 21, "PREFERENCE"),
        ("Say It Anonymously", 13, 24, "PREFERENCE"),
        ("Campus Creator Network", 13, 24, "PREFERENCE"),
        ("Campus ClearStreak League", 19, 24, "HABIT"),
    ],
    "3-Step Daily Routine Lock": [
        ("Benzac App: Day-1 Onboarding", 1, 24, "TALK + TRY"),
        ("ClearStreak Tracker (Always-On)", 1, 24, "TALK + TRY"),
        ("The 15-Second Routine Preview", 1, 9, "TALK + TRY"),
        ("Trial Pack: Start Your 3 Steps", 1, 11, "TALK + TRY"),
        ("Week One: What's Normal", 2, 16, "TRUST"),
        ("Treat Acne, Respect Your Barrier", 7, 19, "TRUST"),
        ("Derm-Approved Routine Checks", 9, 21, "TRUST"),
        ("AM/PM Routines That Feel Real", 13, 24, "PREFERENCE"),
        ("Marks & SPF: The Next Step", 15, 24, "PREFERENCE"),
        ("ClearStreak 30 Challenge", 19, 24, "HABIT"),
        ("Smart Auto-Replenish Rewards", 20, 24, "HABIT"),
    ],
}

# -----------------------------------------------------------------------------
# SUB-THEME EXECUTION DETAIL
# platforms · format · partners · content · listening insight · KPI
# -----------------------------------------------------------------------------
D = {}

D["First Pimple? Let's Talk."] = {
    "Myth Busters: What Nobody Told You": ("Instagram Reels · YouTube Shorts · Snapchat", "15–30s myth-vs-fact, Hinglish VO", "Agasthya Shah · Tarini Shah · Taneesho", "Fast myth-vs-fact takes that make acne easier to talk about — dirt, diet, popping.", "Community myth-busting already exists on Reddit; amplify it with derm voices instead of lecturing.", "Reach · saves per view"),
    "10-Min Relief: First-Pimple Fix": ("Instagram Reels · Google Search · Benzac App", "Vertical explainer + search landing page", "Skin educators · Pharmacist creators", "One clear first step for the moment a new pimple appears, in Hinglish.", "‘pimple kaise hataye’ and ‘overnight’ dominate India search — meet the panic query with a real first step.", "Search CTR · app installs"),
    "30-Day Real Skin Series": ("YouTube Shorts · Instagram Reels", "Serialised 30-day diary, unretouched", "Teen creators · Student volunteers", "Unfiltered 30-day diaries showing what starting treatment actually looks like.", "Proof means a timeline from a real person, not a claim from a brand.", "Completion rate · follows"),
    "Festival & Function Ready": ("Instagram · Blinkit · Zepto · Search", "Event-week burst + quick-commerce banners", "Micro-creators · Quick-commerce partners", "What to do — and what not to start — in the week before a function.", "Wedding and festival panic posts spike Sep–Nov; close to an event people stop actives, so recruit before, not during.", "Quick-commerce sales lift"),
    "Before & After, With the Science": ("YouTube · Instagram", "Split-screen progress + derm caption", "Derm educators · Galderma medical team", "Progress visuals paired with a plain-language explanation of what changed.", "Before/after alone reads as advertising; the science caption is what makes it credible.", "View-through · claim recall"),
    "Real Progress: 30-Day Check-Ins": ("YouTube Shorts · Instagram Stories", "Weekly check-in format", "Real users · Campus contributors", "Weekly check-ins that normalise uneven progress and continued use.", "Most ‘it didn't work’ posts are duration failures — normalise week 3.", "Repeat viewership"),
    "Derm Reacts: Acne, Unfiltered": ("YouTube Shorts · Instagram Reels", "Reaction / duet format", "Dr. Aanchal Panth · Dr. Manasi Shirolikar", "Derm reactions to viral acne claims, routines and hacks.", "Derm AMAs draw hundreds of questions; unscripted expert access outperforms polished brand education.", "Comment volume · trust lift"),
    "Unfiltered Real Skin Stories": ("Instagram · Reddit-style communities", "Long-form user story + carousel", "Peer creators · Acne community voices", "Honest stories that build relatability and reduce stigma.", "Public acne shaming posts draw very high engagement — the emotional territory is unclaimed in India.", "Shares · sentiment"),
    "The Real Skin Wall": ("Campus pop-ups · Instagram", "Physical wall → social amplification", "Student communities · Festival crowds", "Anonymous real skin stories collected offline and amplified socially.", "Anonymity is what unlocks the honest version of the story.", "Participation · UGC volume"),
    "Routine Streak Reels": ("Instagram Reels · Benzac App", "Streak card + reel template", "Habit creators · Campus ambassadors", "Short streak updates that make consistency visible and social.", "Consistency is the behaviour the category never rewards.", "Streaks > 21 days"),
}

D["Benzac Derm Board & Science Hub"] = {
    "OTC Acne Care: Safety in Practice": ("HCP portals · LinkedIn", "Clinical one-pager + short module", "Galderma Medical Affairs", "Concise safety guidance for practical OTC acne conversations.", "Irritation is the main adherence barrier — safety framing is what HCPs need first.", "HCP module completions"),
    "First-Visit Conversation Guides": ("Clinic kits · HCP portals", "Printed consult aid + digital kit", "Dermatology clinics · Resident networks", "Simple aids for explaining first-line acne care in a 7-minute consult.", "Patients arrive having already self-treated; the guide has to start from that.", "Kits placed · clinics active"),
    "Benzoyl Peroxide: The Deep Dive": ("Webinars · Medical portals", "CME-style science module", "Acne specialists · Galderma scientific team", "Mechanism, use, strength selection and patient suitability.", "Indian consensus positions BPO as cornerstone therapy with no antimicrobial resistance — an ownable argument.", "CME attendance"),
    "Clinical Evidence, Made Practical": ("CME hubs · HCP email", "Evidence digest series", "Dr. Rashmi Shetty · Dermatology faculty", "Evidence summaries translated into consultation takeaways.", "Scarring 34% / pigmentation 40% in a South India study — the scar-prevention case is clinically defensible.", "Recommendation share"),
    "Better Patient Conversations": ("Clinic aids · Webinars", "Counselling toolkit", "Dermatologists · Patient educators", "Tools that improve explanation, adherence and follow-up.", "Counselling on timeline and expected irritation is what prevents dropout.", "Adherence proxy · refills"),
    "Expert Reacts: Acne Online": ("YouTube Shorts · Instagram Reels", "Derm reaction to viral content", "Dr. Manasi Shirolikar · Dr. Aanchal Panth", "Credible reactions to viral acne myths and hacks.", "Influencer endorsement now reads as evidence against; unpaid-feeling expert correction reads as evidence for.", "Reach · myth recall"),
    "Derm-Backed Real Skin Stories": ("Instagram · YouTube", "Patient story + expert context", "Dr. Rashmi Shetty · Clinic creators", "Real progress stories contextualised with responsible expert guidance.", "Pairing a real journey with a clinician closes the credibility gap neither closes alone.", "Trust lift"),
    "Access Clinics & Camp Days": ("Government & teaching hospitals · Schools", "Free consult camps", "IADVL chapters · Public hospital derms", "Low-cost derm access days in tier-1 and tier-2 cities.", "The top community post on derm care is to use government hospitals because private clinics are unaffordable — access, not belief, is the barrier.", "Consults delivered"),
    "Long-Term Maintenance Plans": ("Clinic POS · HCP CRM", "Maintenance pathway card", "Derm clinic partners", "Simple maintenance pathways for post-improvement continuity.", "Conversation shifts to marks once acne clears — that is the retention cliff.", "Maintenance conversion"),
}

D["Clear Skin, Confident Parenting"] = {
    "Acne Isn't a Hygiene Failure": ("Facebook · YouTube · Parent communities", "Short explainer + carousel", "Parent creators · Family health pages", "Reassuring myth-busting that removes blame from acne.", "Teens report being blamed for ‘not washing your face’ — the myth turns a medical condition into a character judgement at home.", "Parent reach · myth shift"),
    "Your Teen's First Treatment Guide": ("Google Search · Parent blogs", "SEO guide + printable", "Family physicians · Parenting publishers", "A practical first-step guide for parents deciding what to do next.", "Parents search before they buy; the guide is the moment Benzac becomes an option.", "Organic sessions"),
    "It's Not the Oily Food": ("YouTube · WhatsApp · Facebook", "Myth-bust film + shareable card", "Paediatric dermatologists · Nutrition educators", "What actually causes acne, in plain language for the family.", "Diet moralising displaces treatment and delays effective action.", "Share rate"),
    "Ask the Derm, Ask the Paediatrician": ("YouTube · Facebook Live", "Live Q&A", "Paediatric dermatologists · Paediatricians", "Parent questions answered calmly, in plain language.", "Parents want a professional to sanction the decision before they spend.", "Live attendance"),
    "Gentle Care: What to Compare": ("Search · E-commerce education", "Comparison module on PDPs", "Pharmacists · Skin educators", "Simple comparison tools for evaluating acne-care options.", "‘Harsh formula’ is the top parent rejection reason — comparison has to answer that head-on.", "PDP conversion"),
    "Parents Who've Been Through It": ("WhatsApp communities · Facebook", "Peer testimonial series", "Parent ambassadors · School parent networks", "Peer stories about navigating teen acne without overreacting.", "Parents trust other parents more than brands, and about as much as doctors.", "Referral rate"),
    "The Family Acne-Care Shelf": ("Nykaa · PharmEasy · Apollo · Modern trade", "Shelf + PDP decision aid", "Pharmacists · Parent creators", "Where Benzac fits in a family care routine.", "69% of parents buy at the pharmacy — the shelf is the decision point.", "Offtake per store"),
    "School-Term Stock-Up": ("E-commerce · CRM · Pharmacy", "Seasonal bundle", "Retail partners · Parent communities", "Replenishment prompts timed to the June school term.", "Term start is a natural household restock moment.", "Bundle sales"),
    "Care Routine & Refill Reminders": ("WhatsApp · Email", "Lifecycle CRM", "Benzac Care Team", "Reminders that support continuity without nagging.", "Adherence, not efficacy, is the real battleground.", "Refill rate"),
}

D["Youth Spaces & Campus Pop-Ups"] = {
    "Post-Board Campus Sessions": ("Schools · Junior colleges", "Derm-led session + Q&A", "Youth derm panel · Student wellness cells", "Live myth-vs-fact conversations built for first-time questions.", "Teens declare the post-board window (Mar–Jun) as a reset moment with time to build a habit.", "Sessions · attendees"),
    "Try-It-Here Starter Access": ("Campus booths · Pharmacy counters", "Sampling + QR", "College fests · Retail pharmacists", "Low-friction sampling and QR-led product discovery.", "Teens self-treat before they consult — the OTC shelf is the real first consultation.", "Samples · QR scans"),
    "Know Your Skin Stations": ("Campus pop-ups · Festival booths", "Interactive station", "Skin experts · Student volunteers", "Stations that turn curiosity into an informed next step.", "Participation beats advertising in spaces teens already occupy.", "Footfall · dwell time"),
    "Interactive Acne Check-Ins": ("Pop-up diagnostics · QR microsite", "Guided self-assessment", "Derm educators · Campus wellness teams", "Self-assessment and education without over-medicalising it.", "Beginners actively ask communities to critique their routine — the audit is the unmet service.", "Check-ins completed"),
    "Admission-Month Freshers Drive": ("Colleges · Instagram · Snapchat", "Freshers kit + campus takeover", "Campus ambassadors · Student societies", "Reach first-years in their first weeks on campus.", "College entry is an identity reset where skin is judged by strangers.", "First-year penetration"),
    "The Real Skin Wall": ("Campus pop-ups · Instagram", "Physical participation wall", "Students · Festival communities", "A public wall celebrating real, imperfect skin.", "Acne shaming is a live, unclaimed emotional territory in India.", "Notes posted · UGC"),
    "Say It Anonymously": ("Anonymous QR wall · Instagram Stories", "Anonymous prompt wall", "Student mental-health clubs · Peer moderators", "Anonymous prompts that surface the emotions behind acne.", "Anonymity is what makes the honest version of the story possible.", "Submissions"),
    "Campus Creator Network": ("Instagram Reels · College media pages", "Always-on creator programme", "Campus ambassadors · Student creators", "Creator-led routines, reviews and local event amplification.", "The first cart is peer-initiated and community-validated, not advertising-led.", "Creators active · EMV"),
    "Campus ClearStreak League": ("Benzac App · Campus groups", "Inter-campus leaderboard", "Campus ambassadors · Student societies", "Friendly inter-campus consistency challenges.", "Consistency becomes social when it is visible and competitive.", "Participants · streaks"),
}

D["3-Step Daily Routine Lock"] = {
    "Benzac App: Day-1 Onboarding": ("Benzac App · QR on pack", "Onboarding flow, live from launch", "Benzac Skin Coach · Product team", "Scan the pack, set the routine, start the streak — from day one.", "The app is live from M1, so onboarding must catch the first-use moment, not a later phase.", "Install → activation rate"),
    "ClearStreak Tracker (Always-On)": ("Benzac App · WhatsApp", "Daily tracker + nudges", "Benzac Skin Coach", "Wash–Treat–Moisturize tracking with light daily prompts.", "Simplicity is the credibility signal — a 3-step routine is what people actually keep.", "DAU · 30-day retention"),
    "The 15-Second Routine Preview": ("Instagram Reels · YouTube Shorts", "Ultra-short demo", "Routine creators · Skincare educators", "The whole routine in fifteen seconds.", "‘One product, one job’ is the community's own rule — show it, don't explain it.", "Completion rate"),
    "Trial Pack: Start Your 3 Steps": ("Pharmacy · Blinkit · Zepto · Nykaa", "Starter kit + shelf education", "Pharmacy chains · Quick-commerce partners", "A starter pack that makes the routine easy and cheap to begin.", "Teens set explicit rupee budgets — value and pack longevity are a first filter, before efficacy.", "Trial packs sold"),
    "Week One: What's Normal": ("Benzac App · Google Search · Instagram", "Day 1–7 guidance series", "Dermatologists · Pharmacist educators", "Is this purging or a reaction? What to do, day by day.", "Redness and purge-or-react confusion in week one is the densest cluster in Indian skincare communities — and where trial is lost.", "Week-2 continuation rate"),
    "Treat Acne, Respect Your Barrier": ("YouTube · Google Search", "Education film + FAQ", "Dermatologists · Pharmacist educators", "Treatment consistency and barrier-aware care.", "48% of Asian acne patients show poor adherence, largely from side effects and missing moisturiser.", "Adherence proxy"),
    "Derm-Approved Routine Checks": ("Instagram · Benzac App", "Derm routine audit", "Derm creators · Resident doctors", "Expert reviews that correct common sequencing mistakes.", "Beginners ask communities to critique their routine — a derm-reviewed check is the branded version of that.", "Checks completed"),
    "AM/PM Routines That Feel Real": ("Instagram Reels · Stories", "Day-in-the-life format", "Lifestyle creators · Campus creators", "Real morning and night routines built around school and college schedules.", "Routines have to survive a 7am school run, not a studio.", "Saves · shares"),
    "Marks & SPF: The Next Step": ("Benzac App · Nykaa · Instagram", "Post-clearance journey", "Derm creators · Beauty reviewers", "What to do once the acne clears — marks, pigmentation, SPF habit.", "Conversation shifts entirely to marks after clearance; this is where repeat purchase is won or lost.", "Post-clearance repeat rate"),
    "ClearStreak 30 Challenge": ("Benzac App · WhatsApp · Campus", "30-day gamified challenge", "Benzac Skin Coach · Habit community", "Thirty days, milestones, encouragement and rewards.", "An honest 30-day promise beats competing on ‘overnight’.", "Challenge completion"),
    "Smart Auto-Replenish Rewards": ("CRM · Quick-commerce · E-commerce", "Subscription + reward", "Retail CRM partners", "Timed replenishment rewards that reinforce repeat use.", "Replenishment prompts work when tied to the actual routine cycle.", "Subscription share"),
}

SUBTHEME_DETAILS = D


# =============================================================================
# CSS
# =============================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family:'Plus Jakarta Sans', system-ui, sans-serif; }
[data-testid="stAppViewContainer"] { background:#F2F6FC; }
#MainMenu, footer, header { visibility:hidden; }
.block-container { max-width:1560px; padding:1.1rem 2rem 3.5rem; }

/* ---------- HERO : two columns, nothing overlaps ---------- */
.hero{
  position:relative; overflow:hidden; border-radius:28px; margin-bottom:20px; color:#fff;
  background:linear-gradient(115deg,#061A3A 0%,#0B2A8C 52%,#1E63D8 100%);
  box-shadow:0 20px 44px rgba(9,26,60,.22);
  display:grid; grid-template-columns:minmax(0,1.35fr) minmax(0,.65fr);
}
.hero-left{ padding:40px 30px 34px 46px; position:relative; z-index:2; }
.hero-right{ position:relative; display:flex; flex-direction:column; justify-content:center;
  gap:10px; padding:34px 40px 34px 12px; z-index:2; }
.hero-kicker{ font-size:.7rem; letter-spacing:.22em; font-weight:800; color:#8AD6F5; margin-bottom:18px; }
.hero h1{ color:#fff!important; font-size:2.85rem; line-height:1.04; letter-spacing:-.045em;
  margin:0 0 14px; font-weight:800; }
.hero p{ color:#CFE0F2!important; font-size:1rem; font-weight:500; line-height:1.62; margin:0; max-width:640px; }
.hero-badges{ display:flex; gap:8px; flex-wrap:wrap; margin-top:20px; }
.hero-badge{ font-size:.66rem; font-weight:800; letter-spacing:.09em; padding:7px 12px; border-radius:999px;
  background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.22); color:#EAF3FF; }
.hero-stat{ display:flex; align-items:center; gap:14px; background:rgba(255,255,255,.10);
  border:1px solid rgba(255,255,255,.2); border-radius:15px; padding:12px 16px; }
.hero-stat b{ font-size:1.5rem; line-height:1; color:#fff; min-width:52px; }
.hero-stat span{ font-size:.63rem; letter-spacing:.1em; text-transform:uppercase; color:#B9D2EA; font-weight:800; }
.hero-art{ position:absolute; right:-30px; top:50%; transform:translateY(-50%); width:430px; opacity:.42; z-index:1; }

/* ---------- TABS : big, obvious, branded ---------- */
.nav-hint{ font-size:.62rem; font-weight:800; letter-spacing:.18em; color:#8FA3BD; margin:2px 0 8px 4px; }

.st-key-nav_view [data-baseweb="button-group"]{ gap:10px!important; background:transparent!important; width:100%; }

.st-key-nav_view button{
  flex:1 1 0!important; border-radius:14px!important; border:1.5px solid #D6E3F4!important;
  background:#FFFFFF!important; padding:.9rem 1.4rem!important; font-size:1.02rem!important;
  font-weight:800!important; color:#26456F!important; transition:.15s ease; letter-spacing:-.01em;
  box-shadow:0 2px 6px rgba(16,38,74,.05);
}
.st-key-nav_view button p{ font-size:1.02rem!important; font-weight:800!important;
  color:inherit!important; overflow:visible!important; text-overflow:clip!important; white-space:nowrap!important; }
.st-key-nav_view button div{ max-width:none!important; overflow:visible!important;
  text-overflow:clip!important; }

.st-key-nav_view button:hover{ background:#EDF4FF!important; border-color:#9FC2EE!important; color:#0B2A8C!important; }

.st-key-nav_view button[aria-checked="true"],
.st-key-nav_view button[aria-pressed="true"],
.st-key-nav_view button[kind="segmented_controlActive"],
.st-key-nav_view [data-testid="stBaseButton-segmented_controlActive"]{
  background:linear-gradient(120deg,#0B2A8C,#1E63D8)!important; color:#FFFFFF!important;
  border-color:#0B2A8C!important; box-shadow:0 10px 20px rgba(11,42,140,.30)!important;
}
.st-key-nav_view button[aria-checked="true"] p,
.st-key-nav_view button[aria-pressed="true"] p,
.st-key-nav_view button[kind="segmented_controlActive"] p,
.st-key-nav_view [data-testid="stBaseButton-segmented_controlActive"] p{ color:#FFFFFF!important; }

/* track filter pills */
.st-key-track_filter [data-baseweb="button-group"]{ gap:8px!important; flex-wrap:wrap; }
.st-key-track_filter button{ border-radius:999px!important; border:1.5px solid #D6E3F4!important;
  background:#fff!important; padding:.45rem 1rem!important; font-weight:700!important; color:#3D5170!important; }
.st-key-track_filter button p{ font-size:.78rem!important; font-weight:700!important; color:inherit!important;
  white-space:nowrap!important; overflow:visible!important; text-overflow:clip!important; }
.st-key-track_filter button div{ max-width:none!important; overflow:visible!important; }
.st-key-track_filter button[aria-checked="true"],
.st-key-track_filter button[aria-pressed="true"],
.st-key-track_filter button[kind="pillsActive"],
.st-key-track_filter [data-testid="stBaseButton-pillsActive"]{
  background:#1E63D8!important; border-color:#1E63D8!important; }
.st-key-track_filter button[aria-checked="true"] p,
.st-key-track_filter button[aria-pressed="true"] p,
.st-key-track_filter button[kind="pillsActive"] p,
.st-key-track_filter [data-testid="stBaseButton-pillsActive"] p{ color:#fff!important; }

/* ---------- widget recolour: Benzac blue, never red ---------- */
:root, [data-testid="stAppViewContainer"]{
  --primary-color:#1E63D8; --p-color:#1E63D8; --link-color:#1E63D8;
}
[data-baseweb="tag"]{ background-color:#1E63D8!important; background-image:none!important;
  border-radius:9px!important; font-weight:700!important; border:0!important; color:#fff!important; }
[data-baseweb="tag"] *{ color:#fff!important; fill:#fff!important; background-color:transparent!important; }
[data-baseweb="tag"] [role="presentation"]:hover{ background-color:rgba(255,255,255,.22)!important; }
[data-testid="stMultiSelect"] div[data-baseweb="select"] > div{
  border-radius:13px!important; border:1.5px solid #D6E3F4!important; }
[data-testid="stRadio"] label p{ font-size:.82rem!important; font-weight:700!important; color:#33475F!important; }
[data-testid="stRadio"] [data-baseweb="radio"] div[aria-checked="true"]{ background-color:#1E63D8!important; }
[data-testid="stWidgetLabel"] p{ font-size:.7rem!important; font-weight:800!important;
  letter-spacing:.1em; text-transform:uppercase; color:#8FA3BD!important; }
[data-testid="stExpander"] summary p{ font-weight:800!important; color:#0B2A8C!important; }
[data-testid="stDownloadButton"] button{ background:#0B2A8C!important; color:#fff!important;
  border:0!important; border-radius:12px!important; font-weight:800!important; }

/* the one selectbox in the app = the campaign picker */
[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
.stSelectbox div[data-baseweb="select"] > div{
  border-radius:14px!important; border:2px solid #1E63D8!important; background:#fff!important;
  min-height:58px!important; box-shadow:0 10px 22px rgba(11,42,140,.16); }
[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div,
.stSelectbox div[data-baseweb="select"] > div > div{
  font-weight:800!important; font-size:1.02rem!important; color:#0B2A8C!important; }
[data-testid="stSelectbox"] div[data-baseweb="select"] svg,
.stSelectbox div[data-baseweb="select"] svg{ fill:#1E63D8!important; width:26px; height:26px; }

/* ---------- SECTION BANNER ---------- */
.banner{ position:relative; overflow:hidden; border-radius:22px; margin:16px 0 6px;
  background:linear-gradient(110deg,#0B2A8C,#1E63D8 70%,#35AEE6); color:#fff;
  padding:22px 28px; display:flex; justify-content:space-between; align-items:center; gap:20px; }
.banner h3{ margin:0; font-size:1.45rem; font-weight:800; letter-spacing:-.03em; color:#fff; }
.banner p{ margin:6px 0 0; font-size:.85rem; color:#CBDDF3; max-width:820px; line-height:1.55; }
.banner img{ height:96px; border-radius:14px; opacity:.9; }

.section-title{ font-size:1.55rem; font-weight:800; letter-spacing:-.035em; color:#12294A; margin:24px 0 4px; }
.section-sub{ color:#6B7C93; font-size:.88rem; margin-bottom:14px; }

/* ---------- OVERVIEW ---------- */
.journey{ display:grid; grid-template-columns:repeat(4,1fr); background:#fff; border:1px solid #E0E9F5;
  border-radius:20px; overflow:hidden; margin:14px 0 20px; }
.journey-step{ min-height:130px; padding:18px 20px; position:relative; border-right:1px solid #EAF0F8; }
.journey-step:last-child{ border-right:0; }
.journey-num{ font-size:.62rem; font-weight:800; letter-spacing:.13em; color:#8AA0BC; }
.journey-name{ font-size:1.02rem; font-weight:800; color:#14294A; margin-top:8px; }
.journey-desc{ font-size:.74rem; color:#6B7C93; line-height:1.5; margin-top:7px; }
.journey-accent{ position:absolute; left:0; right:0; bottom:0; height:5px; }

.metric-strip{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:22px; }
.metric{ background:#fff; border:1px solid #E0E9F5; border-radius:16px; padding:15px 18px; }
.metric b{ font-size:1.45rem; color:#0B2A8C; display:block; }
.metric span{ font-size:.66rem; color:#7B8CA3; font-weight:800; text-transform:uppercase; letter-spacing:.09em; }

.signal-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin:12px 0 8px; }
.signal{ background:#fff; border:1px solid #E0E9F5; border-radius:16px; padding:16px 18px; }
.signal b{ display:block; font-size:1.02rem; color:#0B2A8C; font-weight:800; margin-bottom:7px; }
.signal .obs{ font-size:.73rem; color:#61738C; line-height:1.5; }
.signal .act{ font-size:.71rem; color:#1E63D8; font-weight:700; line-height:1.45; margin-top:9px;
  border-top:1px solid #EDF2F9; padding-top:9px; }

.campaign-grid{ display:grid; grid-template-columns:repeat(5,1fr); gap:14px; }
.campaign-card{ background:#fff; border:1px solid #E0E9F5; border-radius:20px; overflow:hidden;
  transition:.2s ease; display:flex; flex-direction:column; }
.campaign-card:hover{ transform:translateY(-4px); box-shadow:0 16px 32px rgba(16,38,74,.12); }
.campaign-art{ height:118px; position:relative; overflow:hidden; }
.campaign-art img{ width:100%; height:100%; object-fit:cover; display:block; }
.campaign-art .tag{ position:absolute; left:14px; top:12px; font-size:.6rem; letter-spacing:.13em;
  font-weight:800; color:#fff; background:rgba(0,0,0,.24); padding:4px 9px; border-radius:999px; }
.campaign-body{ padding:15px 16px 17px; display:flex; flex-direction:column; flex:1; }
.campaign-name{ font-size:.98rem; font-weight:800; line-height:1.24; color:#12294A; min-height:46px; }
.campaign-aud{ font-size:.66rem; color:#1E63D8; font-weight:800; margin:8px 0 9px; }
.campaign-goal{ font-size:.72rem; color:#66788F; line-height:1.55; flex:1; }
.mini-chip{ display:inline-block; font-size:.58rem; font-weight:800; border-radius:999px;
  padding:5px 9px; margin:9px 4px 0 0; }

/* ---------- CALENDAR ---------- */
.cal-controls{ background:#fff; border:1px solid #DFE8F4; border-radius:18px; padding:14px 18px; margin-bottom:14px; }
.phase-strip{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin:0 0 16px; }
.phase-brief{ border-radius:16px; padding:14px 16px; color:#fff; }
.phase-brief b{ font-size:.82rem; font-weight:800; letter-spacing:.04em; display:block; }
.phase-brief small{ font-size:.6rem; opacity:.85; font-weight:800; letter-spacing:.1em; }
.phase-brief p{ font-size:.7rem; margin:8px 0 0; line-height:1.5; opacity:.94; }

.calendar-shell{ background:#fff; border:1px solid #DFE8F4; border-radius:20px; padding:16px;
  box-shadow:0 10px 26px rgba(16,38,74,.06); overflow-x:auto; }
.calendar-board{ min-width:1280px; }
.cal-head{ display:grid; grid-template-columns:250px repeat(24,minmax(40px,1fr)); }
.cal-head-label{ background:#0B2A8C; color:#fff; border-radius:12px 0 0 0; padding:14px 16px;
  font-size:.7rem; font-weight:800; letter-spacing:.08em; display:flex; align-items:center; }
.cal-phase{ padding:11px 4px 9px; text-align:center; font-weight:800; font-size:.68rem; color:#fff;
  border-left:1px solid rgba(255,255,255,.2); }
.cal-phase small{ display:block; font-size:.55rem; opacity:.85; margin-top:3px; letter-spacing:.07em; }
.month-row{ display:grid; grid-template-columns:250px repeat(24,minmax(40px,1fr)); }
.month-label{ background:#F7FAFE; border-bottom:1px solid #E4ECF6; border-right:1px solid #EEF3F9;
  min-height:42px; display:flex; flex-direction:column; justify-content:center; align-items:center;
  font-size:.55rem; color:#6E819C; font-weight:800; }
.month-label span{ font-size:.5rem; color:#A6B4C7; }
.season-row{ display:grid; grid-template-columns:250px repeat(24,minmax(40px,1fr)); }
.season-label{ font-size:.55rem; font-weight:800; letter-spacing:.09em; color:#8CA0BA;
  display:flex; align-items:center; padding-left:16px; min-height:30px; }
.season-chip{ margin:4px 3px; border-radius:7px; background:#EAF2FF; border:1px dashed #A9C6F0;
  color:#1E63D8; font-size:.55rem; font-weight:800; display:flex; align-items:center;
  justify-content:center; padding:0 6px; text-align:center; line-height:1.15; overflow:hidden; }

.campaign-group{ display:grid; grid-template-columns:250px 1fr; border-top:1px solid #E7EEF7; background:#fff; }
.group-label{ padding:16px 15px; border-right:1px solid #EAF0F8; }
.group-name{ font-size:.8rem; font-weight:800; color:#14294A; line-height:1.3; }
.group-aud{ font-size:.6rem; color:#7688A0; font-weight:700; margin-top:5px; }
.group-meta{ font-size:.55rem; font-weight:800; letter-spacing:.08em; margin-top:8px; text-transform:uppercase; }
.group-track{ padding:8px 0; background-color:#fff;
  background-image:linear-gradient(to right,#EDF2F9 1px,transparent 1px); background-size:calc(100%/24) 100%; }
.subtheme-row{ display:grid; grid-template-columns:repeat(24,minmax(40px,1fr)); min-height:34px; align-items:center; }
.subtheme-bar{ height:26px; margin:3px 2px; border-radius:7px; color:#fff; padding:0 9px; display:flex;
  align-items:center; font-size:.58rem; font-weight:800; white-space:nowrap; overflow:hidden;
  text-overflow:ellipsis; box-shadow:0 3px 7px rgba(11,42,140,.16); }
.bar-talk{ background:linear-gradient(90deg,#35AEE6,#1E9AD8); }
.bar-trust{ background:linear-gradient(90deg,#2E86E0,#1E63D8); }
.bar-pref{ background:linear-gradient(90deg,#7E63E8,#6B4FE0); }
.bar-habit{ background:linear-gradient(90deg,#1B3FA8,#0B2A8C); }
.legend{ display:flex; flex-wrap:wrap; gap:16px; margin:14px 2px 0; }
.legend-item{ display:flex; align-items:center; gap:7px; font-size:.68rem; color:#66788F; font-weight:700; }
.legend-dot{ width:11px; height:11px; border-radius:3px; }

/* ---------- PICKER ---------- */
.picker-card{ background:linear-gradient(115deg,#0B2A8C,#1E63D8); border-radius:20px;
  padding:18px 22px 6px; margin:16px 0 18px; box-shadow:0 12px 26px rgba(11,42,140,.24); }
.picker-card .plabel{ font-size:.68rem; letter-spacing:.18em; font-weight:800; color:#9FD3F5; margin-bottom:8px; }
.picker-card .phint{ font-size:.74rem; color:#CFE3F8; margin:0 0 12px; }

/* ---------- DETAILS ---------- */
.detail-hero{ background:#fff; border:1px solid #E0E9F5; border-radius:24px; overflow:hidden;
  display:grid; grid-template-columns:1.4fr .6fr; margin:6px 0 18px; }
.detail-main{ padding:26px 30px; }
.detail-kicker{ font-size:.63rem; letter-spacing:.14em; font-weight:800; margin-bottom:11px; }
.detail-main h2{ font-size:2rem; letter-spacing:-.04em; color:#12294A; margin:0 0 11px; }
.detail-main p{ font-size:.9rem; color:#5D708A; line-height:1.65; max-width:760px; margin:0; }
.detail-art img{ width:100%; height:100%; object-fit:cover; display:block; }
.insight-band{ background:#F3F8FF; border:1px solid #D9E7FA; border-left:5px solid #1E63D8;
  border-radius:12px; padding:13px 16px; margin-top:16px; }
.insight-band b{ font-size:.58rem; letter-spacing:.13em; color:#1E63D8; font-weight:800; display:block; margin-bottom:5px; }
.insight-band span{ font-size:.78rem; color:#42566F; line-height:1.55; }
.detail-stat-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:16px; }
.detail-stat{ background:#F7FAFF; border:1px solid #E5EDF8; border-radius:13px; padding:12px; }
.detail-stat b{ font-size:.88rem; color:#0B2A8C; display:block; }
.detail-stat span{ font-size:.56rem; color:#8598B1; text-transform:uppercase; letter-spacing:.09em; font-weight:800; }

.roster-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin:6px 0 4px; }
.roster{ background:#fff; border:1px solid #E0E9F5; border-radius:16px; padding:15px 17px; }
.roster b{ font-size:.58rem; letter-spacing:.12em; color:#8FA3BD; font-weight:800; display:block; margin-bottom:7px; }
.roster span{ font-size:.76rem; color:#33475F; font-weight:600; line-height:1.55; }

.mix-card{ background:#fff; border:1px solid #E0E9F5; border-radius:18px; padding:16px 20px; }
.mix-row{ display:grid; grid-template-columns:150px 1fr 42px; align-items:center; gap:10px; margin:9px 0; }
.mix-name{ font-size:.72rem; font-weight:700; color:#3D5170; }
.mix-track{ background:#EAF1FB; border-radius:999px; height:11px; overflow:hidden; }
.mix-fill{ height:11px; border-radius:999px; background:linear-gradient(90deg,#35AEE6,#1E63D8); }
.mix-val{ font-size:.68rem; font-weight:800; color:#1E63D8; text-align:right; }

.detail-theme-table{ background:#fff; border:1px solid #E0E9F5; border-radius:18px; padding:14px; overflow-x:auto; }
.detail-theme-grid{ min-width:1040px; }
.detail-theme-months,.detail-theme-row{ display:grid; grid-template-columns:230px repeat(24,1fr); }
.detail-theme-month{ min-height:34px; display:flex; align-items:center; justify-content:center;
  border-bottom:1px solid #EAF0F8; border-right:1px solid #F0F4FA; font-size:.52rem; color:#7688A0; font-weight:800; }
.detail-theme-name{ display:flex; align-items:center; padding:0 12px; border-bottom:1px solid #EAF0F8;
  font-size:.66rem; font-weight:800; color:#2E4763; }
.detail-subtheme-bar{ height:25px; align-self:center; margin:5px 2px; border-radius:7px; color:#fff;
  padding:0 9px; display:flex; align-items:center; font-size:.56rem; font-weight:800;
  overflow:hidden; white-space:nowrap; text-overflow:ellipsis; }

.exec-grid{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; margin:12px 0 6px; }
.exec-card{ background:#fff; border:1px solid #E0E9F5; border-radius:18px; padding:18px 19px;
  box-shadow:0 6px 16px rgba(16,38,74,.045); }
.exec-top{ display:flex; justify-content:space-between; align-items:flex-start; gap:12px; margin-bottom:13px; }
.exec-name{ font-size:.95rem; font-weight:800; color:#14294A; line-height:1.25; }
.exec-when{ font-size:.66rem; color:#7789A1; font-weight:700; margin-top:5px; }
.exec-status{ flex:0 0 auto; font-size:.56rem; font-weight:800; color:#1E63D8; background:#EAF2FF;
  border:1px solid #CFE0F8; border-radius:999px; padding:5px 9px; white-space:nowrap; }
.exec-meta{ display:grid; grid-template-columns:1fr 1fr; gap:11px 18px; border-top:1px solid #EDF2F9; padding-top:12px; }
.exec-block.full{ grid-column:1 / -1; }
.exec-label{ font-size:.54rem; font-weight:800; letter-spacing:.11em; color:#9BADC6; margin-bottom:4px; }
.exec-value{ font-size:.72rem; line-height:1.5; font-weight:600; color:#48607C; }
.exec-listen{ grid-column:1 / -1; background:#F5F9FF; border:1px solid #DFEAFA; border-radius:11px;
  padding:10px 13px; margin-top:2px; }
.exec-listen .exec-label{ color:#1E63D8; }
.exec-listen .exec-value{ color:#3D5675; }

@media(max-width:1180px){
  .hero{ grid-template-columns:1fr; } .hero-art{ display:none; }
  .hero-right{ padding:0 46px 34px; flex-direction:row; flex-wrap:wrap; }
  .campaign-grid{ grid-template-columns:repeat(2,1fr); }
  .signal-grid,.roster-grid{ grid-template-columns:repeat(2,1fr); }
  .detail-hero{ grid-template-columns:1fr; }
  .exec-grid{ grid-template-columns:1fr; }
  .phase-strip{ grid-template-columns:repeat(2,1fr); }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# =============================================================================
# HELPERS
# =============================================================================
def esc(v):
    return html.escape(str(v))


def phase_meta(phase):
    return next(x for x in PHASES if x[0] == phase)


def get_subthemes(campaign):
    rows = SUBTHEMES.get(campaign["name"], [])
    items = [{"name": n, "start": s, "end": e, "phase": p} for n, s, e, p in rows]
    return sorted(items, key=lambda x: (x["start"], -(x["end"] - x["start"]), x["name"]))


def timing_label(t):
    if t["start"] <= 2 and t["end"] == 24:
        return "Always-on from Day 1"
    if t["end"] == 24:
        return "Always-on"
    if (t["end"] - t["start"] + 1) <= 4:
        return "Seasonal burst"
    if (t["end"] - t["start"] + 1) >= 12:
        return "Sustained stream"
    if t["start"] <= 6:
        return "Launch focus"
    return "Core stream"


def exec_detail(campaign_name, theme_name):
    d = SUBTHEME_DETAILS.get(campaign_name, {}).get(theme_name)
    if d:
        return {"platforms": d[0], "format": d[1], "partners": d[2],
                "content": d[3], "listening": d[4], "kpi": d[5]}
    return {"platforms": "Integrated campaign channels", "format": "Multi-format",
            "partners": "Campaign partners", "content": "Content adapted to campaign objective",
            "listening": "—", "kpi": "—"}


# =============================================================================
# HERO
# =============================================================================
def render_hero():
    st.markdown(f'''
    <div class="hero">
      <div class="hero-left">
        <div class="hero-kicker">BENZAC BY GALDERMA &nbsp;•&nbsp; PROMOTION ARCHITECTURE</div>
        <h1>24-Month Integrated<br>Promotion Engine</h1>
        <p>A connected growth system that moves teens, parents and dermatologists from
        first-pimple discovery to long-term skincare habit.</p>
        <div class="hero-badges">
          <div class="hero-badge">TEENS 13–18</div>
          <div class="hero-badge">PARENTS</div>
          <div class="hero-badge">DERMATOLOGISTS</div>
          <div class="hero-badge">APP LIVE FROM DAY 1</div>
        </div>
      </div>
      <div class="hero-right">
        <img class="hero-art" src="{ART_HERO}" alt=""/>
        <div class="hero-stat"><b>24</b><span>Months mapped</span></div>
        <div class="hero-stat"><b>5</b><span>Campaign tracks</span></div>
        <div class="hero-stat"><b>4</b><span>Lifecycle phases</span></div>
      </div>
    </div>
    ''', unsafe_allow_html=True)


def banner(title, sub, art):
    st.markdown(
        f'<div class="banner"><div><h3>{esc(title)}</h3><p>{esc(sub)}</p></div>'
        f'<img src="{art}" alt=""/></div>',
        unsafe_allow_html=True,
    )


# =============================================================================
# TAB 1 — OVERVIEW
# =============================================================================
def render_overview():
    banner("The promotion journey, at a glance.",
           "One integrated engine. Five campaign tracks running in parallel, each with independently "
           "timed sub-themes entering and extending at different moments.",
           TAB_ART["overview"])

    journey = ""
    for i, (name, s, e, color, pale, desc) in enumerate(PHASES, start=1):
        journey += (
            f'<div class="journey-step"><div class="journey-num">PHASE {i} • M{s}–M{e}</div>'
            f'<div class="journey-name">{name}</div><div class="journey-desc">{desc}</div>'
            f'<div class="journey-accent" style="background:{color}"></div></div>'
        )
    st.markdown(f'<div class="journey">{journey}</div>', unsafe_allow_html=True)

    st.markdown('''<div class="metric-strip">
      <div class="metric"><b>3</b><span>Priority audiences</span></div>
      <div class="metric"><b>5</b><span>Connected tracks</span></div>
      <div class="metric"><b>48</b><span>Execution streams</span></div>
      <div class="metric"><b>24</b><span>Months mapped</span></div>
    </div>''', unsafe_allow_html=True)

    st.markdown('<div class="section-title">What the conversation is telling us</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Six signals from public digital listening that this plan is built to answer.</div>',
                unsafe_allow_html=True)
    sig = ""
    for headline, obs, act in SIGNALS:
        sig += (f'<div class="signal"><b>{esc(headline)}</b><div class="obs">{esc(obs)}</div>'
                f'<div class="act">→ {esc(act)}</div></div>')
    st.markdown(f'<div class="signal-grid">{sig}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Campaign portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Each track has its own audience, strategic job and independently timed sub-themes.</div>',
                unsafe_allow_html=True)

    cards = ""
    for c in CAMPAIGN_DATA:
        chips = ""
        for p, _, _, col, pale, _ in PHASES:
            chips += f'<span class="mini-chip" style="background:{pale};color:{col}">{p}</span>'
        cards += f'''
        <div class="campaign-card">
          <div class="campaign-art"><img src="{c['art']}" alt=""/><div class="tag">{esc(c['months'])}</div></div>
          <div class="campaign-body">
            <div class="campaign-name">{esc(c['name'])}</div>
            <div class="campaign-aud">◉ {esc(c['audience'])}</div>
            <div class="campaign-goal">{esc(c['goal'])}</div>
            <div>{chips}</div>
          </div>
        </div>'''
    st.markdown(f'<div class="campaign-grid">{cards}</div>', unsafe_allow_html=True)
    st.caption("Open **Campaign Details** to inspect platforms, partner voices, content and the listening insight behind every stream.")


# =============================================================================
# TAB 2 — CALENDAR
# =============================================================================
def render_calendar():
    banner("Integrated campaign calendar",
           "Which campaign runs when. Months across, tracks down — every sub-theme has its own bar and "
           "duration, and the plan is timed to the Indian school, exam and festival calendar.",
           TAB_ART["calendar"])

    strip = ""
    for name, s, e, color, pale, desc in PHASES:
        strip += (f'<div class="phase-brief" style="background:linear-gradient(125deg,{color},{color}dd)">'
                  f'<small>M{s}–M{e}</small><b>{name}</b><p>{esc(desc)}</p></div>')
    st.markdown(f'<div class="phase-strip">{strip}</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-hint">FILTER THE VIEW</div>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        chosen = st.pills(
            "Show campaign tracks",
            [c["name"] for c in CAMPAIGN_DATA],
            selection_mode="multi",
            default=[c["name"] for c in CAMPAIGN_DATA],
            key="track_filter",
        ) or [c["name"] for c in CAMPAIGN_DATA]
    with col2:
        year = st.radio("Time window", ["Full 24 months", "Year 1", "Year 2"],
                        horizontal=False, key="year_window")

    lo, hi = (1, 24)
    if year == "Year 1":
        lo, hi = 1, 12
    elif year == "Year 2":
        lo, hi = 13, 24
    n_cols = hi - lo + 1

    def clamp(v):
        return min(max(v, lo), hi) - lo + 1

    grid = f"250px repeat({n_cols},minmax(40px,1fr))"

    board = ['<div class="calendar-shell"><div class="calendar-board" style="min-width:%dpx">' % (250 + n_cols * 44)]

    # phase header
    board.append(f'<div class="cal-head" style="grid-template-columns:{grid}">'
                 f'<div class="cal-head-label">CAMPAIGN TRACK &amp; AUDIENCE</div>')
    for name, s, e, color, pale, _ in PHASES:
        span = max(0, min(e, hi) - max(s, lo) + 1)
        if span > 0:
            board.append(f'<div class="cal-phase" style="grid-column:span {span};background:{color}">'
                         f'{name}<small>M{s}–M{e}</small></div>')
    board.append("</div>")

    # month header
    board.append(f'<div class="month-row" style="grid-template-columns:{grid}">'
                 f'<div class="month-label" style="align-items:flex-start;padding-left:16px">MONTH</div>')
    for i in range(lo - 1, hi):
        mon, yr = MONTH_LABELS[i]
        board.append(f'<div class="month-label">{mon}<span>{yr} · M{i+1}</span></div>')
    board.append("</div>")

    # season markers
    board.append(f'<div class="season-row" style="grid-template-columns:{grid}">'
                 f'<div class="season-label">KEY INDIAN MOMENTS</div>')
    for s, e, label in SEASON_MARKERS:
        if e < lo or s > hi:
            continue
        cs, ce = clamp(s), clamp(e)
        board.append(f'<div class="season-chip" style="grid-column:{cs} / span {ce - cs + 1}">{esc(label)}</div>')
    board.append("</div>")

    for c in CAMPAIGN_DATA:
        if c["name"] not in chosen:
            continue
        cls = PHASE_CLASS[c["ruler_phase"]]
        color = phase_meta(c["ruler_phase"])[3]
        themes = [t for t in get_subthemes(c) if t["end"] >= lo and t["start"] <= hi]
        board.append('<div class="campaign-group" style="grid-template-columns:250px 1fr">')
        board.append(f'<div class="group-label"><div class="group-name">{esc(c["name"])}</div>'
                     f'<div class="group-aud">◉ {esc(c["audience"])}</div>'
                     f'<div class="group-meta" style="color:{color}">{esc(c["months"])} • {len(themes)} STREAMS</div></div>')
        board.append(f'<div class="group-track" style="background-size:calc(100%/{n_cols}) 100%">')
        for t in themes:
            cs, ce = clamp(t["start"]), clamp(t["end"])
            board.append(f'<div class="subtheme-row" style="grid-template-columns:repeat({n_cols},minmax(40px,1fr))">')
            board.append(f'<div class="subtheme-bar bar-{cls}" style="grid-column:{cs} / span {ce - cs + 1}" '
                         f'title="{esc(t["name"])} • M{t["start"]}–M{t["end"]}">{esc(t["name"])}</div>')
            board.append("</div>")
        board.append("</div></div>")

    board.append("</div>")
    board.append(f'''<div class="legend">
      <div class="legend-item"><span class="legend-dot" style="background:{SKY}"></span>Discovery &amp; trial track</div>
      <div class="legend-item"><span class="legend-dot" style="background:{BLUE}"></span>Trust-building tracks</div>
      <div class="legend-item"><span class="legend-dot" style="background:{VIOLET}"></span>Preference track</div>
      <div class="legend-item"><span class="legend-dot" style="background:{NAVY}"></span>Habit track</div>
    </div></div>''')
    st.markdown("".join(board), unsafe_allow_html=True)
    st.caption("Bar colour shows the strategic home of the track, so a discovery stream can legitimately continue into later phases. "
               "The Benzac app runs from M1 — trial and routine are recruited together, not six months apart.")

    st.markdown('<div class="section-title">Sequencing logic — why this order</div>', unsafe_allow_html=True)
    seq = pd.DataFrame([
        {"Window": "M1 – M2", "In market": "First Pimple, Routine Lock, Benzac app",
         "Why now": "App is live from day one, so trial and week-one guidance launch together."},
        {"Window": "M3 – M6", "In market": "+ Parent Confidence, Campus Sessions",
         "Why now": "Post-board reset window (Mar–Jun) — teens have time to build a habit; parents are deciding."},
        {"Window": "M4 – M6", "In market": "+ Derm Board",
         "Why now": "Derm advocacy enters once there is real product experience to discuss."},
        {"Window": "M7 – M12", "In market": "All five tracks, trust-weighted",
         "Why now": "Evidence, expert access and parent reassurance carry the phase."},
        {"Window": "M9 – M11", "In market": "Festival & Function Ready burst",
         "Why now": "Wedding and festival season is the sharpest event-panic window in India."},
        {"Window": "M13 – M18", "In market": "Preference-weighted: real stories, campus, marks",
         "Why now": "Enough users have results to make social proof the lead argument."},
        {"Window": "M19 – M24", "In market": "Habit-weighted: ClearStreak, refills, maintenance",
         "Why now": "Repeat purchase and post-clearance retention become the growth lever."},
    ])
    st.dataframe(seq, use_container_width=True, hide_index=True)


# =============================================================================
# TAB 3 — DETAILS
# =============================================================================
def render_details():
    banner("Campaign detail explorer",
           "Pick a track to see its streams, exact timing, platforms, partner voices, content and the "
           "listening insight each one answers.",
           TAB_ART["details"])

    st.markdown('<div class="picker-card"><div class="plabel">▼ &nbsp;PICK A CAMPAIGN TRACK</div>'
                '<p class="phint">Choose one of the five tracks to load its full execution detail below.</p></div>',
                unsafe_allow_html=True)
    selected = st.selectbox("Campaign track", [c["name"] for c in CAMPAIGN_DATA], label_visibility="collapsed")

    c = next(x for x in CAMPAIGN_DATA if x["name"] == selected)
    color = phase_meta(c["ruler_phase"])[3]
    cls = PHASE_CLASS[c["ruler_phase"]]
    themes = get_subthemes(c)

    stats = "".join(
        f'<div class="detail-stat"><b>{esc(m)}</b><span>Target metric</span></div>' for m in c["metrics"]
    )
    st.markdown(f'''
    <div class="detail-hero">
      <div class="detail-main">
        <div class="detail-kicker" style="color:{color}">{c["ruler_phase"]} &nbsp;•&nbsp; {esc(c["months"])} &nbsp;•&nbsp; {esc(c["audience"])}</div>
        <h2>{esc(c["name"])}</h2>
        <p>{esc(c["goal"])}</p>
        <div class="insight-band"><b>WHAT THE LISTENING SAYS</b><span>{esc(c["listening"])}</span></div>
        <div class="detail-stat-grid">{stats}</div>
      </div>
      <div class="detail-art"><img src="{c['art']}" alt=""/></div>
    </div>''', unsafe_allow_html=True)

    left, right = st.columns([1, 1])
    with left:
        st.markdown('<div class="section-title" style="font-size:1.15rem;margin-top:6px">Channel mix</div>',
                    unsafe_allow_html=True)
        rows = ""
        for label, val in CHANNEL_MIX[c["name"]]:
            rows += (f'<div class="mix-row"><div class="mix-name">{esc(label)}</div>'
                     f'<div class="mix-track"><div class="mix-fill" style="width:{val * 2.6}%"></div></div>'
                     f'<div class="mix-val">{val}%</div></div>')
        st.markdown(f'<div class="mix-card">{rows}</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="section-title" style="font-size:1.15rem;margin-top:6px">Partner & voice roster</div>',
                    unsafe_allow_html=True)
        r = PARTNER_ROSTER[c["name"]]
        cards = "".join(
            f'<div class="roster"><b>{esc(k.upper())}</b><span>{esc(v)}</span></div>' for k, v in r.items()
        )
        st.markdown(f'<div class="roster-grid" style="grid-template-columns:repeat(2,1fr)">{cards}</div>',
                    unsafe_allow_html=True)
        st.caption("Proposed target list for planning purposes — not confirmed partnerships.")

    st.markdown('<div class="section-title">Sub-theme timeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">The track stays active throughout; each bar is the independent duration of one execution stream.</div>',
                unsafe_allow_html=True)
    tl = ['<div class="detail-theme-table"><div class="detail-theme-grid"><div class="detail-theme-months">'
          '<div class="detail-theme-month"></div>']
    for mon, yr in MONTH_LABELS:
        tl.append(f'<div class="detail-theme-month">{mon}<br>{yr}</div>')
    tl.append("</div>")
    for t in themes:
        span = t["end"] - t["start"] + 1
        tl.append('<div class="detail-theme-row">')
        tl.append(f'<div class="detail-theme-name">{esc(t["name"])}</div>')
        tl.append(f'<div class="detail-subtheme-bar bar-{cls}" style="grid-column:{t["start"] + 1} / span {span}">'
                  f'M{t["start"]}–M{t["end"]}</div>')
        tl.append("</div>")
    tl.append("</div></div>")
    st.markdown("".join(tl), unsafe_allow_html=True)

    st.markdown('<div class="section-title">Sub-theme execution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Where each stream shows up, in what format, who delivers it, what it says — and the consumer signal behind it.</div>',
                unsafe_allow_html=True)

    cards = ['<div class="exec-grid">']
    for t in themes:
        m = exec_detail(c["name"], t["name"])
        cards.append(
            f'<div class="exec-card" style="border-top:4px solid {color}">'
            f'<div class="exec-top"><div>'
            f'<div class="exec-name">{esc(t["name"])}</div>'
            f'<div class="exec-when">M{t["start"]}–M{t["end"]} &nbsp;·&nbsp; {esc(t["phase"].title())} stream</div>'
            f'</div><div class="exec-status">{esc(timing_label(t))}</div></div>'
            f'<div class="exec-meta">'
            f'<div class="exec-block"><div class="exec-label">PLATFORMS</div><div class="exec-value">{esc(m["platforms"])}</div></div>'
            f'<div class="exec-block"><div class="exec-label">FORMAT</div><div class="exec-value">{esc(m["format"])}</div></div>'
            f'<div class="exec-block"><div class="exec-label">PARTNERS / VOICES</div><div class="exec-value">{esc(m["partners"])}</div></div>'
            f'<div class="exec-block"><div class="exec-label">SUCCESS MEASURE</div><div class="exec-value">{esc(m["kpi"])}</div></div>'
            f'<div class="exec-block full"><div class="exec-label">CONTENT</div><div class="exec-value">{esc(m["content"])}</div></div>'
            f'<div class="exec-listen"><div class="exec-label">LISTENING INSIGHT</div><div class="exec-value">{esc(m["listening"])}</div></div>'
            f"</div></div>"
        )
    cards.append("</div>")
    st.markdown("".join(cards), unsafe_allow_html=True)

    with st.expander("Export this track as a table"):
        df = pd.DataFrame([{
            "Sub-theme": t["name"],
            "Months": f'M{t["start"]}–M{t["end"]}',
            "Phase": t["phase"],
            "Platforms": exec_detail(c["name"], t["name"])["platforms"],
            "Partners / voices": exec_detail(c["name"], t["name"])["partners"],
            "Content": exec_detail(c["name"], t["name"])["content"],
            "Listening insight": exec_detail(c["name"], t["name"])["listening"],
            "Success measure": exec_detail(c["name"], t["name"])["kpi"],
        } for t in themes])
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("Download CSV", df.to_csv(index=False).encode(),
                           file_name=f"{c['id']}_{c['short'].lower().replace(' ', '_')}.csv",
                           mime="text/csv")


# =============================================================================
# APP
# =============================================================================
render_hero()

st.markdown('<div class="nav-hint">SELECT A VIEW</div>', unsafe_allow_html=True)
tab = st.segmented_control(
    "Navigation",
    options=["✦  Overview", "▦  Campaign Calendar", "⌕  Campaign Details"],
    default="✦  Overview",
    label_visibility="collapsed",
    key="nav_view",
)

if tab == "▦  Campaign Calendar":
    render_calendar()
elif tab == "⌕  Campaign Details":
    render_details()
else:
    render_overview()
