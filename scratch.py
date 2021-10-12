import time
import numpy as np

x = "x"
matrix = [
    [x,x,x,x,x,x,x],
    [x,x,x,x,x,x,x],
    [x,x,x,x,5,6,x],
    [x,x,x,4,5,6,7],
    [1,2,3,4,5,6,7],
    [1,2,3,4,5,6,7]]

def getAvail(matrix):
    availIdx = []
    
    for col in range(len(matrix[0])):

        # iterasi dari bawah
        for row in range(len(matrix)-1,-1,-1):
            if(matrix[row][col] == "x"):
                availIdx.append((row,col))
                break

    return availIdx

start_time = time.time()
print (getAvail(matrix))
print ("My program took", time.time() - start_time, "to run")

## SLICING
npmatrix = np.array(matrix)

print(npmatrix,"\n")

for r in range(len(matrix)):
    row_array = list(npmatrix[r,:])
    for c in range(len(matrix[0])-3): # krn cuma butuh 4
        window = row_array[c:c+4]

print("score horizontal")
print("row_array terakhir",row_array)
print("window",window)

# for c in range(len(matrix[0])):
#     col_array = list(npmatrix[:,c])
# print("score vertical",col_array)


