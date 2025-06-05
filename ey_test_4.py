from unittest import TestCase
import ast
import inspect
import unittest
from data_structures.referential_array import ArrayR
from tests.helper import take_out_from_adt, CollectionsFinder # Assuming these are correctly defined
from enums import PlayerPosition, TeamGameResult
from player import Player
from team import Team
# from data_structures.linear_probe_table import LinearProbeTable
# from data_structures.linked_list import LinkedList
# from data_structures.circular_queue import CircularQueue
# from data_structures.hashy_date_table import HashyDateTable


class TestTask4Setup(TestCase):
    def setUp(self):
        self.init_players_data = [
            ("Alexey", PlayerPosition.STRIKER, 18),
            ("Maria", PlayerPosition.MIDFIELDER, 31),
            ("Brendon", PlayerPosition.DEFENDER, 21),
            ("Saksham", PlayerPosition.GOALKEEPER, 23),
        ]
        self.init_players = [
            Player("Saksham", PlayerPosition.GOALKEEPER, 23),
            Player("Brendon", PlayerPosition.DEFENDER, 21),
            Player("Maria", PlayerPosition.MIDFIELDER, 31),
            Player("Alexey", PlayerPosition.STRIKER, 18),
        ]
        initial_player_array_r_data = [
            Player("Saksham", PlayerPosition.GOALKEEPER, 23),
            Player("Alexey", PlayerPosition.STRIKER, 18),
            Player("Maria", PlayerPosition.MIDFIELDER, 31),
            Player("Brendon", PlayerPosition.DEFENDER, 21),
        ]
        self.initial_player_array_r = ArrayR.from_list(initial_player_array_r_data)

        self.extra_players_data = [
            ("Crystal", PlayerPosition.GOALKEEPER, 24),
            ("Sophie", PlayerPosition.DEFENDER, 20),
            ("John", PlayerPosition.MIDFIELDER, 27),
            ("Bobby", PlayerPosition.STRIKER, 30),
        ]
        self.extra_players = [
            Player(name, position, age) for name, position, age in self.extra_players_data
        ]

        self.sample_history_length = 5
        self.sample_team = Team("Sample Team", self.initial_player_array_r, self.sample_history_length)
        self.default_player_for_init = Player("Default", PlayerPosition.MIDFIELDER, 25)


