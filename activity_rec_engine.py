import pandas as pd
import gspread
from info import *

#google sheets connection & DataFrame creation
gc = gspread.service_account(filename=fname)
sh = gc.open(spsh)

act_ws = sh.worksheet("Activities")
act_data = act_ws.get_all_values()
act_headers = act_data.pop(0)
act_df = pd.DataFrame(act_data, columns=act_headers)

log_ws = sh.worksheet("Activity Log")
log_data = log_ws.get_all_values()
log_headers = log_data.pop(0)
log_df = pd.DataFrame(log_data, columns=log_headers)

#need to include only activities that are able to be completed or planned during current season

#check Activity Log for recent item


#create recommendation & update activity log



#print(df)


#def small_activity_recommendation():