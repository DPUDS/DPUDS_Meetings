import numpy as np

def np_array_initialize():
    my_list = [1, 2, 3]
    print(my_list)

    my_array = np.array(my_list)
    print(my_array)

    array1 = np.arange(6)
    print('NumPy array from 0 up to 6:', array1)

    array2 = np.zeros((3,))
    print('NumPy array of zeros with the specified shape:', array2)

    array3 = np.ones((5,))
    print('NumPy array of ones with the specified shape:', array3)

def np_array_operations():
    my_array = np.array([1, 3, 5, 2])

    print('Original array:', my_array)
    print('Elements in array multiplied by 3:', my_array * 3)
    print('Elements in array squared:', my_array ** 2)

    new_array = np.array([1, 2, 3, 4])
    print('Another array:', new_array)
    print('Adding two arrays:', my_array + new_array)
    print('Dividing one array by another:', my_array / new_array)

def np_array_shape():
    my_array = np.array([[1, 3, 5], [2, 4, 6]])
    print(my_array)
    print('Number of rows and number of columns:', my_array.shape)

    my_array = my_array.reshape((3,2))
    print(my_array)
    print('Number of rows and number of columns:', my_array.shape)

def np_index_slice_1d():
    my_array = np.array([1, 2, 3, 4, 5])
    print('Element at index 1:', my_array[1])
    print('Element at index 3:', my_array[3])

    sub_array = my_array[1:4]
    print('Sub array from index 1 to index 4:', sub_array)

def np_index_slice_2d():
    my_array = np.array([[1, 2, 3, 4, 5], [2, 3, 6, 7, 3], [-1, 3, -4, 5, 3]])
    print('Original array:')
    print(my_array)

    print('Row at index 1 (second row):', my_array[1,:])
    print('Column at index 0 (first column):', my_array[:,0])

    print('Elements between rows with index 0 and index 2, columns with index 1 and index 3:')
    print(my_array[0:2, 1:3])

def main():
    np_array_initialize()
    np_array_operations()
    np_array_shape()
    np_index_slice_1d()
    np_index_slice_2d()

main()
