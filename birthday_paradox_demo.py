import math
import random
import time
from collections import Counter
from datetime import date, timedelta
from html import escape

import matplotlib.pyplot as plt
import streamlit as st


st.set_page_config(
    page_title="Birthday Paradox Monte Carlo Demo",
    page_icon="🎂",
    layout="wide",
)


FIRST_NAMES = [
    "Ava", "Liam", "Noah", "Emma", "Olivia", "Sophia", "Lucas", "Mia", "Amelia", "Ethan",
    "Elena", "Mateo", "Sofia", "Isabella", "James", "Charlotte", "Benjamin", "Harper", "Henry", "Evelyn",
    "Daniel", "Camila", "Logan", "Scarlett", "Jack", "Aria", "Sebastian", "Luna", "Julian", "Ella",
    "Levi", "Nora", "Owen", "Chloe", "Samuel", "Layla", "Leo", "Grace", "Wyatt", "Zoe",
    "Gabriel", "Hannah", "David", "Violet", "Isaac", "Aurora", "Nathan", "Penelope", "Adrian", "Maya",
    "Christian", "Riley", "Thomas", "Stella", "Josiah", "Lucy", "Aiden", "Hazel", "Colton", "Lily",
    "Roman", "Nova", "Hudson", "Ellie", "Ezra", "Madison", "Elias", "Claire", "Milo", "Naomi",
    "Asher", "Paisley", "Eli", "Alice", "Caleb", "Ruby", "Ryan", "Ivy", "Nolan", "Sadie",
]
LAST_INITIALS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
NAME_POOL = [f"{first} {initial}." for first in FIRST_NAMES for initial in LAST_INITIALS]


MONTH_DAY_FORMAT = "%b %d"


STYLE = """
<style>
    .room-card {
        border: 1px solid rgba(120,120,120,0.25);
        border-radius: 16px;
        padding: 0.85rem 1rem 0.6rem 1rem;
        margin-bottom: 0.5rem;
        background: rgba(250,250,250,0.02);
    }
    .repeat-summary {
        margin-bottom: 0.6rem;
        font-size: 0.95rem;
    }
    .birthday-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
    }
    .birthday-table th, .birthday-table td {
        padding: 0.45rem 0.55rem;
        border-bottom: 1px solid rgba(120,120,120,0.18);
        text-align: left;
    }
    .birthday-table th {
        font-weight: 700;
    }
    .dup-row {
        background: rgba(255, 99, 71, 0.12);
    }
    .dup-badge {
        display: inline-block;
        padding: 0.12rem 0.45rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        background: rgba(255, 99, 71, 0.18);
        border: 1px solid rgba(255, 99, 71, 0.4);
    }
    .ok-badge {
        display: inline-block;
        padding: 0.12rem 0.45rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 700;
        background: rgba(60, 179, 113, 0.16);
        border: 1px solid rgba(60, 179, 113, 0.35);
    }
    .small-note {
        opacity: 0.85;
        font-size: 0.9rem;
        margin-top: 0.35rem;
    }
</style>
"""


def build_calendar(days_in_year: int) -> list[str]:
    year = 2024 if days_in_year == 366 else 2023
    base = date(year, 1, 1)
    return [(base + timedelta(days=offset)).strftime(MONTH_DAY_FORMAT) for offset in range(days_in_year)]


def generate_names(n_people: int, rng: random.Random) -> list[str]:
    if n_people <= len(NAME_POOL):
        return rng.sample(NAME_POOL, n_people)

    names = []
    cycles = math.ceil(n_people / len(NAME_POOL))
    for cycle in range(cycles):
        sampled = NAME_POOL[:]
        rng.shuffle(sampled)
        suffix = "" if cycle == 0 else f" #{cycle + 1}"
        names.extend([name + suffix for name in sampled])
    return names[:n_people]


def exact_birthday_probability(n_people: int, days_in_year: int) -> float:
    if n_people > days_in_year:
        return 1.0

    probability_no_match = 1.0
    for k in range(n_people):
        probability_no_match *= (days_in_year - k) / days_in_year
    return 1.0 - probability_no_match


def simulate_room(n_people: int, calendar_days: list[str], rng: random.Random):
    names = generate_names(n_people, rng)
    birthdays = [rng.choice(calendar_days) for _ in range(n_people)]
    counts = Counter(birthdays)
    repeated_birthdays = {birthday for birthday, count in counts.items() if count > 1}

    room = []
    for person, birthday in zip(names, birthdays):
        room.append(
            {
                "person": person,
                "birthday": birthday,
                "duplicate": birthday in repeated_birthdays,
            }
        )

    return room, bool(repeated_birthdays), repeated_birthdays


