from ._anvil_designer import Form3Template
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form3(Form3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.dom_nodes['my-custom-btn'].add_event_listener('click', self._handle_click)

    def _handle_click(self, event):
      # Raise an event that the parent form can catch
      self.raise_event('click')
