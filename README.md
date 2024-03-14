# AI Analyzer
## Description
Easily analyze and compare models result with this python libary.
Its in heavy beta right now, so no docs or really no help at all!
All of the results are saved as markdown files in the .AI_analyzer directory.
Look at the example .AI_analyzer for more information on what is stored where.

## Why?
This is mainly for comparing results of AI models.
When I work with AI, I find myself wondering "Wait, was this models result really better than before?"
I started saving the images plotted in my notebook but it was really just a pain.
This allows you to easily compare models. This also comes with a nice way
of seeing results, so its really no need for individual plotting of confusion matrixes
or scores when using this libary.

## How?
It isn't hard to implement this kind of stuff, and there is 100% 
a libary out there that does the same thing. But for this I had
some fun with this. I created template markdown files that has my own
python integration with it. Its able to connect to a class and
get all of its members and methods and spit it out into the file. Its pretty cool!
To have a closer look, take a look at the templates folder.

## Example Usage
```python
import analyzer

# Relative or absolute root directory.
# The Root directory is basically where
# the .AI_analyzer folder will be saved
analyzer = Analyzer(root_dir="..")

analyzer.model_overview(
    y_test, y_pred, labels,
    model_name="1.0",
    # When using a jupyter notebook,
    # metrics can be ploted to the output,
    # such as the confusion matrix.
    plot_metrics=True,              
    include_confusion_matrix=False
)
```

You could also compare models with this command
```python
analyzer.compare_models("1.0", "1.1", overwrite=True)
```

## Example Results
Note that the results will of course depend on your own models
result. This is just an arbetary example models result.

The first usage example will result in this type of markdown file
<div style="border: 1px solid #2f3044; padding: 20px;">

# Model Overview: 1.0
## Table Of Contents
- [Score](##Score)
- [Confusion Matrix](##Confusion-Matrix)

## Score
| Type      | Score                         |
|-----------|-------------------------------|
| Accuracy  |  0.962    |
| Precision |  0.962    |
| Recall    |  0.965    |
| F1-Score  |  0.964    |

## Confusion Matrix
![Confusion Matrix](./.AI_analyzer/1.0/confusion-matrix.png)

</div>

The second usage example will result in this type of markdown file
> **_NOTE:_**  The two model that this is comparing is the same
<div style="border: 1px solid #2f3044; padding: 20px;">

# Model Comparison: 1.0 and 1.1 
## Table Of Contents
- [Score](##Score-Comparison)
- [Confusion Matrix Comparison](##Confusion-Matrix-Comparison)

## Score Comparison


| Type      | Score 1.0          | Score 1.1          | Offset                                              |
|-----------|-----------------------------|-----------------------------|-----------------------------------------------------|
| Accuracy  | 0.962 | 0.962 | 0.0 |
| Precision | 0.962 | 0.962 | 0.0 |
| Recall    | 0.965 | 0.965 | 0.0 |
| F1-Score  | 0.964 | 0.964 | 0.0 |

## Confusion Matrix Comparison
Model 1.0                                                      | Model 1.1
:----------------------------------------------------------------------:|:--------------------------------------------------------------:
![](./.AI_analyzer/1.0/confusion-matrix.png) | ![](./.AI_analyzer/1.1/confusion-matrix.png)

</div>

## Future Features
- Custom templates
- Custom metrics
- Show individual metrics
- More metrics!
