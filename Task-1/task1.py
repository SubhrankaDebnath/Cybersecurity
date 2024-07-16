import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read the CSV file
df = pd.read_csv('transactions.csv')


#exercise_0
print(df.head())


#exercise_1
column_names = df.columns.tolist()
print("Column Names:", column_names)


#exercise_2
def get_first_k_rows(dataframe, k):
    return dataframe.head(k)
k = 10
first_k_rows = get_first_k_rows(df, k)
print("First k Rows:")
print(first_k_rows)
# Visualization
plt.figure(figsize=(10, 5))
plt.table(cellText=first_k_rows.values, colLabels=first_k_rows.columns, loc='center')
plt.axis('off')
plt.title(f'First {k} Rows of the Dataframe')
plt.show()


#exercise_3
def get_random_sample(dataframe, k):
    return dataframe.sample(n=k)
random_sample = get_random_sample(df, k)
print("Random Sample of k Rows:")
print(random_sample)
# Visualization
plt.figure(figsize=(10, 5))
plt.table(cellText=random_sample.values, colLabels=random_sample.columns, loc='center')
plt.axis('off')
plt.title(f'Random Sample of {k} Rows')
plt.show()


#exercise_4
unique_transaction_types = df['type'].unique().tolist()
print("Unique Transaction Types:", unique_transaction_types)


#exercise_5
top_10_destinations = df['nameDest'].value_counts().head(10)
print("Top 10 Transaction Destinations:")
print(top_10_destinations)
# Visualization
plt.figure(figsize=(10, 5))
top_10_destinations.plot(kind='bar')
plt.title('Top 10 Transaction Destinations')
plt.xlabel('Destination')
plt.ylabel('Frequency')
plt.show()


#exercise_6
fraud_detected = df[df['isFraud'] == 1]
plt.figure(figsize=(12, 7))
plt.axis('off')
plt.suptitle('Rows with Detected Fraud')
plt.table(cellText=fraud_detected.values, colLabels=fraud_detected.columns)
plt.show()


#exercise_7
def exercise_7(df):
    distinct_destinations_per_source = df.groupby('nameOrig')['nameDest'].nunique().reset_index()
    distinct_destinations_per_source.columns = ['source', 'unique_destinations']
    distinct_destinations_per_source_sorted = distinct_destinations_per_source.sort_values(by='unique_destinations', ascending=False)
    return distinct_destinations_per_source_sorted
result = exercise_7(df)
print(result)


#visual_1
def visual_1(df):
    def transaction_counts(df):
        return df['type'].value_counts()
    def transaction_counts_split_by_fraud(df):
        return df.groupby(by=['type', 'isFraud']).size()
    fig, axs = plt.subplots(2, figsize=(6,10))
    transaction_counts(df).plot(ax=axs[0], kind='bar')
    axs[0].set_title('Transaction Types Frequencies')
    axs[0].set_xlabel('Transaction Type')
    axs[0].set_ylabel('Occurrence')
    transaction_counts_split_by_fraud(df).plot(ax=axs[1], kind='bar')
    axs[1].set_title('Transaction Types Frequencies, Split by Fraud')
    axs[1].set_xlabel('Transaction Type, Fraud')
    axs[1].set_ylabel('Occurrence')
    fig.suptitle('Transaction Types')
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    for ax in axs:
      for p in ax.patches:
          ax.annotate(p.get_height(), (p.get_x(), p.get_height()))
    return 'While the transaction frequencies depend on the whims of the ' \
           'available data, what is interesting here is that fraudulent ' \
           'activity is only seen on CASH_OUT and TRANSFER transactions. '\
           'This insight inform management to focus the effort of manual '\
           'reviews which could result in less fraud being missed.'
visual_1(df)


#visual_2
def visual_2(df):
    def query(df):
        df['Origin Delta'] = df['oldbalanceOrg'] -	df['newbalanceOrig']
        df['Destination Delta'] = df['oldbalanceDest'] -	df['newbalanceDest']
        return df[df['type']=='CASH_OUT']
    plot = query(df).plot.scatter(x='Origin Delta',y='Destination Delta')
    plot.set_title('Source v. Destination Balance Delta for Cash Out Transactions')
    plot.set_xlim(left=-1e3, right=1e3)
    plot.set_ylim(bottom=-1e3, top=1e3)
    return 'A cash out occurs when a partipant withdraws money. It is reassuring '\
           'that only two of the four quadrants have activity, as the contrary '\
           'would indicate something wrong with the dataset. The y=-x line is '\
           'particularly interesting as it indicates instant settlement.'
visual_2(df)


#custom_exercise
def exercise_custom(df):
    return df[['isFlaggedFraud', 'isFraud']].value_counts()
def visual_custom(df):
    fig, ax = plt.subplots(1, figsize=(4,6))
    exercise_custom(df).plot(ax=ax, kind='bar')
    ax.set_title('Fraud Detection')
    ax.set_xlabel('isFlaggedFraud, isFraud')
    ax.set_ylabel('Occurrence')
    for p in ax.patches:
        ax.annotate(p.get_height(), (p.get_x(), p.get_height()))
    return "Here we see that the fraud detection at play misses almost all "\
           "of the fradulent activity. However, there are no false negatives "\
           "either. One interpretation could be that the detector does not "\
           "report until it has a high degree of confidence."
visual_custom(df)