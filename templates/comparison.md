[//]: # (This is a comment)

# Model Comparison: {model_name1} and {model_name2} 
## Table Of Contents
- [Score](##Score-Comparison)
- [Confusion Matrix Comparison](##Confusion-Matrix-Comparison)

## Score Comparison
| Type      | Score {model_name1}              | Score {model_name2}              |
|-----------|-----------------------------------|-----------------------------------|
| Accuracy  |  {data["scores"]["accuracy"]}     |   {data["scores"]["accuracy"]}    |
| Precision |  {data["scores"]["precision"]}    |   {data["scores"]["precision"]}   |
| Recall    |  {data["scores"]["recall"]}       |   {data["scores"]["recall"]}      |
| F1-Score  |  {data["scores"]["f1-score"]}     |   {data["scores"]["f1-score"]}    |

## Confusion Matrix Comparison
Model {model_name1}                                             | Model {model_name2}
:--------------------------------------------------------------:|:--------------------------------------------------------------:
![]({ROOT_DIR}/.AI_analyzer/{model_name1}/confusion-matrix.png) | ![]({ROOT_DIR}/.AI_analyzer/{model_name2}/confusion-matrix.png)
