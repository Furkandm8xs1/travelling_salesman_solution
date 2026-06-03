import sys
import math
import time
import random

def calc_dist(city1, city2):
    """Calculate Euclidean distance according to PDF specification."""
    x1, y1 = city1[1], city1[2]
    x2, y2 = city2[1], city2[2]
    # d(i,j) = floor(sqrt((x_i - x_j)^2 + (y_i - y_j)^2) + 0.5)
    return math.floor(math.sqrt((x1 - x2)**2 + (y1 - y2)**2) + 0.5)

def greedy_construct(start_id, cities, city_ids, global_start_time):
    """Construct a tour using simple greedy approach."""
    start_city = cities[start_id]
    current_time = max(0, start_city[3])
    
    if current_time > start_city[4]:
        return None
    
    unvisited = set(city_ids)
    unvisited.discard(start_id)
    
    tour = [start_id]
    current_id = start_id
    
    while unvisited and time.time() - global_start_time < 170:
        best_next = None
        best_score = float('inf')
        best_next_dist = 0
        best_next_wait = 0
        
        for candidate_id in unvisited:
            cand = cities[candidate_id]
            d = calc_dist(cities[current_id], cand)
            arrival = current_time + d
            
            # Must arrive before closing time
            if arrival <= cand[4]:
                wait = max(0, cand[3] - arrival)
                
                # Simple greedy: prioritize distance, then waiting
                score = d + wait * 1.0
                
                if score < best_score:
                    best_score = score
                    best_next = candidate_id
                    best_next_dist = d
                    best_next_wait = wait
        
        if best_next is None:
            break
        
        current_time = current_time + best_next_dist + best_next_wait
        tour.append(best_next)
        unvisited.remove(best_next)
        current_id = best_next
    
    return tour

def calculate_tour_result(tour, cities, start_id):
    """Calculate k, distance, and time for a tour."""
    if not tour:
        return 0, float('inf'), float('inf')
    
    start_city = cities[start_id]
    current_time = max(0, start_city[3])
    total_dist = 0
    
    for i in range(len(tour) - 1):
        curr_id = tour[i]
        next_id = tour[i+1]
        d = calc_dist(cities[curr_id], cities[next_id])
        total_dist += d
        arrival = current_time + d
        
        if next_id == start_id:
            # Return to start
            current_time = arrival
        else:
            # Check time window
            if arrival > cities[next_id][4]:
                return 0, float('inf'), float('inf')
            
            wait = max(0, cities[next_id][3] - arrival)
            current_time = arrival + wait
    
    visited_count = len(tour) - 2
    return visited_count, total_dist, current_time

def solve_tsp_tw(input_file, output_file):
    cities = {}
    
    # 1. Read input
    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            cid, x, y, op, cl = map(int, parts)
            cities[cid] = (cid, x, y, op, cl)

    city_ids = list(cities.keys())
    n = len(city_ids)

    best_k = -1
    best_dist = float('inf')
    best_time = float('inf')
    best_tour = []

    global_start_time = time.time()

    # 2. DETERMINISTIC: Try all cities in order (no random shuffle)
    start_nodes = sorted(city_ids)  # Sort for deterministic order

    # 3. Multi-start greedy
    for start_id in start_nodes:
        # Hard 175-second limit
        if time.time() - global_start_time > 175:
            break

        # Construct tour
        tour = greedy_construct(start_id, cities, city_ids, global_start_time)
        
        if not tour:
            continue

        # Add return to start
        tour.append(start_id)
        
        # Calculate metrics
        k, total_dist, completion_time = calculate_tour_result(tour, cities, start_id)
        
        if k == 0:
            continue

        # Lexicographic: maximize k, then minimize dist, then minimize time
        is_better = False
        if k > best_k:
            is_better = True
        elif k == best_k:
            if total_dist < best_dist:
                is_better = True
            elif total_dist == best_dist and completion_time < best_time:
                is_better = True

        if is_better:
            best_k = k
            best_dist = total_dist
            best_time = completion_time
            best_tour = tour

    # 4. Write output
    with open(output_file, 'w') as f:
        # Output format: k, distance, time, then cities (excluding return)
        output_tour = best_tour[:-1] if best_tour else []
        f.write(f"{len(output_tour)} {best_dist} {best_time}\n")
        for cid in output_tour:
            f.write(f"{cid}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python solver.py <input.txt> <output.txt>")
    else:
        solve_tsp_tw(sys.argv[1], sys.argv[2])
