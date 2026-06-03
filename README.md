# Travelling Salesman Problem with Time Windows (TSP-TW) Solution

## 📋 Project Overview

This project is a solution to the **Travelling Salesman Problem with Time Windows (TSP-TW)**, a challenging NP-Hard optimization problem. The project implements an effective **Greedy Heuristic** algorithm for solving TSP-TW with massive datasets containing up to 50,000 cities.

---

## 🎯 Problem Definition

### What is TSP-TW?

An extended version of the Travelling Salesman Problem with time window constraints:

- **Objective:** A salesman must visit all cities (or as many as possible) and return to the starting city
- **Constraints:**
  - Each city has a **time window**: [open_time, close_time]
  - The salesman can visit a city only if **arrival_time ≤ close_time**
  - If arriving early, the salesman must wait until open_time
  - The time window of the starting city is not considered for the return trip
- **Optimization Goals:**
  - Maximize the number of visited cities (k)
  - Minimize total distance and waiting time

---

## 🚀 Solution Approach: Greedy Heuristic

### 1. **Multi-Start Approach**

- Algorithm generates routes from multiple starting points, not just one
- Begins from cities with the earliest opening times in their time windows
- For large datasets (n > 500), starting candidates are limited (first 500 cities)
- This approach helps avoid local optima

### 2. **Scoring System**

At each step, when selecting the next city from valid options:

```
score = distance + (waiting_time × penalty_coefficient)
```

- City with the lowest score is selected
- Balances both distance and waiting time in a cost function
- **Penalty coefficient:** Applies more aggressive penalties for longer waiting times

### 3. **Time Window Validation**

- Arrival time is checked for each city
- A city is valid if arrival_time ≤ close_time
- If arriving early, waiting is done until open_time
- Time window of starting city is ignored for return route

### 4. **Efficiency Optimization**

- For large datasets (n > 50,000), computation time is limited (maximum 180 seconds)
- Best route is recorded for each starting point
- Final solution is the best among all starting points

---

## 📁 Project File Structure

```
travelling-salesman/
│
├── README.md                   # This file - project documentation
├── solver.py                   # Main solution algorithm (Greedy Heuristic)
├── tsp_tw_verifier.py          # Verification and validation tool
├── example-input-1.txt         # Example input file
├── example-output-1.txt        # Example output file
└── my-output.txt               # Generated output (created by solver.py)
```

### File Descriptions

#### `solver.py`

- **Purpose:** Main algorithm solving the TSP-TW problem
- **Input:** Path to input file (city data)
- **Output:** Path to output file (route and statistics)
- **Working Logic:**
  1. Reads city data from input file
  2. Generates routes from multiple starting points
  3. Finds the best route
  4. Writes results to output file

#### `tsp_tw_verifier.py`

- **Purpose:** Validates solution results and checks correctness
- **Validation Rules:**
  - All time window constraints are satisfied
  - Distance calculations are correct
  - Route connections are valid
  - File format is correct

#### Input File Format (`example-input-1.txt`)

```
city_id x y open_time close_time
0       200 800  0     9000
1       3600 2300 1205 10205
...
```

- **city_id:** City identifier (starting from 0)
- **x, y:** Cartesian coordinates
- **open_time:** City opening time
- **close_time:** City closing time

#### Output File Format

```
k total_length completion_time
city_1
city_2
...
city_k
0
```

- **k:** Number of visited cities
- **total_length:** Total distance traveled (sum of all segments)
- **completion_time:** Return time to start (in seconds)
- **city_1, city_2, ..., city_k:** Route (city 0 is the starting point)
- **0:** Return to starting city

---

## 🛠️ How to Use

### Requirements

- Python 3.7 or later
- Standard library (`math`, `sys`, `time`)

### Execution Steps

#### Step 1: Run the Solver

```bash
python solver.py example-input-1.txt my-output.txt
```

**Parameters:**

- `example-input-1.txt`: Input file (city data)
- `my-output.txt`: Output file (route solution)

**Example Output:**

```
k=18, total_length=48531, completion_time=16733 (best found so far)
Route optimization finished in 3.45 seconds
```

#### Step 2: Verify Results

```bash
python tsp_tw_verifier.py example-input-1.txt my-output.txt
```

