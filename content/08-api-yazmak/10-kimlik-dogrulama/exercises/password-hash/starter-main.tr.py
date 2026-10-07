import hashlib
import hmac

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
SALT = "odyssey-salt"
users = {
    "ada": "887362783edaec9e1b53b6e44e5e7fd3d15211a39abe696032db618b212115b3",
    "alan": "a90c9f1188728ecdf5e047af7c9411d05288916f59c7a7446aa4074b0f0fdf01",
}

# hash_password(password, salt): pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000).hex()
# Login modeli: username, password
# POST /login: ozet users'takiyle esitse {"ok": true, "user": ad}
#   degilse (ya da kullanici yoksa) 401 "Wrong username or password"; karsilastirma hmac.compare_digest
