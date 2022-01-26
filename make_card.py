from datetime import date
from io import BytesIO
import model_card_toolkit as mctlib

from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import plot_roc_curve, plot_confusion_matrix, accuracy_score

import os
import base64
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import uuid


def main():
    cancer = load_breast_cancer()

    X = pd.DataFrame(cancer.data, columns=cancer.feature_names)
    y = pd.Series(cancer.target)

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    clf = GradientBoostingClassifier().fit(X_train, y_train)

    # Utility function that will export a plot to a base-64 encoded string that the model card will accept.
    def plot_to_str():
        img = BytesIO()
        plt.savefig(img, format='png')
        return base64.encodebytes(img.getvalue()).decode('utf-8')

    # Plot the mean radius feature for both the train and test sets
    sns.displot(x=X_train['mean radius'], hue=y_train)
    mean_radius_train = plot_to_str()
    sns.displot(x=X_test['mean radius'], hue=y_test)
    mean_radius_test = plot_to_str()

    # Plot the mean texture feature for both the train and test sets
    sns.displot(x=X_train['mean texture'], hue=y_train)
    mean_texture_train = plot_to_str()
    sns.displot(x=X_test['mean texture'], hue=y_test)
    mean_texture_test = plot_to_str()

    # Plot ROC curve
    plot_roc_curve(clf, X_test, y_test)
    roc_curve = plot_to_str()

    # Plot confusion matrix
    plot_confusion_matrix(clf, X_test, y_test)
    confusion_matrix = plot_to_str()

    y_pred = clf.predict(X_test)
    accuracy = round(accuracy_score(y_test, y_pred), 4)

    mct_directory = '.'  # where the Model Card assets will be generated
    mct = mctlib.ModelCardToolkit(mct_directory)

    model_card = mct.scaffold_assets()
    mct.update_model_card(model_card)

    model_card.model_details.name = 'Breast Cancer Wisconsin (Diagnostic) Dataset'
    model_card.model_details.overview = (
        'This model predicts whether breast cancer is benign or malignant based on '
        'image measurements.')
    model_card.model_details.owners = [
        mctlib.Owner(name= 'Model Cards Team', contact='model-cards@google.com')
    ]
    model_card.model_details.references = [
        mctlib.Reference(reference='https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)'),
        mctlib.Reference(reference='https://minds.wisconsin.edu/bitstream/handle/1793/59692/TR1131.pdf')
    ]
    model_card.model_details.version.name = str(uuid.uuid4())
    model_card.model_details.version.date = str(date.today())

    model_card.considerations.ethical_considerations = [mctlib.Risk(
        name=('Manual selection of image sections to digitize could create '
                'selection bias'),
        mitigation_strategy='Automate the selection process'
    )]
    model_card.considerations.limitations = [mctlib.Limitation(description='Breast cancer diagnosis')]
    model_card.considerations.use_cases = [mctlib.UseCase(description='Breast cancer diagnosis')]
    model_card.considerations.users = [mctlib.User(description='Medical professionals'), mctlib.User(description='ML researchers')]

    model_card.model_parameters.data.append(mctlib.Dataset())
    model_card.model_parameters.data[0].graphics.description = (
      f'{len(X_train)} rows with {len(X_train.columns)} features')
    model_card.model_parameters.data[0].graphics.collection = [
        mctlib.Graphic(image=mean_radius_train),
        mctlib.Graphic(image=mean_texture_train)
    ]
    model_card.model_parameters.data.append(mctlib.Dataset())
    model_card.model_parameters.data[1].graphics.description = (
      f'{len(X_test)} rows with {len(X_test.columns)} features')
    model_card.model_parameters.data[1].graphics.collection = [
        mctlib.Graphic(image=mean_radius_test),
        mctlib.Graphic(image=mean_texture_test)
    ]
    model_card.quantitative_analysis.graphics.description = (
      'ROC curve and confusion matrix')
    model_card.quantitative_analysis.graphics.collection = [
        mctlib.Graphic(image=roc_curve),
        mctlib.Graphic(image=confusion_matrix)
    ]

    model_card.quantitative_analysis.performance_metrics = [
      mctlib.PerformanceMetric(type='accuracy', value=str(accuracy))
    ]

    # Custom properties
    model_card.thingstoknow.intervention = [mctlib.Intervention(description='Assessment')]

    mct.update_model_card(model_card)

    template_path = os.path.join(mct_directory, 'template/html/my_template.html.jinja')
    mct.export_format(model_card, template_path, 'model_card.html')
    return


if __name__ == "__main__":
    main()
