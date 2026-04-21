from ._anvil_designer import DataRowPanel1Template
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class DataRowPanel1(DataRowPanel1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Fill UI with row data
    self.label_rank.text = self.item.get("Rank", "")
    self.label_school.text = self.item.get("School", "")
    self.label_runner.text = self.item.get("Runner", "")
    self.label_grade.text = self.item.get("Grade", "")
    self.label_length.text = self.item.get("Length", "")
    self.text_box_time.text = self.item.get("Time", "")
    self.label_points.text = self.item.get("Points", "")

  def text_box_time_change(self, **event_args):
    new_time = self.text_box_time.text
    self.item["Time"] = new_time

    # optional: update seconds too
    try:
      self.item["time_seconds"] = anvil.server.call("time_to_seconds", new_time)
    except:
      pass

    # tell parent something changed
    self.parent.raise_event("x-refresh")