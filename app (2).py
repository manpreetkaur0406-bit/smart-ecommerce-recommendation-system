import gradio as gr
import pandas as pd
import pickle
import ast
import webbrowser
import matplotlib.pyplot as plt

# =====================================================
# LOAD DATA
# =====================================================

with open("products.pkl", "rb") as f:
    products = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# =====================================================
# IMAGE FUNCTION
# =====================================================

def get_image(image_string):
    try:
        images = ast.literal_eval(image_string)

        if isinstance(images, list) and len(images) > 0:
            return images[0]

    except Exception:
        return None

    return None

# =====================================================
# SHOW PRODUCT DETAILS
# =====================================================

def show_product(product_name):

    row = products.loc[
        products["title"] == product_name
    ].iloc[0]

    image = get_image(row["all_images"])

    return (
        image,
        row["title"],
        row["brand_name"],
        f"₹ {row['price_value']}",
        f"⭐ {row['rating_stars']}",
        row["availability"],
        row["about_item"],
        row["product_url"]
    )

# =====================================================
# RECOMMEND PRODUCTS
# =====================================================

def recommend(product_name):

    index = products[
        products["title"] == product_name
    ].index[0]

    distances = list(enumerate(similarity[index]))

    distances = sorted(
        distances,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for item in distances[1:11]:

        row = products.iloc[item[0]]

        recommendations.append([
            row["title"],
            row["brand_name"],
            row["price_value"],
            row["rating_stars"],
            row["availability"],
            row["product_url"]
        ])

    return recommendations

# =====================================================
# OPEN AMAZON PAGE
# =====================================================

def open_link(url):

    if url:
        webbrowser.open(url)
# =====================================================
# USER INTERFACE
# =====================================================

with gr.Blocks(
    title="Smart E-Commerce Recommendation System"
) as demo:

    gr.Markdown("""
# 🛒 Smart E-Commerce Recommendation System

### AI Powered Product Recommendation using Machine Learning
""")

    # ==========================
    # HOME TAB
    # ==========================

    with gr.Tab("🏠 Home"):

        product = gr.Dropdown(
            choices=sorted(products["title"].tolist()),
            label="🔍 Select a Product",
            interactive=True
        )

        with gr.Row():

            show_btn = gr.Button(
                "Show Product",
                variant="primary"
            )

            recommend_btn = gr.Button(
                "Recommend Products"
            )

        gr.Markdown("---")

        with gr.Row():

            image = gr.Image(
                label="Product Image",
                height=350
            )

            with gr.Column():

                title = gr.Textbox(
                    label="Product Name",
                    interactive=False
                )

                brand = gr.Textbox(
                    label="Brand",
                    interactive=False
                )

                price = gr.Textbox(
                    label="Price",
                    interactive=False
                )

                rating = gr.Textbox(
                    label="Rating",
                    interactive=False
                )

                availability = gr.Textbox(
                    label="Availability",
                    interactive=False
                )

                description = gr.Textbox(
                    label="About Product",
                    lines=8,
                    interactive=False
                )

                product_url = gr.Textbox(
                    label="Amazon URL"
                )

                open_btn = gr.Button(
                    "🛒 Open Amazon Product"
                )

        gr.Markdown("## ❤️ Top 10 Similar Products")

        recommendation_table = gr.Dataframe(
            headers=[
                "Title",
                "Brand",
                "Price",
                "Rating",
                "Availability",
                "Amazon URL"
            ],
            interactive=False,
            wrap=True
        )

    # ==========================
    # BUTTON EVENTS
    # ==========================

    show_btn.click(
        fn=show_product,
        inputs=product,
        outputs=[
            image,
            title,
            brand,
            price,
            rating,
            availability,
            description,
            product_url
        ]
    )

    recommend_btn.click(
        fn=recommend,
        inputs=product,
        outputs=recommendation_table
    )

    open_btn.click(
        fn=open_link,
        inputs=product_url,
        outputs=gr.Textbox(visible=False)
    )
def open_link(url):

    if url:
        webbrowser.open(url)
        return "Amazon page opened successfully."

    return "No URL found."
    open_btn.click(
    fn=open_link,
    inputs=product_url,
    outputs=gr.Textbox(visible=False)
)
    # =====================================================
    # ANALYTICS TAB
    # =====================================================

    with gr.Tab("📊 Analytics"):

        gr.Markdown("# 📊 Product Analytics Dashboard")

        def brand_chart():
            fig, ax = plt.subplots(figsize=(10,5))
            products["brand_name"].value_counts().head(10).plot(
                kind="bar",
                ax=ax
            )
            ax.set_title("Top 10 Brands")
            plt.xticks(rotation=45)
            return fig

        def rating_chart():
            fig, ax = plt.subplots(figsize=(10,5))

            pd.to_numeric(
                products["rating_stars"],
                errors="coerce"
            ).hist(
                bins=10,
                ax=ax
            )

            ax.set_title("Rating Distribution")
            return fig

        def price_chart():
            fig, ax = plt.subplots(figsize=(10,5))

            pd.to_numeric(
                products["price_value"],
                errors="coerce"
            ).hist(
                bins=30,
                ax=ax
            )

            ax.set_title("Price Distribution")
            return fig

        with gr.Row():

            brand_plot = gr.Plot()

            rating_plot = gr.Plot()

        price_plot = gr.Plot()

        load_btn = gr.Button(
            "📈 Load Dashboard",
            variant="primary"
        )

        load_btn.click(
            fn=brand_chart,
            outputs=brand_plot
        )

        load_btn.click(
            fn=rating_chart,
            outputs=rating_plot
        )

        load_btn.click(
            fn=price_chart,
            outputs=price_plot
        )

    # =====================================================
    # ABOUT TAB
    # =====================================================

    with gr.Tab("ℹ️ About"):

        gr.Markdown("""
# 🛒 Smart E-Commerce Recommendation System

### Final Year Data Analytics Project

---

## 📌 Project Objective

This project recommends similar products using Machine Learning
based on product similarity.

---

## 🚀 Technologies Used

- Python
- Pandas
- Gradio
- Machine Learning
- Cosine Similarity
- Matplotlib

---

## ⭐ Features

✅ Product Search

✅ Product Recommendation

✅ Product Details

✅ Product Images

✅ Analytics Dashboard

✅ Amazon Product Links

""")

# =====================================================
# LAUNCH APP
# =====================================================

demo.launch(share=True)
