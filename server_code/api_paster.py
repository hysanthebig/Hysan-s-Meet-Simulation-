import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json
import pandas as pd

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









  
def parse(sport,raw_json, school):
    rows = []

    if sport == "Track":
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
    elif sport == "XC":
      for d in raw_json["results"]:
        rows.append([
          school,
          f"{d['FirstName']} {d['LastName']}",
          "Female" if d["GenderID"] == "F" else "Male",
          d["ShortDesc"],
          d["MeetName"],
          d["Result"].replace("a",""),
          d["Distance"],
          d["MeetDate"].replace("T00:00:00","")
        ])
      
    

    return rows
  


@anvil.server.callable
def load_data(sport,data,school,all_rows):
    data = json.loads(data)
    all_rows.extend(parse(sport,data, school))
    return(all_rows)


  
  
@anvil.server.callable
def rows_into_table(all_rows,sport):
  df = pd.DataFrame(all_rows, columns=[
    "School","Runner","Gender","Grade","Race","Time","Length","Date"
  ])
  sport = sport.lower().strip()
  print(df)

  df.to_csv("athletic_net.csv", index=False)

  print("\nSaved athletic_net.csv")

  df["time_seconds"] = df["Time"].apply(time_to_seconds)
  
  print("DF Located")
  for _, row in df.iterrows():
    row= {k:(None if pd.isna(v) else v) for k,v in row.items()}
    if row["Length"] in field_events_list:
      measured_result = row["Time"]
      row["Time"] = field_event(measured_result)
    if sport == "xc":
      app_tables.xc_table.add_row(
        School = row["School"],Runner=row["Runner"],Race=row["Race"],Grade=row["Grade"],Gender = row['Gender'],Time=row["Time"],Date=row["Date"],Length=str(row["Length"]),time_seconds = row["time_seconds"])
    elif sport == "track":
      app_tables.track_table.add_row(
        School = row["School"],Runner=row["Runner"],Race=row["Race"],Grade=row["Grade"],Gender = row['Gender'],Time=row["Time"],Date=row["Date"],Length=row["Length"],time_seconds = row["time_seconds"])
  return "Done"