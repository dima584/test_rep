import cv2
import numpy as np
from keras.layers import TFSMLayer  # для Keras 3
from imutils.contours import sort_contours
import imutils

# Загрузка изображения
image = cv2.imread("C:/Users/nezol/Downloads/1.jpg")
if image is None:
    print("❌ Ошибка: изображение не найдено по указанному пути.")
    exit()

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Пороговая обработка
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Поиск контуров
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sort_contours(cnts, method="left-to-right")[0]

# Загрузка модели SavedModel через TFSMLayer
model = TFSMLayer("model/handwriting_model_tf", call_endpoint="serve")

output = []

for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    if w >= 5 and h >= 15:
        roi = gray[y:y + h, x:x + w]
        thresh_roi = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        resized = cv2.resize(thresh_roi, (28, 28))
        normalized = resized.astype("float32") / 255.0
        reshaped = normalized.reshape(1, 28, 28, 1)
        
        pred_tensor = model(reshaped, training=False)
        pred = pred_tensor.numpy()
        i = np.argmax(pred[0])
        
        output.append(str(i))
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, str(i), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

print("Распознанный текст: {}".format("".join(output)))
cv2.imshow("Результат", image)
cv2.waitKey(0)
cv2.destroyAllWindows()