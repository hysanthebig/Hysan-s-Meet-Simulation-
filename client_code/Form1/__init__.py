from ._anvil_designer import Form1Template
from .RowTemplate2 import RowTemplate2
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import m3.components as m3

global school_list
school_list = []
sprint_events =["100 Meters","200 Meters","400 Meters"]
distance_events = ["800 Meters","1600 Meters","3200 Meters"]
hurdle_events = ["110m Hurdles","300m Hurdles"]
relay_events = ["4x100 Relay",'4x200 Relay', '4x400 Relay', "4x800 Relay","4x1600 Relay","SMR 800m","SMR 1600m","DMR 4000m"]
field_events = ['Shot Put', 'Discus', 'High Jump', 'Pole Vault', 'Long Jump', 'Triple Jump']
throwing_events = ['Shot Put', 'Discus','Pole Vault']
jumping_events = ['High Jump','Long Jump', 'Triple Jump']
extra_events = ['4x200 Relay',"4x800 Relay","4x1600 Relay","SMR 800m","SMR 1600m","DMR 4000m"]


class Form1(Form1Template):
  
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    anvil.server.call('field_event','''34' 7.5"''')
    self.init_components(**properties)
    if 1 == 0:
      anvil.server.call('main')

      #uni check
    if 1 == 0:
      anvil.server.call('launch_uni_check')
      ######ONLY USE ONCE ERROR TABLE HAS BEEN CHECKED
    if 1 == 0:
      anvil.server.call('add_error_table_to_correct')

    ##### import athletnet csv to table
    if 1 == 0:
      anvil.server.call('import_csv_caller')














    # Any code you write here will run before the form opens.








  def create_datagrids(self,event_list,schools):
    gender = self.dropdown_menu_1.selected_value
    if gender is None:
      gender = "Male"

    self.dict_data = anvil.server.call("call_pr_display",schools,event_list,gender)

    event_points = {}
    self.event_grids = {}
    self.event_panels = {}
    for event in event_list:
      df = self.dict_data[event]
      school_points = {School:0 for School in schools}
      grid = DataGrid()
      self.event_grids[event] = grid
      self.column_panel_1.add_component(grid)
      grid.columns = [{"id":"A","title": event,"data_key":"Rank"},
                      {"id":"B","title":"School","data_key":"School"},
                      {"id":"C","title":"Runner","data_key":"Runner"},
                      {"id":"D","title":"Grade","data_key":"Grade"},
                      {"id":"E","title":"Length","data_key":"Length"},
                      {"id":"F","title":"Time","data_key": "Time","width":140 },
                      {"id":"G","title":"Points","data_key":"Points"}]
      rp = RepeatingPanel(item_template=RowTemplate2)
      if not df:
        grid.remove_from_parent()
        pass

      rp.items = [

        {
          **row,
          "Rank": i + 1,
          "Points": 5 if i == 0 else 3 if i == 1 else 1 if i == 2 else 0
        }
        for i, row in enumerate(df)
      ]

      score_limit = 1 if event in relay_events else 3

      for row in rp.items[:score_limit]:
        school = row["School"]
        if school in school_points:
          school_points[school] += row["Points"]
          
      grid.add_component(rp)
      self.event_panels[event] = rp
      event_points[event] = school_points
    return("",event_points)


  def add_tables(self):
    self.text_3.text =''
    total_points = {}
    event_list = list(filter(lambda x:x is not None,anvil.server.call("count_events")))

    event_list = [e for e in event_list if e not in extra_events]

    if self.button_1.appearance == "outlined":
      event_list = [e for e in event_list if e not in sprint_events]
    if self.button_2.appearance == "outlined":
      event_list = [e for e in event_list if e not in relay_events] 
    if self.button_3.appearance == "outlined":
      event_list = [e for e in event_list if e not in hurdle_events]
    if self.button_4.appearance == "outlined":
      event_list = [e for e in event_list if e not in distance_events]
    if self.button_5.appearance == "outlined":
      event_list = [e for e in event_list if e not in throwing_events]
    if self.button_6.appearance == "outlined":
      event_list = [e for e in event_list if e not in jumping_events]

    empty_o_not,event_points_dict = self.create_datagrids(event_list,school_list)

    if empty_o_not != "empty":
      
      for event,tallies in event_points_dict.items():
        event_text_list = []
        for school,points in tallies.items():
          
          total_points[school] = total_points.get(school,0) + points
          event_text_list += (f"-----{school} {points} \n")
        self.text_3.text += (f"{event} -\n {(''.join(event_text_list))}")





      winning_school = max(total_points, key=total_points.get)
      self.rich_text_1.content = (f"{winning_school} wins.")

      text_list = []
      for school,tpoints in total_points.items():
        text_list += (f"{school} has {tpoints} points. \n")
      self.text_2.text = ("".join(text_list))


  def update_row(self,updated_row,**event_args):
    event = updated_row["Length"]
    grid = self.event_grids[event]
    panel = self.event_panels[event]
    panel.remove_from_parent()
    print(self.dict_data)
    df = self.dict_data[event]
    
    rp = RepeatingPanel(item_template=RowTemplate2)
    
    for row in df:
      if row["Runner"] == updated_row["Runner"] and row["Time"] == updated_row["School"]:
        print(row)
        print
        row["Time"] = updated_row["Time"]
    rp.items = [

          {
            **row,
            "Rank": i + 1,
            "Points": 5 if i == 0 else 3 if i == 1 else 1 if i == 2 else 0
          }
          for i, row in enumerate(df)
        ]

    grid.add_component(rp)

    score_limit = 1 if event in relay_events else 3

    for row in rp.items[:score_limit]:
      school = row["School"]
      if school in school_points:
        school_points[school] += row["Points"]

      
   
      event_points[event] = school_points
    
    


    ############################################# ui under here

  @handle("colony_selector", "click")
  def colony_selector_click(self, **event_args):
    if "Colony" not in school_list:
      school_list.append("Colony")
      self.text_4.text = school_list
    else:
      school_list.remove("Colony")
      self.text_4.text = school_list


  @handle("alta_loma_link", "click")
  def alta_loma_link_click(self, **event_args):
    if "Alta Loma" not in school_list:
      school_list.append("Alta Loma")
      self.text_4.text = school_list

    else:
      school_list.remove("Alta Loma")
      self.text_4.text = school_list

  @handle("los_altos_link", "click")
  def los_altos_link_click(self, **event_args):
    if "Los Altos" not in school_list:
      school_list.append("Los Altos")
      self.text_4.text = school_list
    else:
      school_list.remove("Los Altos")
      self.text_4.text = school_list

  @handle("san_dimas_link", "click")
  def san_dimas_link_click(self, **event_args):
    if "San Dimas" not in school_list:
      school_list.append("San Dimas")
      self.text_4.text = school_list

    else:
      school_list.remove("San Dimas")
      self.text_4.text = school_list

  @handle("south_hills_list", "click")
  def south_hills_link_click(self, **event_args):
    if "South Hills" not in school_list:
      school_list.append("South Hills")
      self.text_4.text = school_list

    else:
      school_list.remove("South Hills")
      self.text_4.text = school_list

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

  @handle("button_5", "click")
  def button_5_click(self, **event_args):
    if self.button_5.appearance == "filled":
      self.button_5.appearance = "outlined"
    else:
      self.button_5.appearance = "filled"

  @handle("button_6", "click")
  def button_6_click(self, **event_args):
    if self.button_6.appearance == "filled":
      self.button_6.appearance = "outlined"
    else:
      self.button_6.appearance = "filled"









