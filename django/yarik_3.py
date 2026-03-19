from tensorflow.keras.models import load_model

# Загружаем модель из файла .keras
model = load_model("model/handwriting_model.keras")

# Сохраняем модель в формате TensorFlow SavedModel (папка)
model.save("model/handwriting_model_tf", save_format="tf")