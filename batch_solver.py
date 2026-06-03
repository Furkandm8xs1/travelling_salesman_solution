import sys
import math
import time
import random
import os

def calc_dist(city1, city2):
    """Euclidean mesafesini hesaplar ve en yakın tamsayıya yuvarlar."""
    x1, y1 = city1[1], city1[2]
    x2, y2 = city2[1], city2[2]
    return math.floor(math.sqrt((x1 - x2)**2 + (y1 - y2)**2) + 0.5)

def solve_instance(input_file, output_file, time_limit=20):
    cities = {}
    
    try:
        with open(input_file, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts: continue
                cid, x, y, op, cl = map(int, parts)
                cities[cid] = (cid, x, y, op, cl)
    except FileNotFoundError:
        print(f"Hata: {input_file} bulunamadı.")
        return

    city_ids = list(cities.keys())
    n = len(city_ids)

    best_k = -1
    best_dist = float('inf')
    best_time = float('inf')
    best_tour = []

    # Başlangıç şehirlerini filtrele (Zamanı en erken başlayan ilk %20'lik dilim)
    sorted_by_open = sorted(city_ids, key=lambda cid: cities[cid][3])
    start_nodes = sorted_by_open[:min(n, max(100, n // 5))]

    start_time_limit = time.time()
    iteration_count = 0

    # Belirlenen süre boyunca rastgeleleştirilmiş açgözlü (GRASP) araması yap
    while time.time() - start_time_limit < time_limit:
        iteration_count += 1
        
        start_id = random.choice(start_nodes)
        start_city = cities[start_id]
        current_time = max(0, start_city[3])
        
        if current_time > start_city[4]:
            continue 

        unvisited = set(city_ids)
        unvisited.remove(start_id)

        current_id = start_id
        tour = [start_id]
        total_dist = 0

        while unvisited:
            candidates = []

            for candidate_id in unvisited:
                cand = cities[candidate_id]
                d = calc_dist(cities[current_id], cand)
                arrival = current_time + d

                if arrival <= cand[4]:
                    wait = max(0, cand[3] - arrival)
                    score = d + (wait * 1.2)
                    candidates.append((score, candidate_id, d, wait))

            if not candidates:
                break

            candidates.sort(key=lambda x: x[0])
            
            top_n = min(3, len(candidates))
            chosen = random.choice(candidates[:top_n])
            
            best_next_dist = chosen[2]
            best_next_wait = chosen[3]
            best_next = chosen[1]

            current_time = current_time + best_next_dist + best_next_wait
            total_dist += best_next_dist
            tour.append(best_next)
            unvisited.remove(best_next)
            current_id = best_next

        # Başlangıç şehrine dön
        d_return = calc_dist(cities[current_id], cities[start_id])
        total_dist += d_return
        current_time += d_return

        k = len(tour)
        
        # Daha iyi bir çözüm bulunduysa güncelle
        if (k > best_k) or \
           (k == best_k and total_dist < best_dist) or \
           (k == best_k and total_dist == best_dist and current_time < best_time):
            best_k = k
            best_dist = total_dist
            best_time = current_time
            best_tour = tour

    # Çıktıyı yaz
    if best_k > 0:
        with open(output_file, 'w') as f:
            f.write(f"{best_k} {best_dist} {best_time}\n")
            for cid in best_tour:
                f.write(f"{cid}\n")
            f.write("\n")
        print(f"  -> Bitti! ({iteration_count} rota denendi) | Ziyaret: {best_k}, Mesafe: {best_dist}, Süre: {best_time}")
    else:
        print(f"  -> Geçerli bir rota bulunamadı.")

if __name__ == "__main__":
    # Test edilecek input dosyaları
    input_files = [
        "example-input-1.txt", 
        "example-input-2.txt", 
        "example-input-3.txt"
    ]
    
    print("Toplu optimizasyon işlemi başlatılıyor... Her dosya için 3 ayrı deneme yapılacak.\n")
    
    for in_file in input_files:
        print(f"=== {in_file} için aramalar başlıyor ===")
        
        # Her input için 3 ayrı output dosyası oluştur
        for run_id in range(1, 4):
            # Dosya isimlendirmesi: example-output-1_run1.txt gibi
            base_name = in_file.replace("input", "output").replace(".txt", "")
            out_file = f"{base_name}_run{run_id}.txt"
            
            print(f"[{run_id}/3] {out_file} oluşturuluyor (20 sn)...", end="\r")
            
            # 20 saniyelik limit ile çalıştır
            solve_instance(in_file, out_file, time_limit=20)
            
        print("-" * 60)
        
    print("Tüm işlemler başarıyla tamamlandı. Çıktı dosyalarını karşılaştırabilirsin.")