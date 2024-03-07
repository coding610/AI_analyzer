
import os
import json
from typing import Optional

from IPython.display import Markdown
from matplotlib import pyplot as plt
import numpy as np

from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

class Analyzer:
    def __init__(self, root_dir: str = ".") -> None:
        self.ROOT_DIR = root_dir
        self.MODEL_NAME: str = ""

    ##########################
    ## COMPARISONS          ##
    ##########################
    def compare_models(
        self,
        model_name1: str,
        model_name2: str,
        view_markdown: bool = True
    ) -> Optional[Markdown]:
        with open(f"{self.ROOT_DIR}/.AI_analyzer/comparisons/{model_name1}-{model_name2}-comparison.md", "w") as f:
            with open(f"{self.ROOT_DIR}/.AI_analyzer/layouts/comparison.md", "r") as layout:
                f.write(layout.read().replace("{model_name1}", model_name1).replace("{model_name2}", model_name2))

        if not view_markdown: return 
        with open(f"{self.ROOT_DIR}/.AI_analyzer/comparisons/{model_name1}-{model_name2}-comparison.md", "w") as f:
            return Markdown(f.read())

    ##########################
    ## OVERVIEW             ##
    ##########################
    def model_overview(
        self,
        y_true: np.ndarray | list,
        y_pred: np.ndarray | list,
        labels: list[str],
        model_name: str,
        view_result: bool = True,
        plot_metrics: bool = False,
        include_report: bool = True,
        include_confusion_matrix: bool = True,
        overwrite: bool = False # When enabled, it overwrites the model analyzation folder if it exists
    ) -> Optional[Markdown]:
        self.MODEL_NAME = model_name;

        if overwrite and os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}"):
            os.system(f"rm -r {self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}")
        elif not os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}"):
            os.system(f"mkdir {self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}")

        if not os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer"):
            os.system(f"mkdir   {self.ROOT_DIR}/.AI_analyzer")
        if not os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/comparisons"):
            os.system(f"mkdir   {self.ROOT_DIR}/.AI_analyzer/comparisons")
        if not os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/.AI_analyzer/layouts"):
            self.__clone_layouts()

        if include_report: self.__write_report(y_true, y_pred)
        if include_confusion_matrix: self.__write_confusion_matrix(y_true, y_pred, labels, plot_metrics)

        with open(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/result.md", "w") as f:
            with open(f"{self.ROOT_DIR}/.AI_analyzer/layouts/overview.md", "r") as layout:
                f.write(layout.read().replace("{model_name}", self.MODEL_NAME))

        if not view_result: return
        with open(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/result.md", "r") as f:
            return Markdown(f.read())

    ##########################
    ## METRICS              ##
    ##########################
    def __write_confusion_matrix(
        self,
        y_true: np.ndarray | list,
        y_pred: np.ndarray | list,
        labels: list[str],
        plot: bool
    ) -> None:
        conf_matrix = confusion_matrix(y_true, y_pred)
        ConfusionMatrixDisplay(
            confusion_matrix = conf_matrix,
            display_labels   = labels
        ).plot(cmap="copper")

        if not plot: plt.ioff()
        plt.savefig(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/confusion-matrix.png")
        if not plot: plt.ion()

        self.__dump_json({
            "confusion-matrix": {
                "0-0": str(conf_matrix[0][0]),
                "0-1": str(conf_matrix[0][1]),
                "1-0": str(conf_matrix[1][0]),
                "1-1": str(conf_matrix[1][1])
            }
        })

    def __write_report(
        self,
        y_true: np.ndarray | list,
        y_pred: np.ndarray | list
    ) -> None:
        self.__dump_json({
            "report": classification_report(y_true, y_pred)
        })

    ##########################
    ## UTILITIES            ##
    ##########################
    def __dump_json(self, new_data: dict):
        with open(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json", "w+") as f:
            if f.read() == "":
                json.dump(new_data, f, indent=4)
                return

            data = json.load(f)

        data.update(new_data)
        with open(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def __clone_layouts(self):
        os.system(f"git clone https://github.com/coding610/AI_analyzer {self.ROOT_DIR}/.AI_analyzer/repo")
        os.system(f"mv {self.ROOT_DIR}/.AI_analyzer/repo/.AI_analyzer/layouts {self.ROOT_DIR}/.AI_analyzer")
        os.system(f"rm -rf {self.ROOT_DIR}/.AI_analyzer/repo")
