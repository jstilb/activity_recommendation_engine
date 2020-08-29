import pandas as pd
import gspread
from info import *
import random

#google sheets connection & DataFrame creation
gc = gspread.service_account(filename=fname)
sh = gc.open(spsh)

act_ws = sh.worksheet("Activities")
act_data = act_ws.get_all_values()
act_headers = act_data.pop(0)
act_df = pd.DataFrame(act_data, columns=act_headers)

log_ws = sh.worksheet("Recommendation Log")
log_data = log_ws.get_all_values()
log_headers = log_data.pop(0)
log_df = pd.DataFrame(log_data, columns=log_headers)

#need to include only activities that are able to be completed or planned during current season

#check Activity Log for recent item
def check_log(log):
    recent_activities = log.tail(10)
    count_easy_act = 0
    count_med_act = 0
    count_hard_act = 0
    plan_dif_rec = 0 # 1 = easy; 2 = med; 3 = hard
    for val in recent_activities['Planning Difficulty']:
        if val == "easy":
            count_easy_act += 1
        elif val == "med":
            count_med_act += 1
        else:
            count_hard_act += 1
    if count_hard_act == 0:
        plan_dif_rec += 3
    elif count_med_act <= 3:
        plan_dif_rec += 2
    else:
        plan_dif_rec += 1
    return plan_dif_rec



#create recommendation using check_log return, priority, and rand. Update actvities and activity log
def recommendation_engine(cl_return, act):
    dif_options = ["easy", "med", "hard"]
    priority_options = ["low", "med", "high"]
    temp_df = pd.DataFrame(act[act["Planning Difficulty"].str.match(dif_options[cl_return - 1])])
    df = pd.DataFrame()
    counter = 1
    while df.empty:
        df = temp_df[temp_df["Priority"].str.match(priority_options[-counter])]
        counter += 1
    print(df)







recommendation_engine(check_log(log_df), act_df)

