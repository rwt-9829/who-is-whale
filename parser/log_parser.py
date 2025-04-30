import pandas as pd
import re
from collections import defaultdict

def parse_log_file(file_path):
    df = pd.read_csv(file_path)
    df = df.sort_values("order")
    return df

def extract_hands(entries):
    hands = []
    current_hand = []
    inside_hand = False
    for entry in entries:
        if entry.startswith("-- starting hand"):
            current_hand = [entry]
            inside_hand = True
        elif entry.startswith("-- ending hand"):
            current_hand.append(entry)
            hands.append(current_hand)
            inside_hand = False
        elif inside_hand:
            current_hand.append(entry)
    return hands

def extract_street_actions(hand):
    streets = {"PREFLOP": [], "FLOP": [], "TURN": [], "RIVER": []}
    current_street = "PREFLOP"
    for entry in hand:
        if entry.startswith("Flop:"):
            current_street = "FLOP"
        elif entry.startswith("Turn:"):
            current_street = "TURN"
        elif entry.startswith("River:"):
            current_street = "RIVER"
        elif '"' in entry and any(kw in entry for kw in ["bets", "calls", "raises", "folds", "checks", "posts"]):
            streets[current_street].append(entry)
    return streets

def extract_stats(df):
    entries = df["entry"].tolist()
    hands = extract_hands(entries)

    player_stats = defaultdict(lambda: {
        "hands": 0, "winnings": 0, "vpip": 0, "pfr": 0,
        "3b": 0, "4b": 0, "5b": 0,
        "vs_2b": 0, "vs_3b": 0, "vs_4b": 0,
        "preflop_raiser": 0, "cbet_flop": 0, "faced_cbet_flop": 0,
        "fold_to_cbet_flop": 0, "x_r_flop": 0, "donk_flop": 0,
        "saw_flop_pfr": 0, "saw_flop_pfc": 0,
        "turn_cbet": 0, "faced_turn_bet": 0, "fold_to_bet_turn": 0,
        "r_turn": 0, "donk_turn": 0, "probe_turn": 0,
        "turn_delay_cbet": 0, "saw_turn_fa": 0, "saw_turn_fc": 0, "saw_turn_xx": 0,
        "river_cbet": 0, "river_delay_cbet": 0, "donk_river": 0,
        "probe_river": 0, "r_river": 0, "fold_to_bet_river": 0,
        "faced_river_bet": 0, "saw_river_fa": 0, "saw_river_fc": 0, "saw_river_xx": 0,
    })

    hand_winnings = []
    bb_size = 100

    for hand in hands:
        actions = extract_street_actions(hand)
        players_in_hand = set()
        contributions = defaultdict(int)
        winnings = defaultdict(int)
        saw_flop = set()
        saw_turn = set()
        vpip_players = set()
        pfr = None
        pfc_set = set()
        flop_aggro = None
        pfr_checked_flop = False

        # PREFLOP
        raise_counts = 0
        for a in actions["PREFLOP"]:
            m = re.match(r'"(.+?)" (.+)', a)
            if m:
                name, move = m.groups()
                players_in_hand.add(name)

                if name not in vpip_players and ("calls" in move or "raises" in move):
                    player_stats[name]["vpip"] += 1
                    vpip_players.add(name)

                if "raises" in move:
                    pfr = name
                    if raise_counts == 0:
                        player_stats[name]["pfr"] += 1
                        player_stats[name]["preflop_raiser"] += 1
                        for other in players_in_hand:
                            if other != name:
                                player_stats[other]["vs_2b"] += 1
                    elif raise_counts == 1:
                        player_stats[name]["3b"] += 1
                        for other in players_in_hand:
                            if other != name:
                                player_stats[other]["vs_3b"] += 1
                    elif raise_counts == 2:
                        player_stats[name]["4b"] += 1
                        for other in players_in_hand:
                            if other != name:
                                player_stats[other]["vs_4b"] += 1
                    elif raise_counts == 3:
                        player_stats[name]["5b"] += 1
                    
                    raise_counts += 1
                elif "calls" in move:
                    pfc_set.add(name)

        for p in players_in_hand:
            player_stats[p]["hands"] += 1
        if pfr:
            player_stats[pfr]["pfr"] += 1
            player_stats[pfr]["preflop_raiser"] += 1

        # FLOP
        for a in actions["FLOP"]:
            m = re.match(r'"(.+?)" ', a)
            if m:
                name = m.group(1)
                saw_flop.add(name)

        if pfr and pfr in saw_flop:
            player_stats[pfr]["saw_flop_pfr"] += 1
        for pfc in pfc_set:
            if pfc in saw_flop:
                player_stats[pfc]["saw_flop_pfc"] += 1

        for a in actions["FLOP"]:
            if "bets" in a:
                m = re.match(r'"(.+?)" bets', a)
                if m:
                    bettor = m.group(1)
                    if flop_aggro is None:
                        flop_aggro = bettor
                    if pfr and bettor == pfr:
                        player_stats[pfr]["cbet_flop"] += 1
                    else:
                        player_stats[bettor]["donk_flop"] += 1
            elif "checks" in a and pfr and a.startswith(f'"{pfr}"'):
                pfr_checked_flop = True
            elif "raises" in a:
                m = re.match(r'"(.+?)" raises', a)
                if m:
                    player_stats[m.group(1)]["x_r_flop"] += 1
                    flop_aggro = m.group(1)
            elif "folds" in a:
                m = re.match(r'"(.+?)" folds', a)
                if m:
                    player_stats[m.group(1)]["fold_to_cbet_flop"] += 1
            if any(x in a for x in ["bets", "calls", "folds"]):
                m = re.match(r'"(.+?)" ', a)
                if m:
                    name = m.group(1)
                    if name != pfr:
                        player_stats[name]["faced_cbet_flop"] += 1

        # TURN
        turn_aggro = None
        for a in actions["TURN"]:
            m = re.match(r'"(.+?)" ', a)
            if m:
                name = m.group(1)
                saw_turn.add(name)

        if flop_aggro:
            for name in saw_turn:
                if name == flop_aggro:
                    player_stats[name]["saw_turn_fa"] += 1
                elif name in pfc_set:
                    player_stats[name]["saw_turn_fc"] += 1
        else:
            for name in saw_turn:
                player_stats[name]["saw_turn_xx"] += 1

        for a in actions["TURN"]:
            if "bets" in a:
                m = re.match(r'"(.+?)" bets', a)
                if m:
                    bettor = m.group(1)
                    if turn_aggro is None:
                        turn_aggro = bettor
                    if flop_aggro and bettor == flop_aggro:
                        player_stats[flop_aggro]["turn_cbet"] += 1
                    elif pfr_checked_flop and pfr and bettor == pfr:
                        player_stats[pfr]["turn_delay_cbet"] += 1
                    elif not flop_aggro and not pfr_checked_flop:
                        player_stats[bettor]["probe_turn"] += 1
                    elif bettor != flop_aggro and bettor != pfr:
                        player_stats[bettor]["donk_turn"] += 1
            elif "raises" in a:
                m = re.match(r'"(.+?)" raises', a)
                if m:
                    player_stats[m.group(1)]["r_turn"] += 1
                    turn_aggro = m.group(1)
            elif "folds" in a:
                m = re.match(r'"(.+?)" folds', a)
                if m:
                    player_stats[m.group(1)]["fold_to_bet_turn"] += 1
            if "calls" in a or "folds" in a:
                m = re.match(r'"(.+?)" ', a)
                if m:
                    name = m.group(1)
                    player_stats[name]["faced_turn_bet"] += 1

        # RIVER
        saw_river = set()
        for a in actions["RIVER"]:
            m = re.match(r'"(.+?)" ', a)
            if m:
                name = m.group(1)
                saw_river.add(name)

        if turn_aggro:
            for name in saw_river:
                if name == turn_aggro:
                    player_stats[name]["saw_river_fa"] += 1
                elif name in pfc_set:
                    player_stats[name]["saw_river_fc"] += 1
        else:
            for name in saw_river:
                player_stats[name]["saw_river_xx"] += 1

        for a in actions["RIVER"]:
            if "bets" in a:
                m = re.match(r'"(.+?)" bets', a)
                if m:
                    bettor = m.group(1)
                    if turn_aggro and bettor == turn_aggro:
                        player_stats[bettor]["river_cbet"] += 1
                    elif pfr_checked_flop and pfr and bettor == pfr:
                        player_stats[pfr]["river_delay_cbet"] += 1
                    elif not turn_aggro and not pfr_checked_flop:
                        player_stats[bettor]["probe_river"] += 1
                    elif bettor != turn_aggro and bettor != pfr:
                        player_stats[bettor]["donk_river"] += 1
            elif "raises" in a:
                m = re.match(r'"(.+?)" raises', a)
                if m:
                    player_stats[m.group(1)]["r_river"] += 1
            elif "folds" in a:
                m = re.match(r'"(.+?)" folds', a)
                if m:
                    player_stats[m.group(1)]["fold_to_bet_river"] += 1
            if "calls" in a or "folds" in a:
                m = re.match(r'"(.+?)" ', a)
                if m:
                    name = m.group(1)
                    player_stats[name]["faced_river_bet"] += 1


        # Contributions
        for street_actions in actions.values():
            cur_contrib = defaultdict(int)
            for line in street_actions:
                m = re.match(r'"(.+?)" (bets|calls|raises|posts a small blind|posts a big blind)(.*?)(\d+)', line)
                if m:
                    name, _, _, amount = m.groups()
                    cur_contrib[name] = int(amount)
            for name in players_in_hand:
                contributions[name] += cur_contrib[name]

        # WINNINGS
        for line in hand:
            if "collected" in line:
                m = re.match(r'"(.+?)" collected (\d+)', line)
                if m:
                    name, amount = m.groups()
                    winnings[name] += int(amount)
            elif "Uncalled bet of" in line:
                m = re.match(r'Uncalled bet of (\d+) returned to "(.+?)"', line)
                if m:
                    amount, name = m.groups()
                    winnings[name] += int(amount)

        net_result = {}
        for player in set(contributions.keys()).union(winnings.keys()):
            net = winnings[player] - contributions[player]
            player_stats[player]["winnings"] += net
            net_result[player] = net

        hand_winnings.append(net_result)

    return player_stats, hand_winnings