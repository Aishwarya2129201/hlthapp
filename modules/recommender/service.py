import numpy as np
import pandas as pd
from scipy.stats import mode
from django.conf import settings

# import matplotlib.pyplot as plt
# import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix


# Defining the Function
# Input: string containing symptoms separated by commas
# Output: Generated predictions by models
def predict_disease(user_symptoms):
    # Reading the train.csv by removing the
    data = pd.read_csv(settings.BASE_DIR / "modules/recommender/assets/Training.csv")

    # Checking whether the dataset is balanced or not
    disease_counts = data["prognosis"].value_counts()
    temp_df = pd.DataFrame(
        {"Disease": disease_counts.index, "Counts": disease_counts.values}
    )

    encoder = LabelEncoder()
    data["prognosis"] = encoder.fit_transform(data["prognosis"])
    np.ravel(data)

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=24
    )

    print(f"Train: {X_train.shape}, {y_train.shape}")
    print(f"Test: {X_test.shape}, {y_test.shape}")

    models = {
        "Gaussian NB": GaussianNB(),
        "Random Forest": RandomForestClassifier(random_state=18),
    }

    # Training and testing Naive Bayes Classifier
    nb_model = GaussianNB()
    nb_model.fit(X_train, y_train)
    preds = nb_model.predict(X_test)
    print(
        f"Accuracy on train data by Naive Bayes Classifier\
    : {accuracy_score(y_train, nb_model.predict(X_train))*100}"
    )

    print(
        f"Accuracy on test data by Naive Bayes Classifier\
    : {accuracy_score(y_test, preds)*100}"
    )

    # Training and testing Random Forest Classifier
    rf_model = RandomForestClassifier(random_state=18)
    rf_model.fit(X_train, y_train)
    preds = rf_model.predict(X_test)
    print(
        f"Accuracy on train data by Random Forest Classifier\
    : {accuracy_score(y_train, rf_model.predict(X_train))*100}"
    )

    print(
        f"Accuracy on test data by Random Forest Classifier\
    : {accuracy_score(y_test, preds)*100}"
    )

    # Training the models on whole data

    final_nb_model = GaussianNB()
    final_rf_model = RandomForestClassifier(random_state=18)

    final_nb_model.fit(X, y)
    final_rf_model.fit(X, y)

    # Reading the test data
    test_data = pd.read_csv(settings.BASE_DIR / "modules/recommender/assets/Testing.csv")

    test_X = test_data.iloc[:, :-1]
    test_Y = encoder.transform(test_data.iloc[:, -1])

    # Making prediction by take mode of predictions
    # made by all the classifiers

    nb_preds = final_nb_model.predict(test_X)
    rf_preds = final_rf_model.predict(test_X)

    final_preds = [mode([i, j])[0][0] for i, j in zip(nb_preds, rf_preds)]

    print(
        f"Accuracy on Test dataset by the combined model\: {accuracy_score(test_Y, final_preds)*100}"
    )

    symptoms = X.columns.values

    # Creating a symptom index dictionary to encode the
    # input symptoms into numerical form
    symptom_index = {}
    for index, value in enumerate(symptoms):
        symptom = " ".join([i.capitalize() for i in value.split("_")])
        symptom_index[symptom] = index

    data_dict = {
        "symptom_index": symptom_index,
        "predictions_classes": encoder.classes_,
    }


    # creating input data for the models
    input_data = [0] * len(data_dict["symptom_index"])
    for symptom in user_symptoms:
        index = data_dict["symptom_index"][symptom]
        input_data[index] = 1

    # reshaping the input data and converting it
    # into suitable format for model predictions
    input_data = np.array(input_data).reshape(1, -1)

    # generating individual outputs
    rf_prediction = data_dict["predictions_classes"][
        final_rf_model.predict(input_data)[0]
    ]
    nb_prediction = data_dict["predictions_classes"][
        final_nb_model.predict(input_data)[0]
    ]

    # making final prediction by taking mode of all predictions
    final_prediction = mode([rf_prediction, nb_prediction])[0][0]
    predictions = {
        "rf_model_prediction": rf_prediction,
        "naive_bayes_prediction": nb_prediction,
        "final_prediction": final_prediction,
    }
    return predictions["final_prediction"]
