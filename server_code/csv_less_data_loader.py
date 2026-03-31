
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import time

print("COnnectected")
# ================= CONFIG =================
URL = "https://files.finishedresults.com/Track2026/Meets/13491-The-Qualifier.html"
SCHOOL_NAME = ["colony","san dimas","alta loma","south hills",'los altos']  # case-insensitive
table = app_tables.tracktable
SPORT = "Track"
# ==========================================


pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)
pd.set_option('display.max_rows',None)


# Helper: convert mm:ss string to total seconds
def time_to_seconds(time_str):
  try:
    if float(time_str) < 60:
      return float(time_str)
  except ValueError:
    try:
      minutes, seconds = time_str.split(":")
      return int(minutes) * 60 + float(seconds)
    except ValueError:
      print(time_str)

  # Helper: average split per distance in minutes:seconds
def avg_split(time_str, distance_meters):
    total_seconds = time_to_seconds(time_str)
    avg_sec = total_seconds / (distance_meters / 1609.34)  # convert meters to miles if needed
    minutes = int(avg_sec // 60)
    seconds = int(round(avg_sec % 60))
    return f"{minutes}:{seconds:02d}"

# ====== Parsing HTML ======
def get_html(url):
  r = requests.get(url)
  r.raise_for_status()
  return r.text

def parse_html(html):
  soup = BeautifulSoup(html, "html.parser")
  text = soup.get_text("\n")
  lines = [line.strip() for line in text.splitlines() if line.strip()]



  records = []
  current_event = None
  current_race_type = None
  current_distance = None
  current_event_number = None

  # Event header regex
  event_regex = re.compile(
    r"Event\s+(\d+)\s+(.*?)\s+(Varsity|JV|FS|Frosh/Soph)$",
    re.IGNORECASE
  )

  # Runner regex
  runner_regex = re.compile(
    r"(?P<place>\d+)\s+"
    r"(?P<name>[A-Z][a-zA-Z ,\-\(\)']+?)\s+"
    r"(?P<grade>\d{1,2})\s+"
    r"(?P<team>.+?)\s+"
    r"(?P<time>(\d+:\d+\.\d+)|(\d+.\d+))"
  )

  for line in lines:
    # Check for event header
    ev = event_regex.search(line)
    if ev:

      current_event_number = ev.group(1)
      event_name_dist = ev.group(2).strip()
      current_race_type = ev.group(3).strip() if ev.group(3) else "Unknown"
      # Extract distance (first number + Meter)
      dist_match = re.search(r"(\d+[x]?\d*\s?Meter)", event_name_dist)
      if "hurdles" in event_name_dist.lower():
        current_distance = dist_match.group(1)+" Hurdles"
      else:
        current_distance = dist_match.group(1) if dist_match else "Unknown"
      current_event = f"{current_event_number}_{current_distance}_{current_race_type}"

      continue


      # Check for runner row
    m = runner_regex.search(line)
    if m and current_event:
      if current_distance == "Unknown":
        continue
      else:
        records.append({
          "Placement": int(m.group("place")),
          "Runner": m.group("name").strip(),
          "Grade": int(m.group("grade")),
          "School": m.group("team").strip(),
          "Time": m.group("time"),
          "EventID": current_event,
          "RaceType": current_race_type,
          "Length": current_distance
        })

  df = pd.DataFrame(records)
  def flip_name(name):
    if "," in name:
      last, first = name.split(",", 1)
      return f"{first.strip()} {last.strip()}"
    return name

  df['Runner'] = df['Runner'].apply(flip_name)


  lines = [line.strip() for line in soup.get_text("\n").split("\n") if line.strip()]
  
  # Print lines with index so you can see structure
  
  # ---- ADJUST THESE AFTER YOU CHECK OUTPUT ----
  race_name = lines[1]

  month_pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December)'
  
  date_line = None
  
  for line in lines:
    if re.search(month_pattern, line):
      date_line = line
      break
  

  month_map = {
    "January": "1", "February": "2", "March": "3", "April": "4",
    "May": "5", "June": "6", "July": "7", "August": "8",
    "September": "9", "October": "10", "November": "11", "December": "12"
  }
  race_date = None
  
  if date_line:
    match = re.search(rf'{month_pattern}\s+(\d{{1,2}}),\s*(\d{{4}})', date_line)
    if match:
      month, day, year = match.groups()
      race_date = f"{month_map[month]}/{int(day)}/{year}"

  return df,race_date,race_name



  # ====== Placement / School Filter ======
def compute_school_placement(df_full, school_name):
    totals = df_full.groupby("EventID")["Placement"].max()
    df_school = df_full[df_full["School"].str.lower().isin(SCHOOL_NAME)].copy()
    df_school["Placement"] = df_school.apply(
      lambda r: f"{r['Placement']}/{totals[r['EventID']]}",
      axis=1
    )
    return df_school

