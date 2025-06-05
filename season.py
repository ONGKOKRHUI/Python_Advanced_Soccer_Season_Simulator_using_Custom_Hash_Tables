from __future__ import annotations
from data_structures.array_set import ArraySet
from data_structures.referential_array import ArrayR
from data_structures.array_list import ArrayList
from enums import TeamGameResult
from game_simulator import GameSimulator, GameSimulationOutcome
from dataclasses import dataclass
from team import Team
from data_structures import *
from algorithms import mergesort

@dataclass
class Game:
    """
    Simple container for a game between two teams.
    Both teams must be team objects, there cannot be a game without two teams.

    Note: Python will automatically generate the init for you.
    Use Game(home_team: Team, away_team: Team) to use this class.
    See: https://docs.python.org/3/library/dataclasses.html

    Do not make any changes to this class.
    """
    home_team: Team = None
    away_team: Team = None


class WeekOfGames:
    """
    Simple container for a week of games.

    A fixture must have at least one game.
    """

    def __init__(self, week: int, games: ArrayR[Game] | ArrayList[Game]) -> None:
        """
        Container for a week of games.

        Args:
            week (int): The week number.
            games (ArrayR[Game]): The games for this week.
        
        No complexity analysis is required for this function.
        Do not make any changes to this function.
        """
        self.games = games
        self.week: int = week

    def __iter__(self):
        """
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
            Explanation:
            - the best and worst case complexity are the same
            - assignment operation of _current and return of self are constant time, O(1)
        """
        self._current = 0
        return self

    def __next__(self):
        """
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
            Explanation: 
            - the best and worst case complexity are the same
            - getitem operation of ArrayR is O(1)
            - comparison between integers and increment and return statements are considered constant time, O(1)
            - raise exception is considered constant time, O(1)
        """
        if self._current < len(self.games):
            game = self.games[self._current]
            self._current += 1
            return game
        else:
            raise StopIteration


