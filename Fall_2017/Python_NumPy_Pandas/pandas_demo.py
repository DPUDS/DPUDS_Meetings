import pandas as pd

def pd_initialize():
    my_df = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 3, 4], 'z': [9, 8, 7]})
    print('The whole dataset:')
    print(my_df)

    print('Accessing specific columns:')
    print(my_df['x'])
    print(my_df['z'])

def pd_index_slice():
    my_df = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 3, 4], 'z': [9, 8, 7]})
    print('The whole dataset:')
    print(my_df)

    print('Getting row at index 1:')
    print(my_df.loc[1])

    print('Getting the rows from index 0 to index 1 (inclusively):')
    print(my_df.loc[0:1])

def pd_reindex():
    my_df = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 3, 4], 'z': [9, 8, 7]})
    print('The whole dataset:')
    print(my_df)

    my_df = my_df.set_index(['x'])
    print(my_df)

def pd_interate():
    my_df = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 3, 4], 'z': [9, 8, 7]})
    print('The whole dataset:')
    print(my_df)

    # looping through the columns
    for column in my_df.columns:
        print(column)
        print(my_df[column])

    # looping through the indices (i.e. through the rows)
    for index in my_df.index:
        print(my_df.loc[index])

def pd_add_column():
    my_df = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 3, 4], 'z': [9, 8, 7]})
    print('Original DataFrame:')
    print(my_df)

    # adding a column with the name 't'
    my_df['t'] = [20, 3, 19]
    print('DataFrame after adding t:')
    print(my_df)

def pd_save_to_file():
    my_df = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 3, 4], 'z': [9, 8, 7]})
    print('Original DataFrame:')
    print(my_df)

    my_df.to_csv('file.csv')

def pd_drop_na():
    my_df = pd.DataFrame({'x': [None, 1, 3, 3], 'y': [4, 2, 9, 8], 'z': [3, 4, None, 5]})
    print(my_df)

    # dropping the rows with NaN values
    filled_df = my_df.dropna(axis=0)
    print(filled_df)

    # dropping the columns with NaN values
    filled_df = my_df.dropna(axis=1)
    print(filled_df)

def pd_fill_na():
    # filling the missing values with the mean, mode, and median of corresponding columns
    filled_df = my_df.fillna(my_df.mean())
    print(filled_df)
    filled_df = my_df.fillna(my_df.mode().loc[0])
    print(filled_df)
    filled_df = my_df.fillna(my_df.median())
    print(filled_df)

    # filling the missing values by interpolating
    filled_df = my_df.interpolate()
    print(filled_df)

def main():
    pd_initialize()
    pd_index_slice()
    pd_reindex()
    pd_interate()
    pd_add_column()
    pd_save_to_file()
    pd_drop_na()
    pd_fill_na()

main()
