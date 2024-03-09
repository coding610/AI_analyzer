[//]: # (This is a comment)

# Model Overview: {model_name}
## Table Of Contents
- [Score](##Score)
- [Confusion Matrix](##Confusion-Matrix)

## Score
| Type      | Score                             |
|-----------|-----------------------------------|
| Accuracy  |  {data["scores"]["accuracy"]}     |
| Precision |  {data["scores"]["precision"]}    |
| Recall    |  {data["scores"]["recall"]}       |
| F1-Score  |  {data["scores"]["f1-score"]}     |

## Confusion Matrix
![Confusion Matrix]({ROOT_DIR}/.AI_analyzer/{model_name}/confusion-matrix.png)
