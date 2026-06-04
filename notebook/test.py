import pandas as pd

df1 = pd.DataFrame({
    'id': [1, 2, 3],
    'datetime': ['2024-01-01 10:00:00', '2024-01-01 11:00:00', '2024-01-01 12:00:00']
})

df2 = pd.DataFrame({
    'values': [4, 1, 0, 10],
    'datetime': ['2024-01-02 10:00:00', '2024-01-02 10:00:00', '2024-01-02 11:10:00', '2024-01-02 13:00:00']
})

# final_df = df1.groupby(df1['datetime'])
# print(final_df.head())
df2_floored = df2.copy()
df2['datetime'] = pd.to_datetime(df2['datetime'])
df2['floored_datetime'] = df2['datetime'].dt.floor('h')
print(df2.head())
df2 = df2.groupby('floored_datetime').size().reset_index(name='rental_count')

print(df2.head())