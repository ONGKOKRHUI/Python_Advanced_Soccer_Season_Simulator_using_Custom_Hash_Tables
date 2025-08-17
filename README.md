---

# **Advanced Soccer Season Simulator using Custom Hash Tables**

## **Project Overview** ⚽

This project is a sophisticated soccer league season simulator, built entirely from scratch in Python. It goes beyond simple game simulation to create a robust engine for managing teams, players, statistics, and a full season schedule.

The core of this project lies in the **design and implementation of advanced data structures**, particularly several custom-built **hash tables**, each tailored for a specific purpose. The entire system is a demonstration of applying complex computer science principles to solve real-world data management challenges in a simulated environment. Every method is accompanied by a rigorous **Big O time complexity analysis**, highlighting a commitment to writing performant and efficient code.

***

## **Key Features**

* **Dynamic Season Simulation:** Generates a full round-robin schedule and simulates the entire season week by week.
* **Persistent Team & Player Stats:** Teams and players have persistent statistics that are updated after every simulated game.
* **Sorted Leaderboard:** Maintains a season leaderboard that is efficiently re-sorted after each week's games using Mergesort.
* **Advanced Custom Data Structures:** Utilizes custom-built hash tables with features like **double hashing** and **lazy deletion**.
* **Object-Oriented Architecture:** A clean, modular design using classes like `Season`, `Team`, and `Player` to logically separate concerns.

***

## **Skills & Concepts Demonstrated**

This project was an in-depth exercise in building and applying complex data structures to manage relational data efficiently.

### **1. Advanced Hash Table Implementation**

The standout feature of this project is the implementation of multiple, purpose-built hash tables from the ground up.

* **LazyDoubleTable:** A highly advanced hash table implementation featuring:
    * **Double Hashing:** A sophisticated collision resolution strategy that uses a second hash function to determine the probe sequence. This significantly reduces the clustering that can occur with simpler methods like linear probing, leading to better performance.
    * **Lazy Deletion:** A technique where items are not immediately removed from the table but are instead marked with a special "deleted" sentinel. This makes the deletion operation extremely fast (amortized O(1)) by avoiding the need to re-arrange subsequent elements.
* **HashyDateTable:** A specialized hash table designed to handle date-stamped blog posts (`YYYY/MM/DD`). It features a **custom hash function** that intelligently converts date strings into a well-distributed integer index. This demonstrates an understanding of how to tailor hashing algorithms to specific data formats to ensure uniform distribution and minimize collisions.
* **LinearProbeTable:** This standard hash table was used as a base and applied to manage:
    * A team's roster, using player positions (`"Striker"`, `"Defender"`, etc.) as keys for quick lookups of all players in a specific role.
    * A player's individual statistics, allowing for dynamic key-value stat tracking (e.g., `player['tackles'] = 10`).

### **2. Other Key Data Structures**

* **CircularQueue:** Implemented to store a team's recent game history (`WIN`, `LOSS`, `DRAW`). Its fixed-size, FIFO (First-In, First-Out) nature was perfect for keeping a rolling log of the last N game results.
* **LinkedList / ArrayList:** Used as foundational data structures throughout the project, such as for storing players within a specific position in the team's hash table.

### **3. Algorithms & Complexity Analysis**

* **Mergesort Algorithm:** The season leaderboard is re-sorted after every week of games using an implementation of Mergesort. This choice reflects an understanding of efficient, stable sorting algorithms (O(N log N)). The custom `__le__` magic method in the `Team` class ensures sorting is handled correctly, first by points, then alphabetically.
* **Rigorous Time Complexity Analysis:** A core discipline practiced throughout this project was the analysis and documentation of the time complexity (Big O notation) for **every single method**. This demonstrates a profound understanding of algorithm performance and the ability to write code that is not just functional, but demonstrably efficient.
* **Schedule Generation Algorithm:** The logic in `_generate_schedule` shows the ability to solve a combinatorial problem: creating a fair round-robin tournament schedule where each team plays every other team home and away, with no team playing more than once per week.

### **4. Object-Oriented Programming (OOP)**

The project is architected with strong OOP principles, using classes to create a clear and logical model of the domain.
* **Encapsulation:** The `Team` class, for instance, encapsulates all the logic for managing its players, history, and points, hiding the complexity of its internal hash tables from the `Season` class.
* **Composition:** The `Season` class is composed of `Team` objects, which are in turn composed of `Player` objects, creating a clear, hierarchical structure.

***

## **How to Run the Project**

1.  Clone the repository to your local machine.
2.  Navigate to the project directory.
3.  To run the simulation, you will likely need a main script that:
    * Creates several `Player` and `Team` instances.
    * Initializes a `Season` with those teams.
    * Calls the `season.simulate_season()` method.
