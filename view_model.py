from tensorflow.keras import models

model = models.load_model("rein.keras")

model.summary()