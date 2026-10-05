import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

# Load dataset
df = pd.read_csv("skin clinic campaign.csv")

# Convert Yes/No to 1/0
df["Response"] = df["Response_to_Campaign"].map({"Yes": 1, "No": 0})

# Product usage grouping
def product_group(n):
    if 1 <= n <= 4:
        return "1–4"
    elif 5 <= n <= 8:
        return "5–8"
    else:
        return ">8"

df["ProductGroup"] = df["Unique_Products_Purchased"].apply(product_group)

def compute_tables():

    # Gender
    gender = df.groupby("Gender")["Response"].mean().reset_index()
    gender["ResponseRate_%"] = (gender["Response"] * 100).round(2)
    gender = gender[["Gender", "ResponseRate_%"]]

    # Age Group
    age = df.groupby("AgeGroup")["Response"].mean().reset_index()
    age["ResponseRate_%"] = (age["Response"] * 100).round(2)
    age = age[["AgeGroup", "ResponseRate_%"]]

    # Purchase Last Quarter
    purchase = df.groupby("Purchase_Last_Quarter")["Response"].mean().reset_index()
    purchase["ResponseRate_%"] = (purchase["Response"] * 100).round(2)
    purchase = purchase[["Purchase_Last_Quarter", "ResponseRate_%"]]

    # Product Usage
    product = df.groupby("ProductGroup")["Response"].mean().reset_index()
    product["ResponseRate_%"] = (product["Response"] * 100).round(2)
    product = product[["ProductGroup", "ResponseRate_%"]]

    return gender, age, purchase, product


def df_to_html(df, title):
    return f"<h2>{title}</h2>{df.to_html(index=False, border=1)}"


# Homepage Route
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>Skin Clinic Campaign API</title>
    </head>
    <body>
        <h1>Skin Clinic Campaign API is running</h1>
        <p>Visit <a href='/campaign-analysis'>/campaign-analysis</a> to view the analysis.</p>
    </body>
    </html>
    """


@app.get("/campaign-analysis", response_class=HTMLResponse)
def campaign_analysis():

    gender, age, purchase, product = compute_tables()

    html = """
    <html>
    <head>
        <title>Campaign Analysis</title>
        <style>
            body { font-family: Arial; margin: 20px; }
            h1 { margin-bottom: 20px; }
            table { border-collapse: collapse; margin-bottom: 30px; }
            th, td { padding: 8px 12px; }
        </style>
    </head>
    <body>
        <h1>Skin Clinic Campaign Analysis</h1>
    """

    html += df_to_html(gender, "Gender vs Campaign Response")
    html += df_to_html(age, "Age Group vs Campaign Response")
    html += df_to_html(purchase, "Purchase Last Quarter vs Campaign Response")
    html += df_to_html(product, "Product Usage vs Campaign Response")

    html += "</body></html>"
    return html
