from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# Absztrakt osztály a szobákhoz
class Szoba(ABC):
    def __init__(self, szobaszam, ar):
        self.szobaszam = szobaszam
        self.ar = ar
    
    @abstractmethod
    def kiir(self):
        pass

# Szálloda osztály
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = {}  # Dictionary-t használunk a foglalások tárolására
    
    # Szoba hozzáadása a szállodához
    def add_szoba(self, szoba):
        self.szobak.append(szoba)
    
           # Foglalás
    def foglal(self, szobaszam, datum, szoba_tipus):
        if szobaszam not in self.foglalasok:
            if self._is_valid_date(datum):  # Elfogadja a mai dátumot
                if szoba_tipus == "Egyagyas":
                    ar = 30000
                elif szoba_tipus == "Ketagyas":
                    ar = 50000
                else:
                    return None, None
                self.foglalasok[szobaszam] = {datum: ar}
                return szobaszam, szoba_tipus
        elif datum not in self.foglalasok[szobaszam] and self._is_valid_date(datum):
            if szoba_tipus == "Egyagyas":
                ar = 30000
            elif szoba_tipus == "Ketagyas":
                ar = 50000
            else:
                return None, None
            self.foglalasok[szobaszam][datum] = ar
            return szobaszam, szoba_tipus
        else:
            return None, None


    
    # Lemondás
    def lemondas(self, szobaszam, datum):
        if szobaszam in self.foglalasok and datum in self.foglalasok[szobaszam]:
            del self.foglalasok[szobaszam][datum]
            if not self.foglalasok[szobaszam]:  # Ha nincs több foglalás a szobán, akkor töröljük azt is
                del self.foglalasok[szobaszam]
            return True
        else:
            return False
    
    # Foglalások listázása
    def listaz_foglalasok(self):
        print("Foglalások a(z) " + self.nev + " szállodában:")
        for szobaszam, foglalasok in self.foglalasok.items():
            for datum, ar in foglalasok.items():
                szoba_tipus = "Egyagyas" if ar == 30000 else "Ketagyas"
                print(f"Foglalás - Szobaszám: {szobaszam} - Dátum: {datum} - Típus: {szoba_tipus} - Ár: {ar}")

    # Dátum érvényességének ellenőrzése
    def _is_valid_date(self, datum):
        try:
            date = datetime.strptime(datum, "%Y-%m-%d")
            return date >= datetime.today() - timedelta(days=1)  # Elfogadjuk a mai napot és későbbi dátumokat
        except ValueError:
            return False


    
class Foglalas:
    pass

# Menü megjelenítése
def menu():
    print("1. Foglalás")
    print("2. Lemondás")
    print("3. Foglalások listázása")
    print("4. Kilépés")

# Főprogram
def main():
    print("Üdvözöljük a Hotel Példa foglalási rendszerében!")
    hotel = Szalloda("Hotel Példa")

    # A program indításakor bevitt foglalások
    alap_foglalasok = {
        "101": {"2024-07-23": 30000},
        "102": {"2024-07-24": 50000},
        "201": {"2024-07-25": 30000},
        "301": {"2024-07-26": 30000},
        "302": {"2024-07-27": 50000}
    }
    hotel.foglalasok = alap_foglalasok

    while True:
        menu()
        valasztas = input("Kérem válasszon egy opciót (1-4): ")

        if valasztas == "1":

            szobaszam = input("Kérem adja meg a szobaszámot: ")

            # Dátum bekérése és ellenőrzése
            while True:
                datum = input("Kérem adja meg a foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")
                if hotel._is_valid_date(datum) and datetime.strptime(datum, "%Y-%m-%d") != datetime.today():
                    break
                else:
                    print("Hibás dátum! Kérem adjon meg egy érvényes dátumot, ami nem mai.")

            # Ágyszám bekérése és ellenőrzése
            while True:
                szoba_tipus = input("Kérem adja meg hány ágyas szobát kér (1 vagy 2): ")
                if szoba_tipus in ["1", "2"]:
                    break
                else:
                    print("Hibás választás. Kérem válasszon 1 vagy 2-t.")

            if szoba_tipus == "1":
                szoba_tipus = "Egyagyas"
            elif szoba_tipus == "2":
                szoba_tipus = "Ketagyas"
            foglalas, tipus = hotel.foglal(szobaszam, datum, szoba_tipus)

            if foglalas is not None:
                print(f"Sikeres foglalás! Az ár: {hotel.foglalasok[foglalas][datum]}")
            else:
                print("Hiba: Nem sikerült foglalni, mert az adott szobára és dátumra már van foglalás.")


        elif valasztas == "2":
            szobaszam = input("Kérem adja meg a lemondani kívánt foglalás szobaszámát: ")
            datum = input("Kérem adja meg a lemondani kívánt foglalás dátumát (ÉÉÉÉ-HH-NN formátumban): ")

            if hotel.lemondas(szobaszam, datum):
                print("Sikeres lemondás!")
            else:
                print("Hiba: Nem található ilyen foglalás.")

        elif valasztas == "3":
            hotel.listaz_foglalasok()

        elif valasztas == "4":
            print("Köszönjük, hogy használta a Hotel Példa foglalási rendszerét!")
            break

        else:
            print("Hibás választás. Kérem válasszon 1 és 4 közötti értéket.")

if __name__ == "__main__":
    main()
