import numpy as np
from sklearn import linear_model


def task_completion(x: np.ndarray, y: np.ndarray, x_test) -> float:
    x_a = x[0].reshape(-1, 1)
    x_p = x[1].reshape(-1, 1)

    active_clf = linear_model.LogisticRegression(C=1e5)
    active_clf.fit(x_a, y)
    payment_clf = linear_model.LogisticRegression(C=1e5)
    payment_clf.fit(x_p, y)

    chance_a = active_clf.predict_proba(x_test[0])[0][1]
    chance_p = payment_clf.predict_proba(x_test[1])[0][1]

    return chance_a + chance_p / 2
