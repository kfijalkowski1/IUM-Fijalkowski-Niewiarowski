from ium_fij_niew.model_usage.model_classes import NormalModel

def main():
    # Tworzenie instancji modelu
    model = NormalModel()

    # Generowanie wykresu
    model.plot_feature_importance('./data/processed/merged_data.csv')

main()