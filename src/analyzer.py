import os
import re
import json
from typing import Optional
import rich

from matplotlib import pyplot as plt
import numpy as np

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, f1_score, precision_score, recall_score

class Analyzer:
    def __init__(self, root_dir: str = ".") -> None:
        expanded_path = os.path.expanduser(root_dir)
        self.ROOT_DIR = expanded_path if expanded_path != root_dir else os.path.abspath(root_dir)

        self.MODEL_NAME: str = ""

    ##########################
    ## COMPARISONS          ##
    ##########################
    def compare_models(
        self,
        model_name1: str,
        model_name2: str,
        overwrite: bool = False
    ):
        if not os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/comparisons"):
            os.system(f"mkdir   {self.ROOT_DIR}/.AI_analyzer/comparisons")
        if not overwrite and os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/comparisons/{model_name1}-{model_name2}-comparison.md"):
            raise Exception(f"Error: Trying to overwrite comparison {model_name1}-{model_name2}, but overwrite parameter is set to false.")

        with open(f"{self.ROOT_DIR}/.AI_analyzer/comparisons/{model_name1}-{model_name2}-comparison.md", "w") as f:
            with open(f"{self.ROOT_DIR}/templates/comparison.md", "r") as layout:
                f.write(
                    re.sub(
                        r'\{data\["([^"]+)"\]\["([^"]+)"\]\}',
                        self.__replace_placeholders,
                        string=layout.read()
                        .replace("{model_name1}", model_name1)
                        .replace("{model_name2}", model_name2)
                        .replace("{ROOT_DIR}", os.path.relpath(self.ROOT_DIR, f"{self.ROOT_DIR}/.AI_analyzer/comparisons"))
                    )
                )

    ##########################
    ## OVERVIEW             ##
    ##########################
    def model_overview(
        self,
        y_true: np.ndarray | list,
        y_pred: np.ndarray | list,
        labels: list[str],
        model_name: str,
        plot_metrics: bool = False,
        include_scores: bool = True,
        include_confusion_matrix: bool = True,
        overwrite: bool = False # When enabled, it overwrites the model analyzation folder if it exists
    ):
        self.MODEL_NAME = model_name;

        if os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}"):
            if overwrite:
                os.system(f"rm -r {self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}")
                os.system(f"mkdir {self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}")
            else:
                raise Exception(f"Error: Trying to overwrite model {self.MODEL_NAME}, but overwrite parameter is set to false.")
        else:
            os.system(f"mkdir {self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}")

        if not os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer"):
            os.system(f"mkdir   {self.ROOT_DIR}/.AI_analyzer")
        if not os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json"):
            os.system(f"touch {self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json")

        if include_scores: self.__write_scores(y_true, y_pred, plot_metrics)
        if include_confusion_matrix: self.__write_confusion_matrix(y_true, y_pred, labels, plot_metrics)

        # Because markdown is best treated with relative paths,
        # so we do this shinaniganse
        with open(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/result.md", "w") as f:
            with open(f"{self.ROOT_DIR}/templates/overview.md", "r") as layout:
                f.write(
                    re.sub(
                        r'\{data\["([^"]+)"\]\["([^"]+)"\]\}',
                        self.__replace_placeholders,
                        string=layout.read()
                            .replace("{model_name}", self.MODEL_NAME)
                            .replace("{ROOT_DIR}", os.path.relpath(self.ROOT_DIR, f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}"))
                    )
                )

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
        if not plot: plt.ioff()

        conf_matrix = confusion_matrix(y_true, y_pred)
        ConfusionMatrixDisplay(
            confusion_matrix = conf_matrix,
            display_labels   = labels
        ).plot(cmap="copper")

        plt.savefig(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/confusion-matrix.png")

        if not plot: plt.ion()

        # int(...) because its int64 (numpy int)
        self.__dump_json({
            "confusion-matrix": {
                "0-0": int(conf_matrix[0][0]),
                "0-1": int(conf_matrix[0][1]),
                "1-0": int(conf_matrix[1][0]),
                "1-1": int(conf_matrix[1][1])
            }
        })

    def __write_scores(self, y_true: np.ndarray | list, y_pred: np.ndarray | list, plot: bool) -> None:
        self.__dump_json({
            "scores": {
                "accuracy": round(accuracy_score(y_true, y_pred), 3),
                "precision": round(precision_score(y_true, y_pred), 3),
                "recall": round(recall_score(y_true, y_pred), 3),
                "f1-score": round(f1_score(y_true, y_pred), 3)
            }
        }, plot, "scores")

    ##########################
    ## UTILITIES            ##
    ##########################
    def __dump_json(self, new_data: dict, print_data: bool = False, key: str = ""):
        if print_data:
            print(json.dumps(new_data, indent=4, default=str))

        with open(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json", "r+") as f:
            if f.read() == "":
                f.seek(0)
                json.dump(new_data, f, indent=4)
                return

            f.seek(0)
            data = json.load(f)

        data.update(new_data)
        with open(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json", "w") as f:
            json.dump(data, f, indent=4)

    def __replace_placeholders(self, match):
        keys = match.groups()
        value = self.__get_current_data() 
        for key in keys:
            value = value.get(key, '')
        return str(value)

    def __get_current_data(self):
        with open(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json", "r") as f:
            return json.loads(f.read())
