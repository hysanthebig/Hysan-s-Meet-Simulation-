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