import numpy as np
from sklearn import linear_model
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF


def task_completion(x: np.ndarray, y: np.ndarray, x_test) -> float:
    x_a = x[0].reshape(-1, 1)  # разделямем данные на показатель многозадачности
    x_t = x[1].reshape(-1, 1)  # и таймменеджмента

    if len(y) != 0 and len(x_a) != 0 and len(x_t) != 0:
        if 0 in y and 1 in y:

            # инициализируем нужные модели
            activity_clf = linear_model.LogisticRegression(C=1e5)
            time_clf = linear_model.LogisticRegression(C=1e5)

            kernel = 1.0 * RBF(1.0)
            x = x.reshape(-1, 2)
            gpc = GaussianProcessClassifier(kernel=kernel, random_state=0)

            # оцениваем точность моделей
            at_score = (activity_clf.score(x_a, y) + time_clf.score(x_t, y)) / 2
            gpc_score = gpc.score(x, y)

            # делаем предсказание о шансе выполнения работы, используя наиболее точную модель
            if at_score <= gpc_score:
                gpc.fit(x, y)
                chance_ap = gpc.predict_proba([[x_test[0], x_test[1]]])[0][1]
                return chance_ap

            else:
                activity_clf.fit(x_a, y)
                time_clf.fit(x_t, y)
                chance_a = activity_clf.predict_proba(x_test[0])[0][1]
                chance_t = time_clf.predict_proba(x_test[1])[0][1]
                return (chance_a + chance_t) / 2

    return 0.5
