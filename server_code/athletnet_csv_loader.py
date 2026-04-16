import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
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
#
pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)
pd.set_option('display.max_rows',None)

#untested
field_events_list = ['Shot Put', 'Discus', 'High Jump', 'Pole Vault', 'Long Jump', 'Triple Jump']
@anvil.server.callable
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


@anvil.server.background_task
def import_csf_to_table():
  with anvil.files.data_files.open("athletic_net.csv") as f:
    df = pd.read_csv(f)
    print(df.head(1))
    df["time_seconds"] = df["Time"].apply(time_to_seconds)
    
  print("DF Located")
  for _, row in df.iterrows():
    row= {k:(None if pd.isna(v) else v) for k,v in row.items()}
    if row["Length"] in field_events_list:
      measured_result = row["Time"]
      row["Time"] = field_event(measured_result)

    app_tables.athletic_table.add_row(
      School = row["School"],Runner=row["Runner"],Race=row["Race"],Grade=row["Grade"],Gender = row['Gender'],Time=row["Time"],Date=row["Date"],Length=row["Length"],time_seconds = row["time_seconds"])
  print("Completed")
  return "Done"

@anvil.server.callable
def import_csv_caller():
  anvil.server.launch_background_task("import_csf_to_table")