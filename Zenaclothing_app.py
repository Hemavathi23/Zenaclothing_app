# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd

# Try to get an active Snowflake session (works only inside Snowflake)
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session

    # Manually create a Snowflake session for external environments
    connection_parameters = {
        "account": "VRHATXJ-QBB31988",
        "user": "HEMAVATHI",
        "password": "Hemah#2303hema",
        "role": "SYSADMIN",
        "warehouse": "COMPUTE_WH",
        "database": "ZENAS_ATHLEISURE_DB",
        "schema": "PRODUCTS"
    }
    
    session = Session.builder.configs(connection_parameters).create()

# Test the session
st.write("Snowflake session initialized successfully!")

st.title("Zena's Amasing Athleisure Catalog")


# get a list of colors for a drop list selection
table_colors = session.sql("select color_or_style from catalog_for_website")
pd_colors = table_colors.to_pandas()

# Oyt the list of colors into a drop list selector 
option = st.selectbox('Pick a sweatsuit color or style:', pd_colors)

# We'll build the image caption now, since we can
product_caption = 'Our warm, comfortable , '+option+'Sweatsuit!'

# use the color selected to go back and get all the info from the database
table_prod_data = session.sql("select file_name, price, size_list, upsell_product_desc, file_url from catalog_for_Website  where color_or_style= '"+option+"';")
pd_prod_data = table_prod_data.to_pandas()


# assign each column of the row returned to its own variable 
price = '$' + str(pd_prod_data['PRICE'].iloc[0]) +'0'
file_name = pd_prod_data['FILE_NAME'].iloc[0]
size_list = pd_prod_data['SIZE_LIST'].iloc[0]
upsell = pd_prod_data['UPSELL_PRODUCT_DESC'].iloc[0]
url = pd_prod_data['FILE_URL'].iloc[0]

# display the info on the page
st.image(image =url, width = 400 , caption = product_caption)
st.markdown('**Price:**' + price)
st.markdown('**Sizes_available:**' + size_list)
st.markdown('**Also Consider:**' + upsell)

#st.write(url)
