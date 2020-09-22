"""Tester for main model module."""

from restart.restart import RestartModel

if __name__ == "__main__":
    oes_test = RestartModel(population="oes", state="California")
    dict_test = RestartModel(population="dict")
