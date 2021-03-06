from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix
from data_preparation import X, y
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
import warnings

# ignore warnings
warnings.filterwarnings(action='ignore')

# show info
print('\nK-Nearest-Neighbours Classifier')

# split data in training and test sets
# set up infinite loop
while True:
    try:
        # ask for user input and save in variable
        eval_fraction = float(input('\nPlease enter the split ratio (float between 0 & 1) you want to use'
                                    ' (e.g. 0.3 for 30% testing, 70% training of classifier): ').strip())
        # if input is float between 0 and 1
        if 0 <= eval_fraction <= 1:
            # split dataset in training and evaluation
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=eval_fraction, random_state=1)
            # break infinite loop
            break
        # if input is float outside range of 0 and 1
        else:
            print('Error - Number not between 0 and 1')
    # catch value error when input is e.g. a string
    except ValueError:
        print('Error - Please enter a number!')

# kNN - Classifier
# heuristic for k: square root of n, also round up as number of neighbours cannot be a float
k_nearest_neighbors = math.ceil((y.shape[0]) ** 0.5)
# set distance metric manhatten
distance_metric = 'manhattan'
# initiation of knn classifier
knn = KNeighborsClassifier(n_neighbors=k_nearest_neighbors, metric=distance_metric)
# train classifier with training set
knn.fit(X_train, y_train)
# use trained model to predict response for test set
knn_prediction = knn.predict(X_test)

## Evaluation
# show model statistics
print('\nPredicted class labels (0 = H1N1, 1 = SARS-CoV-2):\n{}'.format(knn_prediction))
print('\nTrue class labels (0 = H1N1, 1 = SARS-CoV-2):\n{}'.format(y_test.values))
print('\nPrediction Accuracy, k={}: {}\n'.format(k_nearest_neighbors, metrics.accuracy_score(y_test, knn_prediction)))
print('Number of mislabeled points out of a total {} points: {}\n\n'.format(X_test.shape[0],
                                                                            np.sum(y_test != knn_prediction)))
# show classification report
print('Classification Report:\n\n{}'.format(classification_report(y_test, knn_prediction,
                                                                  target_names=['H1N1', 'SARS-CoV-2'])))

## Confusion Matrix
# initiation of confusion matrix
matrix = confusion_matrix(y_test, knn_prediction)
# init the plot
plt.figure(figsize=(7, 7))
# set axis labels
axis_labels = ['H1N1', 'SARS-CoV-2']
# plot confusion matrix heatmap
sns.heatmap(matrix, square=True, annot=True, fmt='d', cbar=False, cmap='RdBu_r',
            xticklabels=axis_labels, yticklabels=axis_labels)
# add plot axis labels
plt.xlabel('[True label]')
plt.ylabel('[Predicted label]')
# add plot title
plt.title('k-NN Confusion Matrix, k = {}'.format(k_nearest_neighbors))
# save as png file, remove all of whitespace around figure
plt.savefig('output/knn_confusion_matrix.png', bbox_inches='tight')
# show matrix
plt.show();

## ROC
# calculate false-positive/true-positive-rate
fpr, tpr, threshold = metrics.roc_curve(y_test, knn_prediction)
# calculate roc auc (area under curve)
roc_auc = metrics.auc(fpr, tpr)
# add title
plt.title('Receiver Operating Characteristic (k Nearest Neighbours), k = {}'.format(k_nearest_neighbors))
# plot roc curve and label
plt.plot(fpr, tpr, label='ROC curve')
# plot straight line to visualize random guessing and label
plt.plot([0, 1], [0, 1], 'r--', label='Random Chances')
# plot only another label with AUC value
plt.plot([], [], ' ', label='AUC (Area Under Curve) = {}'.format(roc_auc))
# plot legend at lower right location of figure
plt.legend(loc='lower right')
# define limits of x and y axis
plt.xlim([0, 1])
plt.ylim([0, 1])
# add x and y labels
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
# save as png file, remove all of whitespace around figure
plt.savefig('output/knn_roc.png', bbox_inches='tight')
# show roc-curve
plt.show();