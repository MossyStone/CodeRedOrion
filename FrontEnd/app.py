import html
from urllib.parse import quote
import streamlit as st

#Connecting FRont to back end
import os
import requests

from games.matchItUI import render_match_it

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

def get_match_it_rounds():
    response = requests.get(
        f"{API_BASE_URL}/practice/match-it",
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def check_match_it_answer(round_id, selected_option):
    response = requests.post(
        f"{API_BASE_URL}/practice/match-it/check",
        json={
            "round_id": round_id,
            "selected_option": selected_option
        },
        timeout=10
    )
    response.raise_for_status()
    return response.json()
#end of connecting front to back end


st.set_page_config(page_title="CodeRed Orion", page_icon="💬", layout="wide", initial_sidebar_state="collapsed")

CATEGORIES = {
    "Feelings": [("😊 Happy", "I feel happy."), ("😢 Sad", "I feel sad."), ("😠 Angry", "I feel angry."), ("😟 Worried", "I feel worried."), ("🤩 Excited", "I feel excited."), ("😌 Calm", "I feel calm."), ("😣 Uncomfortable", "I feel uncomfortable."), ("😴 Tired", "I feel tired.")],
    "Needs": [("🆘 Help", "I need help."), ("🥤 Water", "I need water."), ("🍎 Food", "I am hungry."), ("🚻 Bathroom", "I need the bathroom."), ("⏸️ Break", "I need a break."), ("🤫 Quiet", "I need some quiet."), ("🩹 Pain", "I am in pain."), ("❤️ Comfort", "I need comfort.")],
    "Questions": [("🙋 Help me?", "Can you help me?"), ("🔁 Repeat?", "Can you repeat that?"), ("❓ What does that mean?", "What does that mean?"), ("📍 Where are we going?", "Where are we going?"), ("🗓️ What's next?", "What are we doing next?"), ("💬 Can I ask?", "Can I ask a question?")],
    "Social": [("👋 Hello", "Hello!"), ("👋 Goodbye", "Goodbye!"), ("🙏 Please", "Please."), ("💛 Thank you", "Thank you."), ("✅ Yes", "Yes."), ("❌ No", "No."), ("💬 Let's talk", "I want to talk."), ("🔁 Say it again", "Please say that again.")],
}

if "message" not in st.session_state:
    st.session_state.message = ""

page = st.query_params.get("page", "talk")
category = st.query_params.get("category", "Feelings")
game = st.query_params.get("game", "say-it")
if page not in ("talk", "practice", "words"):
    page = "talk"
if category not in CATEGORIES:
    category = "Feelings"
if game not in ("say-it", "match-it"):
    game = "say-it"

def nav_link(label, target, active=False):
    return f'<a class="menu-link{" active" if active else ""}" href="{html.escape(target, quote=True)}" target="_self">{html.escape(label)}</a>'

def url(**params):
    return "?" + "&".join(f"{quote(str(k))}={quote(str(v))}" for k, v in params.items())

st.markdown("""
<style>
.stApp {background:#0b0b10;color:#f7f7fa;}
.block-container {max-width:1050px;padding-top:0;padding-bottom:3rem;}
/* Header background fills the entire viewport, content stays centered. */
.orion-header {position:relative;isolation:isolate;padding:clamp(20px,4vw,38px) 0 0;margin-bottom:clamp(24px,4vw,40px);}
.orion-header::before {content:"";position:absolute;inset:0 auto 0 50%;width:100vw;transform:translateX(-50%);background:#2110a6;z-index:-1;}
.orion-header h1 {font-size:clamp(2rem,5vw,3.2rem);text-align:center;color:white;margin:0;}
.orion-header .tagline {text-align:center;color:#e4dfff;margin:6px 0 20px;}
.orion-nav {display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:0;}
.orion-menu {position:relative;min-width:0;}
.orion-trigger {display:flex;align-items:center;justify-content:center;width:100%;min-height:clamp(64px,8vw,82px);padding:12px 5px;background:transparent;border:0;color:#fff;font-size:clamp(1.05rem,2.5vw,1.6rem);font-weight:700;text-decoration:none;cursor:pointer;}
.orion-trigger:hover,.orion-trigger:focus-visible,.orion-menu:focus-within>.orion-trigger {background:#3827b7;color:#fff;}
.orion-trigger.current {background:#3220b5;border-bottom:5px solid #ffd166;}
.orion-dropdown {display:none;position:absolute;left:0;top:100%;width:max(100%,220px);max-width:min(350px,90vw);z-index:9999;background:#20202b;border:2px solid #8d88cb;border-radius:0 0 12px 12px;box-shadow:0 12px 28px #0009;padding:8px;}
.orion-menu:hover>.orion-dropdown,.orion-menu:focus-within>.orion-dropdown {display:block;}
.orion-dropdown .menu-link {display:block;padding:12px 12px;color:#fff;text-decoration:none;border-radius:8px;font-size:1rem;}
.orion-dropdown .menu-link:hover,.orion-dropdown .menu-link:focus-visible,.orion-dropdown .menu-link.active {background:#4034a8;color:white;}
.orion-trigger:focus-visible,.menu-link:focus-visible,.stButton button:focus-visible {outline:4px solid #ffd166;outline-offset:2px;}
/* Keep header and dropdown above all page content */
.orion-header {z-index:100;}
/* Large, responsive communication cards */
.st-key-phrase_area .stButton button,.st-key-practice_area .stButton button {width:100%;min-height:clamp(85px,12vw,130px);white-space:normal;font-size:clamp(1.1rem,2.3vw,1.5rem);font-weight:650;color:white;background:#1b1c26;border:2px solid #85899c;border-radius:16px;}
.st-key-phrase_area .stButton button:hover,.st-key-practice_area .stButton button:hover {background:#2a2d3a;border-color:#ffd166;color:white;}
.st-key-message_box {background:#1b1c26;border:2px solid #85899c;border-radius:16px;padding:clamp(14px,3vw,25px);}
.st-key-message_box p {font-size:clamp(1.25rem,3vw,2rem);line-height:1.5;}
@media(max-width:600px){.block-container{padding-left:.7rem;padding-right:.7rem;}.orion-dropdown{width:min(280px,90vw);}.orion-menu:nth-child(2) .orion-dropdown{left:auto;right:0;}}
</style>
""", unsafe_allow_html=True)

# Pure HTML links navigate through Streamlit's URL query parameters.
# Hover works with CSS; click/tap and keyboard focus work without JavaScript.
header = f'''<header class="orion-header">
<h1>CodeRed Orion</h1><p class="tagline">Communication at your own pace</p>
<nav class="orion-nav" aria-label="Main navigation">
  <div class="orion-menu">
    <a class="orion-trigger{' current' if page == 'practice' else ''}" target="_self" href="{url(page='practice',game='say-it')}">Practice ▾</a>
    <div class="orion-dropdown">
      {nav_link('🎤 Say It!', url(page='practice',game='say-it'), page == 'practice' and game == 'say-it')}
      {nav_link('🧩 Match It!', url(page='practice',game='match-it'), page == 'practice' and game == 'match-it')}
    </div>
  </div>
  <div class="orion-menu">
    <a class="orion-trigger{' current' if page == 'talk' else ''}" target="_self" href="{url(page='talk',category='Feelings')}">Talk ▾</a>
    <div class="orion-dropdown">
      {''.join(nav_link(name, url(page='talk',category=name), page == 'talk' and category == name) for name in CATEGORIES)}
    </div>
  </div>
  <div class="orion-menu">
    <a class="orion-trigger{' current' if page == 'words' else ''}" target="_self" href="{url(page='words')}">My Words</a>
  </div>
</nav></header>'''
st.markdown(header, unsafe_allow_html=True)

if page == "talk":
    st.markdown(f'<h2 style="text-align:center;font-size:clamp(2.2rem,5vw,3.4rem);margin:1.5rem 0">{html.escape(category)}</h2>', unsafe_allow_html=True)
    st.caption("Choose a phrase. Selecting another phrase replaces your message.")
    with st.container(key="phrase_area"):
        options = CATEGORIES[category]
        for i in range(0, len(options), 2):
            columns = st.columns(2, gap="small")
            for column, (label, message) in zip(columns, options[i:i+2]):
                with column:
                    if st.button(label, key=f"{category}_{i}_{label}", use_container_width=True):
                        st.session_state.message = message
                        st.rerun()

elif page == "practice":
    if game == "match-it":
        try:
            data = get_match_it_rounds()

            render_match_it(
                data["rounds"],
                check_match_it_answer
            )

        except requests.exceptions.RequestException as error:
            st.error(f"Unable to load Match It!: {error}")

    else:
        st.markdown(
            '<h2 style="text-align:center">🎤 Say It!</h2>',
            unsafe_allow_html=True
        )
        st.info("Say It! is coming next.")
else:
    st.markdown('<h2 style="text-align:center">My Words</h2>', unsafe_allow_html=True)
    st.write("Type your own message to communicate.")
    custom = st.text_area("What would you like to say?", placeholder="Type your message here...", height=140)
    if st.button("Use my message", type="primary", disabled=not custom.strip()):
        st.session_state.message = custom.strip()
        st.rerun()

# Display the message panel only after a message has been selected or written.
# The message persists when switching between Talk and My Words.
if page in ("talk", "words") and st.session_state.message:
    st.divider()
    st.subheader("Your message")
    with st.container(key="message_box"):
        st.write(st.session_state.message)

    # Streamlit's code widget includes a native copy-to-clipboard control.
    st.caption("Copy your message using the copy icon below:")
    st.code(st.session_state.message, language=None)

    if st.button("🗑 Clear message", use_container_width=True):
        st.session_state.message = ""
        st.rerun()
