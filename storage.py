import os
from typing import List, Dict, Optional, Callable


SEP = ';'


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
USERS_F = os.path.join(DATA_DIR, 'users.txt')
FILMS_F = os.path.join(DATA_DIR, 'films.txt')
PROJ_F = os.path.join(DATA_DIR, 'projections.txt')
SALES_F = os.path.join(DATA_DIR, 'sales.txt')


class Storage:
    @staticmethod
    def ensure_data_dir():
        os.makedirs(DATA_DIR, exist_ok=True)

    @staticmethod
    def read_csv(path: str, fieldnames: List[str], cast: Optional[Callable[[Dict[str, str]], Dict]] = None) -> List[Dict]:
        if not os.path.exists(path):
            return []
        rows: List[Dict] = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(SEP)
                row = {fn: parts[i] if i < len(parts) else '' for i, fn in enumerate(fieldnames)}
                if cast:
                    row = cast(row)
                rows.append(row)
        return rows

    @staticmethod
    def write_csv(path: str, rows: List[Dict], fieldnames: List[str]) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            for r in rows:
                line = SEP.join([str(r.get(fn, '')) for fn in fieldnames])
                f.write(line + '\n')
