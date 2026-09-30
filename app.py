from auth import Auth
from repo import Repo
from seed import seed_if_missing
from ui import UI


def main():
    seed_if_missing()        
    Repo.load_all()          
    UI.login()               

    role = UI.current_user.role if UI.current_user else ""
    if role == "administrator":
        UI.admin_menu()
    elif role == "blagajnik":
        UI.blagajnik_menu()
    else:
        UI.kupac_menu()


if __name__ == "__main__":
    try:
        main()
    finally:
        try:
            Repo.save_all()
            print("[Info] Stanje sačuvano.")
        except Exception as e:
            print("[UPOZORENJE] Nije uspelo snimanje:", e)

# U kompleksnijim modulima i klasama sam pisao komentare da bi se i Vi i ja lakse snasli
# Editor u kom sam pisao ne prepoznaje region i endregion separatore pa sam morao komentarima
