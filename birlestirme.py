import zipfile
import os
import shutil
import hashlib

# Zip dosyalarını açmak ve verileri birleştirmek için fonksiyon
def extract_and_merge_zip_files(zip_files, output_dir):
    extracted_files = set()  # Unique dosyalar için set
    os.makedirs(output_dir, exist_ok=True)  # Çıktı klasörünü oluştur

    total_files = 0  # Toplam dosya sayısını takip etmek için
    processed_files = 0  # İşlenen dosyaları takip etmek için

    # İlk olarak toplam dosya sayısını bulalım
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            total_files += len(zip_ref.namelist())

    print(f'Toplam {total_files} dosya bulunuyor. İşlem başlatılıyor...')

    for zip_file in zip_files:
        print(f"{zip_file} zip dosyası işleniyor...")
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Geçici bir klasöre zip dosyasını çıkart
            temp_dir = os.path.join(output_dir, 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            zip_ref.extractall(temp_dir)

            # Çıkartılan dosyaları unique olarak hedef klasöre taşı
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)

                    # Dosyanın hash'ini alarak unique olup olmadığını kontrol et
                    file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()

                    if file_hash not in extracted_files:
                        # Unique ise dosyayı çıktı klasörüne taşı
                        dest_dir = os.path.join(output_dir, os.path.relpath(root, temp_dir))
                        os.makedirs(dest_dir, exist_ok=True)
                        shutil.move(file_path, os.path.join(dest_dir, file))
                        extracted_files.add(file_hash)

                    processed_files += 1
                    # İşlenen dosya sayısını ve ilerlemeyi yazdır
                    print(f"İşlenen dosya: {processed_files}/{total_files} ({(processed_files/total_files)*100:.2f}%)")

            # Geçici klasörü temizle
            shutil.rmtree(temp_dir)

    print(f'Tüm zip dosyaları {output_dir} klasörüne başarıyla birleştirildi.')

# Kullanım
zip_files = ['zip1.zip', 'zip2.zip', 'zip3.zip', 'zip4.zip', 'zip5.zip']  # Zip dosyalarının yolu
output_dir = 'merged_output'  # Sonuç klasörü
extract_and_merge_zip_files(zip_files, output_dir)
