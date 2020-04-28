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
The [CTU-13 dataset](https://www.stratosphereips.org/datasets-ctu13) consists of thirteen scenarios of different botnet samples captured in pcap files. For out use case we will be using the bidieractional netflow files which have the follwing features that will be used to train our model:

| StartTime | Dur | Proto | SrcAddr | Sport | Dir | DstAddr | Dport | State | sTos | dTos | TotPkts | TotBytes | SrcBytes | Label |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | 
| 2011/08/10 09:46:53.047277 | 3550.182373 | udp | 212.50.71.179 | 39678 | <-> | 147.32.84.229 | 13363 | CON | 0 | 0 | 12 | 875 | 473 | flow=Background-UDP-Established |

#### Kddcup99 dataset
https://datahub.io/machine-learning/kddcup99

### Data Preparation

### Modeling

### Model Evaluation
  
### Deployment
