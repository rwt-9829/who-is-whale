import streamlit as st
from app.visualization import show_winnings_chart
from app.stats_display import show_player_stats
from parser.log_parser import parse_log_file, extract_stats

st.set_page_config(page_title="Poker Hand History Analyzer")

st.header("Poker Hand History Analyzer")
st.text("Analyze online poker logs to extract detailed player behavior statistics, including c-bets, donk bets, probes, and fold frequencies at each street. Ideal for improving strategy and gaining insights from historical hands.")

uploaded_file = st.file_uploader("Upload Poker Log File", type=["csv"])
if uploaded_file is not None:
    df = parse_log_file(uploaded_file)
    player_stats, hand_winnings = extract_stats(df)
    show_winnings_chart(hand_winnings)
    show_player_stats(player_stats)

else:
    st.warning("Please upload a log file to proceed.")
