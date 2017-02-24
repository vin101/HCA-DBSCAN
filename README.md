# HCA-DBSCAN
This is a proof-of-concept implementation for a new density based clustering algortihm, called the HCA-DBSCAN.
Paper
===
Please refer our associated paper for a detailed explanation of the HCA-DBSCAN algorithm
https://goo.gl/eVBCkX 


Abstract
===
Density based clustering has proven to be very efficient and has found numerous applications across domains. The Density-Based Spatial Clustering of Applications with Noise (DBSCAN) algorithm is capable of finding clusters of varied shapes and is not sensitive to outliers in the data. In this paper we propose a new clustering algorithm, the HyperCube based Accelerated DBSCAN(HCA-DBSCAN) which runs in O(n log n) bettering the O(n^2 ) complexity of the original DBSCAN algorithm without compromising on clustering accuracy. While DBSCAN can achieve the same complexity when spatial indexing is used, that complexity again grows to O(n^2) for higher dimensional data; which does not happen with our approach. We use a combination of distance based aggregation by overlaying the data with customized grids and use representative points to reduce the number of comparisons. Experimental results show that the proposed algorithm achieves a significant run time speed up of upto 52.57% when compared to other improvements that try to reduce the complexity of DBSCAN to O(n log n). Another significant improvement is that we eliminate the need for one of the two input parameters needed by the original DBSCAN algorithm thus making it more accessible to non expert users.


How to Run
===
Run the visualization.py to test the code on various 2-dimensional data sets and see the results by visulaizing the graphs of the clusters detected in the data
