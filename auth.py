import hashlib
from dataclasses import asdict
from typing import List, Optional
from models import User
from storage import Storage, USERS_F


class Auth:
    @staticmethod
    def hash_password(pw: str) -> str:
        return hashlib.sha256(pw.encode('utf-8')).hexdigest()

    @staticmethod
    def load_users() -> List[User]:
        fieldnames = ['username', 'password_hash', 'role']
        rows = Storage.read_csv(USERS_F, fieldnames)
        return [User(**r) for r in rows]

    @staticmethod
    def save_users(users: List[User]) -> None:
        fieldnames = ['username', 'password_hash', 'role']
        rows = [asdict(u) for u in users]
        Storage.write_csv(USERS_F, rows, fieldnames)

    @staticmethod
    def authenticate(username: str, password: str) -> Optional[User]:
        ph = Auth.hash_password(password)
        for u in Auth.load_users():
            if u.username == username and u.password_hash == ph:
                return u
        return None
