# AI Analyzer
## Description
Easily analyze and compare models result with this python libary.
All of the results will be saved in a markdown file in the directory .AI_analyzer/{modelname}.md
or .AI_analyzer/comparisons/{modelname1}-{modelname2}-comparison.md
Customize what metrics will be used (confusion matrix, score etc.)
Its in heavy beta right now, so no docs or really no help

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
    plot_metrics=True,
    include_confusion_matrix=False
)
```

You could also compare models with this command
```python
analyzer.compare_models("1.0", "1.1", overwrite=True)
```

## Example Results


## Future Features
- Custom templates
- Custom metrics
