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


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if 1 == 0:
      anvil.server.call('background_main')
    if 1 == 0:
      anvil.server.call('launch_uni_check')









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
    print(data)
    if data is None:
      return
    rp.items = [
      {**row, "Rank": i + 1}
      for i, row in enumerate(data)
    ]
    for i, row in enumerate(data):
      points = 0
      if i == 0:
        points = 5
      elif i == 1:
        points  = 3
      elif i == 2:
        points  = 1
      rp.items.append([{**row,"Points": points}])
    

    grid.add_component(rp)


  def add_tables(self):
    for event in list(filter(lambda x:x is not None,anvil.server.call("count_events"))):
      try:
        self.create_datagrids(event,school_list)
      except AttributeError:
        print("error")




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

  @handle("south_hills_link", "click")
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











