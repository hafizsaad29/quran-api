from fastapi import FastAPI, HTTPException
import pandas as pd
import os

app = FastAPI()

def load_surahs():
    file_path = "quran_data.xlsx"
    if not os.path.exists(file_path):
        raise FileNotFoundError("Quran data file not found.")
    return pd.read_excel(file_path)

try:
    quran_data = load_surahs()
except FileNotFoundError as e:
    quran_data = pd.DataFrame()
    print(e)

@app.get("/")
async def root():
    return {"message": "Welcome to the Quran Surah API"}

# 1. Sirf Surah ka Naam
@app.get("/surah/{sura_id}")
async def get_surah_name(sura_id: int):
    if quran_data.empty:
        raise HTTPException(status_code=500, detail="Quran data not loaded.")

    filtered_data = quran_data[quran_data["SuraID"] == sura_id]

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail=f"Surah ID {sura_id} not found.")

    return {
        "Surah Name": filtered_data.iloc[0]["SurahNameU"]
    }

# 2. Surah ka Naam + Arabic Ayah
@app.get("/surah/{sura_id}/ayah/{aya_no}")
async def get_surah_ayah(sura_id: int, aya_no: int):
    if quran_data.empty:
        raise HTTPException(status_code=500, detail="Quran data not loaded.")

    filtered_data = quran_data[(quran_data["SuraID"] == sura_id) & (quran_data["AyaNo"] == aya_no)]

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail=f"Surah ID {sura_id} with Ayah {aya_no} not found.")

    return {
        "Surah Name": filtered_data.iloc[0]["SurahNameU"],
        "Arabic Text": filtered_data.iloc[0]["Arabic Text"]
    }

# 3. Surah ka Naam + Arabic Ayah + Urdu Translation
@app.get("/surah/{sura_id}/ayah/{aya_no}/urdu")
async def get_surah_ayah_urdu(sura_id: int, aya_no: int):
    if quran_data.empty:
        raise HTTPException(status_code=500, detail="Quran data not loaded.")

    filtered_data = quran_data[(quran_data["SuraID"] == sura_id) & (quran_data["AyaNo"] == aya_no)]

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail=f"Surah ID {sura_id} with Ayah {aya_no} not found.")

    return {
        "Surah Name": filtered_data.iloc[0]["SurahNameU"],
        "Arabic Text": filtered_data.iloc[0]["Arabic Text"],
        "Urdu Translation": filtered_data.iloc[0]["Fateh Muhammad Jalandhri"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
