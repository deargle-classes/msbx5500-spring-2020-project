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
The [CTU-13 dataset](https://www.stratosphereips.org/datasets-ctu13) consists of thirteen scenarios of different botnet samples captured in pcap files. For our use case we will be using the bidirectional netflow files which have the following features that will be used to train our model:

| StartTime | Dur | Proto | SrcAddr | Sport | Dir | DstAddr | Dport | State | sTos | dTos | TotPkts | TotBytes | SrcBytes | Label |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | 
| 2011/08/10 09:46:53.047277 | 3550.182373 | udp | 212.50.71.179 | 39678 | <-> | 147.32.84.229 | 13363 | CON | 0 | 0 | 12 | 875 | 473 | flow=Background-UDP-Established |

#### Kddcup99 dataset
The [Kddcup99](https://datahub.io/machine-learning/kddcup99) dataset is a 10% subsample of data used at the 1999 KDD Cup, used to distinguish between "bad" connections (attacks/instrusions) and "good" (normal) connections.

The Kddcup99 dataset consists of 42 features, which can be seen [here](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names), and previewed below:

| duration | protocol_type | service | flag | src_bytes | dst_bytes | land | wrong_fragment | urgent | hot | num_failed_logins | logged_in | lnum_compromised | lroot_shell | lsu_attempted | lnum_root | lnum_file_creations | lnum_shells | lnum_access_files | lnum_outbound_cmds | is_host_login | is_guest_login | count | srv_count | serror_rate | srv_serror_rate | rerror_rate | srv_rerror_rate | same_srv_rate | diff_srv_rate | srv_diff_host_rate | dst_host_count | dst_host_srv_count | dst_host_same_srv_rate | dst_host_diff_srv_rate | dst_host_same_src_port_rate | dst_host_srv_diff_host_rate | dst_host_serror_rate | dst_host_srv_serror_rate | dst_host_rerror_rate | dst_host_srv_rerror_rate | label |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | tcp | http | SF | 181 | 5450 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 8 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 9 | 9 | 1.00 | 0.00 | 0.11 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | normal |

The data consists of compressed TCP dump data from normal and malicious network traffic on a simulated U.S. Air Force LAN. Each connection is labeled as "normal" or an "attack" and "attacks" must fall under one of the four specific categories below:

* **DOS**: denial-of-service, e.g. syn flood;
* **R2L**: unauthorized access from a remote machine, e.g. guessing password;
* **U2R**: unauthorized access to local superuser (root) privileges, e.g., various "buffer overflow" attacks;
* **probing**: surveillance and other probing, e.g., port scanning.

For our use case we will be using this data to build a second model to determine whether or not a connection is malicious.

Each netflow will be ran against both models, leading to two predictions. The CTU-13 model will be able to predict whether the netflow is a botnet according to the CTU-13 scenario used, while the Kddcup99 model will be able to predict whether it's one of 8 different malicious classes.

### Data Preparation

TODO: need some help on how the sampling methodology for CTU-13 was done

All CTU-13 models were trained using the capture20110810.binetflow file from the [Stratosphere Research Library]( https://mcfp.felk.cvut.cz/publicDatasets/CTU-Malware-Capture-Botnet-42/detailed-bidirectional-flow-labels/), where a *.binetflow* is a bidrectional NetFlow file generated with [Argus](https://www.systutorials.com/docs/linux/man/8-argus/).

#### Model 1 - First Pass RandomForest
#### Preprocessing
1. Data is read in from the binetflow file as a CSV format.
2. Rows containing "NA" are dropped
3. The first 15 features are selected for training
4. The test data is split for training, using a .5 test size split
5. The categorical features: Protocol, Direction, and State are one-hot encoded

#### Model 2 - Resampled RandomForest
#### Preprocessing
1. Rows containing "NA" are dropped
3. The first 15 features are selected for training
4. Python libraries used to complete modeling
   - pandas, numpy, sklearn, imblearn, collections
5. SMOTE, Upsampling, Downsampling
6. Categorical features used: 'Proto', 'Dir', 'State'
7. OneHotEncoding
8. Classifier: Random Forest
9. The test data is split for training, using a .5 test size split

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

### Modeling

#### CTU-13 model

The model built for the CTU-13 dataset was originally a random forest trained on CTU example data. However, this model was poor because the original training data was imbalanced. To fix this, we upsampled and downsampled the minority and majority classes to extract a more balanced set. After this, we again ran the random forest to get a better fitted model and pickled that.

### Model Evaluation

#### CTU-13 scoring metrics and Confusion Matrix Non-Normalized (resampled data)
Because of the large amount of resampling needed to be done, the model was not hypertuned and was not tested on a full size training set. The implications of this can be seen in the metrics, we don't have very high recall on our true positives. This makes creating a threshold for the api difficult, but at least gives some insight into how we can improve the model for a future project.

<table align="center"><tr><td align="center" width="9999">
<img src="/images/ctu-13cm2.PNG" align="center" height="300" width="300" alt="Project icon" >
</td></tr></table>


<table align="center"><tr><td align="center" width="9999">
<img src="/images/ctu-13roc.png" align="center" height="300" width="300" alt="Project icon" >
</td></tr></table>



### Deployment
<table align="center"><tr><td align="center" width="9999">
<img src="/images/paas.png" align="center" height="200" width="300" alt="Project icon" >
</td></tr></table>

#### Tools used for deployment
1. GitHub
2. GCP
3. Docker
4. Heroku

The threshold set for deployment for CTU-13 was .3

Each team member shall deploy the final repo individually.

Deployment (for small files only) should be hosted through Heroku, using a Docker image to register the image for Heroku deployment.

