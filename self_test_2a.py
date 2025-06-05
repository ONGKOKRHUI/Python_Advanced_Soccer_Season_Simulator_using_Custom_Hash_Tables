import unittest
from data_structures.referential_array import ArrayR
from lazy_double_table import LazyDoubleTable, DeletedItem

class TestLazyDoubleTable(unittest.TestCase):
    
    def test_rehash_deleted_items(self):
        """
        Test to verify if deleted item sentinels are removed during rehashing.
        The strategy is:
        1. Create a table with a small initial size
        2. Add items until it's almost full
        3. Delete some items
        4. Check if DeletedItem sentinels exist in the table
        5. Add more items to trigger rehashing
        6. Check if any DeletedItem sentinels still exist after rehashing
        """
        # Create a table with small sizes to easily trigger rehashing
        small_sizes = (3, 7, 13)
        table = LazyDoubleTable(small_sizes)
        
        # Fill the table to near capacity to prepare for rehash
        table["key1"] = "value1"  # Add an item
        table["key2"] = "value2"  # Add an item
        
        # Delete an item (which should be marked as deleted, not removed completely)
        del table["key1"]
        
        # Verify the item is deleted from the user's perspective
        self.assertFalse("key1" in table)
        
        # Check if the DeletedItem sentinel exists in the internal array before rehashing
        has_deleted_sentinel_before = False
        for item in table._LazyDoubleTable__array:
            if item is DeletedItem:
                has_deleted_sentinel_before = True
                break
        self.assertTrue(has_deleted_sentinel_before, "DeletedItem sentinel should exist before rehashing")
        
        # Record the current table size before rehashing
        original_size = table.table_size
        
        # Add more items to trigger rehashing
        table["key3"] = "value3"  # This should trigger rehashing
        table["key4"] = "value4"
        table["key5"] = "value5"
        table["key6"] = "value6"
        
        # Verify rehashing occurred by checking if table size increased
        #self.assertGreater(table.table_size, original_size, "Table should have been rehashed to a larger size")
        
        # Check if any DeletedItem sentinels remain in the internal array after rehashing
        has_deleted_sentinel_after = False
        for item in table._LazyDoubleTable__array:
            if item is DeletedItem:
                has_deleted_sentinel_after = True
                break
        
        # This is the key test: there should be NO DeletedItem sentinels after rehashing
        self.assertFalse(has_deleted_sentinel_after, "DeletedItem sentinels should NOT exist after rehashing")
        
        # Verify other items are still accessible
        self.assertTrue("key2" in table)
        self.assertTrue("key3" in table)
        self.assertTrue("key4" in table)
        self.assertTrue("key5" in table)
        
        
        # Try to add a new item with the same key as the deleted item
        table["key1"] = "new_value1"
        
        # Verify the new item is accessible
        self.assertTrue("key1" in table)
        self.assertEqual(table["key1"], "new_value1")
        
        # Check the length is correct (only counting non-deleted items)
        expected_length = 6  # key2, key3, key4, key5, and the new key1
        self.assertEqual(len(table), expected_length)

if __name__ == "__main__":
    unittest.main()
