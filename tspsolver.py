""" 
    if you want to execute file you can write these  on the comman line 
    it is fixed.

    python maingreedysolver.py input.txt output.txt

    python maingreedysolver.py


"""

import sys
import os
import math
import time
import heapq
import random

#BE CAREFUL ABOUT BEFORE CHANGİNG THE VALUES : BE AWARE OF YOUR SYSTEM PROVİDE BİG CALCULATİONS.
#IT MAY BE HARMFUL FOR YOUR PC.

# we can change the value of parameter and we finalized the information about the values
# time is important big files for ex 50000 line
#beam width and max starts big differences input4

BEAM_WIDTH       = 50
NEIGHBOR_K       = 25
OPPORTUNITY_R    = 600
MAX_STARTS       = 80
TIME_LIMIT_SEC   = 120  
LOCAL_SEARCH_SEC = 8      


def dist_int(x1, y1, x2, y2):
    return math.floor(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2) + 0.5)


def read_input(path):
    cities = {}
    with open(path, "r", encoding="utf-8-sig") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 5:
                raise ValueError(f"Satır {line_no}: 5 değer bekleniyor.")
            cid, x, y, o, c = map(int, parts)
            if cid in cities:
                raise ValueError(f"Tekrar eden şehir ID: {cid}.")
            if o > c:
                raise ValueError(f"open > close, şehir {cid}.")
            cities[cid] = (cid, x, y, o, c)
    return cities


def write_output(path, route, total_length, completion_time):
    with open(path, "w") as f:
        f.write(f"{len(route)} {total_length} {completion_time}\n")
        for cid in route:
            f.write(f"{cid}\n")
        f.write("\n")


class KDNode:
    __slots__ = ("city_id", "left", "right", "axis")
    def __init__(self, city_id, axis, left=None, right=None):
        self.city_id = city_id
        self.axis    = axis
        self.left    = left
        self.right   = right


def build_kd(points, depth=0):
    if not points:
        return None
    axis = depth % 2
    points.sort(key=lambda p: p[axis])
    mid = len(points) // 2
    return KDNode(
        city_id=points[mid][2],
        axis=axis,
        left=build_kd(points[:mid], depth + 1),
        right=build_kd(points[mid + 1:], depth + 1),
    )


def kd_nearest_k(root, qx, qy, k, city_coords):
    heap = []

    def search(node):
        if node is None:
            return
        cx, cy = city_coords[node.city_id]
        d2 = (cx - qx) ** 2 + (cy - qy) ** 2
        if len(heap) < k:
            heapq.heappush(heap, (-d2, node.city_id))
        elif d2 < -heap[0][0]:
            heapq.heapreplace(heap, (-d2, node.city_id))
        axis = node.axis
        diff = (qx if axis == 0 else qy) - (cx if axis == 0 else cy)
        near, far = (node.left, node.right) if diff <= 0 else (node.right, node.left)
        search(near)
        if diff * diff < -heap[0][0] or len(heap) < k:
            search(far)

    search(root)
    return [cid for _, cid in heap]


def compute_opportunity(cities, city_coords, kd_root, R=OPPORTUNITY_R):
    opp = {}
    for cid, (x, y) in city_coords.items():
        neighbors = kd_nearest_k(kd_root, x, y, 60, city_coords)
        count = sum(1 for n in neighbors
                    if dist_int(x, y, *city_coords[n]) <= R and n != cid)
        opp[cid] = count
    return opp


def evaluate_route(route, cities):
    """(total_length, completion_time) döner; geçersizse None."""
    if not route:
        return 0, 0
    current_time = 0
    total_length = 0

    sc = route[0]
    _, _, _, o, c = cities[sc]
    current_time = max(current_time, o)
    if current_time > c:
        return None

    for i in range(1, len(route)):
        prev, curr = route[i - 1], route[i]
        _, px, py, _, _   = cities[prev]
        _, cx, cy, o, c   = cities[curr]
        d = dist_int(px, py, cx, cy)
        total_length += d
        visit = max(current_time + d, o)
        if visit > c:
            return None
        current_time = visit

    _, lx, ly, _, _ = cities[route[-1]]
    _, sx, sy, _, _ = cities[route[0]]
    ret_d = dist_int(lx, ly, sx, sy)
    total_length += ret_d
    current_time += ret_d
    return total_length, current_time


