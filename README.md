# Automating the Generation of ICD Codes from Medical

## Abtract
The Electronic Health Records (EHR) have gained a wide range of acceptance and are currently used for many applications. EHRs consist of a large number of patient records displaying information like the diagnosis, procedures performed, and medical admissions of the patients, their medical history, and discharge summaries. The discharge summaries are clinical notes written by the doctors giving the description of the diagnosis and procedures performed on the patients. Using these summaries, the annotation of the related ICD codes is done. This process is currently done by experts and professionals in the medical field and is tedious and error-prone. This leads to the attempts being made to automate the process. The MIMIC III database is a public clinical database consisting of information of more than 50,000 admissions of patients at various hospitals. Using this database, our aim is to automate the process of the generation of ICD codes using the discharge summaries. CNN along with LSTM proves to have advantages over the other methods studied as it studies both the temporal and sequential correlation of the text along with importance given to the key phrases. Thus using C-LSTM the model aims to generate results with better accuracy.

## Working of the project
1. Pre-Processing
2. Word Embeddings using BioWordVec
3. Converting Dataframes using Dictionary
4. Traininnng the model
5. Prediction of ICD Codes

## Results

Result Table

![Result Table](/Images/Result_Table.PNG)

Final Output for All ICD9 Codes

![Result All Codes](/Images/Result_full_30.png)

Final Output for Top 50 ICD9 Codes

![Result Top 50 Codes](/Images/Result_top50_20.png)

## References
- [Zhang Y, Chen Q, Yang Z, Lin H, Lu Z. BioWordVec, improving biomedical word embeddings with subword information and MeSH. Scientific Data. 2019.](https://rdcu.be/b38Dr)
- [Automated detection of diabetes using CNN and CNN-LSTM network and heart rate signals.](https://www.sciencedirect.com/science/article/pii/S1877050918307737)

## Project Authors
- [@Janice Johnson](https://github.com/Janice33/)
- [@Parth Jhunjhunwala](https://github.com/ParthJhunjhunwala/)
- [@Prerna Bhavsar](https://github.com/PrernaBhavsar/)
