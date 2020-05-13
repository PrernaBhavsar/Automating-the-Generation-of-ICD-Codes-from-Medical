import numpy as np
import pandas as pd
import math
from sklearn.metrics import precision_score, recall_score, f1_score, multilabel_confusion_matrix, accuracy_score, average_precision_score
#model, data_test, labels_test, icd_codes, df_test_split
def prediction(model, test_data, test_labels, icd_codes, test_split_df):
    if len(icd_codes) == 50:
        threshold = 0.32
    else: threshold = 0.15
    test_pred = model.predict(test_data, batch_size=50, verbose=1)
    test_pred_b= np.where(test_pred>=threshold, 1, 0)
    average_total, average, recall = 0, 0, 0
    
    # Finding the Average Precision Score
    n=3372
    for i in range(3372):
      if (math.isnan(average_precision_score(test_labels[i], test_pred[i]))):
        n=n-1
        continue
      else:
        average_total +=  average_precision_score(test_labels[i], test_pred[i])
    average_total /= n
    print("Average Precision Score for Test Set: "+ str(average_total) + str("\n"))
    
    # Finding the Average Accuracy Score and Average Recall
    for i in range(0, 3372):
      average +=  accuracy_score(test_labels[i], test_pred_b[i])
      recall +=  recall_score(test_labels[i], test_pred_b[i])
    average/= 3372
    recall/= 3372
    print("Average Accuracy Score for Test Set: "+ str(average) + str("\n"))
    print("Average Recall Score for Test Set: "+ str(recall) + str("\n"))
    
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