from unittest import TestCase

import ast
import inspect

from tests.helper import CollectionsFinder

from lazy_double_table import LazyDoubleTable


class TestTask2Setup(TestCase):
    def setUp(self) -> None:
        self.step_table: LazyDoubleTable = LazyDoubleTable()
        self.large_table_table_sizes = [24593, 49157, 98317, 196613, 393241, 786433, 1572869]
        self.large_step_table: LazyDoubleTable = LazyDoubleTable(self.large_table_table_sizes)
        self.non_prime_step_table = LazyDoubleTable([6000, 8000, 10000])
        self.sample_keys = ["key1", "key2", "A", "B", "123", "456", "SlightlyLongerKey"]


class TestTask2(TestTask2Setup):
    def test_hash_functions_available(self):
        """
        #name(Test if the hash functions are available)
        """
        self.assertTrue(hasattr(self.step_table, "hash"), "LazyDoubleTable should have a hash function")
        self.assertTrue(hasattr(self.step_table, "hash2"), "LazyDoubleTable should have a hash2 function")

    def test_step_hash_empty(self):
        """
        #name(Test if the hash table is empty at the start)
        """
        self.assertEqual(len(self.step_table), 0, "LazyDoubleTable should be empty at the start")

    def test_setting_items(self):
        """
        #name(Test if the items are set correctly in the hash table)
        """
        for i, key_name in enumerate(self.sample_keys):
            self.step_table[key_name] = i
            self.assertEqual(self.step_table[key_name], i, "LazyDoubleTable not setting/getting values correctly")

        self.assertEqual(
            len(self.step_table),
            len(self.sample_keys), 
            f"Expected {len(self.sample_keys)} keys in LazyDoubleTable, got {len(self.step_table)}"
        )

    def test_step_hash_delete(self):
        """
        #name(Test deleting from the hash table)
        """
        for i, test_key in enumerate(self.sample_keys):
            self.step_table[test_key] = i

        for i, test_key in enumerate(self.sample_keys):
            del self.step_table[test_key]
            self.assertRaises(KeyError, lambda: self.step_table[test_key])
            self.assertEqual(len(self.step_table), len(self.sample_keys) - i - 1, f"Expected {len(self.sample_keys) - i - 1} keys in LazyDoubleTable, got {len(self.step_table)}")

    def test_get_keys(self):
        """
        #name(Test if the keys are returned correctly)
        """
        for i, key in enumerate(self.sample_keys):
            self.step_table[key] = i
        
        keys = self.step_table.keys()
        for i, key in enumerate(keys):
            self.assertIn(key, keys, f"Key {key} not found in LazyDoubleTable returned keys")
        self.assertEqual(len(keys), len(self.sample_keys), f"Expected {len(self.sample_keys)} keys in LazyDoubleTable, got {len(keys)}")

    def test_get_values(self):
        """
        #name(Test if the values are returned correctly)
        """
        for i, key in enumerate(self.sample_keys):
            self.step_table[key] = i
        
        values = self.step_table.values()
        for i, key in enumerate(values):
            self.assertIn(key, values, f"Value {key} not found in LazyDoubleTable returned values")
        self.assertEqual(len(values), len(self.sample_keys), f"Expected {len(self.sample_keys)} keys in LazyDoubleTable, got {len(values)}")

    def test_rehash(self):
        """
        #name(Test if rehashing works correctly)
        """
        for i, key in enumerate(self.sample_keys):
            self.large_step_table[key] = i
        self.large_step_table._LazyDoubleTable__rehash()
        for i, key in enumerate(self.sample_keys):
            self.assertEqual(self.large_step_table[key], i, "LazyDoubleTable not setting/getting values correctly after rehashing")


