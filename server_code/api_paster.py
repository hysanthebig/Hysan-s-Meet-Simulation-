import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42

#tables include "trac"
selected_table = "track_table"


field_events_list = ['Shot Put', 'Discus', 'High Jump', 'Pole Vault', 'Long Jump', 'Triple Jump']

def field_event(length):
  if ("m") in length:
    return length
  elif ("'") in length:
    feet,inches = length.split("'")
    total_inches = float(feet)*12 + float(inches.replace('"',""))
    meters = round(total_inches*0.0254,2)
    return f"{meters}m"
  elif ("-") in length:
    feet,inches = length.split("-")
    total_inches = float(feet)*12 + float(inches)
    meters = round(total_inches*0.0254,2)
    return f"{meters}m"

def time_to_seconds(time_str):
  try:
    if float(time_str) < 60:
      return float(time_str)
  except ValueError:
    try:
      minutes, seconds = time_str.split(":")
      return int(minutes) * 60 + float(seconds)
    except ValueError:
      return None








def load_data():
  import json
  import pandas as pd
  
  def parse(raw_json, school):
    rows = []
  
    for d in raw_json["eventRecords"]:
      rows.append([
        school,
        f"{d['FirstName']} {d['LastName']}",
        "Female" if d["Gender"] == "F" else "Male",
        d["GradeID"],
        d["MeetName"],
        d["Result"].replace("a",""),
        d["Event"],
        d["EndDate"].replace("T00:00:00","")
      ])
  
    return rows
  
  
  all_rows = []
  
  print("\nPaste full JSON blocks below.")
  print("Type 'Done' when finished.\n")
  
  school_count = 1
  
  while True:
    raw = input(f"[Input {school_count}] > ")
  
    if raw.strip().lower() == "done":
      break
  
    try:
      data = json.loads(raw)
    except Exception as e:
      print("Invalid JSON. Try again.")
      continue
  
    school = input("School name: ")
  
    all_rows.extend(parse(data, school))
  
    print("Added.\n")
    school_count += 1
  
  
  df = pd.DataFrame(all_rows, columns=[
    "School","Runner","Gender","Grade","Race","Time","Length","Date"
  ])
  
  df.to_csv("athletic_net.csv", index=False)
  
  print("\nSaved athletic_net.csv")

  ########

  df["time_seconds"] = df["Time"].apply(time_to_seconds)
  
  print("DF Located")
  for _, row in df.iterrows():
    row= {k:(None if pd.isna(v) else v) for k,v in row.items()}
    if row["Length"] in field_events_list:
      measured_result = row["Time"]
      row["Time"] = field_event(measured_result)
  
    app_tables.selected_table.add_row(
      School = row["School"],Runner=row["Runner"],Race=row["Race"],Grade=row["Grade"],Gender = row['Gender'],Time=row["Time"],Date=row["Date"],Length=row["Length"],time_seconds = row["time_seconds"])
    print("Completed")
  return "Done"