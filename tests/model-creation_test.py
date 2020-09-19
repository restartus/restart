import sys
import pandas as pd
sys.path.append("../restart")
from restart import RestartModel
from restart.model import Model
from restart.util import set_config

ps = RestartModel(config_dir="../config/wa_groups", data_dir="../../data/ingestion", population="oes", state="Washington", subpop="wa_groupings")
model = ps.model

def test_ps_creation():
    assert type(ps) == RestartModel

def test_model_creation():
    assert type(model) == Model