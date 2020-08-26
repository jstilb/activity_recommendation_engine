import pandas as pd
import gspread
from info import *

gc = gspread.service_account(filename=fname)

sh = gc.open(spsh)
ws = sh.worksheet("Activities")
data = ws.get_all_values()
headers = data.pop(0)

df = pd.DataFrame(data, columns=headers)
print(df)