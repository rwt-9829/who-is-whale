import streamlit as st
from app.visualization import show_winnings_chart
from app.stats_display import show_player_stats
from parser.log_parser import parse_log_file, extract_stats

st.title("Poker Log Analyzer")

print("testing")

df = parse_log_file("poker_now_log.csv")
player_stats = extract_stats(df)

show_winnings_chart(player_stats)
show_player_stats(player_stats)
