# Import python packages
import pandas as pd
import requests
import streamlit as st
from snowflake.snowpark.functions import col

cnx = st.connection('snowflake')
session = cnx.session()

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom Smoothie!"
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

data = session.table("smoothies.public.fruit_options")
pd_df = data.select(col('FRUIT_NAME'), col('SEARCH_ON')).to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect("Choose up to 5 ingredients",
                      data.select(col('FRUIT_NAME')),
                       max_selections=5)
 
ingredients_string = ' '.join(ingredients_list) + ' '

if ingredients_string and st.button('Submit'):
    my_insert_stmt = """ insert into smoothies.public.orders (name_on_order, ingredients)
                values ('""" + name_on_order + """', '""" + ingredients_string + """')
    """
    session.sql(my_insert_stmt).collect()
    st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
