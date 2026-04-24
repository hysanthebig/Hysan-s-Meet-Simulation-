import anvil.files
from anvil.files import data_files

import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import time

field_events_list = ['Shot Put', 'Discus', 'High Jump', 'Pole Vault', 'Long Jump', 'Triple Jump']
print("connected server module")

def table_into_df(sport):
  if sport == "XC":
    rows = app_tables.xc_table.search()
  if sport == "Track":
    rows = app_tables.track_table.search()
  return pd.DataFrame(rows)
  
def seconds_to_mintunes(seconds):
  mint = int(seconds // 60)
  sec = round(seconds % 60, 1)
  if sec < 10:
    sec = f"0{sec}"
  time = f"{mint}:{sec}"
  return (time)

def time_to_seconds(time):
  mintunes, seconds = time.split(":")
  mintunes = int(mintunes)
  seconds = float(seconds)
  time_seconds = mintunes*60 + seconds
  return time_seconds



def filter(df,sort_by,schoollist,lengthlist,gender):
  start = time.time()

  
  readmask = pd.Series(True, index=df.index)
  school_mask = pd.Series(False, index=df.index)
  length_mask = pd.Series(False,index = df.index)
  gender_mask = pd.Series(False,index = df.index)
    ####################Filter#######################

  school_mask = df['School'].str.lower().isin([r.lower() for r in schoollist])
  if len(schoollist) == 0:
    school_mask = pd.Series(True,index =df.index)
  
  
  length_mask = df['Length'].str.lower().isin([r.lower() for r in lengthlist])
  if len(lengthlist) == 0:
    length_mask = pd.Series(True,index =df.index)

  gender_mask = df['Gender'].str.lower() == gender.strip().lower()


  
  readmask = readmask & school_mask & length_mask & gender_mask
  
  df_filtered = df.loc[readmask]
  df_filtered = df_filtered.sort_values(by=[sort_by])
  
  
  end = time.time()
  print(f"filter {end-start:.4f}")


  
  return(df_filtered)

  

def pr_display(df,lengthlist,schoollist,gender):
  df_pr = filter(df,"Runner",schoollist,lengthlist,gender)
  if df_pr is None:
    return None
  length = lengthlist[0]

  if length in field_events_list:
    field_df = df_pr.sort_values(by = ["Time"], key = lambda x:x.str.replace("m","").str.strip().astype(float), ascending = False)
    field_pr_rows = field_df.to_dict(orient="records")
    return(field_pr_rows)    
  else:
    df_pr = df_pr.sort_values(by = ["time_seconds"])
    pr_rows = df_pr.to_dict(orient="records")
    return(pr_rows)

@anvil.server.callable
def call_pr_display(school_list,event_list,gender):
  if event_list == "XC":
    df = table_into_df("XC")
  else:
    df = table_into_df("Track")
  dfs = {event:filter(df,"Runner",school_list,[event],gender) for event in event_list}
  finished_df_dict = {event:pr_display(dfs[event],[event],school_list,gender) for event in event_list}
  return finished_df_dict

  
@anvil.server.callable
def count_events():
  events = list(dict.fromkeys([r['Length'] for r in app_tables.track_table.search()]))
  return events
  
@anvil.server.callable
def re_sort(dictionary):
  start = time.time()
  df = pd.DataFrame(dictionary)
  length = df["Length"].iloc[0]
  if length in field_events_list:
    field_df = df.sort_values(by = ["Time"], key = lambda x:x.str.replace("m","").str.strip().astype(float), ascending = False)
    field_pr_rows = field_df.to_dict(orient="records")
    return(field_pr_rows)
  else:
    df_pr = df.sort_values(by = ["time_seconds"])
    pr_rows = df_pr.to_dict(orient="records")
    end = time.time()
    print(f"resort {end-start:.4f}")
    return(pr_rows)
  
  
