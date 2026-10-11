import streamlit as st


DEFAULT_EXERCISES = [
    {"emoji": "👋", "phrase": "Hello!", "hint": "A friendly greeting."},
    {"emoji": "💧", "phrase": "Water, please.", "hint": "Ask for a drink."},
    {"emoji": "🆘", "phrase": "I need help.", "hint": "Ask someone for support."},
    {"emoji": "🙏", "phrase": "Thank you.", "hint": "Show appreciation."},
    {"emoji": "⏸️", "phrase": "I need a break.", "hint": "Let someone know you need a pause."},
    {"emoji": "🔁", "phrase": "Please say that again.", "hint": "Ask someone to repeat something."},
    {"emoji": "🍎", "phrase": "I would like something to eat.", "hint": "Tell someone you're hungry."},
    {"emoji": "💬", "phrase": "I want to talk.", "hint": "Let someone know you want to communicate."},
]


def _init_state() -> None:
    defaults = {
        "sayit_exercises": DEFAULT_EXERCISES.copy(),
        "sayit_index": 0,
        "sayit_completed": set(),
        "sayit_skipped": set(),
        "sayit_feedback": None,
        "sayit_recording": None,
        "sayit_attempts": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _current_exercise() -> dict:
    exercises = st.session_state.sayit_exercises or DEFAULT_EXERCISES
    index = st.session_state.sayit_index % len(exercises)
    return exercises[index]


def _advance(*, completed: bool = False, skipped: bool = False) -> None:
    exercises = st.session_state.sayit_exercises or DEFAULT_EXERCISES
    current_index = st.session_state.sayit_index % len(exercises)

    if completed:
        st.session_state.sayit_completed.add(current_index)

    if skipped:
        st.session_state.sayit_skipped.add(current_index)

    st.session_state.sayit_index = (
        current_index + 1
    ) % len(exercises)

    st.session_state.sayit_feedback = None
    st.session_state.sayit_recording = None
    st.session_state.sayit_attempts = 0


def render_say_it_ui(exercises: list[dict] | None = None) -> None:
    """Render the Say It! interface inside a Streamlit app.

    Optional exercises can be passed as dictionaries containing:
    phrase, and optionally emoji and hint.
    """

    _init_state()

    if exercises:
        st.session_state.sayit_exercises = [
            {
                "emoji": item.get("emoji", "💬"),
                "phrase": item["phrase"],
                "hint": item.get(
                    "hint",
                    "Take your time and try when you're ready."
                ),
            }
            for item in exercises
            if item.get("phrase")
        ] or DEFAULT_EXERCISES

    items = st.session_state.sayit_exercises
    total = len(items)
    current_index = st.session_state.sayit_index % total
    exercise = _current_exercise()
    completed_count = len(st.session_state.sayit_completed)

    st.markdown(
        
        <style>
        .sayit-wrap {
            max-width: 980px;
            margin: 0 auto;
        }

        .sayit-eyebrow {
            color: #486581;
            font-size: 0.95rem;
            font-weight: 750;
            letter-spacing: .08em;
            text-transform: uppercase;
        }

        .sayit-intro {
            color: #486581;
            font-size: 1.08rem;
            line-height: 1.65;
        }

        .sayit-phrase-card {
            background: linear-gradient(
                135deg, #ffffff 0%, #f1f7ff 100%
            );
            border: 2px solid #c7d9ee;
            border-radius: 24px;
            padding: clamp(24px, 5vw, 48px) 22px;
            text-align: center;
            box-shadow: 0 8px 26px rgba(31, 67, 104, .07);
        }

        .sayit-emoji {
            font-size: clamp(3.3rem, 8vw, 5.4rem);
            line-height: 1.2;
        }

        .sayit-phrase {
            color: #17365d;
            font-size: clamp(2rem, 5.2vw, 3.3rem);
            font-weight: 800;
            line-height: 1.22;
            margin: 18px 0 12px;
            overflow-wrap: anywhere;
        }

        .sayit-hint {
            color: #52677d;
            font-size: 1.03rem;
        }

        .sayit-note {
            background: #f5f8fc;
            border-left: 5px solid #7a9fc8;
            border-radius: 10px;
            padding: 14px 16px;
            color: #29445f;
            line-height: 1.55;
        }

        div.stButton > button {
            min-height: 3.35rem;
            border-radius: 13px;
            font-weight: 700;
            white-space: normal;
            padding: .65rem 1rem;
        }

        div.stButton > button:focus-visible,
        button:focus-visible,
        input:focus-visible,
        textarea:focus-visible {
            outline: 4px solid #e69f00 !important;
            outline-offset: 3px !important;
        }

        [data-testid="stAudioInput"] {
            border-radius: 14px;
        }

        @media (max-width: 640px) {
            .sayit-phrase-card {
                border-radius: 18px;
            }
        }
        </style>
        
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sayit-wrap">',
        unsafe_allow_html=True
    )

    top_left, top_right = st.columns(
        [3, 2],
        vertical_alignment="center"
    )

    with top_left:
        st.markdown(
            '<div class="sayit-eyebrow">'
            '🎤 Communication practice</div>',
            unsafe_allow_html=True
        )
        st.title("Say It!")

    with top_right:
        st.markdown(
            f"**Phrase {current_index + 1} of {total}**  ·  "
            f"**{completed_count} completed**"
        )
        st.progress(
            completed_count / total if total else 0.0,
            text="Practice progress"
        )

    st.markdown(
        '<p class="sayit-intro">'
        'Practice speaking one phrase at a time, at your own pace. '
        'You can listen first, record when you feel ready, or skip any '
        'phrase. Speaking is optional—your other communication tools '
        'remain available.</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <section class="sayit-phrase-card" aria-label="Phrase to practice">
          <div class="sayit-emoji" aria-hidden="true">
            {exercise["emoji"]}
          </div>
          <div class="sayit-phrase">{exercise["phrase"]}</div>
          <div class="sayit-hint">
            {exercise.get("hint", "Take your time.")}
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    listen_col, record_col = st.columns(2, gap="medium")

    with listen_col:
        if st.button(
            "🔊  Listen to example",
            use_container_width=True,
            key="sayit_listen",
        ):
            # TODO: Call your ElevenLabs speech endpoint.
            # Render its returned audio using st.audio(...).
            st.session_state.sayit_feedback = {
                "kind": "info",
                "message": (
                    "Example pronunciation will play here once "
                    "the ElevenLabs endpoint is connected."
                ),
            }

    with record_col:
        st.markdown("**🎙️ Your turn**")
        st.caption(
            "Use the recorder below, say the phrase if you feel ready, "
            "then stop recording."
        )

    # The recording is not uploaded in this frontend-only version.
    audio_value = st.audio_input(
        "Record your attempt",
        key=f"sayit_audio_{current_index}",
    )

    if audio_value is not None:
        st.session_state.sayit_recording = audio_value

        st.audio(audio_value)

        st.markdown(
            '<div class="sayit-note">'
            '<strong>Recording ready.</strong> '
            'Your recording has not been submitted. Backend transcription '
            'and phrase matching will be connected here.'
            '</div>',
            unsafe_allow_html=True,
        )

        if st.button(
            "Check my phrase",
            type="primary",
            use_container_width=True,
            key="sayit_check",
        ):
            # TODO:
            # 1. Send audio_value.getvalue() to the transcription endpoint.
            # 2. Get the transcript.
            # 3. Send the transcript and target phrase to the
            #    response-checking endpoint.
            st.session_state.sayit_feedback = {
                "kind": "info",
                "message": (
                    "Your recording is ready. Phrase checking will be "
                    "enabled when the transcription and response-check "
                    "endpoints are connected."
                ),
            }

    feedback = st.session_state.sayit_feedback

    if feedback:
        kind = feedback.get("kind", "info")
        message = feedback.get("message", "")

        if kind == "success":
            st.success(message, icon="🌟")
        elif kind == "warning":
            st.warning(message, icon="💛")
        else:
            st.info(message, icon="💬")

    st.markdown("#### Remember")

    st.markdown(
        '<div class="sayit-note">'
        'There is no rush and no penalty for trying again. '
        'You can speak, use AAC, type, or take a break whenever you need.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    try_col, skip_col, next_col = st.columns(
        [1.15, 1, 1.25],
        gap="small"
    )

    with try_col:
        if st.button(
            "↻  Try again",
            use_container_width=True,
            key="sayit_retry",
        ):
            st.session_state.sayit_recording = None
            st.session_state.sayit_feedback = None
            st.session_state.sayit_attempts = 0
            st.rerun()

    with skip_col:
        if st.button(
            "Skip phrase",
            use_container_width=True,
            key="sayit_skip",
        ):
            _advance(skipped=True)
            st.rerun()

    with next_col:
        if st.button(
            "Next phrase  →",
            type="primary",
            use_container_width=True,
            key="sayit_next",
        ):
            _advance(completed=True)
            st.rerun()

    st.caption(
        f"Completed: {completed_count} of {total} · "
        f"Skipped: {len(st.session_state.sayit_skipped)} · "
        "Your progress is stored for this session only."
    )

    st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Say It! | CodeRed Orion",
        page_icon="🎤",
        layout="centered",
    )
    render_say_it_ui()
