
# ==========================================
# CODERED ORION - MY WORDS
# ==========================================

import streamlit as st
import requests


# ==========================================
# QUICK AAC COMMUNICATION BUTTONS
# ==========================================

QUICK_WORDS = {
    "Needs": [
        ("🥤 Water", "I need water."),
        ("🍎 Food", "I am hungry."),
        ("🆘 Help", "I need help."),
        ("🚻 Bathroom", "I need the bathroom."),
        ("⏸️ Break", "I need a break."),
        ("😴 Rest", "I need to rest.")
    ],
    "Feelings": [
        ("😊 Happy", "I feel happy."),
        ("😢 Sad", "I feel sad."),
        ("😠 Angry", "I feel angry."),
        ("😟 Worried", "I feel worried."),
        ("😴 Tired", "I feel tired."),
        ("😌 Calm", "I feel calm.")
    ],
    "Questions": [
        ("🙋 Help me?", "Can you help me?"),
        ("🔁 Repeat?", "Can you repeat that?"),
        ("❓ What?", "What does that mean?"),
        ("📍 Where?", "Where are we going?")
    ],
    "Social": [
        ("👋 Hello", "Hello!"),
        ("👋 Goodbye", "Goodbye!"),
        ("🙏 Please", "Please."),
        ("💛 Thank you", "Thank you."),
        ("✅ Yes", "Yes."),
        ("❌ No", "No.")
    ]
}


# ==========================================
# SESSION STATE
# ==========================================

def initialize_my_words():
    """
    Initialize session state values.
    """

    if "my_words_text" not in st.session_state:
        st.session_state.my_words_text = ""

    if "my_words_suggestions" not in st.session_state:
        st.session_state.my_words_suggestions = []

    if "my_words_audio" not in st.session_state:
        st.session_state.my_words_audio = None

    if "my_words_suggestion_source" not in st.session_state:
        st.session_state.my_words_suggestion_source = ""

    if "my_words_audio_source" not in st.session_state:
        st.session_state.my_words_audio_source = ""


# ==========================================
# MESSAGE MANAGEMENT
# ==========================================

def update_my_words(message):
    """
    Replace the message.

    Called through Streamlit callbacks so the
    text area can be updated safely.
    """

    st.session_state.my_words_text = message[:500]

    st.session_state.my_words_suggestions = []
    st.session_state.my_words_suggestion_source = ""

    st.session_state.my_words_audio = None
    st.session_state.my_words_audio_source = ""


def clear_my_words():
    """
    Clear the entire message.
    """
    update_my_words("")


def delete_last_word():
    """
    Remove the last word from the message.
    """

    text = st.session_state.my_words_text.strip()

    words = text.split()

    new_message = " ".join(words[:-1])

    update_my_words(new_message)


def on_message_changed():
    """
    Clear outdated predictions and speech
    whenever the user edits the text area.
    """

    st.session_state.my_words_suggestions = []
    st.session_state.my_words_suggestion_source = ""

    st.session_state.my_words_audio = None
    st.session_state.my_words_audio_source = ""


# ==========================================
# MAIN MY WORDS UI
# ==========================================

