from ._anvil_designer import Form4Template
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form4(Form4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
