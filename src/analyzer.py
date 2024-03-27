import os
import json
import copy

import connectMD
import utils

from matplotlib import pyplot as plt
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    log_loss,
    mean_absolute_error,
    mean_absolute_percentage_error,
    precision_score,
    r2_score,
    recall_score,
    f1_score,
    mean_squared_error,
    ConfusionMatrixDisplay,
    confusion_matrix,
    RocCurveDisplay,
    roc_curve,
    auc,
    PrecisionRecallDisplay,
    root_mean_squared_error
)

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
    ) -> None:
        self.ROOT_DIR = os.path.relpath(self.STABLE_ROOT_DIR, f"{self.STABLE_ROOT_DIR}/comparisons/{model_name1}-{model_name2}.md")

        if not os.path.exists(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/comparisons"):
            os.system(f"mkdir   {self.STABLE_ROOT_DIR}/.AI_analyzer/comparisons")
        if not overwrite and os.path.exists(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/comparisons/{model_name1}-{model_name2}.md"):
            raise Exception(f"Error: Trying to overwrite comparison \"{model_name1}-{model_name2}\", but overwrite parameter is set to false.")

        connectMD.MDConnection(
            target_class=self,
            target_members=connectMD.getmembers(self, locals(), "params"),
            read_file=f"{self.STABLE_ROOT_DIR}/templates/comparison.conmd",
            write_file=f"{self.STABLE_ROOT_DIR}/.AI_analyzer/comparisons/{model_name1}-{model_name2}.md",
            connect=True
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
        metrics_size: tuple[int, int] = (8, 8),
        include_scores: bool = True,
        include_confusion_matrix: bool = True,
        include_roc_curve: bool = True,
        include_precision_recall_curve: bool = True,
        include_residual_plot: bool = True,
        overwrite: bool = False # When enabled, it overwrites the model analyzation folder if it exists
    ):
        self.MODEL_NAME = model_name;
        self.ROOT_DIR = os.path.relpath(self.STABLE_ROOT_DIR, f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}")

        self.__check_validility(model_name, overwrite)

        if include_scores: self.__write_scores(y_true, y_pred, plot_metrics)
        if include_confusion_matrix: self.__write_confusion_matrix(y_true, y_pred, labels, plot_metrics, metrics_size)
        if include_roc_curve: self.__write_roc_curve(y_true, y_pred, plot_metrics, metrics_size)
        if include_precision_recall_curve: self.__write_precision_recall_curve(y_true, y_pred, plot_metrics, metrics_size)
        if include_residual_plot: self.__write_residual_plot(y_true, y_pred, plot_metrics, metrics_size)

        connectMD.MDConnection(
            target_class=self,
            target_members=connectMD.getmembers(self, locals(), "params"),
            read_file=f"{self.STABLE_ROOT_DIR}/templates/overview.conmd",
            write_file=f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/result.md",
            connect=True
        )

    ##########################
    ## HELPERS              ##
    ##########################
    def __check_validility(self, model_name, overwrite):
        if os.path.exists(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{model_name}"):
            if overwrite:
                os.system(f"rm -r {self.STABLE_ROOT_DIR}/.AI_analyzer/{model_name}")
                os.system(f"mkdir {self.STABLE_ROOT_DIR}/.AI_analyzer/{model_name}")
            else:
                raise Exception(f"Error: Trying to overwrite model {model_name}, but overwrite parameter is set to false.")
        else:
            os.system(f"mkdir {self.STABLE_ROOT_DIR}/.AI_analyzer/{model_name}")

        if not os.path.exists(f"{self.STABLE_ROOT_DIR}/.AI_analyzer"):
            os.system(f"mkdir   {self.STABLE_ROOT_DIR}/.AI_analyzer")
        if not os.path.exists(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{model_name}/data.json"):
            os.system(f"touch {self.STABLE_ROOT_DIR}/.AI_analyzer/{model_name}/data.json")

    ##########################
    ## METRICS              ##
    ##########################
    def __write_residual_plot(
        self,
        y_true: np.ndarray | list,
        y_pred: np.ndarray | list,
        plot_metrics: bool,
        metrics_size: tuple[int, int]
    ):
        residuals = np.subtract(y_true, y_pred)
        plt.figure(figsize=metrics_size)
        plt.scatter(y_pred, residuals, alpha=0.5)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
        plt.savefig(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/residual-plot.png")

        if not plot_metrics: plt.close()

        self.__dump_json({
            "residual-plot": { }
        })

    def __write_precision_recall_curve(
        self,
        y_true: np.ndarray | list,
        y_pred: np.ndarray | list,
        plot: bool,
        metrics_size: tuple[int, int]
    ) -> None:
        _, ax = plt.subplots(figsize=metrics_size)
        display = PrecisionRecallDisplay.from_predictions(y_true, y_pred, name="LinearSVC", plot_chance_level=True, ax=ax)
        _ = display.ax_.set_title("2-class Precision-Recall curve")

        plt.savefig(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/precision-recall-curve.png")
        if not plot: plt.close()

        self.__dump_json({
            "precision-recall-curve": { }
        })

    def __write_roc_curve(
        self,
        y_true: np.ndarray | list,
        y_pred: np.ndarray | list,
        plot: bool,
        metrics_size: tuple[int, int]
    ) -> None:
        fpr, tpr, _ = roc_curve(y_true, y_pred)
        roc_auc = auc(fpr, tpr)

        _, ax = plt.subplots(figsize=metrics_size)
        RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc).plot(ax=ax)
        plt.savefig(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/roc-curve.png")

        if not plot: plt.close()

        self.__dump_json({
            "roc-curve": {
                "fpr": list(fpr),
                "tpr": list(tpr),
                "roc_auc": float(roc_auc)
            }
        })

    def __write_confusion_matrix(self, y_true: np.ndarray | list, y_pred: np.ndarray | list, labels: list[str], plot: bool, metrics_size: tuple[int, int]) -> None:
        conf_matrix = confusion_matrix(y_true, y_pred)

        _, ax = plt.subplots(figsize=metrics_size)
        ConfusionMatrixDisplay(confusion_matrix = conf_matrix, display_labels = labels).plot(cmap="copper", ax=ax)
        plt.savefig(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/confusion-matrix.png") # semicolon here suppresses it from being shown

        if not plot: plt.close()

        # conf_matrix[x][y] is a np.float64, therefore the float(...)
        self.__dump_json({
            "confusion-matrix": {
                "0-0": float(conf_matrix[0][0]),
                "0-1": float(conf_matrix[0][1]),
                "1-0": float(conf_matrix[1][0]),
                "1-1": float(conf_matrix[1][1])
            }
        })

    def __write_scores(self, y_true: np.ndarray | list, y_pred: np.ndarray | list, plot: bool) -> None:
        self.__dump_json({
            "scores": {
                "accuracy": round(accuracy_score(y_true, y_pred), 3),
                "precision": round(precision_score(y_true, y_pred), 3),
                "recall": round(recall_score(y_true, y_pred), 3),
                "f1-score": round(f1_score(y_true, y_pred), 3),
                "MSE": round(mean_squared_error(y_true, y_pred), 3), # Average of all elements
                "MAE": round(mean_absolute_error(y_true, y_pred), 3),
                "RMSE": round(root_mean_squared_error(y_true, y_pred), 3),
                "MAPE": round(mean_absolute_percentage_error(y_true, y_pred), 3),
                "log-loss": round(log_loss(y_true, y_pred), 3),
                "R-Squared": round(r2_score(y_true, y_pred), 3), # Ignore this silly error
            }
        }, plot, "scores")

    ##########################
    ## UTILITIES            ##
    ##########################
    def __dump_json(self, new_data: dict, print_data: bool = False, key: str = ""):
        if print_data: utils.dprint(new_data[key])

        with open(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json", "r+") as f:
            if f.read() == "":
                f.seek(0)
                json.dump(new_data, f, indent=4)
                return

            f.seek(0)
            data = json.load(f)

        data.update(new_data)
        with open(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json", "w") as f:
            json.dump(data, f, indent=4)

    ##########################
    ## API FOR MD           ##
    ##########################
    # No runtime error policy for these
    def __get_current_data(self) -> dict:
        try:
            with open(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{self.MODEL_NAME}/data.json", "r") as f:
                return json.loads(f.read())
        except:
            return {}

    def __get_data(self, model_name: str) -> dict:
        try:
            with open(f"{self.STABLE_ROOT_DIR}/.AI_analyzer/{model_name}/data.json", "r") as f:
                return json.loads(f.read())
        except:
            return {}

    def __data_exists(self, data_name: str, model_name1: str, model_name2: str) -> bool:
        return data_name in self.__get_data(model_name1) and data_name in self.__get_data(model_name2)

