import sys
import pandas as pd


if len(sys.argv) != 2:
    sys.exit("Usage: python process data.xlsx")

try:
    full_data = pd.read_excel(f'{sys.argv[1]}')
except:
    print('File not found')
    sys.exit()
else:
    matches = full_data.loc[full_data['CLE'].isin(['01', '02', '03']), 'Sample']
    matches += 2
    proc_data = pd.DataFrame(columns=['Sample', 'Timestamp', 'CLE', 'Unique', 'Duplicate', 'nth Duplicate', 'First use'])

    for i in range(len(matches)):
        address = ''
        new_row = {}
        loc = matches.iloc[i]

        if full_data.at[loc - 1, 'CLE'] == '00' and full_data.at[loc + 5, 'CLE'] == '30':
            for j in range(5):
                address += str(full_data.at[loc + j, 'ALE'])

            new_row = {'Sample': loc - 2, 'Timestamp': full_data.at[loc - 2, 'Absolute(ns)'],
                       'CLE': full_data.at[loc - 2, 'CLE']}

            if address in proc_data['Unique'].unique():
                idx = proc_data.index.values[proc_data['Unique'] == address]
                new_row['First use'] = idx

                new_row['Duplicate'] = address

                num_duplicates = len(proc_data.index[proc_data['Duplicate'] == address])
                new_row['nth Duplicate'] = num_duplicates+1

                proc_data = proc_data.append(new_row, ignore_index=True)
            else:
                new_row['Unique'] = address
                proc_data = proc_data.append(new_row, ignore_index=True)


proc_data.to_csv('out.csv')