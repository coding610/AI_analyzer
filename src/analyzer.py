import os
import json
import copy

import connectMD

from matplotlib import pyplot as plt
import numpy as np

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score, f1_score, precision_score, recall_score

class Analyzer:
    def __init__(self, root_dir: str = ".") -> None:
        expanded_path = os.path.expanduser(root_dir)
        self.STABLE_ROOT_DIR = expanded_path if expanded_path != root_dir else os.path.abspath(root_dir)
        self.ROOT_DIR = copy.deepcopy(self.STABLE_ROOT_DIR)

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

        # self.ROOT_DIR = os.path.relpath(self.STABLEROOT_DIR, f"{self.AROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}")
        # with open(f"{self.ROOT_DIR}/.AI_analyzer/comparisons/{model_name1}-{model_name2}-comparison.md", "w") as f:
        #     with open(f"{self.ROOT_DIR}/templates/comparison.md", "r") as layout:
        #         f.write(layout.read())

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
        self.__check_validility(model_name, overwrite)
        self.MODEL_NAME = model_name;

        if include_scores: self.__write_scores(y_true, y_pred, plot_metrics)
        if include_confusion_matrix: self.__write_confusion_matrix(y_true, y_pred, labels, plot_metrics)

        self.ROOT_DIR = os.path.relpath(self.STABLE_ROOT_DIR, f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}")
        connection = connectMD.MDConnection(
            target_class=self,
            target_members=connectMD.getmembers(self),
            read_file=f"{self.STABLE_ROOT_DIR}/templates/overview.md",
            write_file=f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/result.md"
        )
        connection.connect()
        self.ROOT_DIR = copy.deepcopy(self.STABLE_ROOT_DIR)

    ##########################
    ## HELPERS              ##
    ##########################
    def __check_validility(self, model_name, overwrite):
        if os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/{model_name}"):
            if overwrite:
                os.system(f"rm -r {self.ROOT_DIR}/.AI_analyzer/{model_name}")
                os.system(f"mkdir {self.ROOT_DIR}/.AI_analyzer/{model_name}")
            else:
                raise Exception(f"Error: Trying to overwrite model {model_name}, but overwrite parameter is set to false.")
        else:
            os.system(f"mkdir {self.ROOT_DIR}/.AI_analyzer/{model_name}")

        if not os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer"):
            os.system(f"mkdir   {self.ROOT_DIR}/.AI_analyzer")
        if not os.path.exists(f"{self.ROOT_DIR}/.AI_analyzer/{model_name}/data.json"):
            os.system(f"touch {self.ROOT_DIR}/.AI_analyzer/{model_name}/data.json")

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
                "accuracy": str(round(accuracy_score(y_true, y_pred), 3)),
                "precision": str(round(precision_score(y_true, y_pred), 3)),
                "recall": str(round(recall_score(y_true, y_pred), 3)),
                "f1-score": str(round(f1_score(y_true, y_pred), 3))
            }
        }, plot, "scores")

    ##########################
    ## UTILITIES            ##
    ##########################
    def __dump_json(self, new_data: dict, print_data: bool = False, key: str = ""):
        if print_data:
            print(json.dumps(new_data[key], indent=4, default=str))

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

    def __get_current_data(self):
        with open(f"{self.ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json", "r") as f:
            return json.loads(f.read())
