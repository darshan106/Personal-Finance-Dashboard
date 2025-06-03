#!/usr/bin/env python3
import pandas as pd
import numpy as np
import plotly.express as px
import panel as pn

def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Month Name'] = df['Date'].dt.strftime('%b')
    df = df.drop(columns=[col for col in ['Transaction', 'Transaction vs category'] if col in df.columns])
    df['Category'] = np.where(df['Transaction Type'] == 'Income', df['Transaction Names'], df['Category'])
    return df

def make_pie_chart(df, year, label):
    sub_df = df[(df['Transaction Type'] == label) & (df['Year'] == year)]
    pie_fig = px.pie(sub_df, values='Amount (INR)', names='Category', color_discrete_sequence=px.colors.qualitative.Set2)
    pie_fig.update_traces(textposition='inside', direction='clockwise', hole=0.3, textinfo='label+percent')
    total_expense = df[(df['Transaction Type'] == 'Expense') & (df['Year'] == year)]['Amount (INR)'].sum()
    total_income = df[(df['Transaction Type'] == 'Income') & (df['Year'] == year)]['Amount (INR)'].sum()
    total_text = f"₹ {round(total_expense if label == 'Expense' else total_income)}"
    saving_rate_text = f": Saving rate {round((total_income - total_expense) / total_income * 100)}%" if label == 'Expense' else ""
    pie_fig.update_layout(
        uniformtext_minsize=10,
        uniformtext_mode='hide',
        title=f"{label} Breakdown {year}{saving_rate_text}",
        annotations=[dict(text=total_text, x=0.5, y=0.5, font_size=12, showarrow=False)]
    )
    return pie_fig

def make_monthly_bar_chart(df, year, label):
    df = df[(df['Transaction Type'] == label) & (df['Year'] == year)]
    total_by_month = df.groupby(['Month', 'Month Name'])['Amount (INR)'].sum().to_frame().reset_index().sort_values(by='Month').reset_index(drop=True)
    color_scale = px.colors.sequential.YlGn if label == 'Income' else px.colors.sequential.OrRd
    bar_fig = px.bar(total_by_month, x='Month Name', y='Amount (INR)', text_auto='.2s', title=f"{label} per month", color='Amount (INR)', color_continuous_scale=color_scale)
    return bar_fig

def main():
    pn.extension()
    file_path = '/Categorized_transactions.csv'
    df = load_data(file_path)
    income_pie_fig_2023 = make_pie_chart(df, 2023, 'Income')
    expense_pie_fig_2023 = make_pie_chart(df, 2023, 'Expense')
    income_pie_fig_2024 = make_pie_chart(df, 2024, 'Income')
    expense_pie_fig_2024 = make_pie_chart(df, 2024, 'Expense')
    income_monthly_2023 = make_monthly_bar_chart(df, 2023, 'Income')
    expense_monthly_2023 = make_monthly_bar_chart(df, 2023, 'Expense')
    income_monthly_2024 = make_monthly_bar_chart(df, 2024, 'Income')
    expense_monthly_2024 = make_monthly_bar_chart(df, 2024, 'Expense')
    tabs = pn.Tabs(
        ('2023', pn.Column(pn.Row(income_pie_fig_2023, expense_pie_fig_2023), pn.Row(income_monthly_2023, expense_monthly_2023))),
        ('2024', pn.Column(pn.Row(income_pie_fig_2024, expense_pie_fig_2024), pn.Row(income_monthly_2024, expense_monthly_2024)))
    )
    template = pn.template.FastListTemplate(
        title='Personal Finance Dashboard',
        main=[pn.Row(pn.Column(pn.Row(tabs)))],
        header_background='#c0b9dd'
    )
    template.show()

if __name__ == '__main__':
    main()