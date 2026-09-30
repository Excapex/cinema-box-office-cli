import datetime as dt
from typing import Optional, Dict
from models import Film, Projection, Sale
from repo import Repo


class Services:
    # Pronalaženja
    @staticmethod
    def get_film(film_id: str) -> Optional[Film]:
        return next((f for f in Repo.films if f.film_id == film_id), None)

    @staticmethod
    def get_proj(proj_id: str) -> Optional[Projection]:
        return next((p for p in Repo.projections if p.proj_id == proj_id), None)

    @staticmethod
    def film_exists(film_id: str) -> bool:
        return Services.get_film(film_id) is not None

    @staticmethod
    def proj_exists(proj_id: str) -> bool:
        return Services.get_proj(proj_id) is not None

    # CRUD filmova
    @staticmethod
    def add_film(film: Film):
        if Services.film_exists(film.film_id):
            raise ValueError('Film sa tim ID već postoji.')
        Repo.films.append(film)

    @staticmethod
    def update_film(film_id: str, **kwargs):
        f = Services.get_film(film_id)
        if not f:
            raise ValueError('Film ne postoji.')
        for k, v in kwargs.items():
            if hasattr(f, k):
                setattr(f, k, v)

    @staticmethod
    def delete_film(film_id: str):
        before = len(Repo.films)
        Repo.films[:] = [f for f in Repo.films if f.film_id != film_id]
        if len(Repo.films) == before:
            raise ValueError('Film ne postoji.')
        proj_ids = {p.proj_id for p in Repo.projections if p.film_id == film_id}
        Repo.projections[:] = [p for p in Repo.projections if p.film_id != film_id]
        Repo.sales[:] = [s for s in Repo.sales if s.proj_id not in proj_ids]

    # CRUD projekcija
    @staticmethod
    def add_projection(p: Projection):
        if not Services.film_exists(p.film_id):
            raise ValueError('Ne postoji film za zadati film_id.')
        if Services.proj_exists(p.proj_id):
            raise ValueError('Projekcija sa tim ID već postoji.')
        dt.datetime.strptime(p.date, '%Y-%m-%d')
        dt.datetime.strptime(p.time, '%H:%M')
        Repo.projections.append(p)

    @staticmethod
    def update_projection(proj_id: str, **kwargs):
        p = Services.get_proj(proj_id)
        if not p:
            raise ValueError('Projekcija ne postoji.')
        for k, v in kwargs.items():
            if hasattr(p, k):
                if k == 'date': dt.datetime.strptime(v, '%Y-%m-%d')
                if k == 'time': dt.datetime.strptime(v, '%H:%M')
                if k == 'price': v = float(v)
                if k == 'capacity': v = int(v)
                setattr(p, k, v)

    @staticmethod
    def delete_projection(proj_id: str):
        before = len(Repo.projections)
        Repo.projections[:] = [x for x in Repo.projections if x.proj_id != proj_id]
        if len(Repo.projections) == before:
            raise ValueError('Projekcija ne postoji.')
        Repo.sales[:] = [s for s in Repo.sales if s.proj_id != proj_id]
     

    # Prodaja karata
    @staticmethod
    def sold_quantity_for_projection(proj_id: str) -> int:
        return sum(s.quantity for s in Repo.sales if s.proj_id == proj_id)

    @staticmethod
    def available_capacity(proj_id: str) -> int:
        p = Services.get_proj(proj_id)
        if not p:
            raise ValueError('Projekcija ne postoji.')
        return p.capacity - Services.sold_quantity_for_projection(proj_id)

    @staticmethod
    def sell_tickets(proj_id: str, username: str, quantity: int) -> Sale:
        p = Services.get_proj(proj_id)
        if not p:
            raise ValueError('Projekcija ne postoji.')
        if quantity <= 0:
            raise ValueError('Količina mora biti > 0.')
        if Services.available_capacity(proj_id) < quantity:
            raise ValueError('Nema dovoljno mesta na projekciji.')
        sale = Sale(
            sale_id=f"S{len(Repo.sales)+1:04d}",
            proj_id=proj_id,
            username=username,
            quantity=quantity,
            unit_price=p.price,
            timestamp=dt.datetime.now().isoformat(timespec='seconds'),
        )
        Repo.sales.append(sale)
        return sale

    @staticmethod
    def cancel_sale(sale_id: str):
        before = len(Repo.sales)
        Repo.sales[:] = [s for s in Repo.sales if s.sale_id != sale_id]
        if len(Repo.sales) == before:
            raise ValueError('Prodaja sa datim ID ne postoji.')

    # Izveštaji i složenije funkcije
    @staticmethod
    def revenue_per_projection() -> Dict[str, float]:
        rev: Dict[str, float] = {}
        for s in Repo.sales:
            rev[s.proj_id] = rev.get(s.proj_id, 0.0) + s.quantity * s.unit_price
        return rev

    @staticmethod
    def revenue_per_film() -> Dict[str, float]:
        rev: Dict[str, float] = {}
        for proj_id, amount in Services.revenue_per_projection().items():
            p = Services.get_proj(proj_id)
            if not p:
                continue
            rev[p.film_id] = rev.get(p.film_id, 0.0) + amount
        return rev

    @staticmethod
    def avg_occupancy_by_film() -> Dict[str, float]:
        sold_by_proj = {p.proj_id: Services.sold_quantity_for_projection(p.proj_id) for p in Repo.projections}
        cap_by_film: Dict[str, int] = {}
        sold_by_film: Dict[str, int] = {}
        for p in Repo.projections:
            cap_by_film[p.film_id] = cap_by_film.get(p.film_id, 0) + p.capacity
            sold_by_film[p.film_id] = sold_by_film.get(p.film_id, 0) + sold_by_proj[p.proj_id]
        out: Dict[str, float] = {}
        for film_id in cap_by_film:
            if cap_by_film[film_id] == 0:
                out[film_id] = 0.0
            else:
                out[film_id] = round(100.0 * sold_by_film.get(film_id, 0) / cap_by_film[film_id], 2)
        return out

    @staticmethod
    def tickets_per_day() -> Dict[str, int]:
        per_day: Dict[str, int] = {}
        for s in Repo.sales:
            day = s.timestamp[:10]
            per_day[day] = per_day.get(day, 0) + s.quantity
        return per_day
