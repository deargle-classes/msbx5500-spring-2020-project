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

For this project we will use the [CTU-13 dataset](https://www.stratosphereips.org/datasets-ctu13) of botnet traffic that was captured by the CTU University, Czech Republic, in 2011. We will use predictive analytics to classify the netflow as malicious or benign and also provide the type of malicious attack (multiclass prediction).

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

The data consists of compressed TCP dump data from network traffic on a simulated US Air Force LAN. Each connection is labeled as "normal" or an "attack" and "attacks" must fall under one specific category:
Attacks categories:
* **DOS**: denial-of-service, e.g. syn flood;
* **R2L**: unauthorized access from a remote machine, e.g. guessing password;
* **U2R**: unauthorized access to local superuser (root) privileges, e.g., various "buffer overflow" attacks;
* **probing**: surveillance and other probing, e.g., port scanning.

For our use case:.... ?

### Data Preparation

### Modeling

### Model Evaluation
  
### Deployment
