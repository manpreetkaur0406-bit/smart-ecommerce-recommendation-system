
import streamlit as st
import pickle
import pandas as pd

products = pickle.load(open("products.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))

st.title("🛒 Smart E-Commerce Recommendation System")

selected_product = st.selectbox(
    "Select Product",
    products['title'].values
)

def recommend(product):

    index = products[products['title']==product].index[0]

    distances = similarity[index]

    recommended = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:11]

    for i in recommended:

        row = products.iloc[i[0]]

        st.write("###", row['title'])
        st.write("Brand:", row['brand_name'])
        st.write("Price:", row['price_value'])
        st.write("Rating:", row['rating_stars'])

        if pd.notna(row['product_url']):
            st.write(row['product_url'])

        st.write("---")

if st.button("Recommend"):
    recommend(selected_product)
