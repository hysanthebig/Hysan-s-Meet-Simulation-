from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import m3.components as m3

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
