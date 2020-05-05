#!/usr/bin/env python
# coding: utf-8

# In[38]:


import pandas as pd
import numpy as np
import numpy.ma as ma
import pickle as pkl
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import plot_precision_recall_curve
from sklearn.metrics import average_precision_score
from sklearn.metrics import log_loss
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.ensemble import GradientBoostingClassifier
from imblearn.over_sampling import SMOTENC
from imblearn.under_sampling import RandomUnderSampler
from imblearn.under_sampling import CondensedNearestNeighbour
from collections import Counter
from scipy.stats import hmean



filename = 'capture20110810.binetflow'
try:
    # try to load the file from a local directory
    data = pd.read_csv(filename)
    pass
except:
    # fetch it from the url
    data = pd.read_csv('https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-42/detailed-bidirectional-flow-labels/{}'.format(filename))
    data.to_csv(filename)
    pass


# In[39]:


data.head()


# In[4]:


data['Target'] = data['Label'].str.startswith('flow=From-Botnet').astype(int)


# In[5]:


targetno = data[data['Target']==0]


# In[6]:


targetyes = data[data['Target']==1]


# In[7]:


print('Percent Minority %f' % ((sum(data['Target'])/len(data['Target']))*100))


# In[8]:


targetno.shape


# # Smote takes too long with categoricals, so I manaully resampled due to computing power restrictions

# In[18]:


drop_indices = np.random.choice(targetno.index, 2740000, replace=False)
targetno_new = targetno.drop(drop_indices)


# In[19]:


net_flows_new = targetno_new.append(targetyes)


# In[20]:


print('Percent Minority %f' % ((sum(net_flows_new['Target'])/len(net_flows_new['Target']))*100))


# In[21]:


net_flows = net_flows_new.dropna()
X = net_flows.iloc[:,0:14]
y = net_flows['Target']


# In[23]:


print('Percent Minority %f' % ((sum(y)/len(y))*100))


# # Actually fitting smote

# In[24]:


categorics = ['StartTime', 'Proto', 'SrcAddr', 'Sport', 'Dir', 'DstAddr', 'Dport', 'State']


# In[25]:


cat_index = [net_flows.columns.get_loc(c) for c in categorics if c in X]


# In[26]:


sm = SMOTENC(random_state = 42, categorical_features=[0, 2, 3, 4, 5, 6, 7, 8])


# In[27]:


X_res, y_res = sm.fit_resample(X, y)


# In[28]:


print('Percent Minority %f' % ((sum(y_res)/len(y_res))*100))


# # AAAANNNNDDD we're at a balanced dataset now

# In[29]:


X.shape


# In[40]:


numeric_features = ['Dur', 'TotPkts', 'TotBytes']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())])


categorical_features = ['Proto','Dir','State']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)])


clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('clf', None)])

roc_things = []
precision_recall_things = []

X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=.2, random_state=42)

classifiers = [
    LogisticRegression(),
    RandomForestClassifier(min_samples_leaf = 10),
    GradientBoostingClassifier()
]

for classifier in classifiers:
    clf.set_params(clf=classifier).fit(X_train, y_train)
    classifier_name = classifier.__class__.__name__
    print(str(classifier_name))
    print("model score: %.3f\n" % clf.score(X_test, y_test))

    
    y_score = clf.predict_proba(X_test)[:,1]
    
    y_pred = clf.predict(X_test)
    
    roc_auc = roc_auc_score(y_test, y_score)
    fpr, tpr, _ = roc_curve(y_test, y_score)
    roc_things.append((fpr, tpr, '{} AUC: {:.3f}'.format(classifier_name, roc_auc)))
    
    
    titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
    for title, normalize in titles_options:
        disp = plot_confusion_matrix(clf, X_test, y_test,
                                     cmap=plt.cm.Blues,
                                     normalize=normalize)
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)

    plt.show()
    
    
    print(classification_report(y_test, y_pred))
    
    precision, recall, thresholds = precision_recall_curve(y_test, y_score)
    pr_auc = auc(recall, precision)
    precision_recall_things.append((recall, precision, thresholds, '{} AUC: {:.3f}'.format(classifier_name, pr_auc)))
    
    
    print('average precision score: {:.3f}'.format(average_precision_score(y_test, y_score)))
    print('roc_auc_score: {:.3f}'.format(roc_auc))
    print('precision-recall AUC: {:.3f}'.format(pr_auc))
    print()
    
    with open('{}.pkl'.format(str(classifier_name)), 'wb') as f:
        pkl.dump(clf, f)

roc_plt = plt.figure()
lw = 4
for roc_thing in roc_things:
    fpr, tpr, label = roc_thing
    plt.plot(fpr, tpr, lw=lw, label=label)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--') # dadgum no-skill line
plt.legend()
plt.title('ROC curve')

pr_plt = plt.figure()
for pr_thing in precision_recall_things:
    recall, precision, _, label = pr_thing
    plt.plot(recall, precision, lw=lw, label=label)
#ratio = y_test[y_test].shape[0] / y_test.shape[0]
#plt.hlines(y=ratio, xmin=0, xmax=1, color='navy', lw=lw, linestyle='--') # dadgum no-skill line
plt.title('Precision-recall plot')
plt.legend()   


# # Threshold Stuffs

# In[41]:


print(thresholds)


# In[42]:


precision, recall, thresholds_2 = precision_recall_curve(y_test, y_score)

a = np.column_stack((recall,precision))

a = ma.masked_less_equal(a,0)
a = ma.mask_rows(a)
f1 = hmean(a,axis=1)


# In[43]:


threshold_maximizing_F1 = thresholds[np.argmax(f1)]
print('f1 optimizing threshold: {}'.format(threshold_maximizing_F1))


# In[ ]:




