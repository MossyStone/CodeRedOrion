import streamlit as st
import html

st.set_page_config(
    page_title="CodeRed Orion — Communication",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Focused, high-contrast communication interface
st.markdown(
    
    <style>
    :root {
        color-scheme: dark;
    }
    .stApp {
        background: #000000;
        color: #f1f1f1;
    }
    .block-container {
        max-width: 1050px;
        padding-top: 1.25rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, p, label, div {
        color: #eeeeee;
    }
    h1 {
        font-size: 1.45rem !important;
        font-weight: 650 !important;
        letter-spacing: -0.02em;
    }
    .subtitle {
        color: #c8c8c8;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0.2rem 0 1rem 0;
    }
    .concept-pill {
        display: inline-block;
        background: #1b1b1b;
        border-radius: 999px;
        padding: 0.25rem 0.65rem;
        font-size: 0.85rem;
        color: #eeeeee;
    }
    .stButton > button {
        width: 100%;
        min-height: 74px;
        white-space: normal;
        font-size: 1.15rem !important;
        font-weight: 450 !important;
        color: #eeeeee !important;
        background: #000000 !important;
        border: 1px solid #343434 !important;
        border-radius: 13px !important;
        padding: 0.8rem 1rem !important;
        transition: background 0.15s ease, border-color 0.15s ease;
    }
    .stButton > button:hover {
        border-color: #858585 !important;
        background: #171717 !important;
    }
    .stButton > button:focus-visible {
        outline: 4px solid #f0a202 !important;
        outline-offset: 3px !important;
    }
    div[role="radiogroup"] {
        gap: 0.6rem;
    }
    div[role="radiogroup"] label {
        border: 1px solid #373737;
        border-radius: 999px;
        padding: 0.55rem 0.85rem;
        min-height: 44px;
        background: #000000;
        justify-content: center;
    }
    div[role="radiogroup"] label p {
        font-size: 1rem !important;
    }
    .selected-label {
        color: #c9c9c9;
        font-size: 0.95rem;
        margin-top: 0.6rem;
        margin-bottom: 0.5rem;
    }
    .selected-message {
        color: #eeeeee;
        font-size: 1.2rem;
        line-height: 1.6;
        min-height: 2.2rem;
        overflow-wrap: anywhere;
        padding: 0.1rem 0 0.8rem 0;
    }
    .top-rule {
        border: none;
        border-top: 1px solid #191919;
        margin: 1.2rem 0 1.4rem 0;
    }
    .stTextArea textarea, .stTextInput input {
        color: #eeeeee !important;
        background: #080808 !important;
        border-color: #444444 !important;
        font-size: 1.1rem !important;
    }
    [data-testid="stAlert"] {
        background: #161616;
    }
    </style>
    ,
    unsafe_allow_html=True,
)

# Message and undo history
if "message" not in st.session_state:
    st.session_state.message = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "custom_text" not in st.session_state:
    st.session_state.custom_text = ""
if "category" not in st.session_state:
    st.session_state.category = "💬 Questions"
if "copy_ready" not in st.session_state:
    st.session_state.copy_ready = False


def add_phrase(phrase: str):
    st.session_state.history.append(st.session_state.message)
    if st.session_state.message.strip():
        st.session_state.message += " "
    st.session_state.message += phrase
    st.session_state.copy_ready = False


def add_custom_phrase():
    phrase = st.session_state.custom_text.strip()
    if phrase:
        add_phrase(phrase)
        st.session_state.custom_text = ""


def undo_message():
    if st.session_state.history:
        st.session_state.message = st.session_state.history.pop()
    st.session_state.copy_ready = False


def clear_message():
    st.session_state.message = ""
    st.session_state.history.clear()
    st.session_state.copy_ready = False


phrases = {
    "❤️ I need": [
        "🆘  I need help.",
        "🍎  I am hungry.",
        "🥤  I am thirsty.",
        "🚻  I need the bathroom.",
        "😴  I am tired.",
        "🩹  I am in pain.",
        "⏸️  I need a break.",
        "🤫  I need some quiet.",
    ],
    "☺ I feel": [
        "😊  I am happy.",
        "😢  I am sad.",
        "😟  I am worried.",
        "😠  I am frustrated.",
        "🤩  I am excited.",
        "😣  I feel uncomfortable.",
        "😌  I feel calm.",
        "❤️  I need comfort.",
    ],
    "💬 Questions": [
        "Can you help me?",
        "Can you repeat that?",
        "Could you explain that again?",
        "What are we doing next?",
        "Where are we going?",
        "What does that mean?",
        "Can I ask a question?",
        "I do not understand.",
    ],
    "👥 Social": [
        "👋  Hello!",
        "👋  Goodbye!",
        "🙏  Please.",
        "💛  Thank you.",
        "✅  Yes.",
        "❌  No.",
        "🔁  Please say that again.",
        "💬  I want to talk.",
    ],
}

# Header
header_left, header_right = st.columns([5, 1])
with header_left:
    st.title("CodeRed Orion — Communication")
with header_right:
    st.markdown(
        '<div style="text-align:right;padding-top:0.2rem">'
        '<span class="concept-pill">Concept</span></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="subtitle">Select a category to see possible messages. '
    'These are examples of the interface, not AI predictions.</div>',
    unsafe_allow_html=True,
)

category = st.radio(
    "Message category",
    list(phrases.keys()),
    index=list(phrases.keys()).index(st.session_state.category),
    horizontal=True,
    label_visibility="collapsed",
    key="category",
)

st.markdown('<hr class="top-rule">', unsafe_allow_html=True)

# Two-column phrase grid
items = phrases[category]
for start in range(0, len(items), 2):
    cols = st.columns(2, gap="small")
    for offset, col in enumerate(cols):
        idx = start + offset
        if idx >= len(items):
            continue
        phrase = items[idx]
        # Display labels without decorative category icons where appropriate.
        with col:
            if st.button(
                phrase,
                key=f"phrase_{category}_{idx}",
                use_container_width=True,
            ):
                add_phrase(phrase)
                st.rerun()

st.markdown('<hr class="top-rule">', unsafe_allow_html=True)

st.markdown('<div class="selected-label">Selected message</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="selected-message">{html.escape(st.session_state.message) if st.session_state.message else " "}</div>',
    unsafe_allow_html=True,
)

# Message editing and action controls
with st.expander("Edit message or add your own words"):
    st.text_area(
        "Edit your message",
        key="message",
        height=110,
        placeholder="Select phrases above or type your message here.",
    )
    st.text_input(
        "Custom message",
        key="custom_text",
        placeholder="Type anything you want to say",
    )
    add_col, undo_col, clear_col = st.columns(3)
    with add_col:
        st.button("➕ Add text", on_click=add_custom_phrase, use_container_width=True)
    with undo_col:
        st.button("↩ Undo", on_click=undo_message, use_container_width=True)
    with clear_col:
        st.button("Clear", on_click=clear_message, use_container_width=True)

# Copy action: use Streamlit's native copy-friendly text display as a fallback
# plus an optional browser clipboard button via a small inline component.
copy_col, arrow_col = st.columns([5, 1])
with copy_col:
    if st.session_state.message:
        escaped_message = html.escape(st.session_state.message)
        st.components.v1.html(
            f
            <div style="display:flex;justify-content:flex-end;background:transparent;">
              <button id="copy-message" style="
                border:1px solid #e8e8e8;border-radius:999px;
                background:#ededed;color:#111;padding:11px 20px;
                font-size:16px;cursor:pointer;min-height:44px;">
                ▢ &nbsp; Copy message
              </button>
            </div>
            <script>
              const btn = document.getElementById('copy-message');
              btn.addEventListener('click', async () => {{
                try {{
                  await navigator.clipboard.writeText({st.session_state.message!r});
                  btn.textContent = '✓ Copied';
                }} catch (e) {{
                  btn.textContent = 'Select the message above to copy';
                }}
              }});
            </script>
            ,
            height=54,
        )
    else:
        st.caption("Choose a phrase to build your message.")
with arrow_col:
    if st.button("↓", help="Scroll to the message editing controls", use_container_width=True):
        st.session_state.show_editor = True
        st.rerun()

st.caption("Accessible communication at your own pace. You can use text instead of speech.")
