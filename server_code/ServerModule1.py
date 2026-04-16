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
def tabler(rows):
  data_list = []
  try:
    for r in rows:
      data_list.append({
        "Runner": r["Runner"],
        "Race": r["Race"],
        "Grade": r["Grade"],
        "Date":r["Date"],
        "Time":r["Time"],
        "time_seconds":r["time_seconds"],
        "Length":r["Length"],
        "School":r['School'],
        "Gender":r['Gender']
      })
    df = pd.DataFrame(data_list)
    return df
  except TypeError:
    print("1")

def table_into_df(sport):
  if sport == "XC":
    rows = app_tables.datatable.search()
  if sport == "Track":
    rows = app_tables.athletic_table.search()
  return tabler(rows)
  
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


@anvil.server.callable
def filter(sport,sort_by,runnerlist,schoollist,gradelist,lengthlist,gender):
  start = time.time()
  df = table_into_df(sport)
  print(gender)
  
  readmask = pd.Series(True, index=df.index)
  runner_mask = pd.Series(False, index=df.index)
  school_mask = pd.Series(False, index=df.index)
  grade_mask = pd.Series(False, index = df.index)
  length_mask = pd.Series(False,index = df.index)
  gender_mask = pd.Series(False,index = df.index)
    ####################Filter#######################
  runner_mask = df["Runner"].str.lower().isin([r.lower() for r in runnerlist])
  if len(runnerlist) == 0:
    runner_mask = pd.Series(True,index =df.index)
  
  school_mask = df['School'].str.lower().isin([r.lower() for r in schoollist])
  if len(schoollist) == 0:
    school_mask = pd.Series(True,index =df.index)
  
  grade_mask = df['Grade'].astype(str).isin([r.lower() for r in gradelist])
  if len(gradelist) == 0:
    grade_mask = pd.Series(True,index =df.index)
  
  length_mask = df['Length'].str.lower().isin([r.lower() for r in lengthlist])
  if len(lengthlist) == 0:
    length_mask = pd.Series(True,index =df.index)

  gender_mask = df['Gender'].str.lower() == gender.strip().lower()


  
  readmask = readmask & runner_mask & school_mask & grade_mask & length_mask & gender_mask
  
  df_filtered = df.loc[readmask]
  df_filtered = df_filtered.sort_values(by=[sort_by])
  df_filtered =df_filtered.to_dict(orient="records")
  print(df_filtered)
  
  
  end = time.time()
  print(f"filter {end-start:.4f}")

  if not df_filtered:
    return None
  
  return(df_filtered)

  

@anvil.server.callable
def pr_display(sport,runnerlist,lengthlist,gradelist,schoollist,gender):
  filitered_df = filter(sport,"Runner",runnerlist,schoollist,gradelist,lengthlist,gender)
  if filitered_df is None:
    return None
  df_pr = tabler(filitered_df)
  if lengthlist in field_events_list:
    field_df = df_pr.sort_values(by = ["Time"], key = lambda x:x.str.replace("m","").astype(float), Ascending = True)
    print(field_df)
    field_pr_rows = field_df.drop(columns = ['time_seconds']).to_dict(orient="records")
    return(field_pr_rows)    
  else:
    df_pr = df_pr.sort_values(by = ["time_seconds"])
    pr_rows = df_pr.drop(columns = ['time_seconds']).to_dict(orient="records")
    return(pr_rows)


@anvil.server.callable
def count_events():
  events = list(dict.fromkeys([r['Length'] for r in app_tables.athletic_table.search()]))
  return events
  

