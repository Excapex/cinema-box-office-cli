import os
from auth import Auth
from models import User
from storage import Storage, USERS_F, FILMS_F, PROJ_F, SALES_F


def seed_if_missing():
    Storage.ensure_data_dir()

    if not os.path.exists(USERS_F):
        users = [
            User('admin', Auth.hash_password('admin'), 'administrator'),
            User('pera', Auth.hash_password('pera123'), 'blagajnik'),
            User('mika', Auth.hash_password('mika123'), 'kupac'),
        ]
        Auth.save_users(users)

    if not os.path.exists(FILMS_F):
        Storage.write_csv(FILMS_F, [
            {'film_id': 'F001', 'title': 'Interstellar', 'genre': 'Sci-Fi', 'duration_min': 169},
            {'film_id': 'F002', 'title': 'Inception', 'genre': 'Action', 'duration_min': 148},
            {'film_id': 'F003', 'title': 'Dune: Part Two', 'genre': 'Sci-Fi', 'duration_min': 165},
        ], ['film_id', 'title', 'genre', 'duration_min'])

    if not os.path.exists(PROJ_F):
        Storage.write_csv(PROJ_F, [
            {'proj_id': 'P001', 'film_id': 'F001', 'date': '2025-09-01', 'time': '20:00', 'hall': 'A', 'price': 6.5, 'capacity': 120},
            {'proj_id': 'P002', 'film_id': 'F002', 'date': '2025-09-01', 'time': '18:00', 'hall': 'B', 'price': 5.8, 'capacity': 90},
            {'proj_id': 'P003', 'film_id': 'F003', 'date': '2025-09-02', 'time': '21:00', 'hall': 'A', 'price': 7.0, 'capacity': 120},
        ], ['proj_id', 'film_id', 'date', 'time', 'hall', 'price', 'capacity'])

    if not os.path.exists(SALES_F):
        Storage.write_csv(SALES_F, [], ['sale_id', 'proj_id', 'username', 'quantity', 'unit_price', 'timestamp'])
