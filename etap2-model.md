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
Dane zostały podzielone na dane uczące, dane walidacyjne oraz dane przeznaczone do przeprowadzenia testu AB, poprzez wybranie po 1000 danych o losowych indeksach i przyniesienie ich z danych uczących ich do danych walidujących oraz danych do testów AB.

Dane zostały następnie zapisane do folderu data/processed w postaci następujących plików csv:
- merged_data.csv - dane uczące do modelu
- y.csv - etykiety dla danych uczących
- validation_data.csv - dane walidujące
- validation_classes.csv - etykiety dla danych walidujących
- ab_test_data.csv


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

### Mikroserwis

Mikroserwis został zaimplementowany przy użyciu frameworka FastAPI, który umożliwia serwowanie predykcji dwóch modeli: naiwnego i docelowego. Serwis zawiera trzy główne endpointy:

1. /naive - obsługuje predykcje wykonywane przez model naiwny (BaseModel).
2. /recommend - zwraca predykcję wygenerowaną przez model docelowy (NormalModel).
3. /abtest - realizuje test A/B, losowo wybierając jeden z dwóch modeli (z równym prawdopodobieństwem) i zwracając jego predykcję. Informacje o wybranym modelu, użytkowniku, utworze i wyniku predykcji są zapisywane w pliku logów (model_usage_log.json).
Dane wejściowe są przesyłane jako obiekt JSON, opisany przez model Pydantic (PredictionRequest). Każda predykcja jest przetwarzana przez odpowiedni model, a jej wynik (np. PLAY lub SKIP) jest zwracany klientowi i zapisywany do logów w celu późniejszej analizy. Logi są inicjalizowane przy pierwszym uruchomieniu aplikacji, jeśli plik logów nie istnieje.

## Instrukcja uruchomienia

Uruchom Mikroserwis używając uvicorn:
``` 
   uvicorn api.app:app --host 0.0.0.0 --port 8000
```

Przykładowe zapytanie z poziomu PowerShell:

```
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/recommend" `
   >> -Method POST `
   >> -Headers @{ "Content-Type" = "application/json" } `
   >> -Body '{"user_id": 101, "track_id": "31PzY79H10HCgJs533Xq6B"}'
```

### Testy AB

Testy A/B w mikroserwisie są realizowane za pośrednictwem dedykowanego endpointu /abtest, który losowo wybiera jeden z dwóch modeli (naiwny lub docelowy) z równym prawdopodobieństwem 50/50. Dla każdego żądania serwis:

Losowy wybór modelu: Decyduje, czy predykcja zostanie wygenerowana przez model naiwny (BaseModel), czy docelowy (NormalModel).
Wykonanie predykcji: Wybrany model generuje wynik dla danego użytkownika (user_id) i utworu (track_id), wskazując, czy utwór zostanie odtworzony (PLAY) czy pominięty (SKIP).
Logowanie wyników: Informacje o wybranym modelu, wejściowych danych użytkownika i wyniku predykcji są zapisywane w pliku logów (model_usage_log.json). Każdy wpis logu zawiera nazwę modelu, identyfikator użytkownika i utworu oraz wynik predykcji.

Aby ułatwić przeprowadzenie testów opracowany został skrypt wczytujący wcześniej przygotowane dane i wysyłający zapytanie do mikroserwisu.

Wyniki przeprowadzonego testu:

Dla obu modeli otrzymaliśmy następującą accuracy:
```
      model  accuracy
   0   naive  0.415354
   1  target  0.754065
```

W dobry sposób prezentuje to sporządzony wykres:

![Opis alternatywny](./figures/v2/accuracy.png)

Wnioski na podstawie testów AB

1. Uzyskane wyniki testu A/B wyraźnie wskazują, że model docelowy (target) osiąga znacznie lepszą skuteczność (accuracy: 75,41%) w porównaniu do modelu naiwnego (naive), którego dokładność wynosi jedynie 41,54%. Taka różnica sugeruje, że model docelowy lepiej przewiduje zachowania użytkowników, co czyni go bardziej wartościowym w praktycznym zastosowaniu, np. w systemach rekomendacyjnych.

2. Sporządzony wykres nie tylko wizualizuje tę różnicę, ale także podkreśla istotność prowadzenia testów A/B jako narzędzia do podejmowania decyzji opartych na danych. Wyniki wskazują, że wdrożenie modelu docelowego może znacząco poprawić jakość rekomendacji i zadowolenie użytkowników.