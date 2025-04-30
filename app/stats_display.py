import streamlit as st

def show_player_stats(player_stats):
    st.header("Player Statistics")
    bb_size = 100
    for name, stats in player_stats.items():
        hands = stats["hands"]
        winnings = stats["winnings"]
        # basic
        vpip = (stats["vpip"] / hands * 100) if hands else 0
        pfr = (stats["pfr"] / hands * 100) if hands else 0
        bb_per_100 = (winnings / (hands * bb_size) * 100) if hands else 0
        # flop
        cbet_flop = (stats["cbet_flop"] / stats["saw_flop_pfr"] * 100) if stats["saw_flop_pfr"] else 0
        fold_to_cbet = (stats["fold_to_cbet_flop"] / stats["faced_cbet_flop"] * 100) if stats["faced_cbet_flop"] else 0
        x_r_flop = (stats["x_r_flop"] / stats["saw_flop_pfc"] * 100) if stats["saw_flop_pfc"] else 0
        donk_flop = (stats["donk_flop"] / stats["saw_flop_pfc"] * 100) if stats["saw_flop_pfc"] else 0
        # turn
        turn_cbet = (stats["turn_cbet"] / stats["saw_turn_pfr"] * 100) if stats["saw_turn_pfr"] else 0
        turn_delay_cbet = (stats["turn_delay_cbet"] / stats["saw_turn_pfr"] * 100) if stats["saw_turn_pfr"] else 0
        probe_turn = (stats["probe_turn"] / stats["saw_turn_pfc"] * 100) if stats["saw_turn_pfc"] else 0
        donk_turn = (stats["donk_turn"] / stats["saw_turn_pfc"] * 100) if stats["saw_turn_pfc"] else 0
        r_turn = (stats["r_turn"] / stats["faced_turn_bet"] * 100) if stats["faced_turn_bet"] else 0
        fold_to_bet_turn = (stats["fold_to_bet_turn"] / stats["faced_turn_bet"] * 100) if stats["faced_turn_bet"] else 0
        
        # display
        st.subheader(name)

        st.markdown("**BASIC STATS**")
        st.write(f"Hands: {hands}")
        st.write(f"Winnings: {winnings}")
        st.write(f"BB/100: {bb_per_100:.2f}")
        st.write(f"VPIP: {vpip:.2f}%")
        st.write(f"PFR: {pfr:.2f}%")

        st.markdown("**FLOP STATS**")
        st.write(f"Flop CBet%: {cbet_flop:.2f}%")
        st.write(f"Flop Fold to CBet%: {fold_to_cbet:.2f}%")
        st.write(f"Flop X/R%: {x_r_flop:.2f}%")
        st.write(f"Flop Donk%: {donk_flop:.2f}%")

        st.markdown("**TURN STATS**")
        st.text(f"Turn C-bet: {turn_cbet:.2f}%")
        st.text(f"Delayed Turn C-bet: {turn_delay_cbet:.2f}%")
        st.text(f"Turn Probe: {probe_turn:.2f}%")
        st.text(f"Turn Donk: {donk_turn:.2f}%")
        st.text(f"Turn Raise: {r_turn:.2f}%")
        st.text(f"Fold to Turn Bet: {fold_to_bet_turn:.2f}%")