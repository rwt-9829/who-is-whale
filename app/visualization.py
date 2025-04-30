import streamlit as st
import matplotlib.pyplot as plt
from collections import defaultdict

def show_winnings_chart(hand_winnings):
    st.header("Cumulative Winnings Over Hands")

    cumulative = defaultdict(int)
    history = defaultdict(list)

    for i, hand in enumerate(hand_winnings):
        for player, amount in hand.items():
            cumulative[player] += amount
        for player in cumulative:
            history[player].append((i + 1, cumulative[player]))

    fig, ax = plt.subplots()
    for player, data in history.items():
        x = [h[0] for h in data]
        y = [h[1] for h in data]
        ax.plot(x, y, label=player)

    ax.set_xlabel("Hand #")
    ax.set_ylabel("Cumulative Winnings")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
