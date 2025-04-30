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
        "preflop_raiser": 0, "cbet_flop": 0, "faced_cbet_flop": 0,
        "fold_to_cbet_flop": 0, "x_r_flop": 0, "donk_flop": 0
    })
    hand_winnings = []
    bb_size = 100

    for hand in hands:
        actions = extract_street_actions(hand)
        players_in_hand = set()
        contributions = defaultdict(int)
        winnings = defaultdict(int)
        saw_flop = set()
        vpip_players = set()
        pfr = None  # track the latest raiser preflop

        # Track bets/contributions
        for street_actions in actions.values():
            for line in street_actions:
                m = re.match(r'"(.+?)" (bets|calls|raises|posts small blind|posts big blind)(.*?)(\d+)', line)
                if m:
                    name, _, _, amount = m.groups()
                    contributions[name] += int(amount)

        # PREFLOP stats
        for a in actions["PREFLOP"]:
            m = re.match(r'"(.+?)" (.+)', a)
            if m:
                name, move = m.groups()
                players_in_hand.add(name)

                if name not in vpip_players and ("calls" in move or "raises" in move):
                    player_stats[name]["vpip"] += 1
                    vpip_players.add(name)

                if "raises" in move:
                    pfr = name  # last preflop raiser

        for p in players_in_hand:
            player_stats[p]["hands"] += 1
        if pfr:
            player_stats[pfr]["pfr"] += 1
            player_stats[pfr]["preflop_raiser"] += 1

        # Detect who saw the flop
        for a in actions["FLOP"]:
            m = re.match(r'"(.+?)" ', a)
            if m:
                saw_flop.add(m.group(1))

        # FLOP stats
        for a in actions["FLOP"]:
            if pfr and f'"{pfr}" bets' in a and pfr in saw_flop:
                player_stats[pfr]["cbet_flop"] += 1
            if "bets" in a and not a.startswith(f'"{pfr}"'):
                m = re.match(r'"(.+?)" bets', a)
                if m:
                    player_stats[m.group(1)]["donk_flop"] += 1
            if "folds" in a:
                m = re.match(r'"(.+?)" folds', a)
                if m:
                    player_stats[m.group(1)]["fold_to_cbet_flop"] += 1
            if "raises" in a:
                m = re.match(r'"(.+?)" raises', a)
                if m:
                    player_stats[m.group(1)]["x_r_flop"] += 1
            if any(x in a for x in ["bets", "calls", "folds"]):
                m = re.match(r'"(.+?)" ', a)
                if m:
                    name = m.group(1)
                    if name != pfr:
                        player_stats[name]["faced_cbet_flop"] += 1

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
            #if net > 0:
            #    net = 2 * net
            player_stats[player]["winnings"] += net
            net_result[player] = net

        hand_winnings.append(net_result)

    return player_stats, hand_winnings