from unittest import TestCase

from data_structures.referential_array import ArrayR
from player import Player
from random_gen import RandomGen
from season import Season
from team import Team
from enums import PlayerPosition
from tests.helper import take_out_from_adt

class TestTask6FullSeason(TestCase):

    def test_multiple_seeds_simulate_season(self) -> None:
        team_win_counts = {}

        first_names = [
            "John", "Jane", "Alice", "Bob", "Charlie", "David",
            "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy",
            "Mallory", "Niaj", "Olivia", "Peggy", "Robert", "Sybil",
            "Trent", "Uma", "Victor", "Walter", "Xena", "Yara", "Zane"
        ]
        last_names = [
            "Smith", "Johnson", "Williams", "Jones", "Brown",
            "Davis", "Miller", "Wilson", "Moore", "Taylor",
            "Anderson", "Thomas", "Jackson", "White", "Harris",
            "Martin", "Thompson", "Garcia", "Martinez", "Robinson",
        ]
        team_names = [
            "Tornadoes", "Sharks", "Wolves", "Eagles", "Lions", "Dragons",
            "Panthers", "Bears", "Hawks", "Falcons", "Tigers", "Mustangs",
        ]

        for seed in range(1000):
            RandomGen.set_seed(seed)

            NUMBER_OF_TEAMS = 12
            NUMBER_OF_PLAYERS_PER_POSITION = 4

            teams: list[Team] = []
            used_names = set()
            for i in range(NUMBER_OF_TEAMS):
                players = []
                for pos in PlayerPosition:
                    for _ in range(NUMBER_OF_PLAYERS_PER_POSITION):
                        player_name = f"{RandomGen.random_choice(first_names)} {RandomGen.random_choice(last_names)}"
                        while player_name in used_names:
                            player_name = f"{RandomGen.random_choice(first_names)} {RandomGen.random_choice(last_names)}"
                        used_names.add(player_name)
                        player = Player(player_name, pos, RandomGen.randint(18, 40))
                        players.append(player)
                team = Team(team_names[i], ArrayR.from_list(players), RandomGen.randint(5, 15))
                teams.append(team)

            season = Season(ArrayR.from_list(teams))

            try:
                season.simulate_season()
            except Exception as e:
                self.fail(f"Seed {seed}: simulate_season() raised an exception: {e}")

            winner = take_out_from_adt(season.leaderboard)[0]
            winner_name = winner.name

            if winner_name not in team_win_counts:
                team_win_counts[winner_name] = 0
            team_win_counts[winner_name] += 1

            print(f"Seed: {seed}, Winner: {winner_name}")

        print("\nFinal Win Counts:")
        for team_name, wins in team_win_counts.items():
            print(f"{team_name}: {wins}")

a = TestTask6FullSeason()
a.test_multiple_seeds_simulate_season()