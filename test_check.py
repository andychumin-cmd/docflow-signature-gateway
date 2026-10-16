from sqlalchemy.orm import Session
from db import engine
from verifier import verify_document

with Session(engine) as session:
    ok   = verify_document(session, "Chumin_AY_kleo.txt", "Chumin_AY_kleo.txt.sig")
    bad  = verify_document(session, "requirements.txt", "Chumin_AY_kleo.txt.sig")
    none = verify_document(session, "app.py", "not_exist.sig")
    session.commit()
    print("Верная подпись :", ok.status, "|", ok.details)
    print("Чужой документ :", bad.status,  "|", bad.details[:60])
    print("Без подписи    :", none.status, "|", none.details)
