import quandl
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')


fiddy_state = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
print(fiddy_state[0]['Name &postal abbreviation[1]']['Name &postal abbreviation[1].1'].columns.tolist())