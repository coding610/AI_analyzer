# Model Overview: {{ self.MODEL_NAME }}
## Table Of Contents
- [Score](##Score)
- [Confusion Matrix](##Confusion-Matrix)

## Score
{<
data = self.__get_current_data()
scores = data["scores"]
>}

| Type      | Score                         |
|-----------|-------------------------------|
| Accuracy  |  {{ scores["accuracy"]  }}    |
| Precision |  {{ scores["precision"] }}    |
| Recall    |  {{ scores["recall"]    }}    |
| F1-Score  |  {{ scores["f1-score"]  }}    |

## Confusion Matrix
![Confusion Matrix]({{ self.ROOT_DIR }}/.AI_analyzer/{{ self.MODEL_NAME }}/confusion-matrix.png)
