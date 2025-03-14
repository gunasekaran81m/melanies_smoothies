# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
    f"""Choose the fruits you want in your custom Smoothie!

    """)

name_on_order = st.text_input("Name on Smoothie")
st.write('The Name of your Smoothie will be', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredients_list:
   ingredients_string = ''

   for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '   
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=true)
        #st.write(ingredients_string) 

        my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

        #st.write(my_insert_stmt)

   if ingredients_string:
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie is ordered!', icon="✅")


    
