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

def tabler(rows):
  data_list = []
  for r in rows:
    data_list.append({
      "Runner": r["Runner"],
      "Race": r["Race"],
      "Grade": r["Grade"],
      "Placement":r["Placement"],
      "Date":r["Date"],
      "Date_dt":r["Date_dt"],
      "Time":r["Time"],
      "time_seconds":r["time_seconds"],
      "Length":r["Length"],
      "Avr_splits":r['Avr_splits']
    })
  df = pd.DataFrame(data_list)
  return df

def table_into_df(sport):
  if sport == "XC":
    rows = app_tables.datatable.search()
  if sport == "Track":
    rows = app_tables.track_table.search()
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
def filter(sport,sort_by,runnerlist,racelist,gradelist,lengthlist):
  start = time.time()
  df = table_into_df(sport)

  readmask = pd.Series(True, index=df.index)
  runner_mask = pd.Series(False, index=df.index)
  race_mask = pd.Series(False, index=df.index)
  grade_mask = pd.Series(False, index = df.index)
  length_mask = pd.Series(False,index = df.index)
  ####################Filter#######################
  runner_mask = df["Runner"].str.lower().isin([r.lower() for r in racelist])
  if len(runnerlist) == 0:
    runner_mask = pd.Series(True,index =df.index)

  race_mask = df['Race'].str.lower().isin([r.lower() for r in racelist])
  if len(racelist) == 0:
    race_mask = pd.Series(True,index =df.index)

  grade_mask = df['Grade'].astype(str).isin([r.lower() for r in gradelist])
  if len(gradelist) == 0:
    grade_mask = pd.Series(True,index =df.index)

  length_mask = df['Length'].str.lower().isin([r.lower() for r in lengthlist])
  if len(lengthlist) == 0:
    length_mask = pd.Series(True,index =df.index)

  readmask = readmask & runner_mask & race_mask & grade_mask & length_mask

  df_filtered = df.loc[readmask]
  df_filtered = df_filtered.sort_values(by=[sort_by])
  df_filtered =df_filtered.to_dict(orient="records")


  end = time.time()
  print(f"filter {end-start:.4f}")

  return(df_filtered)

def pr_display(sport,runnerlist,lengthlist,gradelist):
  filitered_df = filter(sport,"Runner",runnerlist,[],gradelist,lengthlist)
  df_pr = tabler(filitered_df)
  df_pr = df_pr.sort_values(by = ["time_seconds"])
  pr_df = df_pr.groupby("Runner")['time_seconds'].min().copy()
  pr_rows = df_pr[df_pr["time_seconds"] == df_pr["Runner"].map(pr_df)]
  pr_rows = pr_rows.drop(columns = ['time_seconds','Date_dt']).to_dict(orient="records")
  return(pr_rows)
