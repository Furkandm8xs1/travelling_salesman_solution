import os
import matplotlib.pyplot as plt

def read_cities(filepath):
    """Girdi dosyasından şehir koordinatlarını okur ve sözlük olarak döndürür."""
    cities = {}
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 5:
                cid = int(parts[0])
                x, y = int(parts[1]), int(parts[2])
                cities[cid] = (x, y)
    return cities

def read_tour(filepath):
    """Çıktı dosyasından ziyaret edilen şehirlerin (CID) sırasını okur."""
    tour_cids = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()
        if not lines:
            return []
        
        # İlk satırda (ziyaret sayısı, uzunluk, tamamlanma süresi) bilgileri var, onu atlıyoruz
        for line in lines[1:]:
            line = line.strip()
            if line:
                tour_cids.append(int(line))
    return tour_cids

def visualize_tour(cities, tour_cids, input_filename, output_filename, script_dir):
    """Rotayı çizer ve PNG dosyası olarak kaydeder."""
    if not tour_cids:
        print(f"Uyarı: {output_filename} içinde rota bulunamadı!")
        return

    # Tüm şehirlerin koordinatları (Arka plan için)
    all_x = [pos[0] for pos in cities.values()]
    all_y = [pos[1] for pos in cities.values()]

    plt.figure(figsize=(12, 8))
    
    # 1. Bütün şehirleri soluk gri renkte çiz
    plt.scatter(all_x, all_y, c='lightgray', s=10, label='Ziyaret Edilmeyen Şehirler')

    # 2. Rota koordinatlarını çıkar
    tour_x = []
    tour_y = []
    for cid in tour_cids:
        if cid in cities:
            tour_x.append(cities[cid][0])
            tour_y.append(cities[cid][1])
    
    # Başlangıca geri dönüş çizgisini ekle
    if tour_cids[0] in cities:
        tour_x.append(cities[tour_cids[0]][0])
        tour_y.append(cities[tour_cids[0]][1])

    # 3. Rotayı çiz
    plt.plot(tour_x, tour_y, c='blue', linewidth=1.5, marker='o', markersize=4, 
             markerfacecolor='cyan', label='Ziyaret Edilen Şehirler / Rota')

    # 4. Başlangıç/Bitiş noktasını vurgula
    start_x = tour_x[0]
    start_y = tour_y[0]
    plt.scatter(start_x, start_y, c='red', s=150, marker='*', zorder=5, 
                edgecolors='black', label='Başlangıç / Bitiş')

    # Grafik ayarları
    plt.title(f"Rota Görselleştirmesi - {input_filename}\nToplam Ziyaret Edilen: {len(tour_cids)}")
    plt.xlabel("X Koordinatı")
    plt.ylabel("Y Koordinatı")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    # Dosyayı kaydet
    image_filename = input_filename.replace('.txt', '-rota.png')
    save_path = os.path.join(script_dir, image_filename)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Görsel kaydedildi: {image_filename}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Girdi ve çıktı dosya eşleştirmeleri
    files_to_process = [
        ('duzguninput.txt', 'output_duzguninput.txt'),
        ('example-input-1.txt', 'output_example-input-1.txt'),
        ('example-input-2.txt', 'output_example-input-2.txt'),
        ('example-input-3.txt', 'output_example-input-3.txt'),
        ('example-input-4.txt', 'output_example-input-4.txt')
    ]

    print("Görselleştirme başlatılıyor...\n" + "-"*40)

    for in_file, out_file in files_to_process:
        input_path = os.path.join(script_dir, in_file)
        output_path = os.path.join(script_dir, out_file)

        # Dosyaların varlığını kontrol et
        if not os.path.exists(input_path):
            print(f"Atlanıyor: {in_file} bulunamadı.")
            continue
        if not os.path.exists(output_path):
            print(f"Atlanıyor: {in_file} için çıktı dosyası ({out_file}) bulunamadı.")
            continue

        print(f"İşleniyor: {in_file} ve {out_file}...")
        
        # Verileri oku
        cities = read_cities(input_path)
        tour = read_tour(output_path)
        
        # Görselleştir ve kaydet
        visualize_tour(cities, tour, in_file, out_file, script_dir)

    print("-" * 40 + "\nTüm işlemler tamamlandı.")

if __name__ == '__main__':
    main()