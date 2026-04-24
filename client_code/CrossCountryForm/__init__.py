from ._anvil_designer import CrossCountryFormTemplate
from .RowTemplate2 import RowTemplate2
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import m3.components as m3

global school_list
school_list = []


class CrossCountryForm(CrossCountryFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if 1 == 0:
      anvil.server.call("main")

      # uni check
    if 1 == 0:
      anvil.server.call("launch_uni_check")
      ######ONLY USE ONCE ERROR TABLE HAS BEEN CHECKED
    if 1 == 0:
      anvil.server.call("add_error_table_to_correct")

    ##### import athletnet csv to table
    if 1 == 0:
      anvil.server.call("import_csv_caller")

    # Any code you write here will run before the form opens.

  def time_to_seconds(self, timea):
    if ":" in timea:
      mintunes, seconds = timea.split(":")
      mintunes = int(mintunes)
      seconds = float(seconds)
      time_seconds = mintunes * 60 + seconds
    else:
      time_seconds = float(timea)
    return time_seconds

  def count_points(self):
    self.text_3.text = ""
    for event, panel in self.event_panels.items():
      school_points = {School: 0 for School in school_list}
      school_count = {School: 0 for School in school_list}
      for row in panel.items:
        school = row["School"]
        if school_count[school] < 5:
          school_points[school] += row["Points"]




    winning_school = min(school_points, key=school_points.get)
    self.rich_text_1.content = f"{winning_school} wins."

    text_list = []
    for school, tpoints in school_points.items():
      text_list += f"{school} has {tpoints} points. \n"
    self.text_2.text = "".join(text_list)

  def create_datagrids(self, event_list, schools):
    gender = self.dropdown_menu_1.selected_value
    if gender is None:
      gender = "Male"
    event_list = "3200 Meters"

    self.dict_data = anvil.server.call("call_pr_display", schools, event_list, gender)

    self.event_grids = {}
    self.event_panels = {}
    for event in event_list:
      df = self.dict_data[event]
      grid = DataGrid()
      self.event_grids[event] = grid
      self.column_panel_1.add_component(grid)
      grid.columns = [
        {"id": "A", "title": event, "data_key": "Rank"},
        {"id": "B", "title": "School", "data_key": "School"},
        {"id": "C", "title": "Runner", "data_key": "Runner"},
        {"id": "D", "title": "Grade", "data_key": "Grade"},
        {"id": "E", "title": "Length", "data_key": "Length"},
        {"id": "F", "title": "Time", "data_key": "Time", "width": 140},
        {"id": "G", "title": "Points", "data_key": "Points"},
      ]
      rp = RepeatingPanel(item_template=RowTemplate2)
      if not df:
        grid.remove_from_parent()
        pass

      rp.items = [
        {
          **row,
          "Rank": i + 1,
          "Points": i+1
        }
        for i, row in enumerate(df)
      ]

      grid.add_component(rp)
      self.event_panels[event] = rp

    return ""

  def add_tables(self):
    event_list = list(
      filter(lambda x: x is not None, anvil.server.call("count_events"))
    )
    empty_o_not = self.create_datagrids(event_list, school_list)

    if empty_o_not != "empty":
      self.count_points()

  def update_row(self, updated_row, **event_args):
    event = updated_row["Length"]
    grid = self.event_grids[event]
    panel = self.event_panels[event]
    panel.remove_from_parent()
    updated_row["time_seconds"] = self.time_to_seconds(updated_row["Time"])
    df = self.dict_data[event]

    rp = RepeatingPanel(item_template=RowTemplate2)

    for row in df:
      if (
        row["Runner"] == updated_row["Runner"]
        and row["School"] == updated_row["School"]
      ):
        row["Time"] = updated_row["Time"]
        row["time_seconds"] = updated_row["time_seconds"]

    new_df = anvil.server.call("re_sort", df)

    rp.items = [
      {
        **row,
        "Rank": i + 1,
        "Points": i + 1
      }
      for i, row in enumerate(new_df)
    ]

    grid.add_component(rp)

    self.event_panels[event] = rp

    self.count_points()

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

  