def score_candidate(cid, current_time, cx, cy, cities, city_coords, opp):
    _, nx, ny, o, c = cities[cid]
    d = dist_int(cx, cy, nx, ny)
    visit_t = max(current_time + d, o)
    if visit_t > c:
        return None
    slack    = c - visit_t
    urgency  = 1.0 / (slack + 1)
    distance = 1.0 / (d + 1)
    density  = opp.get(cid, 0) / 30.0
    return distance * 2.0 + urgency * 1.5 + density * 1.0, visit_t, d

# greedy algorithm 

def greedy_route(start_id, cities, city_coords, kd_root, opp):
    unvisited = set(cities.keys())
    route = [start_id]
    unvisited.discard(start_id)

    _, sx, sy, so, sc = cities[start_id]
    current_time = max(0, so)
    if current_time > sc:
        return []
    cx, cy = sx, sy

    while True:
        neighbors = kd_nearest_k(kd_root, cx, cy, NEIGHBOR_K * 2, city_coords)
        best_score, best_cid, best_t = -1, None, None
        for cid in neighbors:
            if cid not in unvisited:
                continue
            result = score_candidate(cid, current_time, cx, cy, cities, city_coords, opp)
            if result is None:
                continue
            s, vt, _ = result
            if s > best_score:
                best_score, best_cid, best_t = s, cid, vt
        if best_cid is None:
            break
        route.append(best_cid)
        unvisited.discard(best_cid)
        current_time = best_t
        _, cx, cy, _, _ = cities[best_cid]

    return route


def beam_search(start_id, cities, city_coords, kd_root, opp, beam_width=BEAM_WIDTH):
    _, sx, sy, so, sc_t = cities[start_id]
    t0 = max(0, so)
    if t0 > sc_t:
        return []

    beam      = [(0, 0, frozenset([start_id]), [start_id], t0, sx, sy)]
    best_route = [start_id]

    for _ in range(min(len(cities), 3000)):
        if not beam:
            break
        next_beam = []
        for neg_vis, tie_dist, vis_set, route, cur_t, cx, cy in beam:
            neighbors = kd_nearest_k(kd_root, cx, cy, NEIGHBOR_K, city_coords)
            for cid in neighbors:
                if cid in vis_set:
                    continue
                result = score_candidate(cid, cur_t, cx, cy, cities, city_coords, opp)
                if result is None:
                    continue
                _, vt, d = result
                _, nx, ny, _, _ = cities[cid]
                next_beam.append((
                    -(len(vis_set) + 1),
                    tie_dist + d,
                    vis_set | {cid},
                    route + [cid],
                    vt, nx, ny
                ))

        if not next_beam:
            break
        next_beam.sort(key=lambda s: (s[0], s[1]))
        beam = next_beam[:beam_width]
        if len(beam[0][2]) > len(best_route):
            best_route = beam[0][3]

    return best_route

#two optional search gives us to chance in example 4
def two_opt(route, cities, time_limit_sec):
    t_start = time.time()
    n = len(route)
    if n < 4:
        return route
    improved = True
    while improved and (time.time() - t_start) < time_limit_sec:
        improved = False
        old_result = evaluate_route(route, cities)
        if not old_result:
            break
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                new_route = route[:i] + route[i:j+1][::-1] + route[j+1:]
                result = evaluate_route(new_route, cities)
                if result and result[0] < old_result[0]:
                    route = new_route
                    improved = True
                    break
            if improved:
                break
    return route


def or_opt(route, cities, time_limit_sec):
    t_start = time.time()
    n = len(route)
    if n < 3:
        return route
    improved = True
    while improved and (time.time() - t_start) < time_limit_sec:
        improved = False
        old_result = evaluate_route(route, cities)
        if not old_result:
            break
        for i in range(n):
            city = route[i]
            rest = route[:i] + route[i+1:]
            for j in range(1, len(rest)):
                candidate = rest[:j] + [city] + rest[j:]
                result = evaluate_route(candidate, cities)
                if result and result[0] < old_result[0]:
                    route = candidate
                    n = len(route)
                    improved = True
                    break
            if improved:
                break
    return route


def solution_key(route, cities):
    if not route:
        return (0, 0)
    result = evaluate_route(route, cities)
    if result is None:
        return (0, 0)
    return (len(route), -result[0])


