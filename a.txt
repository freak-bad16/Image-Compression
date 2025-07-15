import cv2 as cv
import pywt
import numpy as np
import os

wavelet = 'haar'
threshold = 0.05  
path = input("Do you want to give the path of any image? If no, just press Enter: ")
image_path = r"C:\Users\sumit\OneDrive\Desktop\internship\image compression\image.png" if path == "" else path
user_input = input("Do you want aggressive compression? (yes/no): ").strip().lower()
isAgrasive = user_input in ["yes", "y"]

img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
original_size = os.path.getsize(image_path)

# x , (y ,z ,w) = pywt.dwt2(img , wavelet)
# a , (b ,c ,d) = pywt.dwt2(x , wavelet)
ll , (lh ,hl ,hh) = pywt.dwt2(img , wavelet)

if(isAgrasive):
    lh[:] = 0 
    hl[:] = 0 
    hh[:] = 0 
else:
    lh[np.abs(lh) < threshold] = 0 
    hl[np.abs(hl) < threshold] = 0 
    hh[np.abs(hh) < threshold] = 0 

resizeImg = pywt.idwt2((ll , (lh ,hl ,hh)) , wavelet)

cv.imwrite("compressed_temp.png", np.uint8(resizeImg))
resizeImg_size = os.path.getsize("compressed_temp.png")  

print("Original size : ", original_size / 1024, "KB")
print("New size      : ", resizeImg_size / 1024, "KB")
print("Compression ratio : ", original_size / resizeImg_size)

cv.namedWindow("Original Image", cv.WINDOW_NORMAL)
cv.resizeWindow("Original Image", 600, 400)
cv.imshow("Original Image", img)

cv.namedWindow("Compressed Image", cv.WINDOW_NORMAL)
cv.resizeWindow("Compressed Image", 600, 400)
cv.imshow("Compressed Image", np.uint8(resizeImg))  

cv.waitKey(0)
cv.destroyAllWindows()