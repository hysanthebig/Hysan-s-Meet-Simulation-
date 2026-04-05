from ._anvil_designer import Form1Template
import anvil
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import m3.components as m3

global school_list
school_list = []
sprint_events =["100 Meter","200 Meter","400 Meter"]
distance_events = ["800 Meter","1600 Meter","3200 Meter"]
hurdle_events = ["110 Meter Hurdles","300 Meter Hurdles"]
relay_events = ["4x100 Meter", "4x400 Meter", "4x800 Meter"]



class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if 1 == 0:
      anvil.server.call('main')
    if 1 == 0:
      anvil.server.call('launch_uni_check')
      ######ONLY USE ONCE ERROR TABLE HAS BEEN CHECKED
    if 1 == 0:
      anvil.server.call('add_error_table_to_correct')


  
    









    # Any code you write here will run before the form opens.


  def pr_screen_display(self):
    selected_runners = []
    selected_lengths = ["400 Meter"]
    selected_grades = []
    selected_schools = ["Alta Loma"]
    sport = "Track"
    data = anvil.server.call("pr_display",sport,selected_runners,selected_lengths,selected_grades,selected_schools)

    self.repeating_panel_1.items = [
      {**row, "Rank": i + 1}
      for i, row in enumerate(data)
    ]





  def create_datagrids(self,event,schools):
    school_1, school_2 = (schools + [None,None])[:2]
    school_1_points = 0
    school_2_points = 0
    grid = DataGrid()
    self.column_panel_1.add_component(grid)
    grid.columns = [{"id":"A","title": event,"data_key":"Rank"},
                    {"id":"B","title":"School","data_key":"School"},
                    {"id":"C","title":"Runner","data_key":"Runner"},
                    {"id":"D","title":"Grade","data_key":"Grade"},
                    {"id":"E","title":"Length","data_key":"Length"},
                    {"id":"F","title":"Time","data_key":"Time"},
                    {"id":"G","title":"Points","data_key":"Points"}]
    rp = RepeatingPanel(item_template=DataRowPanel)
    data = anvil.server.call("pr_display","Track",[],[event],[],schools)
    if data is None:
      return
    rp.items = [
      {
        **row,
        "Rank": i + 1,
        "Points": 5 if i == 0 else 3 if i == 1 else 1 if i == 2 else 0
      }
      for i, row in enumerate(data)
    ]
    for row in rp.items[:3]:
      if school_1 == row["School"]:
        school_1_points = school_1_points + row["Points"]
      elif school_2 == row["School"]:
        school_2_points = school_2_points + row["Points"]

      
    grid.add_component(rp)
    return(school_1_points,school_2_points)


  def add_tables(self):
    school_1_total_points = 0
    school_2_total_points = 0
    school_1, school_2 = (school_list + [None,None])[:2]
    event_list = list(filter(lambda x:x is not None,anvil.server.call("count_events")))
    

      
    event_list.remove("100 Meter Hurdles")
    if self.button_1.appearance == "outlined":
        event_list = [e for e in event_list if e not in sprint_events]
    if self.button_2.appearance == "outlined":
      event_list = [e for e in event_list if e not in relay_events] 
    if self.button_3.appearance == "outlined":
      event_list = [e for e in event_list if e not in hurdle_events]
    if self.button_4.appearance == "outlined":
      event_list = [e for e in event_list if e not in distance_events]
    
    for event in event_list:
      try:
        school_1_points,school_2_points = self.create_datagrids(event,school_list)
        school_1_total_points = school_1_points + school_1_total_points
        school_2_total_points = school_2_points + school_2_total_points
    
        self.text_3.text += (f"{event} - {school_1}-{school_1_points}, {school_2}-{school_2_points} \n")
        
      except AttributeError:
        print("error")

      if school_1_total_points < school_2_total_points:
        winning_school = school_2
      else:
        winning_school = school_1
      self.rich_text_1.content = (f"{winning_school} is winning.")
      self.text_2.text = (f"{school_1} has {school_1_total_points} points. \n {school_2} has {school_2_total_points} Points")
      
      



    ############################################# ui under here

  @handle("colony_selector", "click")
  def colony_selector_click(self, **event_args):
    if "Colony" not in school_list:
      school_list.append("Colony")
      print("added")
    else:
      school_list.remove("Colony")
      print("removed")

  @handle("alta_loma_link", "click")
  def alta_loma_link_click(self, **event_args):
    if "Alta Loma" not in school_list:
      school_list.append("Alta Loma")
    else:
      school_list.remove("Alta Loma")

  @handle("los_altos_link", "click")
  def los_altos_link_click(self, **event_args):
    if "Los Altos" not in school_list:
      print("Lost Altos")
      school_list.append("Los Altos")
    else:
      school_list.remove("Los Altos")

  @handle("san_dimas_link", "click")
  def san_dimas_link_click(self, **event_args):
    if "San Dimas" not in school_list:
      print("San Dimas")
      school_list.append("San Dimas")
    else:
      school_list.remove("San Dimas")

  @handle("south_hills_list", "click")
  def south_hills_link_click(self, **event_args):
    if "South Hills" not in school_list:
      school_list.append("South Hills")
      print("South hills")

    else:
      school_list.remove("South Hills")

  @handle("icon_button_1", "click")
  def icon_button_1_click(self, **event_args):
    self.column_panel_1.clear()
    self.add_tables()

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    if self.button_1.appearance == "filled":
      self.button_1.appearance = "outlined"
    else:
      self.button_1.appearance = "filled"

  @handle("button_2", "click")
  def button_2_click(self, **event_args):
    if self.button_2.appearance == "filled":
      self.button_2.appearance = "outlined"
    else:
      self.button_2.appearance = "filled"

  @handle("button_3", "click")
  def button_3_click(self, **event_args):
    if self.button_3.appearance == "filled":
      self.button_3.appearance = "outlined"
    else:
      self.button_3.appearance = "filled"

  @handle("button_4", "click")
  def button_4_click(self, **event_args):
    if self.button_4.appearance == "filled":
      self.button_4.appearance = "outlined"
    else:
      self.button_4.appearance = "filled"













