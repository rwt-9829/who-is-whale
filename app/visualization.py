import streamlit as st
import pandas as pd

def show_winnings_chart(player_stats):
    st.header("Cumulative Winnings")
    df = pd.DataFrame([
        {"Player": name, "Winnings": stats["winnings"]}
        for name, stats in player_stats.items()
    ])
    st.bar_chart(df.set_index("Player"))
