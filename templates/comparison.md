{< MNAME1 = params["model_name1"] >}
{< MNAME2 = params["model_name2"] >}

# Model Comparison: {{ MNAME1 }} and {{ MNAME2 }} 
## Table Of Contents
- [Score](##Score-Comparison)
- [Confusion Matrix Comparison](##Confusion-Matrix-Comparison)

{% if self.__get_data(params["model_name1"]) is not None and self.__get_data(params["model_name1"]) is not None %}

## Score Comparison
{< scoresm1 = self.__get_data(params["model_name1"])["scores"] >}
{< scoresm2 = self.__get_data(params["model_name2"])["scores"] >}
| Type      | Score {{ MNAME1 }}          | Score {{ MNAME2 }}          | Offset                                              |
|-----------|-----------------------------|-----------------------------|-----------------------------------------------------|
| Accuracy  | {{ scoresm1["accuracy"]  }} | {{ scoresm2["accuracy"]  }} | {{ scoresm1["accuracy"]  - scoresm2["accuracy"]  }} |
| Precision | {{ scoresm1["precision"] }} | {{ scoresm2["precision"] }} | {{ scoresm1["precision"] - scoresm2["precision"] }} |
| Recall    | {{ scoresm1["recall"]    }} | {{ scoresm2["recall"]    }} | {{ scoresm1["recall"]    - scoresm2["recall"]    }} |
| F1-Score  | {{ scoresm1["f1-score"]  }} | {{ scoresm2["f1-score"]  }} | {{ scoresm1["f1-score"]  - scoresm2["f1-score"]  }} |

{% endif %}

## Confusion Matrix Comparison
Model {{ MNAME1 }}                                                      | Model {{ MNAME2 }}
:----------------------------------------------------------------------:|:--------------------------------------------------------------:
![]({{ self.ROOT_DIR }}/.AI_analyzer/{{ MNAME1 }}/confusion-matrix.png) | ![]({{ self.ROOT_DIR }}/.AI_analyzer/{{ MNAME2 }}/confusion-matrix.png)
