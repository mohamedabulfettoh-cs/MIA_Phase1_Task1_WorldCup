from random import random, uniform, choice


class Player:
    Valid_Positions = ["FORWARD", "MIDFIELDER", "DEFENDER", "GOALKEEPER"]
    def __init__(self, name, position, base_attack, base_defense):
        self.name = name
        if position not in self.Valid_Positions:
            raise ValueError(f"Invalid position. Choose from {self.Valid_Positions}")
        self.position = position
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.stamina = 100.0
        
    def deplete_stamina(self, rate):
      self.stamina = max(10.0, self.stamina - rate)

    def get_effective_attack(self):
        return (self.base_attack * (self.stamina / 100.0))

    def get_effective_defense(self):
        return (self.base_defense * (self.stamina / 100.0))     

class Team:
    def __init__(self, country_name, roster, active_lineup, bench, remaining_substitutions):
        self.country_name = country_name
        self.roster = roster
        self.active_lineup = active_lineup
        self.bench = bench
        self.remaining_substitutions = remaining_substitutions
        
    def get_aggregate_attack(self):
        attackers = [p for p in self.active_lineup if p.position in ("FORWARD", "MIDFIELDER")]
        if not attackers:
            return 0
        return sum(player.get_effective_attack() for player in attackers)/len(attackers)
    
    def get_aggregate_defense(self):
        defenders = [p for p in self.active_lineup if p.position in ("DEFENDER", "GOALKEEPER")]
        if not defenders:
            return 0
        return sum(player.get_effective_defense() for player in defenders)/len(defenders)
    
    def execute_substitution(self,player_out, player_in):
        if player_out not in self.active_lineup:
            raise ValueError(f"{player_out.name} is not in the active lineup.")
        if player_in not in self.bench:
            raise ValueError(f"{player_in.name} is not on the bench.")
        if self.remaining_substitutions <= 0:
            raise ValueError("No substitutions remaining.")

    # Perform the substitution
        self.active_lineup.remove(player_out)
        self.bench.append(player_out)
        self.bench.remove(player_in)
        self.active_lineup.append(player_in)
        self.remaining_substitutions -= 1

class MatchEvent:
    def __init__(self, event_id, event_type,minute, team, player, outcome_text):
        self.event_id = event_id
        self.event_type = event_type
        self.minute = minute
        self.team = team
        self.player = player
        self.outcome_text = outcome_text
    def to_string(self):
        return f"Event ID: {self.event_id}, Type: {self.event_type}, Minute: {self.minute}, Team: {self.team.country_name}, Player: {self.player.name}, Outcome: {self.outcome_text}"


class Match:
    Valid_Phases = ["REGULATION", "FINISHED"]
    def __init__(self, home_team, away_team, current_minute, timeline, phase):
        self.home_team = home_team
        self.away_team = away_team
        self.home_score = 0
        self.away_score = 0
        self.current_minute = current_minute
        self.timeline = timeline
        if phase not in self.Valid_Phases:
            raise ValueError(f"Invalid phase. Choose from {self.Valid_Phases}")
        self.phase = phase

    def run_minute_tick(self):
        self.current_minute += 1
        
        for player in self.home_team.active_lineup:
            player.deplete_stamina(0.5)
        for player in self.away_team.active_lineup:
            player.deplete_stamina(0.5)
        self.process_goal_attempt(self.home_team, self.away_team)
        self.process_goal_attempt(self.away_team, self.home_team)
        
    def process_goal_attempt(self, attacking_team, defending_team):
         if random() < 0.10:  # 10% chance a genuine attempt occurs this minute
            attack_strength = attacking_team.get_aggregate_attack() * uniform(0.75, 1.25)
            defense_strength = defending_team.get_aggregate_defense() * 1.3 * uniform(0.80, 1.20)
            if attack_strength > defense_strength:
               self.record_goal(attacking_team)
               
    def record_goal(self, scoring_team):
        event_id = len(self.timeline) + 1
        event_type = "GOAL"
        minute = self.current_minute
        attackers = [p for p in scoring_team.active_lineup if p.position in ("FORWARD", "MIDFIELDER")]
        player = choice(attackers) if attackers else scoring_team.active_lineup[0]
        if scoring_team == self.home_team:
            self.home_score += 1
        else:
            self.away_score += 1
        outcome_text = f"Goal scored by {player.name} for {scoring_team.country_name}"
        goal_event = MatchEvent(event_id, event_type, minute, scoring_team, player, outcome_text)
        self.timeline.append(goal_event)        
        
def build_team(country_name):
    """Helper: builds a 26-player roster with a position-balanced
    11-player active lineup (1 GK, 4 DEF, 4 MID, 2 FWD) and 15-player bench."""
    positions_11 = (
        ["GOALKEEPER"] +
        ["DEFENDER"] * 4 +
        ["MIDFIELDER"] * 4 +
        ["FORWARD"] * 2
    )
    positions_bench = (
        ["GOALKEEPER"] +
        ["DEFENDER"] * 5 +
        ["MIDFIELDER"] * 5 +
        ["FORWARD"] * 4
    )

    active_lineup = [
        Player(f"{country_name}_Starter{i+1}", pos, base_attack=70, base_defense=70)
        for i, pos in enumerate(positions_11)
    ]
    bench = [
        Player(f"{country_name}_Bench{i+1}", pos, base_attack=65, base_defense=65)
        for i, pos in enumerate(positions_bench)
    ]
    roster = active_lineup + bench

    return Team(
        country_name=country_name,
        roster=roster,
        active_lineup=active_lineup,
        bench=bench,
        remaining_substitutions=5,
    )


def main():
    home_team = build_team("ARG")
    away_team = build_team("FRA")

    match = Match(
        home_team=home_team,
        away_team=away_team,
        current_minute=0,
        timeline=[],
        phase="REGULATION",
    )

    for _ in range(90):
        match.run_minute_tick()

    match.phase = "FINISHED"

    print(f"\nFinal Score: {home_team.country_name} {match.home_score} - {match.away_score} {away_team.country_name}")
    if match.home_score > match.away_score:
        print(f"Result: {home_team.country_name} wins!")
    elif match.away_score > match.home_score:
        print(f"Result: {away_team.country_name} wins!")
    else:
        print("Result: DRAW")

    print("\nMatch Timeline:")
    if not match.timeline:
        print("  No goals scored.")
    for event in match.timeline:
        print(" ", event.to_string())


if __name__ == "__main__":
    main()