# ====== Reformat Columns for CSV ======
def format_for_csv(df_school,MEET_NAME,MEET_DATE, race_distance_meters=1600):
  df = df_school.copy()
  df["Race"] = MEET_NAME
  df["Date"] = MEET_DATE
  df["Sport"] = SPORT

  df["Date_dt"] = pd.to_datetime(df["Date"])
  df["time_seconds"] = df["Time"].apply(time_to_seconds)


  # Reorder columns
  df = df[["School","Runner", "Race", "Placement", "Grade", "Time"
           , "Date", "Length", "RaceType", "Sport",
           "Date_dt", "time_seconds"]]


  return df


#######################++++++++++++++++++++++++++++++++++++++++++++++++++above is html to take for data, below is filitering to keep faster time

def tabler(rows):
  data_list = []
  for r in rows:
    data_list.append({
      "School":r["School"],
      "Runner": r["Runner"],
      "Race": r["Race"],
      "Grade": r["Grade"],
      "Placement":r["Placement"],
      "Date":r["Date"],
      'Date_dt':r["Date_dt"],
      "Time":r["Time"],
      "time_seconds":r["time_seconds"],
      "Length":r["Length"],
      "RaceType":r["RaceType"]
    })
  df = pd.DataFrame(data_list)
  return df

def table_into_df(sport):
  if sport == "XC":
    rows = app_tables.datatable.search()
  if sport == "Track":
    rows = app_tables.tracktable.search()
  return tabler(rows)



def filter(temp_df,sort_by,runnerlist,racelist,gradelist,lengthlist):
  start = time.time()
  df = temp_df

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

def pr_display(df,runnerlist,lengthlist,gradelist):
  try:
    filitered_df = filter(df,"Runner",[],[],[],lengthlist)
    df_pr = tabler(filitered_df)
    df_pr = df_pr.sort_values(by = ["time_seconds"])
    pr_df = df_pr.groupby("Runner")['time_seconds'].min().copy()
    pr_rows = df_pr[df_pr["time_seconds"] == df_pr["Runner"].map(pr_df)]
    return(pr_rows)
  except KeyError:
    print(lengthlist)
    

#########################################################################above is filitering, below is pipeline

# ====== Main Pipeline ======
@anvil.server.background_task
def main():
  html = get_html(URL)
  df_full,MEET_DATE,MEET_NAME = parse_html(html)
  df_school = compute_school_placement(df_full, SCHOOL_NAME)
  df_full = format_for_csv(df_school,MEET_NAME,MEET_DATE)
  df_final = df_full
  df_final["Date_dt"] = df_final['Date_dt'].dt.strftime("%Y-%m-%d")

  og_df = table_into_df(SPORT)
  temp_df = pd.concat([og_df,df_final],ignore_index = True)
  lengths = temp_df["Length"].unique()
  new_df = pd.DataFrame()
  a=0
  b=0
  for length in lengths:
    test = [f"{length}"]
    pr_df = pr_display(temp_df,[],test,[])
    new_df = pd.concat([new_df,pr_df])



  for _, row in new_df.iterrows():
    row= {k:(None if pd.isna(v) else v) for k,v in row.items()}
    exists = table.search(Runner=row["Runner"],Length=row["Length"],School=row["School"])
    exists = list(exists)
    if exists:
      existing_row = exists[0]
      if row['time_seconds'] < existing_row["time_seconds"]:
        print(f"NEW PR {row}")
        a = a+1
        existing_row.update(School = row["School"],Runner=row["Runner"],Race=row["Race"],
                     Placement=row["Placement"],Grade=row["Grade"],Time=row["Time"]
                     ,Date=row["Date"],Length=row["Length"],RaceType = row["RaceType"],
                     Date_dt=row["Date_dt"],time_seconds=row["time_seconds"])
    else:
        print(f"NEW RUNNER {row}")
        b = b+1
        table.add_row(School = row["School"],Runner=row["Runner"],Race=row["Race"],
                     Placement=row["Placement"],Grade=row["Grade"],Time=row["Time"]
                    ,Date=row["Date"],Length=row["Length"],RaceType = row["RaceType"],
                     Date_dt=row["Date_dt"],time_seconds=row["time_seconds"])
      
  return a,b
  

@anvil.server.background_task
def uni_check():
  for row in table.search():
    exists = list(table.search(Runner=row["Runner"],Length=row["Length"],School=row["School"]))
    number_of_similar_rows = len(exists)
    if number_of_similar_rows > 1:
      print("Warning, duplicate detected")
      print(row["Runner"],row["School"],row["Length"])
  print("UNI-Check completed")


@anvil.server.callable
def background_main():
  anvil.server.launch_background_task("main")

@anvil.server.callable
def launch_uni_check():
  anvil.server.launch_background_task("uni_check")


