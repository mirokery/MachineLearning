import quandl
import pandas as pd
import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm, preprocessing, model_selection
from matplotlib import style
style.use('fivethirtyeight')


def create_labels(cur_hpi, fut_hpi):
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0


housing_data = pd.read_pickle('HPI.pickle')
housing_data = housing_data.pct_change()

housing_data.replace([np.inf, -np.inf], np.nan, inplace=True) # replace inf values to nan
housing_data['US_HPI_FUTURE'] = housing_data['United States'].shift(-1)
housing_data.dropna(inplace=True) # drop all nan values

housing_data['label'] = list(map(create_labels,housing_data['United States'],housing_data['US_HPI_FUTURE']))
print(housing_data[['United States','US_HPI_FUTURE','label']].head(20))

X = np.array(housing_data.drop(['label','US_HPI_FUTURE'],1))
X = preprocessing.scale(X)
y = np.array(housing_data['label'])


X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y, test_size=0.2)
clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)

print(clf.score(X_test,y_test))