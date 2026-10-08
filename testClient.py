import json
import requests

# 1. Tentukan URL endpoint LangServe Anda
# LangServe secara otomatis membuat suffix '/invoke' untuk eksekusi chain
URL_API = "http://127.0.0.1:8000/agent_MOM/invoke"

def send_transcript_to_api(file_path: str):
    try:
        # 2. Membaca isi file transkrip rapat (MOM)
        with open(file_path, "r", encoding="utf-8") as f:
            transcript_content = f.read()
        
        # 3. Susun Payload JSON sesuai skema input LangServe Anda
        # Menggunakan struktur {'input': {'messages': [...]}} sesuai standar eksekusi LangServe
        payload = {
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": transcript_content
                    }
                ]
            }
        }
        
        print(f"🚀 Mengirimkan transkrip dari '{file_path}' ke API LangServe...")
        
        # 4. Kirim HTTP POST Request ke Server
        headers = {"Content-Type": "application/json"}
        response = requests.post(URL_API, data=json.dumps(payload), headers=headers)
        
        # 5. Cek jika HTTP Request berhasil
        if response.status_code == 200:
            response_data = response.json()
            
            # Mengambil output teks bersih hasil akhir dari struktur response LangServe
            final_mom = response_data.get("output", "")
            
            print("\n================ HASIL NOTULENSI RAPAT (MOM) ================\n")
            print(final_mom)
            print("\n=============================================================\n")
            
            # Opsional: Simpan hasil balasan API ke file lokal baru
            with open("MOM_from_api.txt", "w", encoding="utf-8") as out_file:
                out_file.write(final_mom)
                print("💾 Hasil MoM berhasil disimpan ke 'MOM_from_api.txt'")
                
        else:
            print(f"❌ Gagal mendapatkan respons. Status Code: {response.status_code}")
            print("Detail Error:", response.text)
            
    except FileNotFoundError:
        print(f"❌ Error: File '{file_path}' tidak ditemukan di lokal.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan teknis: {str(e)}")

if __name__ == "__main__":
    # Pastikan file 'mom_test.txt' Anda berada di folder yang sama
    send_transcript_to_api("mom_test.txt")