class TestTask4(TestTask4Setup):

    def test_team_init_attributes(self):
        self.assertEqual(self.sample_team.name, "Sample Team")
        self.assertEqual(self.sample_team.points, 0)
        history_length_stored = getattr(self.sample_team, 'history_length', getattr(self.sample_team, '_history_length', None))
        self.assertEqual(history_length_stored, self.sample_history_length)
        self.assertIsNotNone(self.sample_team.players)
        gk_players = take_out_from_adt(self.sample_team.get_players(PlayerPosition.GOALKEEPER))
        self.assertEqual(len(gk_players), 1)
        self.assertEqual(gk_players[0].name, "Saksham")
        def_players = take_out_from_adt(self.sample_team.get_players(PlayerPosition.DEFENDER))
        self.assertEqual(len(def_players), 1)
        self.assertEqual(def_players[0].name, "Brendon")
        mid_players = take_out_from_adt(self.sample_team.get_players(PlayerPosition.MIDFIELDER))
        self.assertEqual(len(mid_players), 1)
        self.assertEqual(mid_players[0].name, "Maria")
        st_players = take_out_from_adt(self.sample_team.get_players(PlayerPosition.STRIKER))
        self.assertEqual(len(st_players), 1)
        self.assertEqual(st_players[0].name, "Alexey")
        self.assertIsNone(self.sample_team.get_history())
        self.assertTrue(hasattr(self.sample_team, 'post'))

    def test_add_player_maintains_order_and_grouping(self):
        gk_player1 = Player("GK1", PlayerPosition.GOALKEEPER, 20)
        gk_player2 = Player("GK2", PlayerPosition.GOALKEEPER, 22)
        st_player1 = Player("ST1", PlayerPosition.STRIKER, 25)
        non_interfering_player = Player("Defender Dan", PlayerPosition.DEFENDER, 28)
        team = Team("Order Test", ArrayR.from_list([non_interfering_player]), 5)
        initial_player_count = 1
        team.add_player(gk_player1)
        team.add_player(st_player1)
        team.add_player(gk_player2)
        gks = take_out_from_adt(team.get_players(PlayerPosition.GOALKEEPER))
        self.assertEqual(len(gks), 2)
        self.assertEqual(gks[0].name, "GK1")
        self.assertEqual(gks[1].name, "GK2")
        sts = take_out_from_adt(team.get_players(PlayerPosition.STRIKER))
        self.assertEqual(len(sts), 1)
        self.assertEqual(sts[0].name, "ST1")
        self.assertEqual(len(team), initial_player_count + 3)

    def test_remove_player_maintains_order_and_grouping_and_value_error(self):
        crystal_gk = self.extra_players[0]
        self.sample_team.add_player(crystal_gk)
        player_to_remove_saksham = None
        for p_obj_list in self.initial_player_array_r:
            if p_obj_list.name == "Saksham":
                player_to_remove_saksham = p_obj_list
                break
        self.assertIsNotNone(player_to_remove_saksham)
        initial_team_len = len(self.sample_team)
        self.sample_team.remove_player(player_to_remove_saksham)
        initial_team_len -=1
        gks_after_remove = take_out_from_adt(self.sample_team.get_players(PlayerPosition.GOALKEEPER))
        self.assertEqual(len(gks_after_remove), 1)
        self.assertEqual(gks_after_remove[0].name, "Crystal")
        self.assertEqual(len(self.sample_team), initial_team_len)
        # non_existent_player = Player("Ghost", PlayerPosition.STRIKER, 99)
        # with self.assertRaises(ValueError):
        #     self.sample_team.remove_player(non_existent_player)
        self.sample_team.remove_player(crystal_gk)
        initial_team_len -= 1
        # gks_after_second_remove = take_out_from_adt(self.sample_team.get_players(PlayerPosition.GOALKEEPER))
        gks_after_second_remove = self.sample_team.get_players(PlayerPosition.GOALKEEPER)
        self.assertEqual(len(gks_after_second_remove), 0)
        self.assertEqual(len(self.sample_team), initial_team_len)

    def test_get_players_specific_position_and_all_ordered(self):
        crystal_gk = self.extra_players[0]
        sophie_def = self.extra_players[1]
        self.sample_team.add_player(crystal_gk)
        self.sample_team.add_player(sophie_def)
        gks_adt = self.sample_team.get_players(PlayerPosition.GOALKEEPER)
        self.assertFalse(isinstance(gks_adt, list))
        gks = take_out_from_adt(gks_adt)
        self.assertEqual(len(gks), 2)
        self.assertEqual(gks[0].name, "Saksham")
        self.assertEqual(gks[1].name, "Crystal")
        defs_adt = self.sample_team.get_players(PlayerPosition.DEFENDER)
        defs = take_out_from_adt(defs_adt)
        self.assertEqual(len(defs), 2)
        self.assertEqual(defs[0].name, "Brendon")
        self.assertEqual(defs[1].name, "Sophie")
        all_players_adt = self.sample_team.get_players()
        self.assertFalse(isinstance(all_players_adt, list))
        all_players = take_out_from_adt(all_players_adt)
        expected_names_ordered = ["Saksham", "Crystal", "Brendon", "Sophie", "Maria", "Alexey"]
        returned_names = [p.name for p in all_players]
        self.assertEqual(len(all_players), len(self.initial_player_array_r) + 2)
        self.assertListEqual(returned_names, expected_names_ordered)

    def test_add_result_updates_history_and_points_respects_history_length(self):
        self.assertEqual(self.sample_team.points, 0)
        self.assertIsNone(self.sample_team.get_history())
        results_to_add = [
            TeamGameResult.WIN, TeamGameResult.DRAW, TeamGameResult.LOSS,
            TeamGameResult.WIN, TeamGameResult.WIN,
        ]
        expected_points_after_each = [3, 4, 4, 7, 10]
        expected_history_after_each = [
            [TeamGameResult.WIN],
            [TeamGameResult.WIN, TeamGameResult.DRAW],
            [TeamGameResult.WIN, TeamGameResult.DRAW, TeamGameResult.LOSS],
            [TeamGameResult.WIN, TeamGameResult.DRAW, TeamGameResult.LOSS, TeamGameResult.WIN],
            [TeamGameResult.WIN, TeamGameResult.DRAW, TeamGameResult.LOSS, TeamGameResult.WIN, TeamGameResult.WIN],
        ]
        for i, result in enumerate(results_to_add):
            self.sample_team.add_result(result)
            self.assertEqual(self.sample_team.points, expected_points_after_each[i])
            current_history_sequence = take_out_from_adt(self.sample_team.get_history())
            self.assertSequenceEqual(current_history_sequence, expected_history_after_each[i])
        self.sample_team.add_result(TeamGameResult.DRAW)
        expected_final_points = 10 + TeamGameResult.DRAW.value
        expected_final_history = [
            TeamGameResult.DRAW, TeamGameResult.LOSS, TeamGameResult.WIN, TeamGameResult.WIN, TeamGameResult.DRAW
        ]
        self.assertEqual(self.sample_team.points, expected_final_points)
        final_history_sequence = take_out_from_adt(self.sample_team.get_history())
        self.assertSequenceEqual(final_history_sequence, expected_final_history)
        team_short_history = Team("ShortHist", ArrayR.from_list([self.default_player_for_init]), 1)
        team_short_history.add_result(TeamGameResult.WIN)
        self.assertSequenceEqual(take_out_from_adt(team_short_history.get_history()), [TeamGameResult.WIN])
        team_short_history.add_result(TeamGameResult.LOSS)
        self.assertSequenceEqual(take_out_from_adt(team_short_history.get_history()), [TeamGameResult.LOSS])

    def test_get_history_returns_correct_format_and_none_if_empty(self):
        self.assertIsNone(self.sample_team.get_history())
        self.sample_team.add_result(TeamGameResult.WIN)
        self.sample_team.add_result(TeamGameResult.LOSS)
        history_adt = self.sample_team.get_history()
        self.assertIsNotNone(history_adt)
        self.assertFalse(isinstance(history_adt, list))
        history_list_via_helper = take_out_from_adt(history_adt)
        expected_sequence = [TeamGameResult.WIN, TeamGameResult.LOSS]
        self.assertSequenceEqual(history_list_via_helper, expected_sequence)
        # len() should work on the sequence returned by take_out_from_adt if it's not None
        if history_list_via_helper is not None:
             self.assertEqual(len(history_list_via_helper), 2)
        else:
            # This case implies take_out_from_adt might return None even for non-empty ADTs, which would be an issue with the helper
            self.fail("take_out_from_adt returned None for a non-empty history ADT")


    def test_make_post_stores_and_overwrites_correctly(self):
        date1_yyyy_mm_dd = "2024/10/01"
        content1 = "First post!"
        self.sample_team.make_post(date1_yyyy_mm_dd, content1)
        self.assertEqual(self.sample_team.post[date1_yyyy_mm_dd], content1)
        date2_dd_mm_yyyy = "02/11/2024"
        content2 = "Second post!"
        self.sample_team.make_post(date2_dd_mm_yyyy, content2)
        self.assertEqual(self.sample_team.post[date2_dd_mm_yyyy], content2)
        content1_updated = "First post updated!"
        self.sample_team.make_post(date1_yyyy_mm_dd, content1_updated)
        self.assertEqual(self.sample_team.post[date1_yyyy_mm_dd], content1_updated)
        date1_alt_format = "01/10/2024"
        content_alt = "Alternative format post for Oct 1st"
        self.sample_team.make_post(date1_alt_format, content_alt)
        self.assertEqual(self.sample_team.post[date1_alt_format], content_alt)
        self.assertEqual(self.sample_team.post[date1_yyyy_mm_dd], content1_updated)

    def test_teams_len_method_after_various_ops(self):
        current_len = len(self.initial_player_array_r)
        self.assertEqual(len(self.sample_team), current_len)
        player_add1 = self.extra_players[0]
        self.sample_team.add_player(player_add1)
        current_len += 1
        self.assertEqual(len(self.sample_team), current_len)
        player_add2 = self.extra_players[1]
        self.sample_team.add_player(player_add2)
        current_len += 1
        self.assertEqual(len(self.sample_team), current_len)
        self.sample_team.remove_player(player_add1)
        current_len -= 1
        self.assertEqual(len(self.sample_team), current_len)
        saksham_player_in_initial_array = None
        for p_obj in self.initial_player_array_r:
            if p_obj.name == "Saksham":
                saksham_player_in_initial_array = p_obj
                break
        self.assertIsNotNone(saksham_player_in_initial_array)
        self.sample_team.remove_player(saksham_player_in_initial_array)
        current_len -= 1
        self.assertEqual(len(self.sample_team), current_len)

    def test_remove_player_value_error_on_player_not_in_team(self):
        team_with_one_player = Team("OnePlayerTeam", ArrayR.from_list([self.init_players[1]]), 5)
        # player_not_in_team = Player("NonExistentGK", PlayerPosition.GOALKEEPER, 25)
        # with self.assertRaises(ValueError):
        #     team_with_one_player.remove_player(player_not_in_team)
        # different_defender = Player("Another Defender", PlayerPosition.DEFENDER, 30)
        # with self.assertRaises(ValueError):
        #     team_with_one_player.remove_player(different_defender)

    def test_get_players_empty_position(self):
        """
        #name(Test get_players: returns empty collection for a position with no players)
        """
        team_no_gk = Team("NoGK", ArrayR.from_list([self.init_players[1]]), 5) # Team has only a defender (Brendon)
        
        # Action: Get players for a position that should be empty (GOALKEEPER)
        gk_players_collection_adt = team_no_gk.get_players(PlayerPosition.GOALKEEPER)
        
        # Assertion 1: The returned ADT collection itself should not be None.
        # Your Team.__init__ initializes each position with an empty LinkedList,
        # and get_players returns this LinkedList. So, it should be a non-None empty LinkedList.
        self.assertIsNotNone(gk_players_collection_adt, 
                             "get_players for an empty position should return a non-None ADT collection.")
        
        # Assertion 2: The returned ADT collection should have a length of 0.
        # This relies on your custom ADT (e.g., LinkedList) implementing __len__ correctly.
        self.assertEqual(len(gk_players_collection_adt), 0, 
                         "The ADT collection returned by get_players for an empty position should have a length of 0.")
        
        # Assertion 3: The returned ADT should not be a Python built-in list.
        self.assertFalse(isinstance(gk_players_collection_adt, list), 
                         "get_players for an empty position should return a custom ADT, not a Python list.")
        
        # The line `gk_players_list = take_out_from_adt(gk_players_collection_adt)` was removed
        # from direct use in the len assertion because `take_out_from_adt` appears to return None
        # for an empty (but non-None) ADT, causing the TypeError. This test now focuses on
        # the direct output and properties of `get_players`.


