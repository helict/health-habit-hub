# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from classifier import segment_and_classify
from fuseki_store import store_donation_fuseki

app = FastAPI(title="Habit Segmentation API")

class HabitInput(BaseModel):
    donor_id: int
    text: str
    lang: str = "en"  # "en" for English or "de" for German
    source: str = "user"  # Default source is "user"

@app.post("/segment/")
def segment_and_store_habit(data: HabitInput):
    sentence = data.text
    donor_id = data.donor_id
    language = data.lang
    source = data.source
    
    # Segment and classify the sentence.
    parts = segment_and_classify(sentence, lang=language)
    
    # Store the donation data in Fuseki.
    status = store_donation_fuseki(donor_id, language, source, sentence, parts)
    
    return {
        "donor_id": donor_id,
        "parts": parts,
        "fuseki_status": status
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)