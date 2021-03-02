import numpy as np
import matplotlib.pyplot as plt
import copy
import math
from PIL import Image


# declaring variables for saving the data
band1_data = []
band2_data = []
band3_data = []
band4_data = []

# function to read the data of all four bands (band1, band2, band3, band4)
def readFiles():
    # reading data for band2
    textfile = open("/Users/mitali/Downloads/orion/i170b2h0_t0.txt")
    lines = textfile.readlines()
    lines = list(reversed(lines))
    for line in lines:
        data = line.split(',')
        for value in data:
            band2_data.append(float(value.replace("\"", "")))
    band2_data

    # reading data for band1
    textfile = open("/Users/mitali/Downloads/orion/i170b1h0_t0.txt")
    lines = textfile.readlines()
    lines = list(reversed(lines))
    for line in lines:
        data = line.split(',')
        for value in data:
            band1_data.append(float(value.replace("\"", "")))
    band1_data

    # reading data for band3
    textfile = open("/Users/mitali/Downloads/orion/i170b3h0_t0.txt")
    lines = textfile.readlines()
    lines = list(reversed(lines))
    for line in lines:
        data = line.split(',')
        for value in data:
            band3_data.append(float(value.replace("\"", "")))
    band3_data

    # reading data for band4
    textfile = open("/Users/mitali/Downloads/orion/i170b4h0_t0.txt")
    lines = textfile.readlines()
    lines = list(reversed(lines))
    for line in lines:
        data = line.split(',')
        for value in data:
            band4_data.append(float(value.replace("\"", "")))
    band4_data


# a) calculate the max, min, mean and variance value of band2 2D dataset
# function to calculate the max, min, mean and variance value of band2 dataset
def computation():
    max_value= np.max(band2_data)
    min_value= np.min(band2_data)
    mean_value= np.mean(band2_data)
    var_value= np.var(band2_data)


# b) profile line through maximum value of band2 dataset
# function to plot the profile line through maximum value of band2 dataset
def profileLine():
    plt.cla()
    band2_data_arr = np.asarray(band2_data)
    band2_reshape_arr = band2_data_arr.reshape((500,500))
    index_maxvalue = np.where(band2_reshape_arr == (max(band2_data)))
    row_value = band2_reshape_arr[67]
    log = np.log(row_value +1)
    plt.plot(log)
    plt.title("Profile Line of Max value of Band2")
    plt.xlabel("X Range")
    plt.ylabel("Y Range")
    # saving image
    plt.savefig("Task_B_profilelineband2.png")
    plt.close()


# c) histogram of band2 2D dataset
# function to plot the line histogram of band2 2D dataset
def displayHistogram():
    plt.cla()
    band2_data_arr = np.asarray(band2_data)
    reshape_arr = band2_data_arr.reshape((500, 500))
    log_arr =np.log(reshape_arr +1)
    values,occurences=np.unique(log_arr,return_counts=True)
    plt.plot(values,occurences)
    plt.title("Histogram Plot of Band2 dataset")
    plt.xlabel("X Values")
    plt.ylabel("Occurences")
    # saving Image
    plt.savefig("Task_C_Histogramband2.png")
    plt.close()


# d) rescale the values to range between 0 to 255 for band2 2D dataset
# function to rescale value from 0 to 255 for band2 data using nn-linear transformation
def getBand2Image():
    plt.cla()
    band2_data_arr = np.asarray(band2_data)
    reshape_arr = band2_data_arr.reshape((500, 500))
    max_value = np.max(band2_data_arr)
    non_linear =[]

    for x in range(reshape_arr.shape[0]):
        for y in range(reshape_arr.shape[1]):
            non_linear.append(255 *((np.log(reshape_arr[x][y] + 1)/max_value)))
    non_linear_arr = np.asarray(non_linear, dtype=np.double)
    nonli_reshape_arr = non_linear_arr.reshape((500,500))
    plt.imshow(nonli_reshape_arr)
    cbar = plt.colorbar(ticks=[np.min(nonli_reshape_arr), np.max(nonli_reshape_arr)], orientation='vertical')
    plt.title("Non- Linear Transformation of Band2 dataset")
    plt.xlabel("X Scale")
    plt.ylabel("Y Scale")
    cbar.ax.set_yticklabels(['0.014[Min]', '0.145[Max]'])
    cbar.set_label("Color Scale")
    #saving Image
    plt.savefig("Task_D_nonlinearimageband2.png")
    plt.close()


