import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from sklearn.metrics import precision_score, recall_score, f1_score, multilabel_confusion_matrix, accuracy_score, average_precision_score, precision_recall_curve
#model, data_test, labels_test, icd_codes, df_test_split
def prediction(model, test_data, test_labels, icd_codes, test_split_df):
    if len(icd_codes) == 50:
        threshold = 0.32
    else: threshold = 0.15
    test_pred = model.predict(test_data, batch_size=50, verbose=1)
    test_pred_b= np.where(test_pred>=threshold, 1, 0)
    average_total, average, recall = 0, 0, 0
    
    # Finding the Average Precision Score
    n=len(test_data)
    for i in range(len(test_data)):
      if (math.isnan(average_precision_score(test_labels[i], test_pred[i]))):
        n=n-1
        continue
      else:
        average_total +=  average_precision_score(test_labels[i], test_pred[i])
    average_total /= n
    print("Average Precision Score for Test Set: "+ str(average_total) + str("\n"))
    
    # Finding the Average Accuracy Score and Average Recall
    for i in range(0, len(test_data)):
      average +=  accuracy_score(test_labels[i], test_pred_b[i])
      recall +=  recall_score(test_labels[i], test_pred_b[i])
    average/= len(test_data)
    recall/= len(test_data)
    print("Average Accuracy Score for Test Set: "+ str(average) + str("\n"))
    print("Average Recall Score for Test Set: "+ str(recall) + str("\n"))

    #FINDING PREDICTION RECALL CURVE

    # For each class
    precision = dict()
    recall = dict()
    average_precision = dict()
    for i in range(len(icd_codes)):
        precision[i], recall[i], _ = precision_recall_curve(test_labels[:, i],
                                                            test_pred[:, i])
        average_precision[i] = average_precision_score(test_labels[:, i], test_pred[:, i])

    precision["micro"], recall["micro"], _ = precision_recall_curve(test_labels.ravel(),
    test_pred.ravel())

    average_precision["micro"] = average_precision_score(test_labels, test_pred,
                                                     average="micro")


    plt.figure()
    plt.step(recall['micro'], precision['micro'], where='post')

    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    if icd_codes==50:

        plt.title(
            'Average precision score, micro-averaged over all classes: AP={0:0.4f} \n For Top 50 ICD9 codes'
            .format(average_precision["micro"]))
    else:
        plt.title(
            'Average precision score, micro-averaged over all classes: AP={0:0.4f} \n For All ICD9 codes'
            .format(average_precision["micro"]))


    # Converting the Binary Predicted Labels of Test Set to Predicted ICD Codes
    test_pred_codes = pd.DataFrame('', index = range(0, test_pred_b.shape[0]), columns = ['LABELS'])

    for i in range(0, test_pred_b.shape[0]):
        for j in range(0, test_pred_b.shape[1]):
            if test_pred_b[i][j] == 1:
                test_pred_codes.iloc[i, 0] = test_pred_codes.iloc[i, 0] + icd_codes[j] + ', '
    
    #Finding the Y_labels of test set containing only the TOP 50 Actual Codes
    if threshold == 0.32:
        test_top50=pd.DataFrame('', index = range(0, test_labels.shape[0]), columns = ['LABELS'])
        for i in range(0, test_labels.shape[0]):
            for j in range(0, test_labels.shape[1]):
                if test_labels[i][j] == 1:
                    test_top50.iloc[i, 0] = test_top50.iloc[i, 0] + icd_codes[j] + ', '
                
    test_output = pd.DataFrame(columns=['SUBJECT_ID','HADM_ID','ACTUAL LABELS','PREDICTED LABELS'])
    test_output['SUBJECT_ID']= test_split_df['SUBJECT_ID']
    test_output['HADM_ID']= test_split_df['HADM_ID']
    test_output['PREDICTED LABELS']= test_pred_codes['LABELS']
    if threshold == 0.32:
        test_output['ACTUAL LABELS']= test_top50
    else:
        test_output['ACTUAL LABELS']= test_pred_codes['LABELS']
    return test_output