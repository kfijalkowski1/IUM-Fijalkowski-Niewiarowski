from ium_fij_niew.model_usage.model_classes import BaseModel, PredictResult, NormalModel

model_a = BaseModel()
model_b = NormalModel()

predict = model_b.predict(101, "31PzY79H10HCgJs533Xq6B")

print(predict)

print(model_a.predict(101, "31PzY79H10HCgJs533Xq6B"))
print(model_b.predict(101, "31PzY79H10HCgJs533Xq6B"))
print(model_b.predict(101, "31PzY79H10HCgJs533Xq6B"))
print(model_b.predict(101, "31PzY79H10HCgJs533Xq6B"))
print(model_b.predict(101, "31PzY79H10HCgJs533Xq6B"))

