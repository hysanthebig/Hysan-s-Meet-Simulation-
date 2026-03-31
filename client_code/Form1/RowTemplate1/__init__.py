from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if hasattr(self, "item") and self.item:
      name = str(self.item.get('Runner', ''))
      names = name.split(" ")
      first_name = names[0]
      last_name = names[-1]
      if "," in name:
        self.repeating_panel_1.text = f"{last_name[:1]}. {first_name}"
      else:
        self.repeating_panel_1.text.text = f"{first_name[:1]}. {last_name}"
      self.repeating_panel_1.text.text = str(self.item.get('Grade', ''))
      self.data_row_panel_2.text = str(self.item.get('Time', ''))
      self.column_panel_5.text = str(self.item.get('Length', ''))
      self.column_panel_1.text = str(self.item.get('School', ''))

    self.lbl_runner.role = 'min-width-repeater'
    # Any code you write here will run before the for