import itertools
import random
import time

import streamlit as st


st.set_page_config(page_title="Random Question", page_icon="?")


def initialize_state() -> None:
    defaults = {
        "names": [],
        "questions": [],
        "drawn_pairs": set(),
        "current_pick": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def available_pairs(no_repeats: bool) -> list[tuple[str, str]]:
    pairs = list(itertools.product(st.session_state.names, st.session_state.questions))
    if no_repeats:
        pairs = [pair for pair in pairs if pair not in st.session_state.drawn_pairs]
    return pairs


def add_item(state_key: str, value: str) -> None:
    item = value.strip()
    if item:
        st.session_state[state_key].append(item)


def draw_pair(no_repeats: bool) -> None:
    pairs = available_pairs(no_repeats)
    if not pairs:
        st.error("Add at least one name and one question, or turn off no repeats.")
        return

    preview = st.empty()
    for _ in range(6):
        name, question = random.choice(pairs)
        preview.info(f"**{name}**, please answer: {question}")
        time.sleep(0.5)

    chosen_pair = random.choice(pairs)
    st.session_state.current_pick = chosen_pair
    st.session_state.drawn_pairs.add(chosen_pair)
    preview.empty()


initialize_state()

st.title("Random Question")
st.caption("Build a roster, add questions, then draw a prompt for the group.")

no_repeats = st.checkbox("No repeats", help="Do not draw the same name/question pair twice in this session.")

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Roster")
    with st.form("add_name", clear_on_submit=True):
        name = st.text_input("Name", placeholder="Add a name")
        if st.form_submit_button("Add"):
            add_item("names", name)
            st.rerun()
    if st.session_state.names:
        st.write("\n".join(f"- {item}" for item in st.session_state.names))
    else:
        st.caption("No names yet.")

with right_column:
    st.subheader("Questions")
    with st.form("add_question", clear_on_submit=True):
        question = st.text_input("Question", placeholder="Add a question")
        if st.form_submit_button("Add"):
            add_item("questions", question)
            st.rerun()
    if st.session_state.questions:
        st.write("\n".join(f"- {item}" for item in st.session_state.questions))
    else:
        st.caption("No questions yet.")

st.divider()
if st.button("Draw", type="primary", disabled=not st.session_state.names or not st.session_state.questions):
    draw_pair(no_repeats)

if st.session_state.current_pick:
    name, question = st.session_state.current_pick
    st.success(f"**{name}**, please answer: {question}")