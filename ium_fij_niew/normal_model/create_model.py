import time

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, \
    roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC

import ium_fij_niew.normal_model.data_parser as data_parser
import os
import datetime
from pickle import dump

X, y, validation_data, validation_classes = data_parser.get_data(True)

print("Creating linear svc model..")

start_time = time.time()
clf = make_pipeline(StandardScaler(),
                    LinearSVC(class_weight='balanced', random_state=0, tol=1e-5))
clf.fit(X, y)
end_train_time = time.time()

end_valid_time = time.time()

y_pred = clf.predict(validation_data)

# Calculate Metrics
accuracy = accuracy_score(validation_classes, y_pred)
precision = precision_score(validation_classes, y_pred)
recall = recall_score(validation_classes, y_pred)
f1 = f1_score(validation_classes, y_pred)
roc_auc = roc_auc_score(validation_classes, y_pred)


# Print Metrics
print("Accuracy: ", accuracy)
print("Precision: ", precision)
print("Recall: ", recall)
print("F1 Score: ", f1)
print("ROC-AUC Score:", roc_auc)

# Display a detailed classification report
print("\nClassification Report:\n")
print(classification_report(validation_classes, y_pred))


print("Saving model to file")

today = str(datetime.datetime.now()).replace(" ", "_").replace(":", "-").split(".")[0]

with open(os.path.join("models", f"linear_svc_{today}"), "wb") as f:
    dump(clf, f, protocol=5)

print("Model saved")