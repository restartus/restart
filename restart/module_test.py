"""Tester for main model module."""

from restart.restart import RestartModel

if __name__ == "__main__":
    oes_test = RestartModel(
        configdir="restart", population="oes", state="California"
    )
    dict_test = RestartModel(configdir="restart", population="dict")
