[//]: # (This is a comment)

# Model Comparison: {model_name1} and {model_name2} 
## Table Of Contents
- [Score](##Score-Comparison)
- [Confusion Matrix Comparison](##Confusion-Matrix-Comparison)

## Score Comparison
| Type      | Score {model_name1}               | Score {model_name2}               | Offset
|-----------|-----------------------------------|-----------------------------------|--------
| Accuracy  |  {model1_data["scores"]["accuracy"]}     |   {model2_data["scores"]["accuracy"]}    | 
| Precision |  {model1_data["scores"]["precision"]}    |   {model2_data["scores"]["precision"]}   |
| Recall    |  {model1_data["scores"]["recall"]}       |   {model2_data["scores"]["recall"]}      |
| F1-Score  |  {model1_data["scores"]["f1-score"]}     |   {model2_data["scores"]["f1-score"]}    |

## Confusion Matrix Comparison
Model {model_name1}                                             | Model {model_name2}
:--------------------------------------------------------------:|:--------------------------------------------------------------:
![]({ROOT_DIR}/.AI_analyzer/{model_name1}/confusion-matrix.png) | ![]({ROOT_DIR}/.AI_analyzer/{model_name2}/confusion-matrix.png)
