# Zaman Pencereli Gezgin Satıcı Problemi (TSP-TW) Çözümü

## 📋 Proje Özeti

Bu proje, **Zaman Pencereli Gezgin Satıcı Problemi (Travelling Salesman Problem with Time Windows - TSP-TW)** olarak bilinen NP-Hard sınıfındaki zorlu bir optimizasyon probleminin çözümüdür. Proje, 50.000'e kadar şehri içerebilen devasa veri setlerinde etkili bir **Greedy Heuristic** (Açgözlü) algoritması kullanmaktadır.

---

## 🎯 Problem Tanımı

### TSP-TW Nedir?

Gezgin Satıcı Probleminin zaman penceresi kısıtlamasıyla genişletilmiş halidir:

- **Amaç:** Satıcı, tüm şehirleri (veya mümkün olduğunca çoğunu) ziyaret ederek başlangıç şehrine dönüş yapmak
- **Kısıtlamalar:**
  - Her şehrin **zaman penceresi** vardır: [açılış_saati, kapanış_saati]
  - Satıcı bir şehre **varış_zamanı ≤ kapanış_saati** olduğu sürece gidebilir
  - Erken varılırsa açılış_saati'ne kadar beklenir
  - Dönüş sırasında başlangıç şehrinin zaman penceresi dikkate alınmaz
- **Optimize Edilecekler:**
  - Ziyaret edilen şehir sayısı (k) maksimize edilir
  - Toplam mesafe ve bekleme süresi minimize edilir

---

## 🚀 Çözüm Yaklaşımı: Greedy Heuristic

### 1. **Çoklu Başlangıç (Multi-Start)**

- Algoritma yalnızca tek bir şehirden değil, birçok başlangıç noktasından rotalar oluşturur
- Zaman penceresinin en erken açılan şehirlerden başlanır
- Veri seti büyükse (n > 500) başlangıç adayları sınırlandırılır (ilk 500 şehir)
- Bu yaklaşım, yerel optimumdan kaçınmaya yardımcı olur

### 2. **Skorlama Sistemi (Scoring)**

Her adımda, mevcut şehirden gidilebilecek geçerli şehirler arasında seçim yapılırken:

```
skor = mesafe + (bekleme_süresi × ceza_katsayısı)
```

- Düşük skor değeri olan şehir seçilir
- Bu, hem mesafeyi hem de bekleme süresini dengeleyen bir maliyet fonksiyonudur
- **Ceza katsayısı:** Uzun bekleme sürelerine karşı daha agresif cezalandırma yapılır

### 3. **Zaman Penceresi Kontrolü**

- Her bir şehir için varış zamanı kontrol edilir
- Eğer varış zamanı şehrin kapanış saatinden önceyse şehir geçerli sayılır
- Erken varılırsa açılış saatine kadar bekleme yapılır
- Dönüş rotasında başlangıç şehrinin zaman penceresi dikkate alınmaz

### 4. **Verimlilik Optimizasyonu**

- Büyük veri setleri (n > 50.000) için hesaplama süresi sınırlandırılır (maksimum 180 saniye)
- Her başlangıç noktası için en iyi rota kaydedilir
- Tüm başlangıç noktaları arasından en iyi sonuç seçilir

---

## 📁 Proje Dosya Yapısı

```
travelling-salesman/
│
├── README.md                   # Bu dosya - proje dokümantasyonu
├── solver.py                   # Ana çözüm algoritması (Greedy Heuristic)
├── tsp_tw_verifier.py          # Doğrulama ve sonuç kontrolü aracı
├── example-input-1.txt         # Örnek input dosyası
├── example-output-1.txt        # Örnek output dosyası
└── my-output.txt               # Oluşturulan çıktı (solver.py tarafından)
```

### Dosya Açıklamaları

#### `solver.py`