# e) histogram equalization for all bands(band1, band2, band3 and band4)
# function to compute the histogram equalization
def histogramEqualization(data_arr, imageName, titlename):

    equalized_arr = [value for value in data_arr]
    unique, occurances = np.unique(data_arr, return_counts=True)
    dictionary = dict(zip(unique, occurances))
    # calculate PDF
    pdf_list = []
    occurances = [float(value) for value in list(dictionary.values())]
    for items in occurances:
        pdf_list.append((items/len(data_arr)))
    # calculate CDF
    index = 0
    cdf_list =[]
    for value in pdf_list:
        index = index + value
        cdf_list.append(index)
    # mapping the cdf values for the equalized image
    mapping_list=[]
    for key in dictionary:
        mapping_list.append(key)
    for index in range(len(equalized_arr)):
        Value = equalized_arr[index]
        indexitr = mapping_list.index(Value)
        equalized_arr[index]= cdf_list[indexitr]
    convt_equalized_arr = np.asarray(equalized_arr, dtype=np.double)
    high_equalized_arr = np.reshape(convt_equalized_arr,(500,500))
    plt.imshow(high_equalized_arr, cmap = 'gray')
    cbar = plt.colorbar(ticks=[np.min(high_equalized_arr), np.max(high_equalized_arr)], orientation='vertical')
    plt.title(titlename)
    plt.xlabel("X Scale")
    plt.ylabel("Y Scale")
    cbar.ax.set_yticklabels(['0', '1'])
    cbar.set_label("Color Scale")
    # saving image
    plt.savefig(imageName)
    plt.cla()
    plt.clf()
    plt.close(imageName)
    return high_equalized_arr



# f) Combine the histogram-equalized 2D data set to an RGB-image (band4=r, band3=g, band1=b)
# function to create RGB image from three 2D array
def displayRGBImage(color_r, color_g, color_b):
    #plt.cla()
    rgb_list =[]
    for row in range(0,500):
        for col in range(0,500):
            rgb_list.append(color_r[row][col])
            rgb_list.append(color_g[row][col])
            rgb_list.append(color_b[row][col])
    rgb_array = np.asarray(rgb_list,  dtype=np.double)
    reshape_rgb = np.reshape(rgb_array, (500,500,3))
    plt.imshow(reshape_rgb)
    cbar = plt.colorbar(ticks=[np.min(reshape_rgb), np.max(reshape_rgb)], orientation='vertical')
    plt.title("RGB image of band 4, 3 and 1 dataset")
    plt.xlabel("X Scale")
    plt.ylabel("Y Scale")
    cbar.ax.set_yticklabels(['0', '255'])
    cbar.set_label("Color Scale")
    # saving image
    plt.savefig('Task_F_RGB_image.png')
    plt.cla()
    plt.clf()
    plt.close('Task_F_RGB_image.png')


# main function calling all other functions
def main():
    readFiles()
    computation()
    profileLine()
    displayHistogram()
    getBand2Image()
    color_b = histogramEqualization(band1_data,'Task_E_histeq_band1.png', 'Histogram Equalization of Band1 dataset')
    histogramEqualization(band2_data,'Task_E_histeq_band2.png', 'Histogram Equalization of Band2 dataset')
    color_g = histogramEqualization(band3_data,'Task_E_histeq_band3.png', 'Histogram Equalization of Band3 dataset')
    color_r = histogramEqualization(band4_data,'Task_E_histeq_band4.png', 'Histogram Equalization of Band4 dataset')

    displayRGBImage(color_r, color_g, color_b)


# call the main() function
if __name__ == "__main__":
    main()