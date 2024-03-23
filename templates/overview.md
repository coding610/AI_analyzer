# Model Overview: {{ self.MODEL_NAME }}
## Table Of Contents
{% if params["include_scores"] %} - [Score](##Score) {% endif %}
{% if params["include_confusion_matrix"] %} - [Confusion Matrix](##Confusion-Matrix) {% endif %}

{% if params["include_scores"] %}
## Score
{< scores = self.__get_current_data()["scores"] >}
| Type      | Score                         |
|-----------|-------------------------------|
| Accuracy  |  {{ scores["accuracy"]  }}    |
| Precision |  {{ scores["precision"] }}    |
| Recall    |  {{ scores["recall"]    }}    |
| F1-Score  |  {{ scores["f1-score"]  }}    |
{% endif %}

{% if params["include_confusion_matrix"] %}
## Confusion Matrix
![Confusion Matrix]({{ self.ROOT_DIR }}/.AI_analyzer/{{ self.MODEL_NAME }}/confusion-matrix.png)
{% endif %}
