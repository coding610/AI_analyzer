# Model Overview: {{ self.MODEL_NAME }}
## Table Of Contents
- [Score](##Score)
- [Confusion Matrix](##Confusion-Matrix)

## Score
| Type      | Score                                                     |
|-----------|-----------------------------------------------------------|
| Accuracy  |  {{ self.__get_current_data()["scores"]["accuracy"]  }}   |
| Precision |  {{ self.__get_current_data()["scores"]["precision"] }}   |
| Recall    |  {{ self.__get_current_data()["scores"]["recall"]    }}   |
| F1-Score  |  {{ self.__get_current_data()["scores"]["f1-score"]  }}   |

## Confusion Matrix
![Confusion Matrix]({{ self.ROOT_DIR }}/.AI_analyzer/{{ self.MODEL_NAME }}/confusion-matrix.png)
