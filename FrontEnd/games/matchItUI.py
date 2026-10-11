import streamlit as st

from sounds import play_success_sound

def render_match_it(rounds, check_answer):
    # ==========================================
    # MATCH IT! GAME INTERFACE
    # ==========================================

    st.markdown(
        '<h2 style="text-align:center">🧩 Match It!</h2>',
        unsafe_allow_html=True
    )

    st.caption(
        "Choose the card that matches the phrase. "
        "You can try again if you get it wrong!"
    )

    if not rounds:
        st.info("No matching rounds are available.")
        return

    # ==========================================
    # GAME SESSION STATE
    # ==========================================

    if "match_round_index" not in st.session_state:
        st.session_state.match_round_index = 0

    if "match_result" not in st.session_state:
        st.session_state.match_result = None

    index = st.session_state.match_round_index

    # ==========================================
    # GAME COMPLETION
    # ==========================================

    if index >= len(rounds):
        st.progress(1.0)
        st.success("🎉 You've completed Match It!")
        st.write("Great job practicing your communication skills!")

        if st.button(
            "🔄 Play Again",
            key="match_restart",
            use_container_width=True
        ):
            st.session_state.match_round_index = 0
            st.session_state.match_result = None
            st.rerun()

        return

    # ==========================================
    # CURRENT QUESTION
    # ==========================================

    current_round = rounds[index]

    st.progress(index / len(rounds))

    st.caption(
        f"Question {index + 1} of {len(rounds)}"
    )

    st.markdown(
        f"### Find the match for: {current_round['phrase']}"
    )

    # ==========================================
    # ANSWER CHOICES
    # ==========================================

    with st.container(key="practice_area"):
        options = current_round["options"]

        # Display answer cards in two columns
        for i in range(0, len(options), 2):
            columns = st.columns(2, gap="small")

            for column, option in zip(
                columns,
                options[i:i + 2]
            ):
                with column:
                    label = (
                        f"{option['emoji']} "
                        f"{option['label']}"
                    )

                    # Disable choices only after a correct answer
                    answered_correctly = (
                        st.session_state.match_result is not None
                        and st.session_state.match_result.get(
                            "is_match", False
                        )
                    )

                    if st.button(
                        label,
                        key=f"match_{index}_{option['id']}",
                        use_container_width=True,
                        disabled=answered_correctly
                    ):
                        try:
                            # Send the selected answer to FastAPI
                            result = check_answer(
                                current_round["id"],
                                option["id"]
                            )

                            st.session_state.match_result = result
                            st.rerun()

                        except Exception as error:
                            st.error(
                                f"Unable to check answer: {error}"
                            )

    # ==========================================
    # ANSWER FEEDBACK
    # ==========================================

    if st.session_state.match_result is not None:
        result = st.session_state.match_result

        if result.get("is_match", False):
            st.success(
                "✅ " + result.get(
                    "feedback",
                    "You found the matching card!"
                )
            )
        else:
            st.error(
                "❌ " + result.get(
                    "feedback",
                    "Not quite. Try again!"
                )
            )

        # Allow users to move on after any attempt
        if st.button(
            "Next Question →",
            key="match_next",
            use_container_width=True
        ):
            st.session_state.match_round_index += 1
            st.session_state.match_result = None
            st.rerun()


# END OF MATCH IT! GAME INTERFACE
