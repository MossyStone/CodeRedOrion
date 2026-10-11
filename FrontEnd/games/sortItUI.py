"""AACE It! Say It! practice page, connected to FastAPI and ElevenLabs.

Install in FrontEnd/sayItUI.py and call render_say_it_ui() from app.py.
"""

import os
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")


def _init_state():
    defaults = {
        "sayit_exercises": [],
        "sayit_index": 0,
        "sayit_completed": set(),
        "sayit_skipped": set(),
        "sayit_attempted": set(),
        "sayit_feedback": None,
        "sayit_transcript": None,
        "sayit_audio": None,
        "sayit_audio_source": None,
        "sayit_recording_version": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _clear_attempt():
    st.session_state.sayit_feedback = None
    st.session_state.sayit_transcript = None
    st.session_state.sayit_audio = None
    st.session_state.sayit_audio_source = None
    st.session_state.sayit_recording_version += 1


def _advance(skipped=False):
    current = st.session_state.sayit_index
    if skipped:
        st.session_state.sayit_skipped.add(current)
    if st.session_state.sayit_exercises:
        st.session_state.sayit_index = (current + 1) % len(st.session_state.sayit_exercises)
    _clear_attempt()


def _load_exercises():
    response = requests.get(f"{API_BASE_URL}/practice/say-it", timeout=10)
    response.raise_for_status()
    exercises = response.json().get("exercises", [])
    if not isinstance(exercises, list) or not exercises:
        raise ValueError("The backend returned no Say It! exercises.")
    return [item for item in exercises if isinstance(item, dict) and item.get("phrase")]


def _speak(phrase):
    response = requests.post(
        f"{API_BASE_URL}/speak", json={"text": phrase}, timeout=35
    )
    response.raise_for_status()
    if not response.content:
        raise ValueError("The speech service returned no audio.")
    return response.content


def _transcribe(recording):
    # Streamlit's st.audio_input produces WAV data.
    response = requests.post(
        f"{API_BASE_URL}/transcribe",
        files={"file": ("sayit_recording.wav", recording.getvalue(), "audio/wav")},
        timeout=75,
    )
    response.raise_for_status()
    return response.json().get("transcription", "")


def _check_phrase(exercise_id, transcript):
    response = requests.post(
        f"{API_BASE_URL}/practice/say-it/check",
        json={"exercise_id": exercise_id, "transcription": transcript},
        timeout=15,
    )
    response.raise_for_status()
    return response.json()


def render_say_it_ui(exercises=None):
    """Display the complete Say It! practice screen.

    Pass backend exercise dictionaries optionally; otherwise fetch them from FastAPI.
    """
    _init_state()

    if exercises is not None:
        valid = [item for item in exercises if isinstance(item, dict) and item.get("phrase")]
        if valid:
            st.session_state.sayit_exercises = valid

    if not st.session_state.sayit_exercises:
        try:
            with st.spinner("Loading practice phrases..."):
                st.session_state.sayit_exercises = _load_exercises()
        except (requests.RequestException, ValueError) as error:
            st.error(f"Couldn't load Say It! exercises: {error}")
            st.info("Make sure your FastAPI backend is running on port 8000.")
            if st.button("Try loading again", key="sayit_reload"):
                st.rerun()
            return

    items = st.session_state.sayit_exercises
    total = len(items)
    index = st.session_state.sayit_index % total
    exercise = items[index]
    phrase = str(exercise["phrase"])
    emoji = str(exercise.get("emoji", "💬"))
    hint = str(exercise.get("hint", "Take your time and try when you're ready."))
    exercise_id = exercise.get("id")

    st.markdown("""
    <style>
    .sayit-eyebrow {color:#7da7d8;font-weight:750;letter-spacing:.08em;text-transform:uppercase;}
    .sayit-phrase-card {background:linear-gradient(135deg,#f9fcff,#edf5ff);
        border:2px solid #c7d9ee;border-radius:22px;padding:30px 20px;
        text-align:center;margin:16px 0;color:#17365d;}
    .sayit-emoji {font-size:4rem;}
    .sayit-phrase {font-size:clamp(1.8rem,4vw,3rem);font-weight:800;
        margin:12px 0;overflow-wrap:anywhere;}
    .sayit-hint {font-size:1rem;color:#52677d;}
    div.stButton > button {min-height:3rem;white-space:normal;}
    button:focus-visible,textarea:focus-visible {outline:3px solid #e69f00 !important;}
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sayit-eyebrow">🎤 Communication practice</div>', unsafe_allow_html=True)
    st.title("Say It!")
    st.write(f"**Phrase {index + 1} of {total}** · **{len(st.session_state.sayit_completed)} completed**")
    st.progress(len(st.session_state.sayit_completed) / total, text="Practice progress")
    st.caption("Listen, record when you're ready, or skip. Speaking is optional; your AAC tools remain available.")

    # The exercise content comes from the local backend, not arbitrary HTML.
    import html
    st.markdown(
        '<section class="sayit-phrase-card" aria-label="Phrase to practice">'
        f'<div class="sayit-emoji" aria-hidden="true">{html.escape(emoji)}</div>'
        f'<div class="sayit-phrase">{html.escape(phrase)}</div>'
        f'<div class="sayit-hint">{html.escape(hint)}</div>'
        '</section>',
        unsafe_allow_html=True,
    )

    st.subheader("🔊 Listen to the example")
    if st.button("🔊 Play example", key="sayit_listen", use_container_width=True):
        try:
            with st.spinner("Generating example speech..."):
                st.session_state.sayit_audio = _speak(phrase)
                st.session_state.sayit_audio_source = (index, phrase)
        except (requests.RequestException, ValueError) as error:
            st.error(f"Couldn't play the example: {error}")

    if st.session_state.sayit_audio is not None and st.session_state.sayit_audio_source == (index, phrase):
        st.audio(st.session_state.sayit_audio, format="audio/mpeg")

    st.divider()
    st.subheader("🎙️ Your turn")
    st.caption("Record yourself saying the phrase. You can listen to your recording before checking it.")

    # A new key ensures an old recording is never submitted for the next exercise.
    recording = st.audio_input(
        "Record your attempt",
        key=f"sayit_audio_{index}_{st.session_state.sayit_recording_version}",
    )
    if recording is not None:
        st.audio(recording)

    if st.button(
        "Check my phrase",
        key="sayit_check",
        type="primary",
        use_container_width=True,
        disabled=(recording is None or exercise_id is None),
    ):
        try:
            with st.spinner("Transcribing your recording..."):
                transcript = _transcribe(recording)
            st.session_state.sayit_transcript = transcript
            st.session_state.sayit_attempted.add(index)

            if not transcript.strip():
                st.session_state.sayit_feedback = {
                    "kind": "warning",
                    "message": "We couldn't detect speech in that recording. You can try again or skip.",
                }
            else:
                with st.spinner("Checking your phrase..."):
                    result = _check_phrase(exercise_id, transcript)

                # Preserve the backend's feedback, without assuming a specific result schema.
                message = (
                    result.get("feedback") or result.get("message")
                    or result.get("explanation")
                )
                if isinstance(message, dict):
                    message = message.get("message") or str(message)
                if not isinstance(message, str) or not message:
                    message = "Your attempt was checked. Review the transcription below."

                success = result.get("correct") is True or result.get("is_correct") is True
                if success:
                    st.session_state.sayit_completed.add(index)
                    st.session_state.sayit_skipped.discard(index)

                st.session_state.sayit_feedback = {
                    "kind": "success" if success else "info",
                    "message": message,
                    "result": result,
                }
        except (requests.RequestException, ValueError) as error:
            st.session_state.sayit_feedback = {
                "kind": "error",
                "message": f"Couldn't check your recording: {error}",
            }

    if exercise_id is None:
        st.info("This exercise has no backend ID, so automatic checking is unavailable.")

    if st.session_state.sayit_transcript is not None:
        st.write("**What the speech recognizer heard:**")
        st.write(st.session_state.sayit_transcript or "(No speech detected)")
        st.caption("Automatic transcription can make mistakes, especially with atypical speech. It is not a measure of communication ability.")

    feedback = st.session_state.sayit_feedback
    if feedback:
        kind = feedback.get("kind", "info")
        message = feedback.get("message", "")
        if kind == "success":
            st.success(message)
        elif kind == "warning":
            st.warning(message)
        elif kind == "error":
            st.error(message)
        else:
            st.info(message)
        result = feedback.get("result")
        if isinstance(result, dict):
            with st.expander("See checking details"):
                st.json(result)

    st.divider()
    st.info("There is no rush or penalty for trying again. You can use AAC, type, or take a break whenever you need.")

    retry_col, skip_col, next_col = st.columns(3)
    with retry_col:
        if st.button("↻ Try again", use_container_width=True, key="sayit_retry"):
            _clear_attempt()
            st.rerun()
    with skip_col:
        if st.button("Skip phrase", use_container_width=True, key="sayit_skip"):
            _advance(skipped=True)
            st.rerun()
    with next_col:
        if st.button("Next phrase →", use_container_width=True, key="sayit_next"):
            _advance(skipped=False)
            st.rerun()

    st.caption(
        f"Completed: {len(st.session_state.sayit_completed)} of {total} · "
        f"Attempted: {len(st.session_state.sayit_attempted)} · "
        f"Skipped: {len(st.session_state.sayit_skipped)} · "
        "Progress is stored for this session only."
    )


if __name__ == "__main__":
    st.set_page_config(page_title="Say It! | AACE It!", page_icon="🎤", layout="centered")
    render_say_it_ui()
