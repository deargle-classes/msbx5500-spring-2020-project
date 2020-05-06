The [Kddcup99](https://datahub.io/machine-learning/kddcup99) dataset is a 10% subsample of data used at the 1999 KDD Cup, used to distinguish between a "DDoS" attack, or not.

The Kddcup99 dataset consists of 42 features, which can be seen [here](http://kdd.ics.uci.edu/databases/kddcup99/kddcup.names), and previewed below:

| duration | protocol_type | service | flag | src_bytes | dst_bytes | land | wrong_fragment | urgent | hot | num_failed_logins | logged_in | lnum_compromised | lroot_shell | lsu_attempted | lnum_root | lnum_file_creations | lnum_shells | lnum_access_files | lnum_outbound_cmds | is_host_login | is_guest_login | count | srv_count | serror_rate | srv_serror_rate | rerror_rate | srv_rerror_rate | same_srv_rate | diff_srv_rate | srv_diff_host_rate | dst_host_count | dst_host_srv_count | dst_host_same_srv_rate | dst_host_diff_srv_rate | dst_host_same_src_port_rate | dst_host_srv_diff_host_rate | dst_host_serror_rate | dst_host_srv_serror_rate | dst_host_rerror_rate | dst_host_srv_rerror_rate | label |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | tcp | http | SF | 181 | 5450 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 8 | 8 | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 | 9 | 9 | 1.00 | 0.00 | 0.11 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | normal |

The data consists of compressed TCP dump data from normal and malicious network traffic on a simulated U.S. Air Force LAN. Each connection is labeled as "DDos Attack" or "Not a DDos Attack" and all attacks fall under one of the four specific categories below:

* **DOS**: denial-of-service, e.g. syn flood;
* **R2L**: unauthorized access from a remote machine, e.g. guessing password;
* **U2R**: unauthorized access to local superuser (root) privileges, e.g., various "buffer overflow" attacks;
* **probing**: surveillance and other probing, e.g., port scanning.
