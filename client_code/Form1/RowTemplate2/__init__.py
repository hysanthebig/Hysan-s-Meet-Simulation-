from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.time_box.text = self.item['Time']
    self.time_box.set_event_handler('pressed_enter', self.time_box_enter)
    

    # Any code you write here will run before the form opens.

  def time_box_enter(self, **event_args):
    

