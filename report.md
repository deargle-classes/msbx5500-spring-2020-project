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

#### Kddcup99 dataset
The [Kddcup99](https://datahub.io/machine-learning/kddcup99) dataset is a 10% subsample of data used at the 1999 KDD Cup, used to distinguish between "bad" connections (attacks/intrusions) and "good" (normal) connections. To be more specific, the target variable was to determine if a given net flow was a DDoS attack, or not.

The Kddcup99 dataset consists of 42 features, which can be seen [here](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names), and previewed below:

| duration | protocol_type | service | flag | src_bytes | dst_bytes | land | wrong_fragment | urgent | hot | num_failed_logins | logged_in | lnum_compromised | lroot_shell | lsu_attempted | lnum_root | lnum_file_creations | lnum_shells | lnum_access_files | lnum_outbound_cmds | is_host_login | is_guest_login | count | srv_count | serror_rate | srv_serror_rate | rerror_rate | srv_rerror_rate | same_srv_rate | diff_srv_rate | srv_diff_host_rate | dst_host_count | dst_host_srv_count | dst_host_same_srv_rate | dst_host_diff_srv_rate | dst_host_same_src_port_rate | dst_host_srv_diff_host_rate | dst_host_serror_rate | dst_host_srv_serror_rate | dst_host_rerror_rate | dst_host_srv_rerror_rate | label |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | tcp | http | SF | 181 | 5450 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 8 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 9 | 9 | 1.00 | 0.00 | 0.11 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | normal |

The data consists of compressed TCP dump data from normal and malicious network traffic on a simulated U.S. Air Force LAN. Each connection is labeled as "DDos Attack" or "Not a DDos Attack" and all attacks fall under one of the four specific categories below:

* **DOS**: denial-of-service, e.g. syn flood;
* **R2L**: unauthorized access from a remote machine, e.g. guessing password;
* **U2R**: unauthorized access to local superuser (root) privileges, e.g., various "buffer overflow" attacks;
* **probing**: surveillance and other probing, e.g., port scanning.

For our use case we will be using this data to build a second model to determine whether or not a connection is malicious.

Each netflow will be ran against both models, leading to two predictions. The CTU-13 model will be able to predict whether the netflow is a botnet according to the CTU-13 scenario used, while the Kddcup99 model will be able to predict whether it's one of 8 different malicious classes.


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

After running our three models on the data, we got average results with the Logistic Regression model. However, we got very strong results with both the Random Forest and Gradient Boosting models. A breakdown of the metrics for all models is shown below.

Figure 1:
![Screen Shot 2020-05-05 at 2 53 57 PM](https://user-images.githubusercontent.com/56977428/81119974-0d4e9780-8ee9-11ea-99e1-ca26f68399a6.png)


Figure 2:
![Screen Shot 2020-05-05 at 2 53 49 PM](https://user-images.githubusercontent.com/56977428/81120054-26efdf00-8ee9-11ea-9ae7-8f0fdc6b9896.png)




### Deployment
<table align="center"><tr><td align="center" width="9999">
<img src="/images/paas.png" align="center" height="200" width="300" alt="Project icon" >
</td></tr></table>

#### app.py: METHOD - process_file(_id)

1. User uploaded .pcap files are fetched from the GridFS Mongo Database
2. This .pcap file is converted into a bytestream using *[argus ra](https://www.systutorials.com/docs/linux/man/1-ra/)*, a tool to read and categorize network flow data from stdin.
	- Argus is configured according to [argus.conf](https://github.com/deargle-classes/msbx5500-spring-2020-project/blob/master/argus.conf)
3. The bytestream is placed into a buffer with BufferIO
4. The buffer is read to a pd dataframe
5. The "Label" column is dropped from the dataframe
6. "NA" values are filled with 0
7. For Kddcup99: the features from the dataframe are read into a array of feature names
8. For each feature in the feature name array, build a new array to be saved as a dataframe with those features and respective data columns

#### Tools used for deployment
1. GitHub
2. GCP
3. Docker
4. Heroku

The threshold set for deployment for CTU-13 was **0.25550653879194696**, which is the threshold that maximizes the F1 score for our CTU-13 model.

Each team member shall deploy the final repo individually.

Deployment (for small files only) should be hosted through Heroku, using a Docker image to register the image for Heroku deployment.