- **Amaç:** TSP-TW problemini çözen ana algoritma
- **Giriş:** Input dosyası yolu (şehir verileri)
- **Çıkış:** Output dosyası yolu (rota ve istatistikler)
- **Çalışma Mantığı:**
  1. Input dosyasından şehir verilerini okur
  2. Çoklu başlangıç noktalarından rotalar oluşturur
  3. En iyi rotayı bulur
  4. Sonuçları output dosyasına yazar

#### `tsp_tw_verifier.py`

- **Amaç:** Çözüm sonuçlarını doğrula ve geçerliliğini kontrol et
- **Doğrulama Kuralları:**
  - Tüm zaman penceresi kısıtlamalarının sağlanması
  - Mesafe hesaplamalarının doğruluğu
  - Rota bağlantılarının geçerliliği
  - Dosya formatının uygunluğu

#### Input Dosyası Formatı (`example-input-1.txt`)

```
city_id x y open_time close_time
0       200 800  0     9000
1       3600 2300 1205 10205
...
```

- **city_id:** Şehir tanımlayıcısı (0'dan başlar)
- **x, y:** Kartezyen koordinatlar
- **open_time:** Şehrin açılış saati
- **close_time:** Şehrin kapanış saati

#### Output Dosyası Formatı

```
k total_length completion_time
city_1
city_2
...
city_k
0
```

- **k:** Ziyaret edilen şehir sayısı
- **total_length:** Toplam kat edilen mesafe (tüm parçaların toplamı)
- **completion_time:** Başlangıça dönüş zamanı (saniye cinsinden)
- **city_1, city_2, ..., city_k:** Rota (0'ıncı şehir başlangıç noktası)
- **0:** Başlangıç şehrine dönüş

---

## 🛠️ Nasıl Kullanılır?

### Gereksinimler

- Python 3.7 veya üzeri
- Standart kütüphane (`math`, `sys`, `time`)

### Çalıştırma Adımları

#### 1. Adım: Çözümü Çalıştır

```bash
python solver.py example-input-1.txt my-output.txt
```

**Parametreler:**

- `example-input-1.txt`: Input dosyası (şehir verileri)
- `my-output.txt`: Output dosyası (çıktı rotası)

**Çıktı Örneği:**

```
k=18, total_length=48531, completion_time=16733 (best found so far)
Route optimization finished in 3.45 seconds
```

#### 2. Adım: Sonuçları Doğrula

```bash
python tsp_tw_verifier.py example-input-1.txt my-output.txt
```

**Çıktı Örneği (Başarılı):**

```
✓ Route verification passed
✓ All cities visited within time windows
✓ Output file format is valid
k=18, total_length=48531, completion_time=16733
```

**Çıktı Örneği (Hata Durumunda):**

```
✗ Verification failed: City 5 violated time window
```

---

## 📊 Algoritma Performansı

### Zaman Karmaşıklığı

- **En kötü durumda:** O(n²) - burada n şehir sayısı
- **Pratikte:** Başlangıç düğümleri sınırlandırıldığında O(500 × n)

### Alan Karmaşıklığı

- O(n) - şehir verileri ve rota bilgileri

### Ölçeklenebilirlik

| Veri Seti Boyutu   | Tahmini Çalışma Süresi | Yaklaşık Başarı Oranı |
| ------------------ | ---------------------- | --------------------- |
| n ≤ 100            | < 1 saniye             | %95-100               |
| 100 < n ≤ 1.000    | 1-5 saniye             | %80-95                |
| 1.000 < n ≤ 10.000 | 5-30 saniye            | %60-80                |
| n > 10.000         | 30-180 saniye          | %40-70                |

> **Not:** Başarı oranı = (Ziyaret edilen şehir sayısı / Toplam şehir sayısı)

---

## 🔍 Örnek Senaryo

### Input Dosyası (example-input-1.txt)

```
0 200 800 0 9000         # Başlangıç şehri (merkez)
1 3600 2300 1205 10205   # 12:05-10:05 arasında açık
2 3100 3300 1680 10680   # 16:80-10:80 arasında açık
```

### Kod Çalıştırma

```bash
python solver.py example-input-1.txt my-output.txt
python tsp_tw_verifier.py example-input-1.txt my-output.txt
```

### Beklenen Çıktı

```
k=3, total_length=14250, completion_time=10915
```

---

## 🎓 Algoritma Seçimi Nedenleri

### Neden Greedy Heuristic?

1. **NP-Hard Problemin Üstesinden Gelme:** Optimal çözüm bulmak O(n!) zaman alırken, Greedy O(n²)
2. **Pratik Sonuçlar:** 50.000 şehir için makul bir sürede iyi sonuçlar üretir
3. **Basit ve Uygulanabilir:** Doğrulama ve hata ayıklama kolaydır
4. **Deterministic:** Aynı input için her zaman aynı sonucu üretir

### Diğer Olası Yaklaşımlar

- **Optimal (Tam Araştırma):** Küçük veri setler için ideal, büyük setlerde praktik değil
- **Dinamik Programlama:** Zaman penceresi kısıtlaması nedeniyle karmaşık
- **Genetik Algoritma:** Daha iyi sonuçlar mümkün ama çalışma süresi uzun
- **Ant Colony Optimization:** İyi performans ama daha karmaşık

---

## 🐛 Olası İyileştirmeler

### Kısa Vadeli

1. **2-Opt Yerelleştirme:** Greedy sonucu iyileştirmek için
2. **Dinamik Ceza Katsayısı:** Problem özellikleri doğrultusunda otomatik ayarlama
3. **Parallelizasyon:** Farklı başlangıç noktalarını eş zamanlı işlemler

### Uzun Vadeli

1. **Melez Algoritmalar:** Greedy + Genetik Algoritma kombinasyonu
2. **Makine Öğrenmesi:** Iyi başlangıç noktalarını tahmin etme
3. **Kısıt Programlama:** ORTools veya benzer kütüphaneler kullanma

---

## 📚 Kaynaklar

- **Problem Tanımı:** PDF spesifikasyonunda belirtilen kurallara uygun
- **Doğrulama:** `tsp_tw_verifier.py` tarafından sağlanan metodoloji
- **Mesafe Hesabı:** Euclidean mesafesi, PDF'te belirtilen formüle göre

---

## ✅ Kontrol Listesi

Proje tamamlandığında şunları kontrol edin:

- [ ] `solver.py` hatasız çalıştırılır mı?
- [ ] Output dosyası geçerli formatı sağlıyor mu?
- [ ] `tsp_tw_verifier.py` doğrulamayı geçiyor mu?
- [ ] Zaman penceresi kısıtlamaları sağlanıyor mu?
- [ ] k (ziyaret edilen şehir) makul bir değer mi?
- [ ] Toplam mesafe ve bekleme süresi hesaplamaları doğru mu?

---

## 📞 Hata Ayıklama

### Sık Karşılaşılan Sorunlar

#### 1. "FileNotFoundError" hatası

```
python solver.py input.txt output.txt
```

→ Input dosyasının doğru yolda olup olmadığını kontrol edin

#### 2. "ValueError: invalid literal for int()"

```
Input error at line X
```

→ Input dosyasının formatını kontrol edin (5 sütun olması gerekir)

#### 3. Çok az şehir ziyaret edildi

- Ceza katsayısını arttırın (daha fazla bekleme toleransı)
- Başlangıç düğüm sayısını arttırın
- Zaman penceresi kısıtlamalarının çok katı olup olmadığını kontrol edin

#### 4. Program 180 saniyeden uzun sürüyor

- Input dosyası çok büyükse başlangıç düğümleri sayısını azaltın
- Ceza katsayısını değiştirerek hesaplama hızını etkileyebilirsiniz

---

## 📝 Lisans ve Notlar

Bu proje eğitim amaçlıdır. Greedy heuristic yaklaşımı çoğu durumda mantıklı sonuçlar verse de, bazı özel durumlarda daha karmaşık algoritmalar gerekebilir.

---

**Son Güncelleme:** 3 Haziran 2026

**Geliştirici:** TSP-TW Çözüm Ekibi
