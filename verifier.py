import gnupg, hashlib, os
from sqlalchemy.orm import Session
from db import PublicKey, SignatureCheck, Document

gpg = gnupg.GPG()   # использует ваше хранилище ключей ~/.gnupg

def sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def import_key(session: Session, armored: str, employee_id: int) -> PublicKey:
    res = gpg.import_keys(armored)
    if not res.fingerprints:
        raise ValueError("Некорректный ключ")
    fp = res.fingerprints[0]
    key = PublicKey(key_fingerprint=fp, key_id=fp[-8:],
                    armored_key=armored, employee_id=employee_id)
    session.add(key)
    return key

def verify_document(session: Session, doc_path: str, sig_path: str,
                    direction: str = "in") -> SignatureCheck:
    if not os.path.exists(sig_path):
        return SignatureCheck(document_id=_add_doc(session, doc_path, direction),
                              signature_file=sig_path, status="missing_sig",
                              details="Файл подписи отсутствует")

    verified = gpg.verify_file(open(sig_path, "rb"), doc_path)
    doc_id = _add_doc(session, doc_path, direction)

    if verified.valid:
        status, details = "valid", f"Good signature from {verified.username}"
        key = session.query(PublicKey).filter_by(
            key_fingerprint=verified.fingerprint).first()
    else:
        status, details = "invalid", (verified.stderr or "Подпись неверна")[:500]
        key = None

    check = SignatureCheck(document_id=doc_id,
                           key_id=key.id if key else None,
                           signature_file=sig_path,
                           status=status, details=details)
    session.add(check)
    return check

def _add_doc(session, doc_path, direction):
    doc = Document(direction=direction, filename=os.path.basename(doc_path),
                   file_hash=sha256(doc_path), storage_path=doc_path)
    session.add(doc); session.flush()
    return doc.id
