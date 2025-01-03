## Model uczelnia maszynowego
### Przygotowanie danych
Zostały połączone dane plików: sessions.jsonl, tracks.jsonl, users.jsonl. W celu wytworzenia jednego zbioru danych. 

Informacje o sesjach zostały przefiltrowane następująco:
- Nie interesują nas wiersze z akcjami innymi niż 'skip' i 'play'
- Jeśli dla danej sesji i dla danego utworu została wykonana akcja 'skip' i 'play' oznacza to, że utwór został pominięty,
tak więc zostawiamy tylko wiersz z operacją 'skip'

Na podstawie sesji zostały również wyliczone dwa dodatkowe atrybuty:
- Średnio ile procent utworów użytkownik pomijał-pokazuje to na tendencję użytkownika do pomijania utworów
- Średnio ile procent dany utwór był pomijany-pokazuje to jak często dany utwór jest pomijany

Ulubione gatunki użytkownika zostały czytane z pliku users.jsonl i zmienione do postaci binarnych atrybutów 
pokazujących czy użytkownik lubi dany gatunek muzyczny.

### Podział danych
Dane zostały podzielone na dane uczące i dane walidacyjne poprzez wybranie 1000 danych o losowych indeksach i 
przyniesienie ich z danych uczących ich do danych walidujących.

Dane zostały następnie zapisane do folderu data/processed w postaci następujących plików csv:
- merged_data.csv - dane uczące do modelu
- y.csv - etykiety dla danych uczących
- validation_data.csv - dane walidujące
- validation_classes.csv - etykiety dla danych walidujących


# Model
Został wykorzystany model LiniearSVC z domyślnymi parametrami.
Pierwsza wersja modelu bez dodatkowych atrybutów opisanych powyżej osiągnęła następujące wyniki:
```
              precision    recall  f1-score   support

           0       0.59      0.05      0.10       430
           1       0.58      0.97      0.72       570

    accuracy                           0.58      1000
   macro avg       0.58      0.51      0.41      1000
weighted avg       0.58      0.58      0.45      1000
```

Po zmienie balansu klas w modelu na 'balanced' otrzymaliśmy następujące wyniki:
```
              precision    recall  f1-score   support

           0       0.45      0.51      0.48       430
           1       0.59      0.52      0.55       570

    accuracy                           0.52      1000
   macro avg       0.52      0.52      0.51      1000
weighted avg       0.53      0.52      0.52      1000

```

Po dodaniu dodatkowych atrybutów opisanych powyżej otrzymaliśmy następujące wyniki:
```
              precision    recall  f1-score   support

           0       0.68      0.74      0.71       429
           1       0.79      0.73      0.76       571

    accuracy                           0.74      1000
   macro avg       0.73      0.74      0.73      1000
weighted avg       0.74      0.74      0.74      1000
```
