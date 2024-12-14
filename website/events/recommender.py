from pathlib import Path
import numpy as np
from tensorflow.keras.models import load_model
from .models import Event
import tensorflow as tf
# Завантаження моделі
MODEL_PATH = Path(__file__).resolve().parent / 'ncf_model.h5'
model = load_model(MODEL_PATH)


def get_recommendations(user_id, event_ids):
    """
    Отримує рекомендації для подій на основі збереженої моделі.
    :param user_id: ID користувача
    :param event_ids: Список ID подій
    :return: Список ID подій, відсортованих за рейтингом
    """
    # Генеруємо дані для моделі
    user_ids = np.array([user_id] * len(event_ids))  # Повторюємо user_id для всіх подій
    event_ids = np.array(event_ids)  # Конвертуємо ID подій у numpy-масив

    # Прогнозування
    predictions = model.predict([user_ids, event_ids])
    predictions = predictions.flatten()  # Перетворюємо у 1D-масив

    # Сортуємо події за рейтингом
    recommended_ids = [event_id for _, event_id in sorted(zip(predictions, event_ids), reverse=True)]
    return recommended_ids




