import pandas as pd
from langchain_community.llms import Ollama

# Initialize LLM
llm = Ollama()

def hop(start, stop, step):
    for i in range(start, stop, step):
        yield i
    yield stop

def categorize_transactions(transaction_names, llm):
    response = llm.invoke(
        "Can you add an appropriate category to the following expenses. "
        "For example: Disney+ Hotstar - Entertainment, Software Engineer - Salary, etc. "
        "Categories should be less than 4 words. " + transaction_names
    )
    response = response.split('\n')

    # Put in dataframe
    categories_df = pd.DataFrame({'Transaction vs category': response})
    categories_df[['Transaction', 'Category']] = categories_df['Transaction vs category'].str.split(' - ', expand=True)

    return categories_df

# Load data
df = pd.read_csv("/Users/darshan/Documents/Projects/DataScience/Personal/FinancialDashboard/Transactions_2023-24.csv")

# Get unique transactions
unique_transactions = df["Transaction Names"].unique()

# Create index list for batch processing
index_list = list(hop(0, len(unique_transactions), 30))

# Initialize categories_df_all dataframe
categories_df_all = pd.DataFrame()

# Loop through index_list to categorize transactions
for i in range(0, len(index_list) - 1):
    transaction_names = unique_transactions[index_list[i]:index_list[i + 1]]
    transaction_names = ','.join(transaction_names)

    categories_df = categorize_transactions(transaction_names, llm)
    categories_df_all = pd.concat([categories_df_all, categories_df], ignore_index=True)

# Save categorized transactions
categories_df_all.to_csv("Categories_df_all.csv", index=False)

# Drop NA values
categories_df_all = categories_df_all.dropna()

# Categorize "Food and Drinks"
categories_df_all.loc[
    categories_df_all['Category'].str.contains("Food/Dining|Restaurant"), 'Category'
] = "Food and Drinks"

# Clean Transaction column
df.loc[df['Transaction Names'].str.contains("Disney"), 'Transaction Names'] = "Disney+ Hotstar"
categories_df_all['Transaction'] = categories_df_all['Transaction'].str.replace(r'^\d+\.\s+', '', regex=True)

# Merge categorized data with original transactions
df = pd.merge(df, categories_df_all, left_on='Transaction Names', right_on='Transaction', how='left')

# Save final categorized transactions
df.to_csv("Categorized_transactions.csv", index=False)