def render_room_html(room: list[dict], repeated_birthdays: set[str]) -> str:
    if repeated_birthdays:
        repeated_text = ", ".join(sorted(repeated_birthdays))
        status_badge = "<span class='dup-badge'>Shared birthday found</span>"
    else:
        repeated_text = "None"
        status_badge = "<span class='ok-badge'>No shared birthday</span>"

    rows = []
    for row in room:
        row_class = "dup-row" if row["duplicate"] else ""
        marker = "🎯 repeated" if row["duplicate"] else ""
        rows.append(
            f"<tr class='{row_class}'>"
            f"<td>{escape(row['person'])}</td>"
            f"<td><b>{escape(row['birthday'])}</b></td>"
            f"<td>{marker}</td>"
            f"</tr>"
        )

    return f"""
    <div class='room-card'>
        <div class='repeat-summary'>
            {status_badge}<br>
            <span class='small-note'><b>Repeated birthdays in this room:</b> {escape(repeated_text)}</span>
        </div>
        <table class='birthday-table'>
            <thead>
                <tr>
                    <th>Person</th>
                    <th>Birthday</th>
                    <th>Flag</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </div>
    """


def main() -> None:
    st.markdown(STYLE, unsafe_allow_html=True)

    st.title("🎂 Birthday Paradox Monte Carlo Demo")
    st.markdown(
        """
        Even though the birthday paradox has an exact solution, this app estimates it with **Monte Carlo simulation**.

        What the simulation does:
        1. Randomly generate birthdays for a room of `n` people.
        2. Check whether at least two birthdays match.
        3. Repeat many times.
        4. Estimate the share of runs with a shared birthday.
        """
    )

    with st.sidebar:
        st.header("Controls")
        n_people = st.slider("Number of people", min_value=2, max_value=100, value=23, step=1)
        n_runs = st.slider("Number of simulation runs", min_value=1, max_value=1000, value=25, step=1)
        days_in_year = st.radio("Days in the year", options=[365, 366], horizontal=True)
        slow_mode = st.toggle("Slow mode", value=True, help="Adds a 1-second pause between iterations.")
        run_clicked = st.button("Run simulation", type="primary", use_container_width=True)

        st.caption(
            "Slow mode is great for presentations. Turbo mode is better when you want the estimate fast."
        )

    exact_prob = exact_birthday_probability(n_people, days_in_year)
    st.info(
        f"With **{n_people}** people and **{days_in_year}** possible birthdays, the exact probability of at least one shared birthday is **{exact_prob:.2%}**."
    )

    with st.expander("Optional note on names"):
        st.write(
            "This version uses a built-in random name pool so the script runs with just Streamlit and the Python standard library. "
            "If you want more variety later, you could swap the name generator for the `faker` package."
        )

    if not run_clicked:
        st.caption("Click **Run simulation** to start.")
        return

    rng = random.Random()
    calendar_days = build_calendar(days_in_year)
    delay_seconds = 1.0 if slow_mode else 0.0

    progress_bar = st.progress(0)

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        metric_placeholder1 = st.empty()
    with metric_col2:
        metric_placeholder2 = st.empty()
    with metric_col3:
        metric_placeholder3 = st.empty()
    with metric_col4:
        metric_placeholder4 = st.empty()

    st.subheader("Monte Carlo estimate by iteration")
    plot_placeholder = st.empty()

    st.subheader("Iteration log")
    history_container = st.container()

    matches = 0
    estimate_history = []

    for iteration in range(1, n_runs + 1):
        room, has_match, repeated_birthdays = simulate_room(n_people, calendar_days, rng)
        matches += int(has_match)
        estimate = matches / iteration
        estimate_history.append(estimate)

        metric_placeholder1.metric("Iterations completed", f"{iteration}/{n_runs}")
        metric_placeholder2.metric("Runs with a match", matches)
        metric_placeholder3.metric("Monte Carlo estimate", f"{estimate:.2%}")
        metric_placeholder4.metric("Exact probability", f"{exact_prob:.2%}")

        with history_container:
            label = "🎯 match" if has_match else "❌ no match"
            with st.expander(f"Iteration {iteration}: {label}", expanded=(iteration == 1)):
                st.markdown(render_room_html(room, repeated_birthdays), unsafe_allow_html=True)

        progress_bar.progress(iteration / n_runs)

        if delay_seconds:
            time.sleep(delay_seconds)

    final_estimate = matches / n_runs
    error = abs(final_estimate - exact_prob)

    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(range(1, n_runs + 1), estimate_history, label="Monte Carlo estimate")
    ax.axhline(exact_prob, linestyle="--", label="Exact probability")
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Probability")
    ax.set_title("Convergence of the Monte Carlo estimate")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plot_placeholder.pyplot(fig)

    st.success(
        f"Finished {n_runs} runs. Estimated probability: {final_estimate:.2%}. "
        f"Exact probability: {exact_prob:.2%}. Absolute error: {error:.2%}."
    )


if __name__ == "__main__":
    main()