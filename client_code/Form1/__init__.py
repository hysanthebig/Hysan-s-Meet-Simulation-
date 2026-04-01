from ._anvil_designer import Form1Template
import anvil
from anvil import Form1
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



    if 1 == 0:
      for event in list(filter(lambda x:x is not None,anvil.server.call("count_events"))):
        try:
          self.create_datagrids(event,school_list)
        except AttributeError:
          print("error")





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
                    {"id":"F","title":"Time","data_key":"Time"}]
    rp = RepeatingPanel(item_template=DataRowPanel)
    data = anvil.server.call("pr_display","Track",[],[event],[],schools)
    print(data)
    if data is None:
      return
    rp.items = [
      {**row, "Rank": i + 1}
      for i, row in enumerate(data)
    ]

    grid.add_component(rp)

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

  @anvil.handle("los_altos_link", "click")
  def los_altos_link_click(self, **event_args):
    """This method is called clicked"""
    pass
  




      







