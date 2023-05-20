import streamlit as st
from PIL import Image
import pandas as pd
# import sys
# sys.path.append('./src')

# from conv_functions import * # NOT WORKING 

# FUNCTIONS

def remove_chars(main_df):
  for i in range(0,5):
    for i, v in enumerate(main_df.columns):
      string = str(v)
      main_df.rename(columns = {v:string.lower()}, inplace = True)

    for i, v in enumerate(main_df.columns): #por algum motivo se vc fizer rename no mesmo 'for' nao funciona
      string = str(v)
      main_df.rename(columns = {v:string.strip()}, inplace = True)

    for i, v in enumerate(main_df.columns):
      string = str(v)
      main_df.rename(columns = {v:string.strip('%')}, inplace = True)

    for i, v in enumerate(main_df.columns):
      string = str(v)
      main_df.rename(columns = {v:string.strip('_')}, inplace = True)
  print(f'Check headers conversion: \n \n {main_df.columns}')
  return main_df

#_____________________________________________________________________________________

def elem_to_oxide(main_df, conversion_df):
  import pandas as pd
  """Converts dataframe's header and values using a conversion sheet as criteria."""
  new_df = main_df.copy( ) # new dataframe to delete data before the remove_chars() to maintain uppercases etc

  ## clean headers ##
  main_df = remove_chars(main_df) # check headers ...

  ##################################
  
  ## creating new empty dataframe ##
  breakFlag = False
  for i, v in enumerate(main_df.columns): 
    for j in conversion_df['Elem']:
      # print(f'{v} == {j.lower()} = {v == j.lower()}')
      if v == j.lower():                                # testing if the column name matches any elements
        to_delete = new_df.iloc[:, i:].columns.tolist() # setting list of columns to delete, based on first 
        new_df.drop(columns= to_delete, inplace=True)
        breakFlag = True # --> all this bullshit is to speed the code, skipping both loops
        break            # otherwise the loop would keep testing if the column in main_df exists
    if breakFlag == True:
      break
    
  ## converting data to new dataframe ##      
  for i in main_df.columns:                             #same loop than before
    if main_df.loc[:, i].all() != 'NaN' or '' or 0. or None: # skip no data columns 
      for j, k, m in zip(conversion_df['Elem'], conversion_df['Oxide'], conversion_df['ElemToOx']): #DataFrame with headers now
        if i == j.lower():   # test if elem matches main_df columns, if True append new pd.Series to the new_df
                             # the thing if when you define a column that doesnt exist, it creates another one, it works like an append
          new_df[f'{k}'] = pd.Series(dtype = 'float16') # saying to new_df to set a new pd.Series named after the Oxide column (k), 
                                                        # so it creates a new empty one 
                                                        # dtype: defining the dtype to skip an output warning
          new_df.loc[:, k] = main_df.loc[:, i] * m      # finally taking the main_df value, multiplying by the 
                                                        # ElemToOx factor and putting to the values of the new column

  return new_df

# PAGE

icon = Image.open('./docs/iron-.png')
st.set_page_config(
    page_title = 'Elements conversion',
    page_icon= icon)


st.markdown('''# **Element-Oxide-Cation conversor**

---''')

conversion_sheet = pd.read_csv('./data/conversion_sheet.csv', delimiter = ';', header = 0)

# UPLOAD DATA

uploaded_files = st.file_uploader('Upload .csv file',accept_multiple_files=False)

if uploaded_files:
    table = pd.read_csv(uploaded_files)

    st.markdown('The conversor assumes zero for nan values. Check the integrity of your table (if there\'s any issue try to change the .csv separator):')
    table.fillna(0, inplace=True)
    st.table(table.head(10))

    # col1, col2 = st.columns(2)

    # first = col1.selectbox('First element column:', table.columns)
    # last = col2.selectbox('Last element column:', table.columns)

# CONVERSION TYPE

    st.markdown('---')
    st.markdown('## **Conversion type**')

    conversor = st.selectbox('', options=['Element to Oxide', 'Oxide to Element', 'Oxide to Cation', 'Element to Cation'])

    if conversor == 'Element to Oxide' or conversor ==  'Element to Cation':
        st.table(elem_to_oxide(table, conversion_sheet))
    

