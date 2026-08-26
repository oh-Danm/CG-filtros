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
    output = imagem
    for i in range(height):
        for j in range(width):
            value = output[i][j][0]
            if imagem[i][j][0] > T:
                value = 255
            else:
                value = 0
            output[i][j] = (value, value, value)

    return output

img = Image.open("input.webp")
largura, altura = img.size
pixels = img.load()
imagem = [[pixels[x, y] for x in range(largura)] for y in range(altura)]

for i in range(largura):
    for j in range(altura):
        r, g, b = imagem[i][j]
        imagem[i][j] = grayify(r, g, b)

new = image_from_matrix(imagem)
new.save("outputs/output_gray.jpg")
pixels = new.load()
gray = [[pixels[x, y] for x in range(largura)] for y in range(altura)]

h = histograma(gray)

'''
plt.bar(range(256), h)
plt.title("histograma")
plt.show()
'''

equal = equalizar(gray)

equal_image = image_from_matrix(equal)
equal_image.save("outputs/output_equal.jpg")

thresh = thresholding(gray, 87)

thresh_image = image_from_matrix(thresh)
thresh_image.save("outputs/output_thresh.jpg")