from sklearn.utils import class_weight
import numpy as np

from data_parser import get_data

_, y, _, _ = get_data()
print("data loaded")
# Ensure y is a NumPy array


# Compute class weights
class_weights = class_weight.compute_class_weight(
    class_weight='balanced',
    classes=np.unique(y),
    y=y
)

class_weights_dict = {0: class_weights[0], 1: class_weights[1]}
print("Class Weights:", class_weights_dict)
