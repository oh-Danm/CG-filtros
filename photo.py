from PIL import Image
from matplotlib import pyplot as plt 
import math as math

def image_from_matrix(matrix):
    new = Image.new('RGB', (len(matrix[0]), len(matrix)))
    flat = [pixel for row in matrix for pixel in row]
    new.putdata(flat)

    return new

def grayify(r,g,b):
    s = (r + g + b) // 3
    return (s, s, s)

def histograma(imagem):
    h = [0]*256

    for i in range(len(imagem)):
        for j in range(len(imagem[0])):
            pos = imagem[i][j][0]
            h[pos] = h[pos]+1

    return h

def equalizar(imagem):
    h = histograma(imagem)
    N = len(imagem[0]) * len(imagem)

    cdf = [0]*256
    soma = 0

    for i in range(256):
        soma += h[i]
        cdf[i] = soma

    new = [0]*256
    for i in range(256):
        new[i] = round(cdf[i]*255/N)

    output = [[(0,0,0) for _ in range(len(imagem[0]))] for _ in range(len(imagem))]
    for i in range(len(imagem)):
        for j in range(len(imagem[0])):
            coiso = imagem[i][j][0]
            equal_coiso = new[coiso]
            output[i][j] = (equal_coiso, equal_coiso, equal_coiso)

    return output

def thresholding(imagem, T):
    width, height = len(imagem[0]), len(imagem)
    output = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            value = output[i][j][0]
            if imagem[i][j][0] > T:
                value = 255
            else:
                value = 0
            output[i][j] = (value, value, value)

    return output

def apply_kernel(imagem, kernel, clamp = True):
    width, height = len(imagem[0]), len(imagem) 
    k = 3
    border = k//2
    output = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    for x in range(border, height-border):
        for y in range(border, width-border):
            soma = 0.0
            for i in range(k):
                ix = x + i - border
                row = imagem[ix]
                for j in range(k):
                    jy = y + j - border
                    soma += row[jy][0] * kernel[i][j]
            coiso = round(soma)
            if clamp:
                coiso = abs(max(0, min(255, round(soma))))
            
            output[x][y] = (coiso, coiso, coiso)

    return output

def choose_kernel(opt):
    if opt == 0:
        kernel = [[1/9]*3 for _ in range(3)]
        return kernel
    elif opt == 1:
        kernel = [
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ]
        return kernel
    elif opt == 2:
        kernel = [
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]
        ]
        return kernel

img = Image.open("input.jpg")
largura, altura = img.size
pixels = img.load()
imagem = [[pixels[x, y] for x in range(largura)] for y in range(altura)]

for i in range(altura):
    for j in range(largura):
        r, g, b = imagem[i][j]
        imagem[i][j] = grayify(r, g, b)

new = image_from_matrix(imagem)
new.save("outputs/output_gray.jpg")
pixels = new.load()
gray = [[pixels[x, y] for x in range(largura)] for y in range(altura)]

h = histograma(gray)


equal = equalizar(gray)

equal_image = image_from_matrix(equal)
equal_image.save("outputs/output_equal.jpg")

thresh = thresholding(gray, 87)

thresh_image = image_from_matrix(thresh)
thresh_image.save("outputs/output_thresh.jpg")

kernel = choose_kernel(0)
soft = apply_kernel(gray, kernel, True)

soft_image = image_from_matrix(soft)
soft_image.save("outputs/output_soft.jpg")

kernel = choose_kernel(1)
sharpen = apply_kernel(gray, kernel, True)

sharp_image = image_from_matrix(sharpen)
sharp_image.save("outputs/output_sharp.jpg")

kernel = choose_kernel(1)
sharpen = apply_kernel(gray, kernel, True)

sharp_image = image_from_matrix(sharpen)
sharp_image.save("outputs/output_sharp.jpg")

kernel = choose_kernel(2)
border = apply_kernel(gray, kernel, True)

border_image = image_from_matrix(border)
border_image.save("outputs/output_border.jpg")

# plt.bar(range(256), h)
# plt.title("histograma")
# plt.show()
