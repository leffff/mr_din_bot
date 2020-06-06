import numpy as np
from sklearn import linear_model
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF


def task_completion(x: np.ndarray, y: np.ndarray, x_test) -> float:
    x_a = x[0].reshape(-1, 1)
    x_p = x[1].reshape(-1, 1)

    active_clf = linear_model.LogisticRegression(C=1e5)
    active_clf.fit(x_a, y)
    payment_clf = linear_model.LogisticRegression(C=1e5)
    payment_clf.fit(x_p, y)

    kernel = 1.0 * RBF(1.0)
    x = x.reshape(-1, 2)
    gpc = GaussianProcessClassifier(kernel=kernel, random_state=0).fit(x, y)

    chance_a = active_clf.predict_proba(x_test[0])[0][1]
    chance_p = payment_clf.predict_proba(x_test[1])[0][1]
    chance_ap = gpc.predict_proba([[x_test[0], x_test[1]]])[0][1]

    return chance_a + chance_p + chance_ap / 3
