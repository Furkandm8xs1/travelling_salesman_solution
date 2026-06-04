import sys
import math
import time
import random

def calc_dist(city1, city2):
    """Euclidean mesafesini hesaplar ve en yakın tamsayıya yuvarlar[cite: 16, 18]."""
    x1, y1 = city1[1], city1[2]
    x2, y2 = city2[1], city2[2]
    return math.floor(math.sqrt((x1 - x2)**2 + (y1 - y2)**2) + 0.5)

def solve_instance(input_file, output_file, time_limit=20):
    cities = {}
    try:
        with open(input_file, 'r', encoding='utf-8-sig') as f:
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

    start_time_limit = time.time()
    iteration_count = 0

    # Belirlenen süre sınırı boyunca aramayı sürdür
    while time.time() - start_time_limit < time_limit:
        iteration_count += 1
        
        # Her iterasyonda keşif alanını genişletmek için rastgele bir başlangıç noktası seç
        start_id = random.choice(city_ids)
        start_city = cities[start_id]
        current_time = max(0, start_city[3])
        
        if current_time > start_city[4]:
            continue 

        unvisited = set(city_ids)
        unvisited.remove(start_id)

        current_id = start_id
        tour = [start_id]
        total_dist = 0

        # --- Kapsamlı Tam Tarama (O(N) - Kör Noktalar Temizlendi) ---
        while unvisited:
            best_candidates = []
            c_city = cities[current_id]
            
            for candidate_id in unvisited:
                cand = cities[candidate_id]
                
                if current_time <= cand[4]:
                    d = calc_dist(c_city, cand)
                    arrival = current_time + d

                    if arrival <= cand[4]:
                        wait = max(0, cand[3] - arrival)
                        # Mesafe ve bekleme maliyetine göre saf skorlama
                        score = d + (wait * 1.5)
                        best_candidates.append((score, candidate_id, d, wait))

            if not best_candidates:
                break

            # En iyi 3 olasılıktan birini rastgele seç (GRASP Çeşitliliği)
            best_candidates.sort(key=lambda x: x[0])
            top_n = min(3, len(best_candidates))
            chosen = random.choice(best_candidates[:top_n])
            
            best_next_dist = chosen[2]
            best_next_wait = chosen[3]
            chosen_id = chosen[1]

            current_time = current_time + best_next_dist + best_next_wait
            total_dist += best_next_dist
            tour.append(chosen_id)
            unvisited.remove(chosen_id)
            current_id = chosen_id

        # Başlangıç noktasına geri dönüş rotasını bağla [cite: 13, 15]
        d_return = calc_dist(cities[current_id], cities[start_id])
        total_dist += d_return
        current_time += d_return

        k = len(tour)
        
        # Leksikografik Karşılaştırma Kuralı [cite: 39, 40, 41, 42]
        if (k > best_k) or \
           (k == best_k and total_dist < best_dist) or \
           (k == best_k and total_dist == best_dist and current_time < best_time):
            best_k = k
            best_dist = total_dist
            best_time = current_time
            best_tour = list(tour)

    # --- Dosya Çıktısını Şartnameye Uygun Biçimde Yazdırırma ---
    if best_k > 0:
        with open(output_file, 'w') as f:
            # İlk satır: k, toplam uzunluk, bitiş zamanı [cite: 58, 59, 60, 61]
            f.write(f"{best_k} {best_dist} {best_time}\n")
            # Sonraki k satırda şehir ID'leri [cite: 62]
            for cid in best_tour:
                f.write(f"{cid}\n")
            # Dosyanın son satırı boş bırakılmalıdır [cite: 65]
            f.write("\n")
        print(f"  -> {output_file} Tamamlandı! ({iteration_count} rota denendi) | Şehir (K): {best_k}, Mesafe: {best_dist}, Süre: {best_time}")
    else:
        print(f"  -> {output_file} için geçerli bir rota üretilemedi.")

if __name__ == "__main__":
    # İşlenecek girdi veri setleri
    input_files = [
        "input1.txt",
        "input2.txt",
        "input3.txt",
        "input4.txt",
        "input5.txt",
        "input6.txt",
        "input7.txt"
    ]
    
    print("Toplu V3 Optimizasyon Süreci Başlatıldı...\n")
    
    for in_file in input_files:
        print(f"=== {in_file} İçin Çoklu Denemeler Başlıyor ===")
        
        for run_id in range(1, 4):
            # Dosya isimleri otomatik olarak 'example-output-X_runY.txt' formatına dönüştürülür
            base_name = in_file.replace("input", "output").replace(".txt", "")
            out_file = f"{base_name}_run{run_id}.txt"
            
            # Dev veri kümesi (Input-3) için arama süresini 40 saniyeye çıkarıp derinliği artırıyoruz
            t_limit = 40 if "input-3" in in_file else 20
            
            print(f" [{run_id}/3] {out_file} hesaplanıyor...", end="\r")
            solve_instance(in_file, out_file, time_limit=t_limit)
            
        print("-" * 65)
        
    print("Tüm çoklu çalıştırmalar başarıyla bitti! Çıktı dosyalarını dilediğin gibi kıyaslayabilirsin.")