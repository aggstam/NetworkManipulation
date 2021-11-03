# NetworkManipulation
This python script performs fundamental social network analysis tasks on the temporal network graph for the StackOverflow-related dataset [1].
<br>
On each execution, a dedicated folder is created containing all result files.
<br>
Script calculates tmin and tmax timestamps and splits records in N sub-networks.
<br>
For each sub-network, the following are calculated:
- Various centralities (e.g. Degree, Closeness, Eigenvector, etc.)
- Similarity tables (e.g. Graph Distance, Jaccard's Coefficient, etc.)
- Metrics predictions of consecutive sub-networks
<br>
<br>
References:
<br>
[1] https://snap.stanford.edu/data/sx-stackoverflow.html
