import unittest
from unittest import TestCase

import inspect
import ast

from enums import PlayerPosition
from data_structures.referential_array import ArrayR
from tests.helper import take_out_from_adt, CollectionsFinder
from player import Player
from random_gen import RandomGen
from season import Season
from team import Team



class TestTask6Setup(TestCase):
    def setUp(self) -> None:
        RandomGen.set_seed(123)

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

        # Create random teams
        NUMBER_OF_TEAMS = 6
        NUMBER_OF_PLAYERS_PER_POSITION = 4

        self.teams: list[Team] = []
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
            self.teams.append(team)

        self.season = Season(ArrayR.from_list(self.teams))


class TestTask6(TestTask6Setup):
    def test_simulate_season(self):
        """
        #name(Test simulating the season doesn't raise any exceptions)
        """
        # Just check the code runs with no exception
        try:
            self.season.simulate_season()
        except Exception as e:
            self.fail(f"simulate_season() didn't finish properly, it raised an exception: {e}")

    def test_simulate_season_winner(self):
        """
        #name(Test simulating the season and getting the winner)
        """
        self.season.simulate_season()

        winner = take_out_from_adt(self.season.leaderboard)[0]

        self.assertIsInstance(winner, Team, "First team in the leaderboard is not a Team object")
        self.assertEqual(
            winner.name,
            "Dragons",
            "The winner of the season is not correct"
        )

    def test_team_players_grouped_by_position(self):
        for team in self.teams:
            for position in PlayerPosition:
                players = team.get_players(position)
                self.assertEqual(len(players), 4, f"{team.name} should have 4 players in position {position.name}")

    def test_team_game_history_length_respected(self):
        self.season.simulate_season()
        for team in self.teams:
            history = team.get_history()
            if history is not None:
                self.assertLessEqual(len(history), team.history_length, f"{team.name} has too many history entries")

    def test_teams_played_games(self):
        self.season.simulate_season()
        for team in self.teams:
            self.assertIsNotNone(team.get_history(), f"{team.name} did not play any games")
            self.assertGreater(len(team.get_history()), 0, f"{team.name} has empty history after season")

    def test_leaderboard_sorted_by_points(self):
        self.season.simulate_season()
        leaderboard = take_out_from_adt(self.season.leaderboard)
        for i in range(1, len(leaderboard)):
            prev, curr = leaderboard[i - 1], leaderboard[i]
            self.assertTrue(prev.points >= curr.points, f"Leaderboard is not sorted: {prev.name} before {curr.name}")

    def test_no_duplicate_player_names(self):
        names = set()
        for team in self.teams:
            for player in team.get_players():
                self.assertNotIn(player.name, names, f"Duplicate player name found: {player.name}")
                names.add(player.name)


class TestTask6Approach(TestTask6Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import season
        modules = [season]

        for f in modules:
            # Get the source code
            f_source = inspect.getsource(f)
            filename = f.__file__

            tree = ast.parse(f_source)
            visitor = CollectionsFinder(filename)
            visitor.visit(tree)

            # Report any failures
            for failure in visitor.failures:
                self.fail(failure[3])

if __name__ == "__main__":
    unittest.main()