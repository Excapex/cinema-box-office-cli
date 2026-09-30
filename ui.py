from auth import Auth
from repo import Repo
from services import Services
from models import Film, Projection
from plots import plot_bar


class UI:
    current_user = None

    @staticmethod
    def prompt(msg: str) -> str:
        return input(msg).strip()

    # --- Login ---
    @staticmethod
    def login():
        print('=== Prijava ===')
        for _ in range(3):
            u = UI.prompt('Korisničko ime: ')
            p = UI.prompt('Lozinka: ')
            user = Auth.authenticate(u, p)
            if user:
                UI.current_user = user
                print(f'Ulogovani ste kao {user.username} [{user.role}]')
                return
            print('Pogrešno korisničko ime ili lozinka.')
        raise SystemExit('Previše pokušaja. Izlaz.')

    # --- Liste ---
    @staticmethod
    def list_films():
        print('\nFILMOVI:')
        for f in Repo.films:
            print(f"{f.film_id} | {f.title} | {f.genre} | {f.duration_min} min")

    @staticmethod
    def list_projections():
        print('\nPROJEKCIJE:')
        for p in Repo.projections:
            film = Services.get_film(p.film_id)
            print(f"{p.proj_id} | {film.title if film else p.film_id} | {p.date} {p.time} | Sala {p.hall} | Cena {p.price} | Kapacitet {p.capacity} | Slobodno {Services.available_capacity(p.proj_id)}")

    @staticmethod
    def list_sales():
        print('\nPRODAJE:')
        for s in Repo.sales:
            print(f"{s.sale_id} | proj={s.proj_id} | user={s.username} | kom={s.quantity} | cena={s.unit_price} | ts={s.timestamp}")

    # --- Meniji po ulogama ---
    @staticmethod
    def admin_menu():
        while True:
            print('\n[ADMIN] 1) filmovi  2) projekcije  3) izveštaji  4) grafici  0) sačuvaj i izlaz')
            ch = UI.prompt('> ')
            if ch == '1': UI.menu_films()
            elif ch == '2': UI.menu_projections()
            elif ch == '3': UI.menu_reports()
            elif ch == '4': UI.menu_plots()
            elif ch == '0': Repo.save_all(); print('Sačuvano.'); return

    @staticmethod
    def blagajnik_menu():
        while True:
            print('\n[BLAGAJNIK] 1) lista projekcija  2) prodaj karte  3) storniraj  4) grafici  0) sačuvaj i izlaz')
            ch = UI.prompt('> ')
            if ch == '1': UI.list_projections()
            elif ch == '2': UI.cmd_sell()
            elif ch == '3': UI.cmd_cancel()
            elif ch == '4': UI.menu_plots()
            elif ch == '0': Repo.save_all(); print('Sačuvano.'); return

    @staticmethod
    def kupac_menu():
        while True:
            print('\n[KUPAC] 1) liste filmova/projekcija  2) kupi karte  3) moje kupovine  0) izlaz')
            ch = UI.prompt('> ')
            if ch == '1': UI.list_films(); UI.list_projections()
            elif ch == '2': UI.cmd_sell()
            elif ch == '3': UI.list_my_sales()
            elif ch == '0': Repo.save_all(); print('Sačuvano.'); return

    # --- Podmeniji ---
    @staticmethod
    def menu_films():
        while True:
            print('\n[FILMOVI] 1) lista  2) dodaj  3) izmeni  4) obriši  0) nazad')
            ch = UI.prompt('> ')
            if ch == '1': UI.list_films()
            elif ch == '2': UI.cmd_add_film()
            elif ch == '3': UI.cmd_update_film()
            elif ch == '4': UI.cmd_delete_film()
            elif ch == '0': return

    @staticmethod
    def menu_projections():
        while True:
            print('\n[PROJEKCIJE] 1) lista  2) dodaj  3) izmeni  4) obriši  0) nazad')
            ch = UI.prompt('> ')
            if ch == '1': UI.list_projections()
            elif ch == '2': UI.cmd_add_projection()
            elif ch == '3': UI.cmd_update_projection()
            elif ch == '4': UI.cmd_delete_projection()
            elif ch == '0': return

    @staticmethod
    def menu_reports():
        rev_film = Services.revenue_per_film()
        print('\nPrihod po filmu:')
        for film_id, amount in sorted(rev_film.items(), key=lambda x: -x[1]):
            film = Services.get_film(film_id)
            print(f"- {film.title if film else film_id}: {amount:.2f}")
        occ = Services.avg_occupancy_by_film()
        print('\nProsečna popunjenost po filmu (%):')
        for film_id, occp in sorted(occ.items(), key=lambda x: -x[1]):
            film = Services.get_film(film_id)
            print(f"- {film.title if film else film_id}: {occp:.2f}%")

    @staticmethod
    def menu_plots():
        print('\n[Grafici] 1) karte po danu  2) prihod po filmu  0) nazad')
        ch = UI.prompt('> ')
        if ch == '1':
            plot_bar('Broj prodatih karata po danu', Services.tickets_per_day(), 'Dan', 'Broj karata')
        elif ch == '2':
            mapping = {}
            for film_id, amount in Services.revenue_per_film().items():
                film = Services.get_film(film_id)
                mapping[film.title if film else film_id] = amount
            plot_bar('Prihod po filmu', mapping, 'Film', 'Prihod')

    # --- Komande ---
    @staticmethod
    def cmd_add_film():
        film_id = UI.prompt('Novi film_id: ')
        title = UI.prompt('Naslov: ')
        genre = UI.prompt('Žanr: ')
        duration_min = int(UI.prompt('Trajanje (min): '))
        Services.add_film(Film(film_id, title, genre, duration_min))
        print('Dodat film.')

    @staticmethod
    def cmd_update_film():
        film_id = UI.prompt('film_id za izmenu: ')
        title = UI.prompt('(ENTER za preskok) Novi naslov: ')
        genre = UI.prompt('(ENTER) Novi žanr: ')
        dur = UI.prompt('(ENTER) Novo trajanje: ')
        kwargs = {}
        if title: kwargs['title'] = title
        if genre: kwargs['genre'] = genre
        if dur: kwargs['duration_min'] = int(dur)
        Services.update_film(film_id, **kwargs)
        print('Izmenjen film.')

    @staticmethod
    def cmd_delete_film():
        film_id = UI.prompt('film_id za brisanje: ')
        Services.delete_film(film_id)
        print('Obrisan film (i povezani podaci).')

    @staticmethod
    def cmd_add_projection():
        proj_id = UI.prompt('Novi proj_id: ')
        film_id = UI.prompt('film_id: ')
        date = UI.prompt('Datum (YYYY-MM-DD): ')
        time = UI.prompt('Vreme (HH:MM): ')
        hall = UI.prompt('Sala: ')
        price = float(UI.prompt('Cena: '))
        capacity = int(UI.prompt('Kapacitet: '))
        Services.add_projection(Projection(proj_id, film_id, date, time, hall, price, capacity))
        print('Dodata projekcija.')

    @staticmethod
    def cmd_update_projection():
        proj_id = UI.prompt('proj_id za izmenu: ')
        date = UI.prompt('(ENTER) Novi datum: ')
        time = UI.prompt('(ENTER) Novo vreme: ')
        hall = UI.prompt('(ENTER) Nova sala: ')
        price = UI.prompt('(ENTER) Nova cena: ')
        capacity = UI.prompt('(ENTER) Novi kapacitet: ')
        kwargs = {}
        if date: kwargs['date'] = date
        if time: kwargs['time'] = time
        if hall: kwargs['hall'] = hall
        if price: kwargs['price'] = float(price)
        if capacity: kwargs['capacity'] = int(capacity)
        Services.update_projection(proj_id, **kwargs)
        print('Izmenjena projekcija.')

    @staticmethod
    def cmd_delete_projection():
        proj_id = UI.prompt('proj_id za brisanje: ')
        Services.delete_projection(proj_id)
        print('Obrisana projekcija (i prodaje).')

    @staticmethod
    def cmd_sell():
        UI.list_projections()
        proj_id = UI.prompt('proj_id: ')
        qty = int(UI.prompt('Količina karata: '))
        sale = Services.sell_tickets(proj_id, UI.current_user.username, qty)
        print(f'Prodata prodaja {sale.sale_id}. Ukupno = {sale.quantity * sale.unit_price:.2f}')

    @staticmethod
    def cmd_cancel():
        UI.list_sales()
        sale_id = UI.prompt('sale_id za storniranje: ')
        Services.cancel_sale(sale_id)
        print('Prodaja stornirana.')

    @staticmethod
    def list_my_sales():
        print('\nMOJE KUPOVINE:')
        for s in Repo.sales:
            if s.username == UI.current_user.username:
                print(f"{s.sale_id} | proj={s.proj_id} | kom={s.quantity} | cena={s.unit_price} | ts={s.timestamp}")
