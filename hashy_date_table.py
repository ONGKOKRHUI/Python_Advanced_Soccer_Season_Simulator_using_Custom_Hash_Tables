"""
This module implements the `HashyDateTable`, a specialized hash table
designed to work with date strings as keys.

It inherits from `LinearProbeTable` and features a custom hash function
that intelligently parses date strings in various formats (e.g., YYYY/MM/DD,
DD-MM-YYYY). This tailored function ensures a uniform distribution of date
keys across the table, minimizing collisions and maintaining performance.
"""

from __future__ import annotations

from data_structures.hash_table_linear_probing import LinearProbeTable


class HashyDateTable(LinearProbeTable[str]):
    """
    HashyDateTable assumed the keys are strings representing dates, and therefore tries to
    produce a balanced, uniform distribution of keys across the table.

    Conflicts are resolved using Linear Probing.
    
    All values will also be strings.
    """
    def __init__(self) -> None:
        """
        Initialise the Hash Table with with increments of 366 as the table size.
        This means, initially we will have 366 slots, once they are full, we will have 4 * 366 slots, and so on.

        No complexity is required for this function.
        Do not make any changes to this function.
        """
        LinearProbeTable.__init__(self, [366, 4 * 366, 16 * 366])

    def hash(self, key: str) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.
        The key will always be exactly 10 characters long and can be any of these formats, but nothing else:
        - DD/MM/YYYY
        - DD-MM-YYYY
        - YYYY/MM/DD
        - YYYY-MM-DD

        The function assumes the dates will always be valid i.e. the input will never be something like 66/14/2020.
        
        Complexity:
        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        Explanation:
        - The hash function has a time complexity of O(1) in both the best and worst cases 
        - because it operates on a fixed-length input size (10-character date strings)
        - it only performs constant-time operations like slicing of strings with CONSTANT number of characters, 
          integer conversion, arithmetic calculations, and tuple lookups.
        - comparison operation done between characters in the string is constant time.
        - comparison operation done between integers is constant time. 
        - all steps are deterministic and bounded, regardless of the input format.
        - in short, because the key is constant format (10 char), the input is constant and thus the function is O(1)
        """
        DAYS_IN_YEAR = 366
        MIN_YEAR = 1970
        non_leap_cumulative = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)
        leap_cumulative = (0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335)
        if key[4] in ('/', '-'):
            year = int(key[0:4])
            month = int(key[5:7]) 
            day = int(key[8:10])
        else:
            day = int(key[0:2])
            month = int(key[3:5])
            year = int(key[6:10])
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            cumulative = leap_cumulative
        else:
            cumulative = non_leap_cumulative
        day_of_year = cumulative[month - 1] + day
        table_years = int(self.table_size / DAYS_IN_YEAR)
        year_offset = (year-MIN_YEAR) % table_years
        base_index = day_of_year -1
        position = base_index * table_years + year_offset
        return position
