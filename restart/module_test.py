"""Tester for main model module."""

from restart.restart import RestartModel

if __name__ == "__main__":
    oes_test = RestartModel(
        config_dir="restart", population="oes", state="California"
    )
    dict_test = RestartModel(config_dir="restart", population="dict")
