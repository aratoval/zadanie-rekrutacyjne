# zadanie-rekrutacyjne
Jest to jedno z moich zadań rekrutacyjnych

# 1. Opis zadania
Zadanie polega na stworzeniu mikroserwisu wspierającego pracę programistów zajmujących się uczeniem maszynowym. System ma pomóc w gromadzeniu i udostępnianiu informacji pobranych z sieci. Główna funkcjonalnością systemu jest pobieranie tekstu oraz obrazków ze stron internetowych.

# 2. Funkcjonalność
* Zlecenie pobrania tekstu z danej strony internetowej i zapis jej w systemie.
* Zlecenie pobrania wszystkich obrazków z danej strony i zapisaniu ich w systemie.
* sprawdzenie statusu zleconego zadania.
* Możliwość pobrania stworzonych zasobów (tekstu i obrazków).

# 3. Architektura
* Zadanie polega na zaprojektowaniu i zaimplementowaniu REST API dla tego systemu. Mikroserwis powinien być napisany w języku Python.
* Rozwiązanie powinno zwierać testy automatyczne.
* Uruchomienie mikroserwisu powinno być maksymalnie zautomatyzowane (preferowane użycie Dockera lub podobnych narzędzi).

# 4. FAQ
* Czy wymagane jest wykonanie JavaScriptu w celu uzyskania tekstu/obrazków na stronie?  
*Nie, pobieramy tylko statyczne zasoby.*
* Czy z tekstu pobieranego ze strony powinien usuwać tagi HTML i kod JavaScript?  
*Tak.*
* Czy napisanie frontendu jest częścią zadania?  
*Nie.*
* Czy można założyć, że pobieranie tekstu/obrazków ze strony jest szybkie?  
*Nie, pobieranie może trwać bardzo długo*

# 5. Kryteria sukcesu:
* Właściwa architektura dla tego problemu.
* Poprawnie zaprojektowane API.
* Poprawnie zaimplementowane API.
* Automatyzacja systemu.
* Testy systemu.
* Kod dostarczony jako udostępnione repozytorium gita (np. w BitBucket)


**Odpowiednia architektura tego systemu i design API są ważniejsze niż dogłębna implementacja**
