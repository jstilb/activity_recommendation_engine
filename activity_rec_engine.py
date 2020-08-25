import pandas as pd
import gspread

gc = gspread.oauth()

sh = gc.open("Activity Recommendation Engine")

print(sh.sheet1.get('A1'))

#test data frame
d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)
print(df)