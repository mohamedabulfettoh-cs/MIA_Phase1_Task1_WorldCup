"""
Task 1.1 - Group Stage Standings Engine
MIA World Cup Broadcast & Analytics Center
"""

Teams = ["ARG", "MEX", "POL", "KSA"]

Matchups = [
    ("ARG", "MEX"),
    ("ARG", "POL"),
    ("ARG", "KSA"),
    ("MEX", "POL"),
    ("MEX", "KSA"),
    ("POL", "KSA"),
]


def init_standings(teams):
    standings = {}
    for team in teams:
        standings[team] = {
            "P": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "GF": 0,
            "GA": 0,
            "GD": 0,
            "Pts": 0,
        }
    return standings


def process_match(standings, team1, team2, team1_goals, team2_goals):
    standings[team1]["P"] += 1
    standings[team2]["P"] += 1
    standings[team1]["GF"] += team1_goals
    standings[team2]["GF"] += team2_goals
    standings[team1]["GA"] += team2_goals
    standings[team2]["GA"] += team1_goals
    standings[team1]["GD"] = standings[team1]["GF"] - standings[team1]["GA"]
    standings[team2]["GD"] = standings[team2]["GF"] - standings[team2]["GA"]
    if team1_goals > team2_goals:
        standings[team1]["W"] += 1
        standings[team1]["Pts"] += 3
        standings[team2]["L"] += 1
    elif team1_goals == team2_goals:
        standings[team1]["Pts"] += 1
        standings[team2]["Pts"] += 1
        standings[team1]["D"] += 1
        standings[team2]["D"] += 1
    else:
        standings[team2]["W"] += 1
        standings[team2]["Pts"] += 3
        standings[team1]["L"] += 1
    
    


def get_match_score(team1, team2):
    while True:
        raw = input(f"Enter score for {team1} vs {team2} (format: 2-0): ")
        try:
            team1_goals, team2_goals = map(int, raw.split("-"))
            return team1_goals, team2_goals
        except ValueError:
            print("Invalid input. Please enter the score in 'X-Y' format (e.g., 2-0).")


def sort_standings(standings):
   items = list(standings.items())
   
   return sorted(items, key=lambda x: (x[1]["Pts"], x[1]["GD"], x[1]["GF"]), reverse = True)


def format_gd(gd):
    if gd > 0:
        return f"+{gd}"
    else:
        return str(gd)
    


def print_standings(standings):
    sorted_table = sort_standings(standings)
    print(f"{'Team':<6}{'P':<4}{'W':<4}{'D':<4}{'L':<4}{'GF':<5}{'GA':<5}{'GD':<5}{'Pts':<4}")
    for team, stats in sorted_table:
        print(f"{team:<6}{stats['P']:<4}{stats['W']:<4}{stats['D']:<4}{stats['L']:<4}{stats['GF']:<5}{stats['GA']:<5}{format_gd(stats['GD']):<5}{stats['Pts']:<4}")


def main():
    standings = init_standings(Teams)

    for team1, team2 in Matchups:
        g1, g2 = get_match_score(team1, team2)
        process_match(standings, team1, team2, g1, g2)

    print_standings(standings)


if __name__ == "__main__":
    main()