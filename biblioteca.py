import csv
from operator import itemgetter

def carica_da_file(file_path):
    """Carica i libri dal file"""
    try:
        f = open(file_path, 'r', encoding='utf-8')
    except FileNotFoundError:
        return None
    csvInputFile = csv.DictReader(f, fieldnames=['title', 'author', 'year', "pages", "section"])
    books = []
    for book in csvInputFile:
        books.append(book)
    books.pop(0)
    library = []
    section = []
    for i in range(int(max(books, key=itemgetter("section"))["section"])):
        j = i + 1
        for book in books:
            if int(book["section"]) == j:
                section.append(book)
        library.append(list(section))
        section.clear()
    f.close()
    return library

def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""
    # TODO
    libro = {"title": titolo, "author": autore, "year": str(anno), "pages": str(pagine), "section": sezione}
    bookAlreadyInThere = False
    try:
        for currentBook in biblioteca[libro["section"]-1]:
            if currentBook["title"] == libro["title"]:
                bookAlreadyInThere = True
    except IndexError:
        return None
    if not bookAlreadyInThere:
        biblioteca[libro["section"]-1].append(libro)
        try:
            f = open(file_path, 'a', encoding='utf-8')
        except FileNotFoundError:
            return None
        f.write(",".join(libro.values()))
        f.close()
        return libro
    else:
        return None

def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    # TODO
    found = False
    for section in biblioteca:
        for book in section:
            if book["title"] == titolo:
                found = True
                return ", ".join(book.values())
    if not found:
        return None

def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    # TODO
    try:
        sortedSection = sorted(biblioteca[sezione-1], key=itemgetter("title"))
    except IndexError:
        return None
    titleList = []
    for book in sortedSection:
        titleList.append(book["title"])
    return titleList

def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print("Questa sezione non esiste")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