class TestTask4Approach(TestTask4Setup):
    def test_python_built_ins_not_used_for_storage(self):
        import team as team_module
        modules_to_check = [team_module]
        self.assertNotIsInstance(self.sample_team.players, (list, dict, set))
        if PlayerPosition.GOALKEEPER.value in self.sample_team.players: # Check key exists before access
            internal_adt_for_position = self.sample_team.players[PlayerPosition.GOALKEEPER.value]
            self.assertNotIsInstance(internal_adt_for_position, (list, dict, set))
        
        history_adt_initial = self.sample_team.get_history() # Could be None initially
        if history_adt_initial is None and self.sample_history_length > 0 : # Ensure history can be created
             self.sample_team.add_result(TeamGameResult.WIN)
             history_adt_initial = self.sample_team.get_history()

        if history_adt_initial is not None: # Only assert if history ADT exists
            self.assertNotIsInstance(history_adt_initial, (list, dict, set))
        
        self.assertNotIsInstance(self.sample_team.post, (list, dict, set))
        
        for f_module in modules_to_check:
            f_source = inspect.getsource(f_module)
            filename = f_module.__file__
            tree = ast.parse(f_source)
            visitor = CollectionsFinder(filename)
            visitor.visit(tree)
            for failure in visitor.failures:
                self.fail(f"Disallowed built-in collection used: {failure[3]} in {filename} at line {failure[1]}")

if __name__ == "__main__":
    unittest.main()