class Season:

    def __init__(self, teams: ArrayR[Team] | ArrayList[Team]) -> None:
        """
        Initializes the season with a schedule.

        Args:
            teams (ArrayR[Team]): The teams played in this season.

        Complexity:
            Best Case Complexity: O(N + N + NlogN + N^2 + 2W) = O(N^2), where N is len(teams) or len(self.teams) or len(self.leaderboard)
              comp(object) is the complexity of object.__le__ between Team objects,
              W is the number of games week in schedule
            Worst Case Complexity: O(K + K + NlogN*S + N^2 + 2W) = O(N^2 + NlogN*S), where N is len(teams) or len(self.teams) or len(self.leaderboard)
              or len(self.leaderboard), S is comp(str) is the comparison between string objects of self.name and other.name
              which depends on the length of the string in __le__() in Teams, W is the number of games week in schedule
            Explanation:
            Both best and worst case:
            - the assignment of self.teams is constant time, O(1)
            - the initialisation of self.leaderboard is O(N) where N is the len(teams) from initialisation of ArraySortedList
              where it will need to assign len(teams) empty spaces to it
            - the for loop iterates N times where N is the len(self.teams)
            - the _generate_schedule is always O(N^2) complexity where n is the number of teams in the season
            - initialisation of schedule ArrayList allocated len(schedule) or number of games week value memory space, O(W)
            - the second for loop loops through the number of games week in schedule to set them to Week of Games object O(W)
            Best case:
            - the mergesort.mergesort(self.leaderboard) is O(NlogN) complexity where N is the number of teams in the season
              or len(self.leaderboard) as we assume that comparison happen between points of Team (int) is constant time O(1)
            Worst case:
            - the mergesort.mergesort(self.leaderboard) is O(NlogN*S) complexity where N is the number of teams in the season
              or len(self.leaderboard) as we assume that comparison happens between names of Team (str) is O(S)
            Assumption:
            - in the final worst case complexity, we retain the complexity NlogN*S because approaching infinity, practically
              the string length of team name will not be infinitely long BUT factually, it is not impossible to be very long,
              just like factually, the number of teams can be infinitely large as well.
            - we drop the complexity of W in the final complexity because the number of game weeks increases linearly 
              with number of teams so although we use W not N to represent it, its complexity is similar to O(N)
        """
        self.teams = teams
        self.leaderboard = ArrayList(len(teams))
        for team in self.teams:
            self.leaderboard.append(team)
        self.leaderboard = mergesort.mergesort(self.leaderboard)
        schedule = self._generate_schedule()
        self.schedule = ArrayList(len(schedule))
        for index, games_week in enumerate(schedule):
            self.schedule.append(WeekOfGames(index+1, games_week))

    def _generate_schedule(self) -> ArrayList[ArrayList[Game]]:
        """
        Generates a schedule by generating all possible games between the teams.

        Return:
            ArrayList[ArrayList[Game]]: The schedule of the season.
                The outer array is the weeks in the season.
                The inner array is the games for that given week.

        Complexity:
            Best Case Complexity: O(N^2) where N is the number of teams in the season.
            Worst Case Complexity: O(N^2) where N is the number of teams in the season.
        
        Do not make any changes to this function.
        """
        num_teams: int = len(self.teams)
        weekly_games: ArrayList[ArrayList[Game]] = ArrayList()
        flipped_weeks: ArrayList[ArrayList[Game]] = ArrayList()
        games: ArrayList[Game] = ArrayList()

        # Generate all possible matchups (team1 vs team2, team2 vs team1, etc.)
        for i in range(num_teams):
            for j in range(i + 1, num_teams):
                games.append(Game(self.teams[i], self.teams[j]))

        # Allocate games into each week ensuring no team plays more than once in a week
        week: int = 0
        while games:
            current_week: ArrayList[Game] = ArrayList()
            flipped_week: ArrayList[Game] = ArrayList()
            used_teams: ArraySet = ArraySet(len(self.teams))

            week_game_no: int = 0
            for game in games:
                if game.home_team.name not in used_teams and game.away_team.name not in used_teams:
                    current_week.append(game)
                    used_teams.add(game.home_team.name)
                    used_teams.add(game.away_team.name)

                    flipped_week.append(Game(game.away_team, game.home_team))
                    games.remove(game)
                    week_game_no += 1

            weekly_games.append(current_week)
            flipped_weeks.append(flipped_week)
            week += 1

        for flipped_week in flipped_weeks:
            weekly_games.append(flipped_week)
        
        return weekly_games

    def simulate_season(self) -> None:
        """
        Simulates the season.

        Complexity:
            Assume GameSimulator.simulate() is O(1)
            Remember to define your variables in your complexity.

            Best Case Complexity: O(W * G * (NlogN + S * 2(Q*(H*K + P) + T))) = O(W*G*(NlogN + S*(Q*(H*K + P) + T)))
                where W is the number of weeks in self.schedule, G is the number of games in each week, 
                N is the number of teams in self.leaderboard, S is the number of scorers in game_outcome.goal_scorers, 
                Q is len(PlayerPosition), H is position.value which is the key, K is the number of items in self.players 
                (number of linkedlist for positions) and P is the average length of self.players[position.value] LinkedList
                T is the average number of players in a team
            Worst Case Complexity: O(W * G * (NlogN*K + S * 2(Q*(H*K + P) + T))) = O(W*G*(NlogN*K + S*(Q*(H*K + P) + T)))
                where W is the number of weeks in self.schedule, G is the number of games in each week, 
                N is the number of teams in self.leaderboard, S is the number of scorers in game_outcome.goal_scorers,
                K is comp(str) is the comparison between string objects of self.name and other.name which depends on the length 
                of the string in __le__() in Team, Q is len(PlayerPosition), H is position.value which is the key, 
                K is the number of items in self.players (number of linkedlist for positions) and P is the average length of 
                self.players[position.value] LinkedList, T is the average number of players in a team
            Explanation:
            Both best and worst case:
            - the first for loop loops through the weeks in self.schedule, where W is the number of weeks (object) in self.schedule
            - the second for loop loops through the games in each week, where G is the number of games in each week
            - the GameSimulator.simulate() is O(1)
            - the third for loop loops through the scorers in game_outcome.goal_scorers, where S is the number of scorers in game_outcome.goal_scorers
            - the get_players() method is O(Q*(H*K + P)) and it obtains all players from a team
            - the for loop loops through the players in a team, where T is the average number of players in a team
              from home team and away team, O(T)
            - we assume all assignment operations and math operations are constant time, O(1)
            - we assume all comparison operations between integers are constant time, O(1)
            Best case:
            - the mergesort.mergesort(self.leaderboard) is O(NlogN) complexity where N is the number of teams in the season
              or len(self.leaderboard) as we assume that comparison happen between points of Team (int) is constant time O(1)
            Worst case:
            - the mergesort.mergesort(self.leaderboard) is O(NlogN*K) complexity where N is the number of teams in the season
              or len(self.leaderboard) as we assume that comparison happens between names of Team (str) is O(K)
            Assumptions:
            - the final complexity of best and worst case are simplified based on factual considerations as some of 
              these variables are practically bounded and not infinite in real world scenarios but factually they can be infinite
            - and since they do not relate are are independent from each other, their complexities are retained in 
              the final complexity.
        """
        for week in self.schedule:                                                      #O(W)
            for game in week:                                                           #O(G)
                game_outcome = GameSimulator.simulate(game.home_team, game.away_team)   #O(1)
                if game_outcome.home_goals > game_outcome.away_goals:                   #O(1)
                    game.home_team.add_result(TeamGameResult.WIN)                       #O(1)
                    game.away_team.add_result(TeamGameResult.LOSS)                      #O(1)
                elif game_outcome.home_goals < game_outcome.away_goals:                 #O(1)
                    game.home_team.add_result(TeamGameResult.LOSS)                      #O(1)
                    game.away_team.add_result(TeamGameResult.WIN)                       #O(1)
                else:
                    game.home_team.add_result(TeamGameResult.DRAW)                      #O(1)
                    game.away_team.add_result(TeamGameResult.DRAW)                      #O(1)
                self.leaderboard = mergesort.mergesort(self.leaderboard)                #O(NlogN)*comp(object)
                for scorer in game_outcome.goal_scorers:                                #O(S)
                    for player in game.home_team.get_players():                         #O(Q*(H*K + P)) + O(T)
                        if player.name == scorer:                                       #O(1)
                            player.goals += 1                                           #O(1)
                    for player in game.away_team.get_players():                         #O(Q*(H*K + P)) + O(T)
                        if player.name == scorer:                                       #O(1)
                            player.goals += 1                                           #O(1)

    def delay_week_of_games(self, orig_week: int, new_week: int | None = None) -> None:
        """
        Delay a week of games from one week to another.

        Args:
            orig_week (int): The original week to move the games from.
            new_week (int or None): The new week to move the games to. If this is None, it moves the games to the end of the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(N + N) = O(N), where N is the length of self.schedule
            Explanation:
            Both best and worst case:
            Best case:
            - in the best case, we obtain the original week from the last index of self.schedule
            - this causes delete_at_index to be O(1) as no shuffling of items is needed
            - Then new_week is None, which means we append the original week to the end of self.schedule
            Worst case:
            - in the worst case, we obtain the original week from the first index of self.schedule
            - this causes delete_at_index to be O(N) as shuffling of rest of the items in schedule is needed
            - Then new_week is the first week in self.schedule, which means we insert the original week to the first index of self.schedule
            - this causes insert to be O(N) as shuffling of rest of the items in schedule is needed
            Both the best and worst case are unlikely but possible as new week can be >= original week (Ed Forum #1309)
        """
        original_week = self.schedule.delete_at_index(orig_week-1)
        if new_week is not None:
            self.schedule.insert(new_week-1, original_week)
        else:
            self.schedule.append(original_week)

    def __len__(self) -> int:
        """
        Returns the number of teams in the season.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
            Explanation: 
            - best and worst case complexity are the same
            - the method simply returns length of self.teams using len() method for ArrayR() which is O(1)
        """
        return len(self.teams)

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the season object.

        Complexity:
            Analysis not required.
        """
        return ""

    def __repr__(self) -> str:
        """Returns a string representation of the Season object.
        Useful for debugging or when the Season is held in another data structure."""
        return str(self)