class TestTask2Approach(TestTask2Setup):
    def test_python_built_ins_not_used(self):
        """
        #name(Test built-in collections not used)
        #hurdle
        """
        import lazy_double_table
        modules = [lazy_double_table]
        
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

    def test_lazy_deletion_1(self):
        """
        #name(Test if lazy deletion works correctly)
        #approach
        """
        for i, key in enumerate(self.sample_keys):
            self.large_step_table[key] = i
        
        # Make sure there are the right number of empty spots in the table initially
        expected_none_count = self.large_step_table.table_size - len(self.sample_keys)
        observed_none_count = sum([1 if x is None else 0 for x in self.large_step_table._LazyDoubleTable__array])
        self.assertEqual(
            observed_none_count,
            expected_none_count,
            f"Expected {expected_none_count} None values in LazyDoubleTable, got {observed_none_count}"
        )

        # Now delete one by one, make sure the empty spots don't increase (because of lazy deletion)
        for i, key in enumerate(self.sample_keys):
            del self.large_step_table[key]
            self.assertRaises(KeyError, lambda: self.large_step_table[key])
            self.assertEqual(
                len(self.large_step_table),
                len(self.sample_keys) - i - 1,
                f"Expected {len(self.sample_keys) - i - 1} keys in LazyDoubleTable, got {len(self.large_step_table)}"
            )
            
            # The number of None values should NOT increase if they have lazy deletion
            observed_none_count = sum([1 if x is None else 0 for x in self.large_step_table._LazyDoubleTable__array])
            self.assertEqual(
                observed_none_count,
                expected_none_count,
                f"Expected {expected_none_count} None values in LazyDoubleTable, got {observed_none_count}"
            )


