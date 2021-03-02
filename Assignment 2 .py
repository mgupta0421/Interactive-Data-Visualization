#importing Libraries
import numpy as np
import matplotlib.pyplot as plt

# reading file
data = np.fromfile("/Users/mitali/Downloads/slice150.raw", dtype=np.uint16)
arr = data.reshape(512, 512)

# a) A profile line through line 256 of the 2D dataset
row_value = arr[255]
plt.plot(row_value)
plt.margins(x=0)
# creating Image
plt.title("Profile Line Plot of 256th line of dataset")
plt.xlabel("X Range")
plt.ylabel("Y Range")
# saving Image
plt.savefig("ProfileLine.png", dpi=600)
plt.show()

# b) The mean and variance value of the 2D dataset
mean_value = np.mean(arr)
variance_value =np.var(arr)


# c) A histogram of the 2D dataset
values,occurences=np.unique(arr,return_counts=True)
plt.plot(values,occurences)
# creating Image
plt.title("Histogram Plot of dataset")
plt.xlabel("X Values")
plt.ylabel("Occurences")
scaleimg=plt.gcf()
scaleimg.set_size_inches(15, 10)
# saving Image
plt.savefig("Histogram_150slice.png", dpi=600)
plt.show()


# d) Rescaling values to range between 0 and 255 using linear transformation
linear_value = []
smax = 255
rmin = np.min(arr)
rmax = np.max(arr)
for r in arr:
    linear = ((r-rmin)/(rmax-rmin))*smax
    linear_value.append(linear)
linear_array = np.array(linear_value)
reshape = linear_array.reshape((512,512))
# creating Image
plt.imshow(reshape,cmap=plt.get_cmap("inferno"))
cbar = plt.colorbar(ticks=[0, 255], orientation='vertical')
plt.title("Linear Transformation of dataset")
plt.xlabel("X Scale")
plt.ylabel("Y Scale")
cbar.ax.set_yticklabels(['0','255'])
cbar.set_label("Color Scaling")
# saving Image
plt.savefig("linearScale150slice_Image.png", dpi=600)
plt.close()


# e) Rescaling values to range between 0 and 255 using non- linear transformation

# Non-linear transformation function with log function
non_linear = np.log(1+arr)
reshape = non_linear.reshape((512,512))
# creating Image
plt.imshow(reshape,cmap=plt.get_cmap("plasma"))
cbar = plt.colorbar(ticks=[0, 7.65], orientation='vertical')
plt.title("Non- Linear Transformation of dataset")
plt.xlabel("X Scale")
plt.ylabel("Y Scale")
cbar.ax.set_yticklabels(['0','255'])
cbar.set_label("Color Scaling")
#saving Image
plt.savefig("nonlinearScale150slice_Image.png", dpi=600)
plt.close()

#f) 11*11 boxcar smoothing filter on the 2D dataset
size = arr.shape
boxcar_filter_op = []
# function adding elements of array
def array_sum(arr):
    addition = 0
    for element in arr:
        addition = addition + element
    return addition
# calculating 11*11 boxcar filter kernel
for row in range(0, size[0] -10):
    for column in range(0, size[1] -10):
        kernel = []
        for x in range(row, row + 10):
            for y in range(column, column + 10):
                kernel.append(arr[x][y])
        kernel_array = np.array(kernel)
        addition = array_sum(kernel_array)
        boxcar_filter_op.append(addition)
new_array = np.array(boxcar_filter_op)
final_arr = new_array.reshape(502,502)
divide_arr = final_arr/121
# creating Image
plt.imshow(divide_arr,cmap=plt.get_cmap("plasma"))
cbar = plt.colorbar(ticks=[11, 1370], orientation='vertical')
plt.title("Boxcar Smoothing Filter Image")
plt.xlabel("X Scale")
plt.ylabel("Y Scale")
cbar.ax.set_yticklabels(['0','255'])
cbar.set_label("Color Scaling")
# saving Image
plt.savefig("Boxcarfilter150slice_Image.png", dpi=600)
plt.close()

#g) 11*11 median filter on the 2D dataset

size = arr.shape
median_filter_op = []
# Sorting the array elements
def array_sorting(arr):
    for n in range(len(arr)):
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
    return arr
# calculating 11*11 median filter kernel
for row in range(0, size[0] -10):
    for column in range(0, size[1] -10):
        kernel = []
        for x in range(row, row + 10):
            for y in range(column, column + 10):
                kernel.append(arr[x][y])
        sorted_array = array_sorting(kernel)
        median_filter_op.append(sorted_array[60])
new_array = np.array(median_filter_op)
final_arr = new_array.reshape(502,502)
# creating Image
plt.imshow(final_arr,cmap=plt.get_cmap("plasma"))
cbar = plt.colorbar(ticks=[12, 1760], orientation='vertical')
plt.title("Median Filter Image")
plt.xlabel("X Scale")
plt.ylabel("Y Scale")
cbar.ax.set_yticklabels(['0','255'])
cbar.set_label("Color Scaling")
# saving Image
plt.savefig("Medianfilter150slice_Image.png", dpi=600)
plt.close()