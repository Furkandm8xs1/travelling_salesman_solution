import sys
import math
import time

def calc_dist(city1, city2):
    """PDF yönergelerine göre Euclidean mesafesi hesaplar."""
    x1, y1 = city1[1], city1[2]
    x2, y2 = city2[1], city2[2]
    # d(i,j) = floor(sqrt((x_i - x_j)^2 + (y_i - y_j)^2) + 0.5)
    return math.floor(math.sqrt((x1 - x2)**2 + (y1 - y2)**2) + 0.5)

def solve_tsp_tw(input_file, output_file):
    cities = {}
    
    # 1. Girdiyi Oku
    with open(input_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if not parts: continue
            cid, x, y, op, cl = map(int, parts)
            cities[cid] = (cid, x, y, op, cl)

    city_ids = list(cities.keys())
    n = len(city_ids)

    best_k = -1
    best_dist = float('inf')
    best_time = float('inf')
    best_tour = []

    # Büyük N değerleri için başlangıç düğümlerini sınırla (Optimizasyon)
    start_nodes = city_ids
    if n > 500:
        # En erken açılan ilk 500 şehri başlangıç adayı yapıyoruz
        start_nodes = sorted(city_ids, key=lambda cid: cities[cid][3])[:500]

    start_time_limit = time.time()

    # 2. Çoklu Başlangıç ile Rota Oluşturma
    for start_id in start_nodes:
        # Programın makul bir sürede bitmesi için 3 dakikalık sınır (180 saniye)
        if time.time() - start_time_limit > 180:
            break

        start_city = cities[start_id]
        current_time = max(0, start_city[3])
        
        # Başlangıç şehri en baştan zaman penceresini kaçırıyorsa atla
        if current_time > start_city[4]:
            continue 

        unvisited = set(city_ids)
        unvisited.remove(start_id)

        current_id = start_id
        tour = [start_id]
        total_dist = 0

        # 3. Greedy (Açgözlü) Şehir Seçimi
        while unvisited:
            best_next = None
            best_score = float('inf')
            best_next_dist = 0
            best_next_wait = 0

            for candidate_id in unvisited:
                cand = cities[candidate_id]
                d = calc_dist(cities[current_id], cand)
                arrival = current_time + d

                # Eğer kapanış saatinden önce veya tam saatinde yetişebiliyorsak
                if arrival <= cand[4]:
                    wait = max(0, cand[3] - arrival)
                    visit_time = arrival + wait

                    # Mesafe ve bekleme süresine dayalı sezgisel skor
                    score = d + wait * 1.5 

                    if score < best_score:
                        best_score = score
                        best_next = candidate_id
                        best_next_dist = d
                        best_next_wait = wait

            # Gidilebilecek geçerli bir şehir kalmadıysa döngüyü kır
            if best_next is None:
                break

            # En iyi şehre ilerle
            current_time = current_time + best_next_dist + best_next_wait
            total_dist += best_next_dist
            tour.append(best_next)
            unvisited.remove(best_next)
            current_id = best_next

        # 4. Başlangıç Şehrine Dönüş (Dönüşte zaman penceresi kontrolü yoktur)
        d_return = calc_dist(cities[current_id], cities[start_id])
        total_dist += d_return
        current_time += d_return

        k = len(tour)
        
        # 5. Leksikografik Karşılaştırma (Daha fazla k > Daha az mesafe > Daha az zaman)
        if (k > best_k) or \
           (k == best_k and total_dist < best_dist) or \
           (k == best_k and total_dist == best_dist and current_time < best_time):
            best_k = k
            best_dist = total_dist
            best_time = current_time
            best_tour = tour

    # 6. Çıktıyı Dosyaya Yazma
    with open(output_file, 'w') as f:
        f.write(f"{best_k} {best_dist} {best_time}\n")
        for cid in best_tour:
            f.write(f"{cid}\n")
        f.write("\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Kullanım: python solver.py <input.txt> <output.txt>")
    else:
        solve_tsp_tw(sys.argv[1], sys.argv[2])