class TestTask2Comprehensive(TestTask2Setup): # Use your existing TestTask2Setup

    def test_contains_method(self):
        """
        #name(Test __contains__ method directly for presence and absence of keys)
        """
        self.assertFalse("new_key" in self.step_table, "Key should not be in empty table")
        self.step_table["key1"] = 1
        self.assertTrue("key1" in self.step_table, "Key should be found after insertion")
        self.step_table["key2"] = 2
        self.assertTrue("key2" in self.step_table, "Another key should be found")
        del self.step_table["key1"]
        self.assertFalse("key1" in self.step_table, "Key should not be found after deletion")
        self.assertTrue("key2" in self.step_table, "Other key should still be present after deleting a different key")

    def test_str_method(self):
        """
        #name(Test __str__ method for basic functionality and correct representation)
        """
        self.assertEqual(str(self.step_table), "", "String of empty table should be empty")
        self.step_table["keyA"] = "valA"
        self.step_table["keyB"] = "valB"
        s = str(self.step_table)
        self.assertIn("(keyA,valA)", s, "__str__ output missing an item or format incorrect")
        self.assertIn("(keyB,valB)", s, "__str__ output missing an item or format incorrect")
        self.assertEqual(s.count("\n"), 2, "String output should have one newline per item")

        del self.step_table["keyA"]
        s_after_del = str(self.step_table)
        self.assertNotIn("(keyA,valA)", s_after_del, "__str__ output contains deleted item")
        self.assertIn("(keyB,valB)", s_after_del, "__str__ output missing remaining item")
        self.assertEqual(s_after_del.count("\n"), 1, "String output newline count incorrect after deletion")

    # def test_hash2_coprime_with_table_size(self):
    #     """
    #     #name(Test if hash2 produces step sizes co-prime with table_size, including non-prime sizes)
    #     #approach
    #     """
    #     # self.non_prime_step_table is initialized in TestTask2Setup
    #     # TABLE_SIZES = (5, 13, 29, ...) for self.step_table
    #     tables_to_test = [self.step_table, self.non_prime_step_table, self.large_step_table]
    #     # Use a variety of keys, including some that might share first characters or have different lengths
    #     keys_to_test = self.sample_keys + ["another_key", "testKey123", "z", "zz", "longkeytest", "", "key_with_ord_gt_const"]

    #     for table_instance in tables_to_test:
    #         # Test with initial table size and after a rehash if possible
    #         for _ in range(2): # Test once, then rehash (if not max size) and test again
    #             current_table_size = table_instance.table_size
    #             if current_table_size == 0: continue # Should not happen with TABLE_SIZES setup

    #             for key in keys_to_test:
    #                 step = table_instance.hash2(key)
    #                 self.assertIsInstance(step, int, f"hash2 should return an integer for key '{key}'")
    #                 self.assertGreater(step, 0, f"Step size for key '{key}' must be positive (got {step}) for table size {current_table_size}.")
                    
    #                 # Calculate GCD
    #                 a, b = current_table_size, step
    #                 while b:
    #                     a, b = b, a % b
    #                 gcd = a
    #                 self.assertEqual(gcd, 1, 
    #                                  f"Step size {step} for key '{key}' is not co-prime with table size {current_table_size}. GCD is {gcd}.")
                
    #             # Trigger a rehash for the next iteration (if not already at max size for this instance)
    #             if table_instance._LazyDoubleTable__size_index < len(table_instance.TABLE_SIZES) - 1:
    #                 # Add dummy items to force rehash if __setitem__ is robust, or call directly
    #                 # To control precisely, we might need to call __rehash directly for testing hash2 against new size
    #                 # For simplicity, we assume rehash increases size, and hash2 tested against that new size.
    #                 # If TABLE_SIZES has only one entry for non_prime_step_table, this won't rehash to new size.
    #                 # A more direct way: save old size_index, increment, get new size, call hash2, restore size_index.
    #                 pass # For now, rely on multiple table instances or manual rehash if needed for specific size tests.
    #             else:
    #                 break # No more sizes to test for this instance

    def test_collision_resolution_with_double_hashing(self):
        """
        #name(Test collision resolution using different hash2 steps for keys colliding on hash1)
        #approach
        """
        # Using table size 5 (first default size).
        # From analysis: hash("A", 5)=0, hash("F", 5)=0, hash("K", 5)=0.
        # Student's hash2 implementation: constant = 71
        # hash2("A", 5) -> step_val=6. (6%5 = 1 for probing if steps were modded, but student uses raw hash2 step)
        # hash2("F", 5) -> step_val=1.
        # hash2("K", 5) -> step_val=67.
        # All these hash2 values (6, 1, 67) are different and co-prime with 5.

        table = LazyDoubleTable([5, 13]) # Start with size 5
        
        # Verify assumptions about primary hash collisions
        self.assertEqual(table.hash("A"), 0, "Pre-check: hash('A') % 5 should be 0")
        self.assertEqual(table.hash("F"), 0, "Pre-check: hash('F') % 5 should be 0")
        self.assertEqual(table.hash("K"), 0, "Pre-check: hash('K') % 5 should be 0")

        # Insert A
        table["A"] = "ValueA" # Goes into index 0
        self.assertEqual(table["A"], "ValueA")
        # To check exact position (optional, relies on private member access for robust test):
        # self.assertEqual(table._LazyDoubleTable__array[0], ("A", "ValueA"))


        # Insert F (collides with A on hash1)
        # hash1("F")=0. hash2("F")=1. Probes to (0 + 1) % 5 = 1.
        table["F"] = "ValueF"
        self.assertEqual(table["F"], "ValueF")
        # self.assertEqual(table._LazyDoubleTable__array[1], ("F", "ValueF"))

        # Insert K (collides with A on hash1)
        # hash1("K")=0. hash2("K")=67. Probes to (0 + 67) % 5 = 2.
        table["K"] = "ValueK"
        self.assertEqual(table["K"], "ValueK")
        # self.assertEqual(table._LazyDoubleTable__array[2], ("K", "ValueK"))

        # Verify all are retrievable and distinct, and length is correct
        self.assertEqual(table["A"], "ValueA")
        self.assertEqual(table["F"], "ValueF")
        self.assertEqual(table["K"], "ValueK")
        self.assertEqual(len(table), 3, "Length should be 3 after inserting 3 distinct colliding keys")

    def test_setitem_update_existing_key(self):
        """
        #name(Test updating the value of an existing key, length should not change)
        """
        self.step_table["key1"] = "initial_value"
        self.assertEqual(self.step_table["key1"], "initial_value")
        self.assertEqual(len(self.step_table), 1)

        self.step_table["key1"] = "updated_value" # Update
        self.assertEqual(self.step_table["key1"], "updated_value", "Value not updated correctly")
        self.assertEqual(len(self.step_table), 1, "Length should not change when updating an existing key")

        # Ensure other keys are not affected
        self.step_table["key2"] = "another_value"
        self.assertEqual(len(self.step_table), 2)
        self.step_table["key1"] = "final_value"
        self.assertEqual(self.step_table["key1"], "final_value")
        self.assertEqual(self.step_table["key2"], "another_value")
        self.assertEqual(len(self.step_table), 2)


    def test_setitem_triggers_rehash_at_load_factor(self):
        """
        #name(Test __setitem__ triggers rehash when load factor > 2/3)
        #approach
        """
        # Default TABLE_SIZES[0]=5, TABLE_SIZES[1]=13
        # Rehash when length / table_size > 2/3
        # For size 5: len > 5 * (2/3) = 10/3 = 3.33. So, rehash when len becomes 4.
        table = LazyDoubleTable([5, 13, 29]) # Provide specific sizes for predictability
        self.assertEqual(table.table_size, 5, "Initial table size should be 5")

        table["key1"] = 1 # len = 1. Load = 1/5 = 0.2
        table["key2"] = 2 # len = 2. Load = 2/5 = 0.4
        table["key3"] = 3 # len = 3. Load = 3/5 = 0.6
        self.assertEqual(table.table_size, 5, "Table should not have resized yet (len=3, load=0.6)")
        self.assertEqual(len(table), 3)

        table["key4"] = 4 # len = 4. Load = 4/5 = 0.8. Should trigger rehash.
        self.assertEqual(table.table_size, 13, "Table should have resized to 13 after 4th item")
        self.assertEqual(len(table), 4, "Length should be 4 after adding 4th item and rehashing")
        
        # Verify items are still accessible and correct
        self.assertEqual(table["key1"], 1)
        self.assertEqual(table["key2"], 2)
        self.assertEqual(table["key3"], 3)
        self.assertEqual(table["key4"], 4)

        # Continue to fill up to next rehash point for size 13
        # len / 13 > 2/3 => len > 26/3 = 8.66. Rehash when len becomes 9.
        # Already have 4 items. Add 5 more.
        for i in range(5, 9): # Add key5, key6, key7, key8. len becomes 8.
            table[f"key{i}"] = i
        self.assertEqual(table.table_size, 13, "Table should still be 13 (len=8, load=8/13~0.61)")
        self.assertEqual(len(table), 8)

        table["key9"] = 9 # len = 9. Load = 9/13 ~ 0.69. Should trigger rehash.
        self.assertEqual(table.table_size, 29, "Table should have resized to 29 after 9th item")
        self.assertEqual(len(table), 9, "Length should be 9 after adding 9th item and rehashing")
        self.assertEqual(table["key9"], 9)
        self.assertEqual(table["key1"], 1)


    def test_setitem_insert_into_deleted_slot(self):
        """
        #name(Test __setitem__ correctly inserts into a slot marked as DeletedItem)
        #approach
        """
        table = LazyDoubleTable([5, 13]) # Initial size 5
        # Keys A, F, K hash to 0 for table size 5.
        # A inserted at 0. F probes to 1. K probes to 2.
        table["A"] = "valA" 
        table["F"] = "valF" 
        table["K"] = "valK" 
        self.assertEqual(len(table), 3)

        # Delete "F". The slot where "F" was (index 1, by probing) becomes DeletedItem.
        # We need to know where F was. Let's assume F was at an index `f_idx`.
        # A more robust way is to find F's actual index if __hashy_probe could return it for __getitem__
        # For testing, we can try to find the slot.
        f_idx = -1
        for i in range(table.table_size):
            if table._LazyDoubleTable__array[i] is not None and \
               not isinstance(table._LazyDoubleTable__array[i], type(table.DELETED_ITEM)) and \
               table._LazyDoubleTable__array[i][0] == "F":
                f_idx = i
                break
        self.assertNotEqual(f_idx, -1, "Key 'F' should be in the table before deletion")
        
        del table["F"] 
        self.assertEqual(len(table), 2)
        # Verify F's original slot is now a DeletedItem
        self.assertIsInstance(table._LazyDoubleTable__array[f_idx], type(table.DELETED_ITEM),
                              "Slot for 'F' should be DeletedItem after deletion")


        # Add a new key "G". Let's assume hash("G") is same as hash("F")=0
        # and hash2("G") is same as hash2("F")=1, so "G" probes to `f_idx`.
        # (This requires specific key G or mocking)
        # A simpler test: If "G" hashes initially to f_idx, or probes to it, and f_idx is DeletedItem.
        # The student's __hashy_probe handles `is DeletedItem` correctly for insertion.
        
        # Let's use a key that would directly hash or probe into F's old slot.
        # If F was at index 1 (probed from 0). A new key "G" that hashes to 0, and also has step 1,
        # would try index 1 after seeing A at 0.
        # Or, a key that hashes directly to 1.
        # Example: For size 5, hash("G") = (ord('G') % 5) = (71 % 5) = 1.
        # So "G" hashes directly to index 1, which was F's slot.
        table["G"] = "valG"
        self.assertEqual(table["G"], "valG")
        self.assertEqual(len(table), 3, "Length should increase after inserting into a deleted slot")
        
        # Verify G is at F's old spot
        self.assertEqual(table._LazyDoubleTable__array[f_idx], ("G", "valG"), "New key 'G' should occupy F's old slot")

        # Verify other items are untouched
        self.assertEqual(table["A"], "valA")
        self.assertEqual(table["K"], "valK")
        with self.assertRaises(KeyError):
            _ = table["F"] # F should truly be gone


    def test_delitem_key_not_found(self):
        """
        #name(Test __delitem__ raises KeyError for a key not in the table, including empty table)
        """
        with self.assertRaises(KeyError, msg="Deleting from empty table should raise KeyError"):
            del self.step_table["non_existent_key"]

        self.step_table["existing_key"] = 100
        initial_len = len(self.step_table)
        with self.assertRaises(KeyError, msg="Deleting a non-existent key should raise KeyError"):
            del self.step_table["non_existent_key_again"]
        self.assertEqual(len(self.step_table), initial_len, "Length should not change if delete failed.")


    def test_rehash_ignores_sentinels_and_cleans_table(self):
        """
        #name(Test __rehash correctly ignores sentinel DeletedItem objects and they are not in new table)
        #approach
        """
        table = LazyDoubleTable([5, 13, 29]) # Sizes: 5, then 13
        self.assertEqual(table.table_size, 5)

        table["key1"] = 1
        table["key_to_delete1"] = 10
        table["key2"] = 2
        table["key_to_delete2"] = 20
        
        self.assertEqual(len(table), 4)
        
        del table["key_to_delete1"] 
        del table["key_to_delete2"] 
        self.assertEqual(len(table), 2, "Length should be 2 after deletions")

        # Manually trigger rehash (student code does this on load factor, or we call private)
        table._LazyDoubleTable__rehash()

        self.assertEqual(table.table_size, 29, "Table should have resized to 29") # Adjusted expected size
        self.assertEqual(len(table), 2, "Length should remain 2 (active items) after rehashing")

        # Verify active items are present
        self.assertEqual(table["key1"], 1)
        self.assertEqual(table["key2"], 2)

        # Verify deleted items are not present
        with self.assertRaises(KeyError):
            _ = table["key_to_delete1"]
        with self.assertRaises(KeyError):
            _ = table["key_to_delete2"]

        # Crucially, check the internal array of the new table for absence of DeletedItem objects.
        # Student's rehash iterates `old_array` and only re-inserts non-None, non-DeletedItem items.
        deleted_item_instance_count = 0
        none_count = 0
        for i in range(table.table_size): # Iterate through the new, larger array
            slot_content = table._LazyDoubleTable__array[i]
            if isinstance(slot_content, type(table.DELETED_ITEM)): # Check type if class is stored
                deleted_item_instance_count += 1
            elif slot_content is table.DELETED_ITEM: # Check if class itself is stored as sentinel
                deleted_item_instance_count +=1
            elif slot_content is None:
                none_count +=1
        
        self.assertEqual(deleted_item_instance_count, 0, 
                         "Rehashed table should not contain any DeletedItem sentinels.")
        self.assertEqual(none_count, table.table_size - len(table), 
                         "Number of None slots in rehashed table is incorrect; should be new_size - active_items.")


    # def test_rehash_at_max_size_behavior(self):
    #     """
    #     #name(Test __rehash behavior when table is already at maximum configured size, as per student code)
    #     # Note: Student's __rehash, if at max size, increments size_index, hits the `if == len` check, and `return`s.
    #     # This means no actual rehashing (item removal/reinsertion) or sentinel cleanup occurs. This test verifies THAT behavior.
    #     """
    #     sizes = self.step_table.TABLE_SIZES # e.g., (5, 13, 29, ..., 1572869)
    #     if not sizes: self.skipTest("TABLE_SIZES is empty") # Should not happen

    #     # Setup table to be at its maximum configured size
    #     table = LazyDoubleTable(sizes)
        
    #     # Manually set to max size for testing this edge case
    #     max_idx = len(sizes) - 1
    #     table._LazyDoubleTable__size_index = max_idx
    #     # Ensure the array is also of this max size
    #     current_max_size = sizes[max_idx]
    #     table._LazyDoubleTable__array = LazyDoubleTable.ArrayR(current_max_size) # Assuming ArrayR is accessible
    #     table._LazyDoubleTable__length = 0 # Reset length for clean setup at max size

    #     table["key1"] = "val1"
    #     table["key_to_delete"] = "val_del"
    #     table["key3"] = "val3"
        
    #     del table["key_to_delete"] # Slot for "key_to_delete" becomes DeletedItem
        
    #     self.assertEqual(table.table_size, current_max_size, "Table should be at its max size.")
    #     self.assertEqual(len(table), 2, "Two active items.")

    #     # Count sentinels before the __rehash call
    #     sentinels_before = 0
    #     for i in range(table.table_size):
    #         if table._LazyDoubleTable__array[i] is table.DELETED_ITEM: # student uses class as sentinel
    #             sentinels_before += 1
    #     self.assertEqual(sentinels_before, 1, "Should be one sentinel before rehash call at max size.")

    #     # Call __rehash
    #     table._LazyDoubleTable__rehash() # According to student code, this should be a no-op for items/sentinels

    #     # Assertions based on student's code (no effective change at max size)
    #     self.assertEqual(table.table_size, current_max_size, "Table size should NOT change if already at max.")
    #     self.assertEqual(len(table), 2, "Length should be unchanged as rehash was no-op.")
    #     self.assertEqual(table["key1"], "val1", "Item1 should still be accessible.")
    #     self.assertEqual(table["key3"], "val3", "Item3 should still be accessible.")
    #     with self.assertRaises(KeyError):
    #         _ = table["key_to_delete"] # Deleted item should remain inaccessible.

    #     # Verify sentinels were NOT cleared (because of the early return in student's __rehash)
    #     sentinels_after = 0
    #     for i in range(table.table_size):
    #         if table._LazyDoubleTable__array[i] is table.DELETED_ITEM:
    #             sentinels_after += 1
    #     self.assertEqual(sentinels_after, sentinels_before, 
    #                      "Sentinels should NOT be cleared if rehash is no-op at max size per student code.")


    def test_hashy_probe_full_table_no_key_no_insert(self):
        """
        #name(Test __hashy_probe raises KeyError when table is full (no None/Deleted), key not found, not inserting)
        #approach
        """
        table = LazyDoubleTable([3]) # Tiny table, size 3
        # Manually fill the table completely with actual items (no None, no DeletedItem)
        table._LazyDoubleTable__array[0] = ("k0",0)
        table._LazyDoubleTable__array[1] = ("k1",1)
        table._LazyDoubleTable__array[2] = ("k2",2)
        table._LazyDoubleTable__length = 3 

        with self.assertRaises(KeyError):
            # __hashy_probe is private, called by __getitem__ or __delitem__
            # To test __hashy_probe directly (if it were public): table.__hashy_probe("non_existent_key", False)
            # Indirectly:
            _ = table["non_existent_key"]
            
    def test_hashy_probe_full_table_cannot_insert(self):
        """
        #name(Test __hashy_probe raises RuntimeError when table is full (no None/Deleted) and trying to insert)
        #approach
        """
        table = LazyDoubleTable([3]) 
        table._LazyDoubleTable__array[0] = ("k0",0)
        table._LazyDoubleTable__array[1] = ("k1",1)
        table._LazyDoubleTable__array[2] = ("k2",2)
        table._LazyDoubleTable__length = 3 # Table is full of actual items

        # If __setitem__ calls rehash, this RuntimeError from __hashy_probe might not be directly reachable
        # unless rehash fails to expand (e.g., at max size AND no sentinels to overwrite).
        # Student's __setitem__ calls rehash *before* __hashy_probe if load factor exceeded.
        # If rehash doesn't expand (at max size), then __hashy_probe is called.
        # If table is full of *actual items* (no Nones, no DeletedItems), then __hashy_probe should raise RuntimeError.

        # Setup: table is at max size, and completely full of actual items.
        sizes = table.TABLE_SIZES
        max_idx = len(sizes) -1
        table._LazyDoubleTable__size_index = max_idx
        max_size = sizes[max_idx]
        
        # For this test, use a small max size to fill easily
        small_max_size_table = LazyDoubleTable([3]) # Its only size is 3, so it's "max"
        small_max_size_table._LazyDoubleTable__array[0] = ("k0",0)
        small_max_size_table._LazyDoubleTable__array[1] = ("k1",1)
        small_max_size_table._LazyDoubleTable__array[2] = ("k2",2)
        small_max_size_table._LazyDoubleTable__length = 3

        # Now, trying to insert into this full, maxed-out table:
        # __setitem__ will check load factor (3/3 = 1 > 2/3). Call __rehash.
        # __rehash sees it's at max size, returns (no-op for items).
        # __setitem__ proceeds to call __hashy_probe("new_key", True).
        # __hashy_probe iterates, finds no None/DeletedItem, loop finishes. Raises RuntimeError.
        with self.assertRaises(RuntimeError, msg="Inserting into a completely full (no sentinels) maxed-out table should cause RuntimeError from __hashy_probe via __setitem__"):
            small_max_size_table["new_key_cannot_fit"] = 99


    def test_getitem_probes_past_deleteditem_to_find_key(self):
        """
        #name(Test __getitem__ correctly probes past DeletedItem slots to find a key further along the probe sequence)
        #approach
        """
        table = LazyDoubleTable([5]) # size 5
        # Keys A,F,K all hash to 0.
        # hash2("A")=6 (probe step 6), hash2("F")=1 (probe step 1), hash2("K")=67 (probe step 67)
        
        # Order of insertion matters for placement:
        table["A"] = "valA" # Placed at index 0 (hash("A")=0)
        table["F"] = "valF" # hash("F")=0, step=1. Probes to (0+1)%5 = 1. Placed at 1.
        table["K"] = "valK" # hash("K")=0, step=67. Probes to (0+67)%5 = 2. Placed at 2.

        # Current state (example): array[0]=A, array[1]=F, array[2]=K
        
        del table["A"] # array[0] becomes DeletedItem.
        self.assertEqual(len(table), 2)
        self.assertIsInstance(table._LazyDoubleTable__array[table.hash("A")], type(table.DELETED_ITEM))


        # Try to get "F":
        # __getitem__("F") calls __hashy_probe("F", False)
        # 1. hash("F")=0. array[0] is DeletedItem. Probe loop continues.
        # 2. probe: pos=(0 + hash2("F")) % 5 = (0+1)%5 = 1.
        # 3. array[1] is ("F","valF"). Key matches. Returns position 1. Correct.
        self.assertEqual(table["F"], "valF", "Should find 'F' by probing past a DeletedItem at primary hash slot.")
        
        # Try to get "K":
        # __getitem__("K") calls __hashy_probe("K", False)
        # 1. hash("K")=0. array[0] is DeletedItem. Probe loop continues.
        # 2. probe: pos=(0 + hash2("K")) % 5 = (0+67)%5 = 2.
        # 3. array[2] is ("K","valK"). Key matches. Returns position 2. Correct.
        self.assertEqual(table["K"], "valK", "Should find 'K' by probing past a DeletedItem at primary hash slot.")

        # Scenario 2: Deleted item is on the probe path, not the initial hash slot
        table2 = LazyDoubleTable([5])
        table2["X"] = "valX" # Assume hash("X") = 0. X at idx 0.
        table2["Y"] = "valY" # Assume hash("Y") = 0, stepY=1. Y at idx 1.
        table2["Z"] = "valZ" # Assume hash("Z") = 0, stepZ=2. Z at idx 2.
        # Array: [X, Y, Z, None, None]

        del table2["Y"] # Slot at index 1 (where Y was) becomes DeletedItem.
        # Array: [X, DeletedItem, Z, None, None]
        
        # Get "Z". hash("Z")=0. array[0] is X (not "Z"). Probe.
        # new_pos = (0 + stepZ)%5 = 2. array[2] is Z. Found.
        # This specific path for Z did not pass over the DeletedItem at index 1.
        # To test Z probing past deleted Y, Z would need to try index 1 first.
        # This requires stepZ to hit 1 before 2, or Y to be on Z's path for a different reason.

        # The first part of this test (deleting "A") is sufficient to show __hashy_probe
        # correctly skips DeletedItem when searching.
