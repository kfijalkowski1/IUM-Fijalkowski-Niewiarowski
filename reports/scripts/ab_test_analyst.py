import pandas as pd
import matplotlib.pyplot as plt
import os

PLOTS_FOLDER_PATH = os.path.join("reports", "figures", "v2/")

def analyze_ab_test(results_path, data_path):
    # Load datasets
    ab_test_results = pd.read_csv(results_path)
    ab_test_data = pd.read_csv(data_path)

    # Merge datasets on user_id and track_id
    merged_data = pd.merge(ab_test_results, ab_test_data, on=['user_id', 'track_id'])

    # Add a column to indicate whether the prediction was correct
    merged_data['correct_prediction'] = (
        (merged_data['prediction'] == 'PLAY') & (merged_data['event_type'] == 1) |
        (merged_data['prediction'] == 'SKIP') & (merged_data['event_type'] == 0)
    )

    # Calculate accuracy for each model
    accuracy_by_model = merged_data.groupby('model')['correct_prediction'].mean().reset_index()
    accuracy_by_model.rename(columns={'correct_prediction': 'accuracy'}, inplace=True)

    # Print accuracy metrics to the console
    print("Model Accuracy Metrics:")
    print(accuracy_by_model)

    # Plot accuracy for each model
    plt.figure(figsize=(8, 6))
    plt.bar(accuracy_by_model['model'], accuracy_by_model['accuracy'], alpha=0.7)
    plt.title('Model Accuracy Comparison', fontsize=16)
    plt.ylabel('Accuracy', fontsize=14)
    plt.xlabel('Model', fontsize=14)
    plt.ylim(0, 1)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(PLOTS_FOLDER_PATH + "accuracy.png", format="png", dpi=300)
    plt.show()

    return accuracy_by_model


results_path = './ab_test_results.csv'
data_path = './data/processed/ab_test_data.csv'
analyze_ab_test(results_path, data_path)