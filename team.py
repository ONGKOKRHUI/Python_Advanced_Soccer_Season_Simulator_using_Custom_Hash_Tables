from __future__ import annotations

from data_structures.referential_array import ArrayR
from enums import TeamGameResult, PlayerPosition
from player import Player
from typing import Collection, TypeVar
from data_structures import *
from hashy_date_table import HashyDateTable

T = TypeVar("T")


class Team:
    def __init__(self, team_name: str, initial_players: ArrayR[Player], history_length: int) -> None:
        """
        Constructor for the Team class

        Args:
            team_name (str): The name of the team
            initial_players (ArrayR[Player]): The players the team starts with initially
            history_length (int): The number of `GameResult`s to store in the history

        Returns:
            None

        Complexity:
            Best Case Complexity: O(A*K + B*K + C) = O(A*K + B*K + C), where A is len(PlayerPosition), K is value of position.value (key),
              B is len(initial_players) and C is history_length
            Worst Case Complexity: O(A*N*K + B*N*K + C) = O(A*N*K + B*N*K + C), where A is len(PlayerPosition), K is value of position.value (key),
              B is len(initial_players) and C is history_length, N is number of items in self.players
            Explanation: 
            Both best and worst case:
            - assignment operation for team_name is considered constant time O(1)
            - initialisation of players is considered constant time O(1)
            - initialisation of points and post are considered constant time O(1)
            - the initialisation of self.results is O(history_length) or O(C) as the Circular Queue is initialised with capacity history_length
            Best case:
            - in the best case complexity, we assume the setitem operation is always best case which is O(K)
              happens when we hash the key and the position is empty
            - thus in the first for loop, with A iterations where A is the length of PlayerPosition, the best case complexity is O(A*K)
            - in the second for loop, with B iterations where B is the length of initial_players, the best case complexity is O(B*K)
            Worst case:
            - in the worst case complexity, we assume the setitem operation is always worst case which is O(N*K)
              happens when we hash the key but the position is taken and we have to search the entire table.
              For each position, we have to check if the key is equal to the one in the table, hence the K factor.
            - thus in the first for loop, with A iterations where A is the length of PlayerPosition, the worst case complexity is O()
            - in the second for loop, with B iterations where B is the length of initial_players, the worst case complexity is O(B*N*K)
            Assumptions: #1191 #1520 (Ed Forum)
        """
        self.name = team_name
        self.players = LinearProbeTable() 
        for position in PlayerPosition:   
            self.players[position.value] = LinkedList() 
        for player in initial_players:  
            self.players[player.position.value].append(player)  
        self.points = 0
        self.history_length = history_length
        self.results = CircularQueue(history_length) 
        self.post = HashyDateTable()  

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the team.

        Args:
            player (Player): The player to add

        Returns:
            None

        Complexity:
            Best Case Complexity: O(K), where K is the length of key
            Worst Case Complexity: O(N*K), where N is the number of items in self.players and K is the length of key
            - assignment operation for key is considered constant time O(1)
            - append() method is considered constant time O(1)
            - in the best case complexity, we assume the getitem operation is always best case which is O(K)
              happens when we hash the key and the position is empty.
            - in the worst case complexity, we assume the getitem operation is always worst case which is O(N*K)
              happens when we hash the key but the position is taken and we have to
              search the entire table. For each position, we have to check if the key is equal to the one in the table,
              hence the K factor.
        """
        key = player.position.value
        self.players[key].append(player)

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the team.

        Args:
            player (Player): The player to remove

        Returns:
            None

        Complexity:
            Best Case Complexity: O(K + P), where P is is the length of self.players[key] LinkedList, len(ll),
             K is the length of key
            Worst Case Complexity: O(N*K + P^2), where P is is the length of self.players[key] LinkedList, len(ll),
             N is number of items in self.players and K is the length of key
            Explanation:
            Both best and worst case:
            - assignment operation for key is considered constant time O(1)
            - the for loop loops through the linked list len(ll) times, O(P)
            Best case:
            - in the best case complexity, we assume the getitem operation is always best case which is O(K)
              happens when we hash the key and the position is empty.
            - we assume the delete_at_index() method is always best case which is O(1) - removing item at index 1
              and do not have to traverse the linked list
            Worst case:
            - in the worst case complexity, we assume the getitem operation is always worst case which is O(N*K)
              happens when we hash the key but the position is taken and we have to
              search the entire table. For each position, we have to check if the key is equal to the one in the table,
              hence the K factor.
            - we assume the delete_at_index() method is always worst case which is O(P) - removing item at the last index
              and have to traverse to it
        """
        key = player.position.value
        ll = self.players[key]
        for i, p in enumerate(ll):
            if player.name == p.name:
                ll.delete_at_index(i)

    def get_players(self, position: PlayerPosition | None = None) -> Collection[Player]:
        """
        Returns the players of the team that play in the specified position.
        If position is None, it should return ALL players in the team.
        You may assume the position will always be valid.
        Args:
            position (PlayerPosition or None): The position of the players to return

        Returns:
            Collection[Player]: The players that play in the specified position
            held in a valid data structure provided to you within
            the data_structures folder.
            
            This includes the ArrayR, which was previously prohibited.

        Complexity:
            Best Case Complexity: O(K), where K is the length of key
            Worst Case Complexity: O(M * (N*K + P)), where M is len(PlayerPosition), 
              K is position.value which is the key, N is the number of items in self.players and P is the average length of 
              self.players[position.value] LinkedList
            Explanation:
            Both best and worst case:
            - we assume all assignment, return and comparison between integer operations are considered constant time O(1)
            - initialisation of players LinkedList() is considered constant time, O(1)
            Best case:
            - in the best case complexity, the position is not none
            - the getitem method for players is considered best case which is O(1)
            - happens when we hash the key and the position is empty, O(K)
            - and len(self.players) is 0 which returns None, O(1)
            Worst case:
            - in the worst case complexity, the position is not none, and len(self.players) is not 0,
            - the outer for loop with M iterations where M is the length of PlayerPosition
            - the __getitem__() method is considered worst case which is O(N*K)
            -  happens when we hash the key but the position is taken and we have to
              search the entire table. For each position, we have to check if the key is equal to the one in the table,
              hence the K factor
            - the inner for loop with P iterations where P is the average length of self.players[position.value] LinkedList
            Assumption: 
            - in this case, for the worst case complexity, it cannot be further simplified as the variables
              are independent from one another
        """
        if position is not None:
            players = self.players[position.value]
            return players
        else:
            players = LinkedList()
            for position in PlayerPosition:
                pos = self.players[position.value]
                if pos is not None:
                    for player in pos:
                        players.append(player)
            return players
        
    def add_result(self, result: TeamGameResult) -> None:
        """
        Add the `result` to this `Team`'s history

        Args:
            result (GameResult): The result to add
            
        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
            Explanation:
            - comparison operation between integers and increment operation of points are considered constant time, O(1)
            Best case:
            - in the best case complexity, the results has not reached the max capacity of history_length, if statement is False
            - append() method is considered constant time, O(1) as it only adds a new result to the end of Circular Queue
            Worst case:
            - in the worst case complexity, the results has reached the max capacity of history_length, if statement is True
            - The serve() method is considered constant time, O(1) as it only removes the first result from the Circular Queue
        """
        if len(self.results) == self.history_length:
            self.results.serve()
        self.results.append(result)
        self.points += result.value

    def get_history(self) -> Collection[TeamGameResult] | None:
        """
        Returns the `GameResult` history of the team.
        If the team has played less than this team's `history_length`,
        return all the result of all the games played so far.

        For example:
        If a team has only played 4 games and they have:
        Won the first, lost the second and third, and drawn the last,
        the result should be a container with 4 objects in this order:
        [GameResult.WIN, GameResult.LOSS, GameResult.LOSS, GameResult.DRAW]

        If this method is called before the team has played any games,
        return None the reason for this is explained in the specification.

        Returns:
            Collection[GameResult]: The most recent `GameResult`s for this team
            or
            None if the team has not played any games.

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
            Explanation:
            - comparison between integers len(self.results) and return statements are considered constant time
            - In the best case complexity, the results is empty, if statement is False and returns None, O(1)
            - In the worst case compelxity, the results is not empty and returns self.results, O(1)
        """
        return self.results if len(self.results) != 0 else None
    
    def make_post(self, post_date: str, post_content: str) -> None:
        """
        Publish a team blog `post` for a particular `post_date`.
       
        A `Team` can have one published post per day. Any duplicate
        posts should overwrite the original post for that day.
        
        Args:
            `post_date` (`str`) - The date of the post
            `post_content` (`str`) - The content of the post
        
        Returns:
            None

        Complexity:
            Best Case Complexity: O(K), where K is the length of key (post_date)
            Worst Case Complexity: O(N*K + N^2*K), where N is the number of items in self.post and K is the length of post_date key
            Explanation:
            - in the best case complexity, we assume the __setitem__() operation is always best case which is O(K)
              happens when we hash the key and the position is empty
            - in the worst case complexity, we assume the __setitem__() operation is always worst case which is O(N*K + N^2K)
              happens when we hash the key but the position is taken and we have to
              search the entire table. For each position, we have to check if the key is equal to the one in the table,
              hence the K factor.
              and then the load factor exceeds half of the table size and rehash is called which is O(N^2*K)
              we use the worst case of rehash which happens when all items need maximum probing to be inserted in the new table.
              This is assuming K here is representing an average key length, and is being used
              as the cost of comparing two keys as well as cost of hashing a key.
        """
        self.post[post_date] = post_content

    def __len__(self) -> int:
        """
        Returns the number of players in the team.

        Complexity:
            Best Case Complexity: O(P*K), where P is len(PlayerPosition) and k is the len(key)
            Worst Case Complexity: O(P*N*K), where P is the len(PlayerPosition),
              K is length of key which is position.value, N is the number of items in self.players and
            Explanation:
            - assignment, increment and return operation of sum are considered constant time O(1)
            Best case complexity:
            - in the best case, we consider the __setitem__ method called to be always best case which is O(K)
            - happens when we hash the key and the position is empty
            - the for loop with P iterations where P is the length of PlayerPosition
            Worst case complexity:
            - in the worst case, we consider the __setitem__ method to be always worst case which is O(K*N)
            - this happens when all items need maximum probing to be inserted in the new table.
              This is assuming K here is representing an average key length, and is being used
              as the cost of comparing two keys as well as cost of hashing a key.
            - the for loop with P iterations where P is the length of PlayerPosition
        """
        sum = 0
        for position in PlayerPosition:
            pos = self.players[position.value]
            if pos is not None:
                sum += len(pos)
        return sum

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the team object.

        Complexity analysis not required.
        """
        return self.name

    def __repr__(self) -> str:
        """Returns a string representation of the Team object.
        Useful for debugging or when the Team is held in another data structure.
        """
        return str(self)

    def __le__(self, other: Team) -> bool:
        """
        magic method to allow use of <less than or equal to> comparison operator between Team objects based on:
        1) the points of the team
        2) the alphabetical order of the team name
        
        Args:
            `other` (`Team`) - another Team object that is placed after the comparison operator
            eg) team1 > team2 - team2 is the other parameter
        
        Returns:
            bool: a boolean value that represents the truth value of the comparison between the Team objects

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(S), where S is comp(str) is the comparison between string objects of self.name and other.name
              which depends on the length of the string.
            Explanation:
            For both best and worst case:
            - the methods points() and name() are both constant time O(1)
            - return operations are constant time, O(1)
            Best case:
            - happens when self.points is not equal to other.points
            - comparison between self.points and other.points which are integers is constant time, O(1)
            Worst case:
            - happens when the points are equal and comparison between names happen.
            - the comparison between string object depends on the length of the string, comp(str) which we denote as O(S)
        """ 
        if self.points != other.points:
            return self.points > other.points
        else:
            return self.name < other.name