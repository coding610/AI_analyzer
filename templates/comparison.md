[//]: # (This is a comment)

# Model Comparison: {model_name1} and {model_name2} 
## Table Of Contents
- [Score](##Score-Comparison)
- [Confusion Matrix Comparison](##Confusion-Matrix-Comparison)


## Score Comparison
| Type      | Score {model_name1}               | Score {model_name2}               | Offset
|-----------|-----------------------------------|-----------------------------------|--------
| Accuracy  | {{ self.__get_current_data["scores"]["accuracy"]  }} | {{ self.__get_current_data["scores"]["accuracy"]}    | 
| Precision | {{ self.__get_current_data["scores"]["precision"] }} | {{ self.__get_current_data["scores"]["precision"]}   |
| Recall    | {{ self.__get_current_data["scores"]["recall"]    }} | {{ self.__get_current_data["scores"]["recall"]}      |
| F1-Score  | {{ self.__get_current_data["scores"]["f1-score"]  }} | {{ self.__get_current_data["scores"]["f1-score"]}    |

## Confusion Matrix Comparison
Model {model_name1}                                             | Model {model_name2}
:--------------------------------------------------------------:|:--------------------------------------------------------------:
![]({ROOT_DIR}/.AI_analyzer/{model_name1}/confusion-matrix.png) | ![]({ROOT_DIR}/.AI_analyzer/{model_name2}/confusion-matrix.png)
