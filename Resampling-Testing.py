#!/usr/bin/env python
# coding: utf-8

# In[62]:


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, confusion_matrix, plot_confusion_matrix
from imblearn.over_sampling import SMOTENC
from imblearn.under_sampling import RandomUnderSampler
from imblearn.under_sampling import CondensedNearestNeighbour
from collections import Counter
import pickle as pkl

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


# In[63]:


data.head()


# In[64]:


data['Target'] = data['Label'].str.startswith('flow=From-Botnet').astype(int)


# In[65]:


targetno = data[data['Target']==0]


# In[66]:


targetyes = data[data['Target']==1]


# In[67]:


print('Percent Minority %f' % ((sum(data['Target'])/len(data['Target']))*100))


# In[68]:


targetno.shape


# In[69]:


drop_indices = np.random.choice(targetno.index, 2750000, replace=False)
targetno_new = targetno.drop(drop_indices)


# In[70]:


net_flows_new = targetno_new.append(targetyes)


# In[71]:


print('Percent Minority %f' % ((sum(net_flows_new['Target'])/len(net_flows_new['Target']))*100))


# In[72]:


net_flows = net_flows_new.dropna()
X = net_flows.iloc[:,0:13]
y = net_flows['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.5, random_state=42)


# In[73]:


print('Percent Minority %f' % ((sum(y_train)/len(y_train))*100))


# # Smote takes too long with categoricals, so I manaully resampled

# In[74]:


#categorics = ['StartTime', 'Proto', 'SrcAddr', 'Sport', 'Dir', 'DstAddr', 'Dport', 'State', 'Label']


# In[75]:


#cat_index = [net_flows.columns.get_loc(c) for c in categorics if c in X]


# In[76]:


#sm = SMOTENC(random_state = 42, categorical_features=[0, 2, 3, 4, 5, 6, 7, 8])


# In[77]:


#X_res, y_res = sm.fit_resample(X_train, y_train)


# In[78]:


#print('Percent Minority %f' % ((sum(y_res)/len(y_res))*100))


# # Going to try to pickle from here

# In[79]:


categorical_features = ['Proto','Dir','State']
categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])
preprocessor = ColumnTransformer(
    transformers=[('cat', categorical_transformer, categorical_features)])
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('clf', RandomForestClassifier(min_samples_leaf = 10))])


# In[80]:


make_pickle = clf.fit(X_train, y_train)


# In[81]:


with open('{}.pkl'.format('pickle'), 'wb') as f:
    pkl.dump(make_pickle, f)


# In[82]:


y_pred = make_pickle.predict(X_test)
print(classification_report(y_test, y_pred))


# In[ ]:




