# Part 1
To generate an ROC-curve and calculate its corresponding AUC, create two files that contain the output of the negative selection algorithm for a file containing normal data, and a file containing the output for anomaly data. In *luna.py*, edit the folder and *fname_\** variables to these corresponding files, and run the file. A ROC-curve plot with the AUC in the title will be automatically created.

# Part 2
To automatically find the optimal hyperparameter settings for a certain file (e.g. *snd-cert.1.test*), edit the folders and filenames in *pipeline.py* to point to the files on your local pc. Then run this file.
