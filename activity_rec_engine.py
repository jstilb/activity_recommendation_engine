import pandas as pd
import gspread
from info import *
import random
from twilio.rest import Client

# Twilio Information
client = Client(account_sid, auth_token)

# google sheets connection & DataFrame creation
gc = gspread.service_account(filename=fname)
sh = gc.open(spsh)

act_ws = sh.worksheet("Activities")
act_df = pd.DataFrame(act_ws.get_all_records())

log_ws = sh.worksheet("Recommendation Log")
log_df = pd.DataFrame(log_ws.get_all_records())


# need to include only activities that are able to be completed or planned during current season

# check Activity Log for recent item to create parameter for recommendaiton engine
def check_log(log):
    recent_activities = log.tail(10)
    count_easy_act = 0
    count_med_act = 0
    count_hard_act = 0
    plan_dif_rec = 0  # 1 = easy; 2 = med; 3 = hard
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


# create recommendation using check_log return, priority, and rand. Update actvities and activity log
def recommendation_engine(cl_return, act):
    # set parameters for recommendation using priority & planning difficulty
    dif_options = ["easy", "med", "hard"]
    priority_options = ["low", "med", "high"]
    temp_df = pd.DataFrame(act[act["Planning Difficulty"].str.match(dif_options[cl_return - 1])])
    df = pd.DataFrame()
    counter = 1
    while df.empty:
        df = temp_df[temp_df["Priority"].str.match(priority_options[-counter])].reset_index(drop=True)
        counter += 1

    # make recommendation
    recommendation = df.loc[random.randrange(len(df.index))]
    message = client.messages \
        .create(
        body=recommendation.to_string(),
        from_=twilio_phone,
        to=jm_phone
    )
    message.sid

    # update recommendation log
    new_log_df = log_df.append(recommendation).reset_index(drop=True).fillna('')
    log_ws.update([new_log_df.columns.values.tolist()] + new_log_df.values.tolist())

    # delete row in activities worksheet
    row_to_delete = act_ws.find(recommendation.get(0)).row
    act_ws.delete_rows(row_to_delete)


recommendation_engine(check_log(log_df), act_df)
