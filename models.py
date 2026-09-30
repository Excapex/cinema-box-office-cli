from dataclasses import dataclass


@dataclass
class User:
    username: str
    password_hash: str
    role: str  # administrator | blagajnik | kupac


@dataclass
class Film:
    film_id: str
    title: str
    genre: str
    duration_min: int


@dataclass
class Projection:
    proj_id: str
    film_id: str
    date: str    # YYYY-MM-DD
    time: str    # HH:MM
    hall: str
    price: float
    capacity: int


@dataclass
class Sale:
    sale_id: str
    proj_id: str
    username: str
    quantity: int
    unit_price: float
    timestamp: str  # ISO 8601
