from __future__ import annotations

from data_structures.referential_array import ArrayR
from data_structures.abstract_hash_table import HashTable
from typing import TypeVar


V = TypeVar('V')

class DeletedItem:
    """
    a deleted item object which is used as a sentinel (label) to 
    represent a deleted item
    """
    pass

class LazyDoubleTable(HashTable[str, V]):
    """
    Lazy Double Table uses double hashing to resolve collisions, and implements lazy deletion.

    Feel free to check out the implementation of the LinearProbeTable class if you need to remind
    yourself how to implement the methods of this class.

    Type Arguments:
        - V: Value Type.
    """
    
    # No test case should exceed 1 million entries.
    TABLE_SIZES = (5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869)
    HASH_BASE = 31
    DELETED_ITEM = DeletedItem()
    def __init__(self, sizes = None) -> None:
        """
        No complexity analysis is required for this function.
        Do not make any changes to this function.
        """
        if sizes is not None:
            self.TABLE_SIZES = sizes

        self.__size_index = 0
        self.__array: ArrayR[tuple[str, V]] = ArrayR(self.TABLE_SIZES[self.__size_index])
        self.__length = 0
    
    @property
    def table_size(self) -> int:
        return len(self.__array)

    def __len__(self) -> int:
        """
        Returns the number of elements in the hash table
        """
        return self.__length

    def keys(self) -> ArrayR[str]:
        """
        Returns all keys in the hash table.
        
        If you need to use this function, you will probably need to update its
        implementation according to how you implemented the lazy deletion.

        :complexity: O(N) where N is the table size.
        """
        res = ArrayR(self.__length)
        i = 0
        for x in range(self.table_size):
            if self.__array[x] is not None and self.__array[x] is not self.DELETED_ITEM: 
                res[i] = self.__array[x][0]
                i += 1
        return res

    def values(self) -> ArrayR[V]:
        """
        Returns all values in the hash table.

        If you need to use this function, you will probably need to update its
        implementation according to how you implemented the lazy deletion.

        :complexity: O(N) where N is the table size.
        """
        res = ArrayR(self.__length)
        i = 0
        for x in range(self.table_size):
            if self.__array[x] is not None and self.__array[x] is not self.DELETED_ITEM:
                res[i] = self.__array[x][1]
                i += 1
        return res

    def __contains__(self, key: str) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See __getitem__.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: str) -> V:
        """
        Get the value at a certain key

        :complexity: See hashy probe.
        :raises KeyError: when the key doesn't exist.
        """
        position = self.__hashy_probe(key, False)
        return self.__array[position][1]
    
    def is_empty(self) -> bool:
        return self.__length == 0
    
    def __str__(self) -> str:
        """
        Returns all they key/value pairs in our hash table (no particular
        order).
        """
        result = ""
        for item in self.__array:
            if item is not None and item is not self.DELETED_ITEM:
                (key, value) = item
                result += "(" + str(key) + "," + str(value) + ")\n"
        return result

    def hash(self, key: str) -> int:
        """
        Hash a key for insert/retrieve/update into the hashtable.
        :complexity: O(K) where K is the length of the key.
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: str) -> int:
        """
        Used to determine the step size for our hash table.

        Complexity:
            Best Case Complexity: O(logN) --> O(1), where N is min(n,m) where n is table_size and m is value of step_size
            Worst Case Complexity:O(A * logN) --> O(1), where N is min(n,m) where n is table_size, m is value of step_size,
                and A is the number of increments needed to find a co-prime candidate.
            Explanation:
            Both best and worst case:
            - The calculation of initial step_size using ord() and arithmetic modulo and subtraction are O(1)
            - assignment, increment and comparison operations in the outer and inner while loops are O(1)
            Best case:
            - best case happens when the initial candidate is already co-prime with table_size.
            - Thus the outer while loop which finds a co-prime candidate loops only once.
            - the best case complexity is dominated by one GCD calculation which takes O(log(min(n, m))) time complexity
            Worst case:
            - The worst case complexity happens when the initial candidate is not co-prime with table_size.
            - and the outer while loop which finds a co-prime candidate loops A times (increments A times)
            - Each increment requires a GCD calculation which is O(log(min(n, m))) time complexity.
            Assumption: #977 (Ed forum)
            - all computations for coprime including GCD are assigned to constant time for readability moving forward
        """
        h = 71
        step_size = h - (ord(key[0]) % h)
        coprime = False
        #using GCD method to find a co-prime
        while not coprime:
            x, y = self.table_size, step_size
            while y != 0:
                x, y = y, x % y
            if x == 1:
                coprime = True
            else:
                step_size += 1
        return step_size


    def __hashy_probe(self, key: str, is_insert: bool) -> int:
        """
        Find the correct position for this key in the hash table using hashy probing.

        Raises:
            KeyError: When the key is not in the table, but is_insert is False.
            RuntimeError: When a table is full and cannot be inserted.

        Complexity:
            Best Case Complexity: O(K) where K is the length of the key, 
            Worst Case Complexity: O(K + P*K) = O(P*K) where K is the length of the key, 
                P is the number of items in the table
            Explanation:
            Both best and worst case:
            - the position is determined using hash() method which has complexity O(K)
              where K is the length of key
            - raising Runtime and Key errors are considered constant time O(1)
            Best case:
            - in the for loop, the first position in the array is None or DeletedItem object
            - and the is_insert is True which is inserting an item in the hash table, O(1)
            - so the for loop iterates only once O(1)
            Worst case:
            - the for loop loops until the last position in the array to search for an item that does not
              exist in the hash table using an invalid key
            - causing the for loop to iterate P times O(P) where P is the number of items in the table
            - each iteration require comparison between a key and a key in the hash table
            - which has complexity O(K) where K is the average length of the key
        """
        # Initial position
        position = self.hash(key)
        stepsize = self.hash2(key)

        for _ in range(self.table_size):
            if self.__array[position] is None or self.__array[position] is self.DELETED_ITEM:
                if is_insert:
                    return position
                elif self.__array[position] is None:
                    raise KeyError(key)
            elif self.__array[position][0] == key:
                return position
            position = (position + stepsize) % self.table_size

        if is_insert:
            raise RuntimeError("Table is full!")
        else:
            raise KeyError(key)

    def __setitem__(self, key: str, data: V) -> None:
        """
        Set a (key, value) pair in our hash table.

        Remember! This is where you will need to call __rehash if the table is full!
        
        Complexity:
            Best Case Complexity: O(K) where K is the length of the key, 
            Worst Case Complexity: O(P*K + P^2*K) = O(P^2*K) where
                - P is the number of items in the table, K is the length of the key 
            Explanation: 
            Both best and worst case:
            - after the position is found, the comparison operation to None and DeletedItem class is assumed to be O(1)
            - the increment of length and __setitem__ operation in ArrayR are also considered O(1)
            Best case:
            - The best case complexity happens when no rehash is needed, and the position is found using best case complexity
              of __hashy_probe method, which is O(K)
            - this happens when items can be inserted immediately after being hashed with no probing needed
            Worst case:
            - The worst case happens the rehash method is called to resize the array, which is O(P^2*K)
              and the position is found using the worst case complexity of the hashy proble method which is O(P*K)
            - happens when we hash the key but the position is taken and we have to
              search the entire table. For each position, we have to check if the key is equal to the one in the table,
              hence the K factor.
        """ 
        position = self.__hashy_probe(key, True)
        if self.__array[position] is None or self.__array[position] is self.DELETED_ITEM: # New item
            self.__length += 1
        self.__array[position] = (key, data)
        if self.__length/self.table_size >= 2/3:
            self.__rehash()

    def __delitem__(self, key: str) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        Complexity:
            Best Case Complexity: O(K), where K is the length of the key, 
            Worst Case Complexity: O(P*K), where K is the length of the key, and P is the number of items in the table
            Explanation:
            Both best and worst case:
            - after finding the position to delete, assignment operation of DeletedItem is considered constant time O(1)
            - Decrement of length is considered constant time O(1)
            Best case:
            - The best case happends when hashy_probe() method has the best complexity O(K)
            - happens when all items can be deleted immediately after being hashed with no probing needed
            Worst case:
            - The worst case happens when hashy_probe() method has the worst complexity O(P*K)
            - happens when we hash the key but the position is taken and we have to
              search the entire table. For each position, we have to check if the key is equal to the one in the table,
              hence the K factor.
        """
        pos = self.__hashy_probe(key, False)
        self.__array[pos] = self.DELETED_ITEM
        self.__length -= 1

    def __rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        Complexity:
            Best Case Complexity: O(1) 
            Worst Case Complexity: O(B + P^2*K)) = O(P^2*K), where B is the value of self.TABLE_SIZES[self.__size_index],
                K is the length of the key, P is the number of items in the table            
            Explanation: 
            Both best and worst case:
            - assignment operation and increment/decrement operations are considered constant time O(1)
            Best case:
            - the best case happens when the the size index reaches the last index in TABLE_SIZES
            - in this case, the table cannot be resized further and returns, so the complexity is O(1)
            Worst case:
            - a new array is initialised and allocated empty spaces equal to the value of the next size index in TABLE_SIZES,
              which is O(B) where B is self.TABLE_SIZES[self.__size_index]
            - The for loop copies items in the old array which are not None and DeletedItem object,
              which is O(P) where P is the number of items in the table
            - inside each for loop iteration, self[key] (set item) is called
            - here we take O(P^2*K) which is the worst case complexity of __setitem__ without rehashing
            - the size of the new array will not be 2/3 full when items are copied from the old array to it so the
              worst case of setitem will not happen.
            This analysis is assuming the default table sizes are used, and thus the
                cost of creating a new table is constant. This assumption can be extended to any table size
                as long as the sizes are growing by a constant factor (e.g. each table size is almost double the previous one).
            Assumption: #1042 All possible conditions are taken into consideration including edge cases like best case
        """
        old_array = self.__array
        self.__size_index += 1
        if self.__size_index == len(self.TABLE_SIZES):
            #cannot be resized further.
            self.__size_index -= 1
            return
        self.__array = ArrayR(self.TABLE_SIZES[self.__size_index])
        self.__length = 0
        for item in old_array:
            if item is not None and item is not self.DELETED_ITEM:
                key, value = item
                self[key] = value