<table align="center"><tr><td align="center" width="9999">

<img src="/images/Leeds Logo.jpg" align="center" width="500" alt="Project icon" >

# MSBX-5500 Spring 2020

## Security Analytics Final Project
</td></tr></table>

### Business Problem Understanding

In today's security operations environments, security professionals need a way to efficiently and effectively understand their organizations network traffic. The answer to this is an automated process that will follow up on alerts to determine if network traffic is from a botnet. Botnets pose the following threats to an organizations network infrastructure:

  * **DDoS**: cyber-attack in which the perpetrator seeks to make a machine or network resource unavailable to its intended users by temporarily or indefinitely disrupting services of a host connected to the Internet.
  * **Data theft**: stealing computer-based information from an unknowing victim with the intent of compromising privacy or obtaining confidential information.
  * **Spam**: unwanted, unsolicited digital communication, often an email, that gets sent out in bulk.
  * **Malware**: any software intentionally designed to cause damage to a computer, server, client, or computer network.
  * **Mine digital currencies**: type of currency that has no physical form and only exists in digital form/ virtual money and cryptocurrency.

For this project we will use the [CTU-13 dataset](https://www.stratosphereips.org/datasets-ctu13) of botnet traffic that was captured by the CTU University, Czech Republic, in 2011, along with the [Kddcup99](https://datahub.io/machine-learning/kddcup99) data set. We will use predictive analytics to classify the netflow as malicious or benign and also provide the type of malicious attack (multiclass prediction).

### Data Understanding
#### CTU-13 dataset
The [CTU-13 dataset](https://www.stratosphereips.org/datasets-ctu13) consists of thirteen scenarios of different botnet samples captured in pcap files. Out of the thirteen scenarios, our team focused on [Scenario 1](https://mcfp.weebly.com/ctu-malware-capture-botnet-42.html). For our use case we will be using the bidirectional netflow files which have the following features that will be used to train our model:

| StartTime | Dur | Proto | SrcAddr | Sport | Dir | DstAddr | Dport | State | sTos | dTos | TotPkts | TotBytes | SrcBytes | Label |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2011/08/10 09:46:53.047277 | 3550.182373 | udp | 212.50.71.179 | 39678 | <-> | 147.32.84.229 | 13363 | CON | 0 | 0 | 12 | 875 | 473 | flow=Background-UDP-Established |




### Data Preparation

All CTU-13 models were trained using the capture20110810.binetflow file from the [Stratosphere Research Library]( https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-42/detailed-bidirectional-flow-labels/), where a *.binetflow* is a bidrectional NetFlow file generated with [Argus](https://www.systutorials.com/docs/linux/man/8-argus/).

For the CTU-13 model, we needed to remove any NAs in the dataset. To do this, our team dropped all rows that contained an NA. For preprocessing, we set up a pipeline that took our categorical features and OneHotEncoded them in order for them to be ready to be fit to the model.

### Modeling

#### CTU-13 Models

The first model built for the CTU-13 dataset was a Random Forest Classifier. A Random Forest Classifier is an ensemble algorithm that generates a large number of decision trees, and aggregates them to get a strong prediction for each class. The reason this algorithm is highly effective is because each generated tree carries a low correlation from tree to tree. Some trees may be poor predictors, but others will be strong, which means the aggregate ensemble will be more accurate than individual trees.

The second model we built for the CTU-13 dataset was Logistic Regression. Logistic Regression is one of the most common machine learning algorithms for classification problems. A logistic regression algorithm uses a Sigmoid function, which maps values between 0 and 1. We can use logistic regression to find probabilities of certain classes.

The third model we built for the CTU-13 dataset was Gradient Boosted Method (GBM). Gradient boosting methods are similar to Random Forests, in that they build an ensemble of trees. However, the key difference is that the Gradient Boosting algorithm builds iteratively. Gradient Boosting builds a tree and combines the results from the previous tree right away, in an effort to be more predictive. Random Forest combines all trees at the end. Gradient Boosting Methods also have loss functions that can be tuned to get better results.

#### Parameters

For all three models, the same version of scikit learn was used for all models(0.22.2). For the Logistic Regression and Gradient Boosting models, all of the default parameters were used. For the Random Forest model, our team changed min_samples_leaf=10. This is done to ensure we do not have one case per leaf, which would give us an overfitted model.

Next, our data was very imbalanced and thus needed to be resampled. We did this using SMOTE which creates similar samples of the minority class in the dataset. This method makes the minority class and makes it equal to the majority class. Once this was completed, we were able to perform our test train split on the data. We did this using scikit-learn's function test_train_split(), which assigns a random sample of the data into the test data. For this split, we chose a percentage of 20%. We feel that 20% is a good hold out percentage, given that the data was balanced using SMOTE. After the split, our training data contained 81,388 rows, while our test data contained 16,277 rows.

#### Features
Finally, the final features that we trained on were as follows:

| StartTime | Dur | Proto | SrcAddr | Sport | Dir | DstAddr | Dport | State | sTos | dTos | TotPkts | TotBytes | SrcBytes | Label |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 2011/08/10 09:46:53.047277 | 3550.182373 | udp | 212.50.71.179 | 39678 | <-> | 147.32.84.229 | 13363 | CON | 0 | 0 | 12 | 875 | 473 | flow=Background-UDP-Established |


### Model Evaluation

#### Overview

After running our three models on the data, we got average results with the Logistic Regression model. However, we got very strong results with both the Random Forest and Gradient Boosting models. While we had two models that scored very well, we ended up choosing Random Forest as the best model for our dataset. A breakdown of the metrics for all models is shown below.

In figures 1-3, we have shown two confusion matrices for each of our given models. First, the "True" label should be interpreted as the Actual outcome of the dataset. The "Predicted" label is interpreted as what this model is predicting. The 1's for this matrix refer to the given netflow being malicious, while the 0 suggests it is benign. The top matrix for each model reports the totals for each section, while the bottom matrix for each model reports the weights of each section.

In figures 4-5, we have the Precision-Recall plot (figure 4) and the ROC Curve (figure 5) shown. Lastly, in figure 6, we have a table that shows all of the models and their respective metrics we chose.


Figure 1:

In Figure 1, we see the two confusion matrices for the Logistic Regression model.

![Screen Shot 2020-05-05 at 4 27 40 PM](https://user-images.githubusercontent.com/56977428/81122048-5274c880-8eed-11ea-9ba3-3fd5b7070037.png)

Figure 2:

In Figure 2, we see the two confusion matrices for the Random Forest model.

![Screen Shot 2020-05-05 at 4 32 23 PM](https://user-images.githubusercontent.com/56977428/81122366-fa8a9180-8eed-11ea-9e74-0bae011f0d24.png)

Figure 3:

In Figure 3, we see the two confusion matrices for the Gradient Boosted model.

![Screen Shot 2020-05-05 at 4 33 03 PM](https://user-images.githubusercontent.com/56977428/81122408-12621580-8eee-11ea-8bd6-46cdcc1ea525.png)

Figure 4:

In Figure 4, we see our Precision-Recall plot for all three models. This plot summarizes the trade off between the Precision (Y-axis) and the Recall (X-Axis). Precision refers to the "positive predictive value" of the model; it describes how good a model is at predicting the positive class (the 1's). Recall refers to the "true positive rate", or the "hit rate" of the model. Recall is the ratio of true positives divided by the sum of true positives and false negatives. Both the Random Forest and the Gradient Boosted models scored very high on this plot, and this is one factor that led us to picking one of these for our final model.
![Screen Shot 2020-05-05 at 2 53 57 PM](https://user-images.githubusercontent.com/56977428/81119974-0d4e9780-8ee9-11ea-99e1-ca26f68399a6.png)

Figure 5:

In Figure 5, we have our ROC curve for all three models. In the ROC curve, the true positive rate (Y-axis) is plotted against the false positive rate (x-axis) for a number of different thresholds. Essentially, it shows the "hit rate" vs. "false alarm rate". Given our curve, the two best performing models were Random Forest and Gradient Boosted.
![Screen Shot 2020-05-05 at 2 53 49 PM](https://user-images.githubusercontent.com/56977428/81120054-26efdf00-8ee9-11ea-9ae7-8f0fdc6b9896.png)

Figure 6:

In Figure 6, a table was created to showcase all of the metrics we chose to test our models. In the table, "model score" refers to a scikit-learn function used which calculates the mean accuracy for the model. When looking at all of our metrics, Random Forest did slightly better than Gradient Boosting. This is the model we ended up choosing for deployment.

| Name of Model       | Model Score | Average Precision | ROC AUC | Precision-Recall AUC |
|---------------------|-------------|-------------------|---------|----------------------|
| Logistic Regression | 0.638       | 0.493             | 0.546   | 0.493                |
| Random Forest       | 0.887       | 0.967             | 0.968   | 0.967                |
| Gradient Boosting   | 0.890       | 0.952             | 0.956   | 0.953                |

### Deployment
<table align="center"><tr><td align="center" width="9999">
<img src="/images/paas.png" align="center" height="200" width="300" alt="Project icon" >
</td></tr></table>

#### Tools used for deployment
1. GitHub
2. GCP
3. Docker
4. Heroku

For this stage, we took our best performing model to pickle. From the model evaluation stages, we selected Random Forest because it had the best scores across the board, just edging out our Gradient Boosted model. Once this model is pickled, we can load it into our app.py document, which is explained below.

The threshold set for deployment for CTU-13 was **0.25**, which is the threshold that maximizes the F1 score for our CTU-13 model.

#### app.py: METHOD - process_file

The app.py file is written using Flask which is seen ![here](https://github.com/deargle-classes/msbx5500-spring-2020-project/blob/master/app.py).


1. User uploaded .pcap files are fetched from the GridFS Mongo Database
2. This .pcap file is converted into a bytestream using *[argus ra](https://www.systutorials.com/docs/linux/man/1-ra/)*, a tool to read and categorize network flow data from stdin.
	- Argus is configured according to [argus.conf](https://github.com/deargle-classes/msbx5500-spring-2020-project/blob/master/argus.conf)
3. The bytestream is placed into a buffer with BufferIO
4. The buffer is read to a pd dataframe
5. The "Label" column is dropped from the dataframe
6. "NA" values are filled with 0
7. For Kddcup99: the features from the dataframe are read into a array of feature names
8. For each feature in the feature name array, build a new array to be saved as a dataframe with those features and respective data columns

#### KDD Cup 99 Data

Also included inside of the app.py is a model already ![trained](https://github.com/deargle/security-analytics-deploy-model/blob/master/LogisticRegression.pkl) on the KDD Cup 99 data. The model uses a simple Logistic Regression to classify between a DDoS attack, or not. For more information on the details of the KDD Cup 99 Data, click ![here](https://github.com/deargle-classes/msbx5500-spring-2020-project/blob/master/KDDinfo.md)

Using this data, we will have a second model that we can use to test against netflows. Each netflow will be ran against both models, leading to two predictions. The CTU-13 model will be able to predict whether the netflow is a botnet according to the CTU-13 scenario used, while the Kddcup99 model will be able to predict whether it is a DDoS attack, or not, among 4 main classes.

#### Use Case

The end product of the flask app, with the best fitted model, is shown below. It allows for pcap files to be uploaded and then processed through both models. Alerts will be shown in the top portion of the webpage The use case is to give two predictions for incoming netflows: the trained CTU model will predict if a given series of netflows identifies as malicious or benign, while the trained KDD model will predict if the netflows are DDoS or not. Both models will give alerts if the netflow is above the threshold we stated above (the threshold for the KDD model is listed inside app.py). Someone using this webapp to review netflow data can quickly spot potential malicious netflows and resolve them.