def solve(cities, time_limit=TIME_LIMIT_SEC):
    t_global    = time.time()
    city_ids    = list(cities.keys())
    city_coords = {cid: (cities[cid][1], cities[cid][2]) for cid in city_ids}
    points      = [(cities[cid][1], cities[cid][2], cid) for cid in city_ids]

    log("KD-Tree kuruluyor...")
    kd_root = build_kd(points)

    log("Fırsat yoğunluğu hesaplanıyor...")
    opp = compute_opportunity(cities, city_coords, kd_root)

    # Başlangıç şehirleri: erken kapananlar + yoğun bölge + rastgele
    by_close   = sorted(city_ids, key=lambda c: cities[c][4])[:MAX_STARTS // 3]
    by_density = sorted(city_ids, key=lambda c: -opp[c])[:MAX_STARTS // 3]
    random.seed(42)
    by_random  = random.sample(city_ids, min(MAX_STARTS // 3, len(city_ids)))
    start_candidates = list(dict.fromkeys(by_close + by_density + by_random))[:MAX_STARTS]

    best_route = []
    best_key   = (0, 0)
    elite_pool = []

    bw = BEAM_WIDTH if len(city_ids) <= 5000 else 30

    for idx, start in enumerate(start_candidates):
        elapsed = time.time() - t_global
        if elapsed > time_limit - LOCAL_SEARCH_SEC - 2:
            log(f"{idx} başlangıçtan sonra zaman doldu.")
            break

        log(f"[{idx+1}/{len(start_candidates)}] start={start}  "
            f"en iyi={best_key[0]} şehir  süre={elapsed:.1f}s")

        route = beam_search(start, cities, city_coords, kd_root, opp, beam_width=bw)
        if not route:
            route = greedy_route(start, cities, city_coords, kd_root, opp)

        key = solution_key(route, cities)
        if key > best_key:
            best_key, best_route = key, route
            log(f"  → Yeni en iyi: {key[0]} şehir, uzunluk={-key[1]}")

        elite_pool.append((key, route))

    # Elite çözümlere local search
    elite_pool.sort(key=lambda x: x[0], reverse=True)
    ls_budget = max(1.0, LOCAL_SEARCH_SEC / max(len(elite_pool[:5]), 1))

    for key, route in elite_pool[:5]:
        if time.time() - t_global > time_limit - 1:
            break
        log(f"Local search: {len(route)} şehirli rota...")
        route = two_opt(route, cities, ls_budget / 2)
        route = or_opt(route, cities, ls_budget / 2)
        k2 = solution_key(route, cities)
        if k2 > best_key:
            best_key, best_route = k2, route
            log(f"  → Local search iyileştirdi: {k2[0]} şehir, uzunluk={-k2[1]}")

    return best_route


def log(msg):
    print(msg, file=sys.stderr)


def process_file(input_path, output_path):
    log(f"\n{'='*50}")
    log(f"Input : {input_path}")
    log(f"Output: {output_path}")
    log(f"{'='*50}")

    cities = read_input(input_path)
    log(f"{len(cities)} şehir yüklendi.")

    route = solve(cities)

    if not route:
        write_output(output_path, [], 0, 0)
        log("Geçerli rota bulunamadı. Boş output yazıldı.")
        return

    result = evaluate_route(route, cities)
    if result is None:
        log("HATA: Son rota geçersiz!")
        return

    total_length, completion_time = result
    log(f"\nSonuç: {len(route)} şehir | uzunluk={total_length} | süre={completion_time}")
    write_output(output_path, route, total_length, completion_time)
    log(f"Output yazıldı: {output_path}")


def main():
    # Tek dosya modu: python tsp_tw_solver.py input.txt output.txt
    if len(sys.argv) == 3:
        process_file(sys.argv[1], sys.argv[2])
        return

    # Toplu mod: python a.py
    if len(sys.argv) == 1:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        input_files= [
        "inputs/input1.txt",
        "inputs/input2.txt",
        "inputs/input3.txt",
        "inputs/input4.txt",
        "inputs/input5.txt",
        "inputs/input6.txt",
        "inputs/input7.txt",
    ]

        for fname in input_files:
            input_path = os.path.join(script_dir, fname)
            if not os.path.exists(input_path):
                log(f"Dosya bulunamadı, atlanıyor: {input_path}")
                continue
            stem = os.path.splitext(fname)[0]
            output_path = os.path.join(script_dir, f"output_{stem}.txt")
            try:
                process_file(input_path, output_path)
            except Exception as e:
                log(f"HATA ({fname}): {e}")
        return

    print("Kullanım:")
    print("  Tek dosya : python tsp_tw_solver.py input.txt output.txt")
    print("  Toplu mod : python tsp_tw_solver.py")
    sys.exit(1)


if __name__ == "__main__":
    main()