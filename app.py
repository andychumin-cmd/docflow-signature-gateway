import shutil, tempfile
from fastapi import FastAPI, UploadFile, File
from sqlalchemy.orm import Session
from db import engine, SignatureCheck
from verifier import verify_document

app = FastAPI(title="DocFlow Signature Gateway")

@app.post("/check")
async def check_document(doc: UploadFile = File(...),
                         sig: UploadFile = File(...),
                         direction: str = "in"):
    with tempfile.TemporaryDirectory() as tmp:
        doc_path = f"{tmp}/{doc.filename}"
        sig_path = f"{tmp}/{sig.filename}"
        with open(doc_path, "wb") as f: shutil.copyfileobj(doc.file, f)
        with open(sig_path, "wb") as f: shutil.copyfileobj(sig.file, f)
        with Session(engine) as session:
            check = verify_document(session, doc_path, sig_path, direction)
            session.commit()
            return {"status": check.status, "details": check.details}

@app.get("/report")
def report():
    with Session(engine) as session:
        rows = session.query(SignatureCheck).all()
        return [{"id": r.id, "status": r.status, "details": r.details} for r in rows]
