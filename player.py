"""
This module defines the `Player` class for the soccer simulation.

Each `Player` instance stores core information such as name, age, and position.
A key feature is its use of a `LinearProbeTable` to manage a dynamic set of
individual statistics (e.g., goals, tackles, assists), allowing for flexible
and efficient stat tracking.
"""

from __future__ import annotations
from enums import PlayerPosition
from data_structures import *
# Do not change the import statement below
# If you need more modules and classes from datetime, do not use
# separate import statements. Use them from datetime like this:
# datetime.datetime, or datetime.date, etc.
import datetime


class Player:

    def __init__(self, name: str, position: PlayerPosition, age: int) -> None:
        """
        Constructor for the Player class

        Args:
            name (str): The name of the player
            position (PlayerPosition): The position of the player
            age (int): The age of the player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
            Explanation: 
            Both best and worst case:
            - assignment operations for name, position and goals are considered constant time O(1)
            - datetime.datetime.now() is considered constant time O(1)
            - subtraction operation for age is considered constant time O(1)
            - initialisation of stats using LinearProbeTable() is considered constant time O(1)
        """
        self.name = name
        self.born_year = datetime.datetime.now().year - age
        self.position = position
        self.goals = 0
        self.stats = LinearProbeTable()

    def reset_stats(self) -> None:
        """
        Reset the stats of the player.
        
        This doesn't delete the existing stats, but resets them to 0.
        I.e. all stats that were previously set should still be available, with a value of 0.

        Complexity:
            Best Case Complexity: O(M + N*K), where M is the table size of self.stats and K is the length of key
                N is the number of items in self.stats
            Worst Case Complexity: O(M + N^2*K), where M is the table size of self.stats and K is the length of key
                N is the number of items in self.stats
            Explanation: 
            Both best and worst case:
            - self.stats.keys() is considered O(M) to loop through the entire table (array) to get all keys
            - the for loop loops through the keys which is O(N), where N is the number of items in self.stats
            Best case:
            - The best case happens when we assume each and every setitem operation uses best case complexity of linear_probe method
              which is O(K) 
              happens when we hash the key and the position is empty
            Worst case:
            - The worst case happens when we assume each and every setitem operation uses worst case complexity of linear_probe method
              which is O(N*K) 
              happens when we hash the key but the position is taken and we have to
              search the entire table. For each position, we have to check if the key is equal to the one in the table,
              hence the K factor.
            Assumption:
            - in this case we retain the complexity M as it is not dependent on any of the values of N and K 
        """
        for key in self.stats.keys():
            if key is not None:
                self.stats[key] = 0

    def __setitem__(self, statistic: str, value: int) -> None:
        """
        Set the given value for the given statistic for the player.

        Args:
            statistic (string): The key of the stat
            value (int): The value of the stat

        Complexity:
            Best Case Complexity: O(K), where K is the length of key
            Worst Case Complexity: O(N*K + N^2*K) = O(N^2*K), where N is the number of items in self.stats and K is the average length of key
            Explanation:
            - the method simply uses setitem method from LinearProbeTable class 
            - so the best case complexity is the best case complexity of setitem method which is O(K)
              happens when we hash the key and the position is empty
            - the worst case complexity is the worst case complexity of setitem method which is O(N*K + N^2*K)
              happens when we hash the key but the position is taken and we have to
              search the entire table. For each position, we have to check if the key is equal to the one in the table,
              hence the K factor.
              and then the load factor exceeds half of the table size and rehash is called which is O(N^2*K)
              we use the worst case of rehash which happens when all items need maximum probing to be inserted in the new table.
              This is assuming K here is representing an average key length, and is being used
              as the cost of comparing two keys as well as cost of hashing a key.
        """
        self.stats[statistic] = value

    def __getitem__(self, statistic: str) -> int:
        """
        Get the value of the player's stat based on the passed key.

        Args:
            statistic (str): The key of the stat

        Returns:
            int: The value of the stat

        Complexity:
            Best Case Complexity: O(K), where K is the length of key
            Worst Case Complexity: O(N*K), where N is the number of items in self.stats and K is the length of key
            Explanation: 
            - the method simply uses getitem method from LinearProbeTable class
            - so the best case complexity is the best case complexity of getitem method which is O(K)
              happens when we hash the key and the position is empty
            - the worst case complexity is the worst case complexity of getitem method which is O(N*K)
              happens when we hash the key but the position is taken and we have to
              search the entire table. For each position, we have to check if the key is equal to the one in the table,
              hence the K factor.
        """
        return self.stats[statistic]

    def get_age(self) -> int:
        """
        Get the age of the player

        Returns:
            int: The age of the player

        Complexity:
            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
            Explanation:
            - for both best and worst case complexity, subtraction operation between year (int) is considered constant time O(1)
            - datetime.datetime.now().year is considered constant time O(1)
        """
        return datetime.datetime.now().year - self.born_year

    def __str__(self) -> str:
        """
        Optional but highly recommended.

        You may choose to implement this method to help you debug.
        However your code must not rely on this method for its functionality.

        Returns:
            str: The string representation of the player object.

        Complexity Analysis not required.
        """
        return self.name

    def __repr__(self) -> str:
        """ String representation of the Player object.
        Useful for debugging or when the Player is held in another data structure.
        """
        return str(self)

