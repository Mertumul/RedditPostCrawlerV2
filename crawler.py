import subprocess

def calistir(dosya_yollar):
    islemler = []
    for dosya_yol in dosya_yollar:
        # Yeni bir süreç oluştur ve Python ile belirtilen dosyayı çalıştır
        proc = subprocess.Popen(['python3', dosya_yol])
        islemler.append(proc)

    # İşlemlerin tamamlanmasını bekleyin
    for islem in islemler:
        islem.wait()

# Çalıştırmak istediğiniz dosyaların adlarını liste olarak belirtin
dosya_adlari = ['main.py', 'app.py', 'database.py']

# Belirtilen dosyaları çalıştır
calistir(dosya_adlari)