from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import threading

from sozluk import sozluk, save_sozluk, load_sozluk, wiktionary_kelime_cek, bulk_load_from_source

app = FastAPI(title="PythonSozluk API", version="0.1")


class AddWord(BaseModel):
    word: str
    definition: str


class BulkRequest(BaseModel):
    source: str
    count: Optional[int] = 100


@app.on_event("startup")
def startup_event():
    # Ensure data loaded on startup
    load_sozluk()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/lookup")
def lookup(word: str):
    key = word.lower().strip()
    if not key:
        raise HTTPException(status_code=400, detail="Empty word")
    if key in sozluk:
        return {"word": key, "definition": sozluk[key], "source": "local"}

    # try wiktionary on-demand
    defn = wiktionary_kelime_cek(key)
    if defn:
        # do not auto-save remote lookups to local store automatically
        return {"word": key, "definition": defn, "source": "wiktionary"}

    raise HTTPException(status_code=404, detail="word not found")


@app.get("/words")
def list_words(limit: Optional[int] = 100):
    items = list(sozluk.items())[:limit]
    return {"count": len(sozluk), "words": [{"word": k, "definition": v} for k, v in items]}


@app.post("/add")
def add_word(payload: AddWord):
    w = payload.word.lower().strip()
    if not w:
        raise HTTPException(status_code=400, detail="Empty word")
    if w in sozluk:
        raise HTTPException(status_code=409, detail="word already exists")
    sozluk[w] = payload.definition
    save_sozluk()
    return {"status": "ok", "word": w}


def _run_bulk(source: str, count: int):
    # runs in a background thread
    try:
        bulk_load_from_source(source, kelime_sayisi=count)
    except Exception:
        pass


@app.post("/bulk")
def bulk(req: BulkRequest):
    # start background thread for bulk load so request returns quickly
    t = threading.Thread(target=_run_bulk, args=(req.source, req.count), daemon=True)
    t.start()
    return {"status": "started", "source": req.source, "count": req.count}
