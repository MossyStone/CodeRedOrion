import io
import math
import struct
import wave

import streamlit as st


def make_success_sound():
    """
    Generate a short, gentle two-note success chime.

    Returns:
        bytes: WAV audio data ready for Streamlit.
    """

    sample_rate = 22050
    samples = []

    # Two cheerful musical notes: C5 and E5
    notes = [
        (523.25, 0.15),
        (659.25, 0.20),
    ]

    for frequency, duration in notes:
        count = int(sample_rate * duration)

        for i in range(count):
            t = i / sample_rate

            # Smooth fade in and out to avoid clicks
            envelope = math.sin(math.pi * i / count) ** 2

            # Gentle volume
            value = int(
                10000
                * envelope
                * math.sin(2 * math.pi * frequency * t)
            )

            samples.append(value)

    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        wav.writeframes(
            struct.pack(f"<{len(samples)}h", *samples)
        )

    return buffer.getvalue()


def play_success_sound():
    """
    Play the success chime in Streamlit.

    Uses the user's sound preference when available.
    """

    if st.session_state.get("sound_enabled", True):
        st.audio(
            make_success_sound(),
            format="audio/wav",
            autoplay=True,
        )


def sound_settings():
    """
    Display an optional sound on/off setting.
    """

    if "sound_enabled" not in st.session_state:
        st.session_state.sound_enabled = True

    st.toggle(
        "🔊 Success sounds",
        key="sound_enabled",
        help="Turn game success sounds on or off.",
    )
