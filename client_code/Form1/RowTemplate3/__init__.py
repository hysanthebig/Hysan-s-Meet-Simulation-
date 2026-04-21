from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate3(RowTemplate3Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Fill UI with row data
    self.text_1.text = self.item.get("Rank", "")
    self.text_2.text = self.item.get("School", "")
    self.text_3.text = self.item.get("Runner", "")
    self.text_4.text = self.item.get("Grade", "")
    self.text_5.text = self.item.get("Length", "")
    self.text_box_1.text = self.item.get("Time", "")
    self.text_6.text = self.item.get("Points", "")

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