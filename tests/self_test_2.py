import unittest
from lazy_double_table import LazyDoubleTable, DeletedItem
from data_structures.referential_array import ArrayR


class TestLazyDoubleTableAdditional(unittest.TestCase):
    def setUp(self) -> None:
        self.step_table = LazyDoubleTable()
        self.sample_keys = ["key1", "key2", "A", "B", "123", "456", "SlightlyLongerKey"]
        # Table with custom sizes including non-prime numbers
        self.non_prime_step_table = LazyDoubleTable([6000, 8000, 10000])
        # Table with exactly the same sizes to test edge case of reaching max size
        self.fixed_sizes_table = LazyDoubleTable([5, 13])

    def test_hash2_returns_coprime(self):
        """Test if hash2 returns a value that is coprime with table_size"""
        for key in self.sample_keys:
            step_size = self.step_table.hash2(key)
            
            # Check that step_size is coprime with table_size
            def gcd(a, b):
                while b:
                    a, b = b, a % b
                return a
            
            self.assertEqual(gcd(self.step_table.table_size, step_size), 1, 
                            f"Step size {step_size} is not coprime with table size {self.step_table.table_size}")
            
            # Step size should be positive and less than table size
            self.assertGreater(step_size, 0, f"Step size {step_size} should be positive")

    def test_hash2_different_values(self):
        """Test if hash2 returns different values for different keys (at least sometimes)"""
        step_sizes = set()
        for key in self.sample_keys:
            step_sizes.add(self.step_table.hash2(key))
        
        # Most keys should produce different step sizes
        # We use len > 1 instead of expecting all different because hash collisions can happen
        self.assertGreater(len(step_sizes), 1, 
                          "Hash2 should produce different step sizes for different keys")

    def test_hash2_with_non_prime_table_size(self):
        """Test if hash2 still returns coprime values with non-prime table sizes"""
        for key in self.sample_keys:
            step_size = self.non_prime_step_table.hash2(key)
            
            # Check that step_size is coprime with table_size
            def gcd(a, b):
                while b:
                    a, b = b, a % b
                return a
            
            self.assertEqual(gcd(self.non_prime_step_table.table_size, step_size), 1, 
                            f"Step size {step_size} is not coprime with non-prime table size {self.non_prime_step_table.table_size}")

    def test_hashy_probe_insert(self):
        """Test if __hashy_probe correctly finds positions for insertion"""
        # We need to access a protected method, so we'll create a test helper class
        class TestableHashyProbe(LazyDoubleTable):
            def test_hashy_probe(self, key, is_insert):
                return self._LazyDoubleTable__hashy_probe(key, is_insert)
        
        table = TestableHashyProbe()
        
        # First position should be determined by hash function
        for key in self.sample_keys:
            position = table.test_hashy_probe(key, True)
            self.assertGreaterEqual(position, 0)
            self.assertLess(position, table.table_size)

    def test_hashy_probe_with_collision(self):
        """Test if __hashy_probe correctly handles collisions"""
        # Create a helper class to access private methods
        class TestableHashyProbe(LazyDoubleTable):
            def test_hashy_probe(self, key, is_insert):
                return self._LazyDoubleTable__hashy_probe(key, is_insert)
            
            def get_array(self):
                return self._LazyDoubleTable__array
        
        table = TestableHashyProbe()
        
        # Create a collision by manually setting a value at a position
        key1 = "test_key"
        position1 = table.hash(key1)
        array = table.get_array()
        array[position1] = ("collision_key", "collision_value")
        
        # Now probing for key1 should find a different position
        position2 = table.test_hashy_probe(key1, True)
        self.assertNotEqual(position1, position2, "Hashy probe should handle collisions")

    def test_hashy_probe_key_error(self):
        """Test if __hashy_probe raises KeyError for non-existent keys"""
        # Create a helper class to access private methods
        class TestableHashyProbe(LazyDoubleTable):
            def test_hashy_probe(self, key, is_insert):
                return self._LazyDoubleTable__hashy_probe(key, is_insert)
        
        table = TestableHashyProbe()
        
        # Try to get a non-existent key
        with self.assertRaises(KeyError):
            table.test_hashy_probe("non_existent_key", False)

    def test_hashy_probe_table_full(self):
        """Test if __hashy_probe raises RuntimeError when table is full"""
        # Create a table with small sizes
        class TestableHashyProbe(LazyDoubleTable):
            def test_hashy_probe(self, key, is_insert):
                return self._LazyDoubleTable__hashy_probe(key, is_insert)
            
            def get_array(self):
                return self._LazyDoubleTable__array
        
        # Use smallest possible table size
        table = TestableHashyProbe([5])
        array = table.get_array()
        
        # Fill every position in the table
        for i in range(5):
            array[i] = (f"key{i}", f"value{i}")
        
        # Now try to insert a new key
        with self.assertRaises(RuntimeError):
            table.test_hashy_probe("new_key", True)

    def test_setitem_updates_existing_item(self):
        """Test if __setitem__ correctly updates an existing item"""
        table = LazyDoubleTable()
        key = "test_key"
        table[key] = "original_value"
        
        # Update the value
        table[key] = "updated_value"
        
        # Check that the value was updated and length is still 1
        self.assertEqual(table[key], "updated_value")
        self.assertEqual(len(table), 1)

    def test_setitem_rehash_called(self):
        """Test if __setitem__ calls __rehash when load factor exceeds 2/3"""
        # Create a helper class to track rehash calls
        class TrackingTable(LazyDoubleTable):
            def __init__(self):
                super().__init__()
                self.rehash_called = False
            
            def _LazyDoubleTable__rehash(self):
                self.rehash_called = True
                super()._LazyDoubleTable__rehash()
        
        table = TrackingTable()
        
        # Calculate how many items to insert to exceed 2/3 load factor
        items_needed = int(table.table_size * 2/3) + 1
        
        # Insert items
        for i in range(items_needed):
            table[f"key{i}"] = f"value{i}"
        
        # Check that rehash was called
        self.assertTrue(table.rehash_called, "__rehash should be called when load factor exceeds 2/3")

    def test_delitem_lazy_deletion(self):
        """Test if __delitem__ correctly implements lazy deletion"""
        # Create a helper class to access private methods
        class TestableTable(LazyDoubleTable):
            def get_array(self):
                return self._LazyDoubleTable__array
        
        table = TestableTable()
        key = "test_key"
        table[key] = "test_value"
        
        # Delete the item
        del table[key]
        
        # Check that the item was marked as deleted
        array = table.get_array()
        position = table.hash(key)
        
        # Find where the item was stored
        found = False
        for i in range(table.table_size):
            if array[(position + i * table.hash2(key)) % table.table_size] is table.DELETED_ITEM:
                found = True
                break
        
        self.assertTrue(found, "Item should be marked as DeletedItem")
        self.assertEqual(len(table), 0)

    def test_delitem_raises_key_error(self):
        """Test if __delitem__ raises KeyError for non-existent keys"""
        table = LazyDoubleTable()
        
        # Try to delete a non-existent key
        with self.assertRaises(KeyError):
            del table["non_existent_key"]

    def test_rehash_ignores_deleted_items(self):
        """Test if __rehash ignores deleted items"""
        # Create a helper class to trigger rehash directly
        class TestableRehash(LazyDoubleTable):
            def test_rehash(self):
                self._LazyDoubleTable__rehash()
            
            def get_array(self):
                return self._LazyDoubleTable__array
            
            def get_size_index(self):
                return self._LazyDoubleTable__size_index
        
        table = TestableRehash()
        
        # Insert some items
        for i in range(3):
            table[f"key{i}"] = f"value{i}"
        
        # Delete one item
        del table["key1"]
        
        # Save the current length
        original_length = len(table)
        original_size_index = table.get_size_index()
        
        # Trigger rehash
        table.test_rehash()
        
        # Check that length remained the same (deleted items weren't reinserted)
        self.assertEqual(len(table), original_length)
        self.assertEqual(table.get_size_index(), original_size_index + 1)
        
        # Check that we can still access the remaining items
        self.assertEqual(table["key0"], "value0")
        self.assertEqual(table["key2"], "value2")
        
        # The deleted item should still raise KeyError
        with self.assertRaises(KeyError):
            _ = table["key1"]

    def test_rehash_at_maximum_size(self):
        """Test __rehash when table is already at maximum size"""
        # Create a helper class to trigger rehash directly
        class TestableRehash(LazyDoubleTable):
            def test_rehash(self):
                self._LazyDoubleTable__rehash()
            
            def get_size_index(self):
                return self._LazyDoubleTable__size_index
        
        # Create a table with only two sizes
        table = TestableRehash([5, 13])
        
        # Insert enough items to trigger one rehash
        for i in range(4):  # 4 > 5*2/3
            table[f"key{i}"] = f"value{i}"
        
        # At this point we should be at the second table size
        self.assertEqual(table.get_size_index(), 1)
        
        # Insert enough items to try to trigger another rehash
        for i in range(4, 10):  # Adding 6 more, total 10 > 13*2/3
            table[f"key{i}"] = f"value{i}"
        
        # Try to manually trigger another rehash
        table.test_rehash()
        
        # We should still be at the last size index
        self.assertEqual(table.get_size_index(), 1)
        
        # Check that all items are still accessible
        for i in range(10):
            self.assertEqual(table[f"key{i}"], f"value{i}")

    def test_insert_after_deletion(self):
        """Test inserting at a spot that was previously deleted"""
        table = LazyDoubleTable()
        
        # Insert and delete to create a DeletedItem spot
        key1 = "test_key"
        table[key1] = "test_value"
        del table[key1]
        
        # Insert a new item
        key2 = "new_key"
        table[key2] = "new_value"
        
        # Check that the new item was inserted
        self.assertEqual(table[key2], "new_value")
        self.assertEqual(len(table), 1)

    def test_keys_values_with_deleted_items(self):
        """Test keys() and values() ignore deleted items"""
        table = LazyDoubleTable()
        
        # Insert some items
        table["key1"] = "value1"
        table["key2"] = "value2"
        table["key3"] = "value3"
        
        # Delete one item
        del table["key2"]
        
        # Check keys
        keys = table.keys()
        self.assertEqual(len(keys), 2)
        self.assertIn("key1", keys)
        self.assertIn("key3", keys)
        self.assertNotIn("key2", keys)
        
        # Check values
        values = table.values()
        self.assertEqual(len(values), 2)
        self.assertIn("value1", values)
        self.assertIn("value3", values)
        self.assertNotIn("value2", values)

    def test_complex_operations_sequence(self):
        """Test a complex sequence of operations to ensure all methods work together"""
        table = LazyDoubleTable()
        
        # Insert items
        for i, key in enumerate(self.sample_keys):
            table[key] = i
        
        # Delete some items
        del table["key1"]
        del table["456"]
        
        # Insert more items including at previously deleted spots
        table["new_key1"] = "new_value1"
        table["new_key2"] = "new_value2"
        
        # Update an existing item
        table["A"] = "updated_A"
        
        # Check all expected items are there
        self.assertEqual(len(table), len(self.sample_keys) - 2 + 2)  # Original - deleted + new
        self.assertEqual(table["A"], "updated_A")
        self.assertEqual(table["new_key1"], "new_value1")
        
        # Deleted items should raise KeyError
        with self.assertRaises(KeyError):
            _ = table["key1"]
        with self.assertRaises(KeyError):
            _ = table["456"]


if __name__ == "__main__":
    unittest.main()