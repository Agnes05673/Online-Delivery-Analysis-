import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("ONINE_FOOD_DELIVERY_ANALYSIS.csv")

# View data
print(df.head())
print(df.info())
print(df.isnull().sum())

# --------------------------------------------------
# STEP 1: DATA CLEANING
# --------------------------------------------------

numeric_columns = [
    'Customer_Age',
    'Delivery_Time_Min',
    'Distance_km',
    'Order_Value',
    'Discount_Applied',
    'Final_Amount',
    'Delivery_Rating',
    'Restaurant_Rating',
    'Profit_Margin'
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

categorical_columns = [
    'Customer_Gender',
    'City',
    'Area',
    'Restaurant_Name',
    'Cuisine_Type',
    'Payment_Mode',
    'Order_Status',
    'Cancellation_Reason'
]

for col in categorical_columns:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].mode()[0])

text_columns = [
    'Customer_Gender',
    'City',
    'Area',
    'Cuisine_Type',
    'Payment_Mode',
    'Order_Status',
    'Cancellation_Reason'
]

for col in text_columns:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.title()

# Fix ratings safely
if 'Delivery_Rating' in df.columns:
    df['Delivery_Rating'] = df['Delivery_Rating'].apply(
        lambda x: 5 if pd.notna(x) and x > 5 else x
    )

if 'Restaurant_Rating' in df.columns:
    df['Restaurant_Rating'] = df['Restaurant_Rating'].apply(
        lambda x: 5 if pd.notna(x) and x > 5 else x
    )

# Fix negative profit
if 'Profit_Margin' in df.columns:
    df['Profit_Margin'] = df['Profit_Margin'].apply(
        lambda x: 0 if pd.notna(x) and x < 0 else x
    )

# Cancelled order logic fix
if 'Order_Status' in df.columns:
    cancelled_mask = df['Order_Status'].astype(str).str.lower().eq('cancelled')

    if 'Delivery_Rating' in df.columns:
        df.loc[cancelled_mask, 'Delivery_Rating'] = np.nan

    if 'Final_Amount' in df.columns:
        df.loc[cancelled_mask, 'Final_Amount'] = np.nan

# --------------------------------------------------
# STEP 2: OUTLIER TREATMENT
# --------------------------------------------------

def cap_outliers(column_name):
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)
    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    df[column_name] = np.where(df[column_name] < lower_limit, lower_limit, df[column_name])
    df[column_name] = np.where(df[column_name] > upper_limit, upper_limit, df[column_name])

# FIXED COLUMN NAME HERE
outlier_columns = ['Delivery_Time_Min', 'Order_Value', 'Distance_km', 'Profit_Margin']

for col in outlier_columns:
    if col in df.columns:
        cap_outliers(col)

# --------------------------------------------------
# STEP 3: FEATURE ENGINEERING (FIXED)
# --------------------------------------------------

# Weekend / weekday
if 'Is_Weekend' in df.columns:
    df['Order_Day_Type'] = df['Is_Weekend'].apply(
        lambda x: 'Weekend' if str(x).lower() == 'true' else 'Weekday'
    )

# FIXED Peak Hour (NO STRING PARSING ERROR)
if 'Order_Time' in df.columns:
    df['Order_Time'] = pd.to_datetime(df['Order_Time'], errors='coerce')

df['Order_Hour'] = df['Order_Time'].dt.hour

df['Peak_Hour'] = df['Order_Hour'].apply(
        lambda h: 'Peak' if h in [12, 13, 19, 20, 21] else 'Non-Peak'
    )

# Profit % safe calculation
if 'Profit_Margin' in df.columns and 'Final_Amount' in df.columns:
    df['Profit_Margin_Percentage'] = np.where(
        df['Final_Amount'].notna() & (df['Final_Amount'] != 0),
        (df['Profit_Margin'] / df['Final_Amount']) * 100,
        np.nan
    )

# Delivery performance
if 'Delivery_Time_Min' in df.columns:
    df['Delivery_Performance'] = df['Delivery_Time_Min'].apply(
        lambda x: 'Fast' if x <= 30 else ('Average' if x <= 60 else 'Slow')
    )

# Age groups
if 'Customer_Age' in df.columns:
    df['Customer_Age_Group'] = df['Customer_Age'].apply(
        lambda x: '18-25' if x <= 25 else
        ('26-35' if x <= 35 else
        ('36-50' if x <= 50 else '50+'))
    )

# --------------------------------------------------
# STEP 4: ANALYSIS
# --------------------------------------------------

print(df.describe())

if 'City' in df.columns:
    print(df['City'].value_counts())

if 'Cuisine_Type' in df.columns:
    print(df['Cuisine_Type'].value_counts())

if 'Cancellation_Reason' in df.columns:
    print(df['Cancellation_Reason'].value_counts())

numeric_df = df.select_dtypes(include=['number'])
print(numeric_df.corr())

# --------------------------------------------------
# STEP 5: SAVE CLEANED DATA
# --------------------------------------------------

df.to_csv('cleaned_food_delivery_data.csv', index=False)

print("Cleaned dataset saved successfully")
print(df.head())

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="jack@snow25",
    database="food_db"
)

cursor = conn.cursor()

print("Connected successfully!")

from sqlalchemy import create_engine

user = "root"
password = "jack@snow25"
host = "127.0.0.1"
db = "food_db"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")

import pymysql

conn = pymysql.connect(
    host="127.0.0.1",
    user="root",
    password="jack@snow25",
    database="food_db"
)

print("Connected!")

from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd

df = pd.read_csv("cleaned_food_delivery_data.csv")

user = "root"
password = quote_plus("jack@snow25")
host = "127.0.0.1"   
db = "food_db"

engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")

df.to_sql("food_orders", con=engine, if_exists="replace", index=False)

print("Data uploaded successfully!")

