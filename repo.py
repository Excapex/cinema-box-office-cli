from dataclasses import asdict
from typing import List
from models import Film, Projection, Sale
from storage import Storage, FILMS_F, PROJ_F, SALES_F


class Repo:
    films: List[Film] = []
    projections: List[Projection] = []
    sales: List[Sale] = []

    @staticmethod
    def load_all():
        
        f_rows = Storage.read_csv(
            FILMS_F,
            ['film_id', 'title', 'genre', 'duration_min'],
            cast=lambda r: {**r, 'duration_min': int(r['duration_min'])}
        )
        Repo.films = [Film(**r) for r in f_rows]

        
        p_rows = Storage.read_csv(
            PROJ_F,
            ['proj_id', 'film_id', 'date', 'time', 'hall', 'price', 'capacity'],
            cast=lambda r: {**r, 'price': float(r['price']), 'capacity': int(r['capacity'])}
        )
        Repo.projections = [Projection(**r) for r in p_rows]

        
        s_rows = Storage.read_csv(
            SALES_F,
            ['sale_id', 'proj_id', 'username', 'quantity', 'unit_price', 'timestamp'],
            cast=lambda r: {**r, 'quantity': int(r['quantity']), 'unit_price': float(r['unit_price'])}
        )
        Repo.sales = [Sale(**r) for r in s_rows]

    @staticmethod
    def save_all():
        Storage.write_csv(FILMS_F, [asdict(f) for f in Repo.films], ['film_id', 'title', 'genre', 'duration_min'])
        Storage.write_csv(PROJ_F, [asdict(p) for p in Repo.projections], ['proj_id', 'film_id', 'date', 'time', 'hall', 'price', 'capacity'])
        Storage.write_csv(SALES_F, [asdict(s) for s in Repo.sales], ['sale_id', 'proj_id', 'username', 'quantity', 'unit_price', 'timestamp'])
