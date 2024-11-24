# IUM-Fijalkowski-Niewiarowski
Repository for realization of 2024Z IUM project


## Analiza danych
Klient udostępnił nam dane dotyczące:

- lista dostępnych artystów i utworów muzycznych,
- baza użytkowników,
- historia sesji użytkowników,
- techniczne informacje dot. poziomu cache dla poszczególnych utworów.

Z analizy dostarczonej wersji danych wyciągneliśmy następujące wnioski:

- Otrzymaliśmy dane tylko 50 użytkowników, pola opisujące użytkownika nie są podpisane co utrudnia zrozumienie struktury danych opisującej użytkownika serwisu pozytywka. Dodatkowo dane części użytkowników są nie kompletne, w 3 przypadkach brakuje ID użytkownika, a dla innych 3 nie została podana wartość pola opisywanego wartością binarną true/false
- W przypadku danych o utworach dostępnych w serwsie pozytywka otrzymaliśmy informację o około ~130 000 utworów, dane są w przeważającej części kompletne poza jedną kolumną (mode), w przypadku tej kolumny w 80% (103718) rekordów jej wartość jest pusta.
- Plik trac_storage zawiera informacje o przechowywaniu poszczególnych utworów w cache, informacja o klasie pamięci w jakiej jest przechowywany oraz koszt obsługi każdego utworu. W dostarczonych danych można zauważyć bardzo małą ilość utworów dla których storage_mode jest inna niż 'Slow'. Dla poszczególnych wartości liczby rekordów prezentują się w następujący sposób:
    
    Liczba wystąpień dla każdej klasy pamięci:
    - Slow: 128182
    - Medium: 1459
    - Fast: 7

    Procentowy rozkład został zaprezentowany na poniższym wykresie:

![Opis alternatywny](./data_analize_scripts/plots/v1/storage_mode.png)

- W pliku sessions otrzymaliśmy informację o około ~10 000 sesjach użytkownika, w przypadku 1301 wierszy posiadało puste wartości. Dodatkowo pola opisujące sesje nie zostały podpsiane, przez co trudno zrozumieć znaczenie biznesowe części pól, w szczególności ostatniej kolumny, będącej dla każdego przypadku liczbą natrualną, dodatnią. Rozkład pola nr. 4 które interpretujemy jako akcję podjętą w danej sesji wygląda w następujący sposób:

![Opis alternatywny](./data_analize_scripts/plots/v1/actions.png)

- Dodatkowo wygenerowaliśmy wykresy ukazujące klasę pamięci dla akcji 'Skip' oraz 'Play', jednak nie staraliśmy się wyciągać jakichkolowiek przypuszczeń bądź wniosków ze względu na duży udział klasy 'Slow' w udostępnionych danych.

![Opis alternatywny](./data_analize_scripts/plots/v1/PlaySession.png)

![Opis alternatywny](./data_analize_scripts/plots/v1/SkipSession.png)

Liczba dostępnych danych na temat sesji jest niewielka w porównaniu do ilości danych na temat utworów

- W pliku artists otrzymaliśmy dane na temat 27650 artystów. Dla ~2600 wierszy dane są niekompletne, występuje to dla pierwszej oraz ostatniej kolumny. Dodatkowo brakuje nazw poszczególnych kolumn.