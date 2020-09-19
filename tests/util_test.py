import sys
import pandas as pd
import confuse
from confuse import Configuration
from ipysheet import Sheet
sys.path.append("../restart")
from restart import RestartModel
from restart.model import Model
from restart.util import *

ps = RestartModel(config_dir="../config/wa_groups", data_dir="../../data/ingestion", population="oes", state="Washington", subpop="wa_groupings")
model = ps.model
sample_df = pd.DataFrame(data=[[0, 1],[2, 3]], index=["i", "ii"], columns=["one", "two"])
# print(set_dataframe(sample_df.values, label=["test1", "test2"], index=sample_df.index, columns=sample_df.columns))
print(type(to_sheet(sample_df)))

def test_set_config():
    assert type(set_config("./config/wa_groups")) == Configuration

def test_is_dir_or_file():
    assert is_dir_or_file("notafile") == False
    assert is_dir_or_file("../config/wa_groups") == True
    assert is_dir_or_file("../restart/restart.py") == True
    assert is_dir_or_file(".") == True
    assert is_dir_or_file("..") == True
    assert is_dir_or_file(":invalidcharacter:") == False

def test_set_dataframe():
    assert set_dataframe(sample_df.values, index=sample_df.index, columns=sample_df.columns)

def test_to_sheet():
    assert type(to_sheet(sample_df)) == Sheet