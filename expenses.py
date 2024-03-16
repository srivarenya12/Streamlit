import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from google.cloud import firestore

# Function to store user's monthly expenses
def store_monthly_expenses(month, data):
    ref = db.collection('monthly_expenses').document(month)
    ref.set(data)

# Function to fetch user's monthly expenses
def fetch_monthly_expenses():
    expenses_ref = db.collection('monthly_expenses')
    expenses_docs = expenses_ref.stream()
    data = []
    for doc in expenses_docs:
        data.append(doc.to_dict())
    return data

# Function to store individual expenses
def store_expense(month, date, category, amount, remarks):
    ref = db.collection('monthly_expenses').document(month)
    ref.update({f'{date}-{category}': {'Amount': amount, 'Remarks': remarks}})

# Firestore setup
db = firestore.Client.from_service_account_json("studentexpenses-25535-firebase-adminsdk-ch5zy-859488da52.json")

# Home page
def home():
    st.title("Student Expenses - Home")
    # Your code for the home page...

# Add an Expense page
def add_expense():
    st.title("Add an Expense")
    month = st.text_input("Month")
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Spent on Food", "Entertainment", "Hostel Fee", "Groceries", "Books & Supplies", "Transportation", "Other"])
    amount = st.number_input("Amount", step=1.0)
    remarks = st.text_area("Remarks")
    
    if st.button("Add Expense"):
        if month and date and category and amount:
            store_expense(month, date, category, amount, remarks)
            st.success("Expense added successfully.")
        else:
            st.error("Please fill in all fields.")
    
    # Option to view monthly expenses
    if st.button("View Monthly Expenses"):
        monthly_expenses()

# Monthly Expenses page
def monthly_expenses():
    st.title("Monthly Expenses")
    month = st.text_input("Month")
    monthly_budget = st.number_input("Monthly Budget", step=1.0)
    spentonfood = st.number_input("Spent on Food", step=1.0)
    entertainment = st.number_input("Entertainment", step=1.0)
    hostelfee = st.number_input("Hostel Fee", step=1.0)
    groceries = st.number_input("Groceries", step=1.0)
    booksandsupplies = st.number_input("Books & Supplies", step=1.0)
    transportation = st.number_input("Transportation", step=1.0)
    
    if st.button("Submit"):
        if month and monthly_budget:
            data = {
                "Month": month,
                "Monthly Budget": monthly_budget,
                "Spent on Food": spentonfood,
                "Entertainment": entertainment,
                "Hostel Fee": hostelfee,
                "Groceries": groceries,
                "Books & Supplies": booksandsupplies,
                "Transportation": transportation
            }
            store_monthly_expenses(month, data)
            st.success("Monthly expenses stored successfully.")
        else:
            st.error("Please fill in all fields.")

# Display Expenses page
def display_expenses():
    st.title("Display Expenses")
    data = fetch_monthly_expenses()
    df = pd.DataFrame(data)
    
    # Filter
    field_to_filter = st.selectbox("Filter by Field", df.columns)
    filter_value = st.text_input(f"Enter value for {field_to_filter} filter")
    filtered_df = df[df[field_to_filter] == filter_value] if filter_value else df

    st.write(filtered_df)

# Main function
def main():
    st.sidebar.title("Navigation")

    # Sidebar navigation options
    if st.sidebar.button("Home"):
        home()
    if st.sidebar.button("Add an Expense"):
        add_expense()
    if st.sidebar.button("Display Expenses"):
        display_expenses()

if __name__ == "__main__":
    main()
