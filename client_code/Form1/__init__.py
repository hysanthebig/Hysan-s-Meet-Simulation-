from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import m3.components as m3

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.data_grid_1.rows_per_page = 0
    self.init_components(**properties)
    if 1 == 0:
      anvil.server.call('background_main')
    if 1 == 0:
      anvil.server.call('launch_uni_check')
    self.pr_screen_display()
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


    
  def pr(self):
    self.pr_screen_display()
for event in anvil.server.call("count_events"):
  print(event)

  