def render_my_words(get_suggestions, speak_message):

    initialize_my_words()

    # ======================================
    # PAGE HEADER
    # ======================================

    st.markdown(
        '<h2 style="text-align:center">My Words</h2>',
        unsafe_allow_html=True
    )

    st.caption(
        "Build your message by typing or selecting "
        "communication cards."
    )

    # ======================================
    # MESSAGE EDITOR
    # ======================================

    st.subheader("Your message")

    st.text_area(
        "Type or edit your message",
        key="my_words_text",
        height=130,
        max_chars=500,
        placeholder=(
            "Type here or select a communication card..."
        ),
        on_change=on_message_changed
    )

    current_text = st.session_state.my_words_text.strip()

    # ======================================
    # GEMINI PREDICTIVE TEXT
    # ======================================

    st.subheader("✨ Predictive text")

    st.caption(
        "Gemini can suggest up to three phrases "
        "based on your current message."
    )

    if st.button(
        "✨ Suggest phrases",
        key="my_words_predict",
        use_container_width=True,
        disabled=not bool(current_text)
    ):

        try:

            with st.spinner("Generating suggestions..."):

                suggestions = get_suggestions(
                    current_text
                )

            st.session_state.my_words_suggestions = (
                suggestions
            )

            st.session_state.my_words_suggestion_source = (
                current_text
            )

        except requests.exceptions.RequestException as error:

            st.session_state.my_words_suggestions = []

            st.error(
                f"Unable to get suggestions: {error}"
            )

    # ======================================
    # DISPLAY GEMINI SUGGESTIONS
    # ======================================

    if st.session_state.my_words_suggestions:

        st.write("Choose a suggestion:")

        for index, suggestion in enumerate(
            st.session_state.my_words_suggestions
        ):

            # IMPORTANT:
            # on_click runs BEFORE Streamlit
            # creates the text area on the next run.

            st.button(
                suggestion,
                key=f"my_words_suggestion_{index}",
                use_container_width=True,
                on_click=update_my_words,
                args=(suggestion,)
            )

    elif (
        st.session_state.my_words_suggestion_source
        == current_text
        and current_text
    ):

        st.info(
            "No suggestions available for this message."
        )

    # ======================================
    # ELEVENLABS TEXT TO SPEECH
    # ======================================

    st.divider()

    st.subheader("🔊 Speak your message")

    if st.button(
        "🔊 Speak",
        key="my_words_speak",
        use_container_width=True,
        disabled=not bool(current_text)
    ):

        try:

            with st.spinner("Generating speech..."):

                audio = speak_message(
                    current_text
                )

            st.session_state.my_words_audio = audio

            st.session_state.my_words_audio_source = (
                current_text
            )

        except requests.exceptions.RequestException as error:

            st.session_state.my_words_audio = None
            st.session_state.my_words_audio_source = ""

            st.error(
                f"Unable to generate speech: {error}"
            )

    # ======================================
    # AUDIO PLAYER
    # ======================================

    if (
        st.session_state.my_words_audio is not None
        and st.session_state.my_words_audio_source
        == current_text
    ):

        st.audio(
            st.session_state.my_words_audio,
            format="audio/mpeg",
            autoplay=True
        )

    # ======================================
    # MESSAGE CONTROLS
    # ======================================

    st.divider()

    left, right = st.columns(2)

    with left:

        st.button(
            "⌫ Delete last word",
            key="my_words_backspace",
            use_container_width=True,
            disabled=not bool(current_text),
            on_click=delete_last_word
        )

    with right:

        st.button(
            "🗑 Clear message",
            key="my_words_clear",
            use_container_width=True,
            disabled=not bool(current_text),
            on_click=clear_my_words
        )

    # ======================================
    # AAC QUICK COMMUNICATION
    # ======================================

    st.divider()

    st.subheader("💬 Quick communication")

    st.caption(
        "Use these buttons to communicate "
        "without typing."
    )

    for category, phrases in QUICK_WORDS.items():

        with st.expander(
            category,
            expanded=(category == "Needs")
        ):

            for i in range(0, len(phrases), 2):

                columns = st.columns(
                    2,
                    gap="small"
                )

                for column, (label, phrase) in zip(
                    columns,
                    phrases[i:i + 2]
                ):

                    with column:

                        # IMPORTANT:
                        # Callback updates the message
                        # before the text area is created.

                        st.button(
                            label,
                            key=(
                                f"my_words_"
                                f"{category}_{i}_{label}"
                            ),
                            use_container_width=True,
                            on_click=update_my_words,
                            args=(phrase,)
                        )


# ==========================================
# END OF MY WORDS UI
# ==========================================
