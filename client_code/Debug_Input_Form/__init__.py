from ._anvil_designer import Debug_Input_FormTemplate
from anvil import *
import anvil.server
import m3.components as m3
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Debug_Input_Form(Debug_Input_FormTemplate):
  current_school = 0

  sport = "XC"


  year = "2025"

  school_id_list = [["Colony", "1619"],
                  ["Alta Loma","1538"],
                  ["Los Altos","1741"],
                  ["South Hills","1896"],
                  ["San Dimas", "1860"]]

  rows =[]
  
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    team_id = self.school_id_list[self.current_school][1]
    if self.sport == "Track": 
      api = f"https://www.athletic.net/api/v1/TeamHome/GetTeamEventRecords?teamId={team_id}&seasonId={self.year}"
    else: 
     api = f"https://www.athletic.net/api/v1/TeamHome/GetSeasonBest?teamId={team_id}&seasonId={self.year}" 
    self.link_1.url = api

    # Any code you write here will run before the form opens.

    




  






  @handle("text_box_1", "pressed_enter")
  def text_box_1_pressed_enter(self, **event_args):


    if self.current_school < 5:
      school = self.school_id_list[self.current_school][0]
      team_id = self.school_id_list[self.current_school][1]
      sport = self.sport
  
      self.rows = anvil.server.call("load_data",sport,self.text_box_1.text,school,self.rows)
  
      self.text_box_1.text = ""
  
  
      self.current_school += 1
      self.link_1.text = f"School {self.current_school}"
      year = self.year
    
      if sport == "Track": 
        api = f"https://www.athletic.net/api/v1/TeamHome/GetTeamEventRecords?teamId={team_id}&seasonId={year}"
      else: 
        api = f"https://www.athletic.net/api/v1/TeamHome/GetSeasonBest?teamId={team_id}&seasonId={year}" 
      self.link_1.url = api

    else:
      anvil.server.call("rows_into_table", self.rows,self.sport)
      self.link_1.remove_from_parent()
    