**Example Output (Success):**

```
✓ Route verification passed
✓ All cities visited within time windows
✓ Output file format is valid
k=18, total_length=48531, completion_time=16733
```

**Example Output (Error):**

```
✗ Verification failed: City 5 violated time window
```

---

## 📊 Algorithm Performance

### Time Complexity

- **Worst case:** O(n²) - where n is the number of cities
- **In practice:** O(500 × n) when starting nodes are limited

### Space Complexity

- O(n) - city data and route information

### Scalability

| Dataset Size       | Estimated Runtime | Approximate Success Rate |
| ------------------ | ----------------- | ------------------------ |
| n ≤ 100            | < 1 second        | 95-100%                  |
| 100 < n ≤ 1,000    | 1-5 seconds       | 80-95%                   |
| 1,000 < n ≤ 10,000 | 5-30 seconds      | 60-80%                   |
| n > 10,000         | 30-180 seconds    | 40-70%                   |

> **Note:** Success rate = (Number of visited cities / Total number of cities)

---

## 🔍 Example Scenario

### Input File (example-input-1.txt)

```
0 200 800 0 9000         # Starting city (center)
1 3600 2300 1205 10205   # Open 12:05-10:05
2 3100 3300 1680 10680   # Open 16:80-10:80
```

### Running the Code

```bash
python solver.py example-input-1.txt my-output.txt
python tsp_tw_verifier.py example-input-1.txt my-output.txt
```

### Expected Output

```
k=3, total_length=14250, completion_time=10915
```

---

## 🎓 Why Greedy Heuristic?

### Reasons for Choosing Greedy Heuristic

1. **Handling NP-Hard Problem:** Finding optimal solution takes O(n!) time, while Greedy takes O(n²)
2. **Practical Results:** Produces good results in reasonable time for 50,000 cities
3. **Simple and Applicable:** Easy to verify and debug
4. **Deterministic:** Always produces the same result for the same input

### Other Possible Approaches

- **Optimal (Brute Force):** Ideal for small datasets, impractical for large ones
- **Dynamic Programming:** Complex due to time window constraints
- **Genetic Algorithm:** Better results possible, but longer execution time
- **Ant Colony Optimization:** Good performance but more complex

---

## 🐛 Possible Improvements

### Short-term

1. **2-Opt Local Search:** Improve Greedy results
2. **Dynamic Penalty Coefficient:** Automatic adjustment based on problem characteristics
3. **Parallelization:** Process different starting points concurrently

### Long-term

1. **Hybrid Algorithms:** Combination of Greedy + Genetic Algorithm
2. **Machine Learning:** Predict good starting points
3. **Constraint Programming:** Use ORTools or similar libraries

---

## 📚 References

- **Problem Definition:** Conforms to rules specified in PDF specification
- **Validation:** Methodology provided by `tsp_tw_verifier.py`
- **Distance Calculation:** Euclidean distance according to formula in PDF

---

## ✅ Checklist

Before submitting the project, verify:

- [ ] `solver.py` runs without errors?
- [ ] Output file has valid format?
- [ ] `tsp_tw_verifier.py` passes validation?
- [ ] Time window constraints are satisfied?
- [ ] k (visited cities) is a reasonable value?
- [ ] Total distance and waiting time calculations are correct?

---

## 📞 Troubleshooting

### Common Issues

#### 1. "FileNotFoundError" Error

```
python solver.py input.txt output.txt
```

→ Check if the input file exists at the correct path

#### 2. "ValueError: invalid literal for int()"

```
Input error at line X
```

→ Verify input file format (must have 5 columns)

#### 3. Too Few Cities Visited

- Increase the penalty coefficient (more waiting tolerance)
- Increase the number of starting nodes
- Check if time window constraints are too strict

#### 4. Program Takes Longer Than 180 Seconds

- Reduce the number of starting nodes if input file is very large
- Adjust the penalty coefficient to affect computation speed

---

## 📝 License and Notes

This project is for educational purposes. While the Greedy heuristic approach produces reasonable results in most cases, more complex algorithms may be needed for special scenarios.

---

**Last Updated:** June 3, 2026

**Developer:** TSP-TW Solution Team
