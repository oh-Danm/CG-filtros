from PIL import Image
from matplotlib import pyplot as plt 
import math as math

def image_from_matrix(matrix):
    new = Image.new('RGB', (len(matrix[0]), len(matrix)))
    flat = [pixel for row in matrix for pixel in row]
    new.putdata(flat)

    return new

def choose_kernel(opt, size = 3):
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
    elif opt == 3:
        kernel = [
            [-1, 0, 1],
            [-2, 0, 2],
            [-1, 0, 1]
        ]
        return kernel
    elif opt == 4:
        kernel = [
            [-1, -2, -1],
            [0, 0, 0],
            [1, 2, 1]
        ]
        return kernel
    elif opt == 5:
        kernel = [
            [-1, 0, 1],
            [-1, 0, 1],
            [-1, 0, 1]
        ]
        return kernel
    elif opt == 6:
        kernel = [
            [-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1]
        ]
        return kernel
    elif opt == 7:
        kernel = [
            [-2, -1, 0],
            [-1, 1, 1],
            [0, 1, 2]
        ]
        return kernel
    elif opt == 8:
        kernel = [[0 for _ in range(size)] for _ in range(size)]
        for i in range(0, size):
            kernel[i][i] = 1/size
        return kernel

def histograma(imagem):
    h = [0]*256

    for i in range(len(imagem)):
        for j in range(len(imagem[0])):
            pos = imagem[i][j][0]
            h[pos] = h[pos]+1

    return h

def grayify(r,g,b):
    s = (r + g + b) // 3
    return (s, s, s)

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

def apply_kernel(imagem, kernel, k = 3, clamp = True):
    width, height = len(imagem[0]), len(imagem) 
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

def sobel_prewitt(imagem, prewitt = True):
    width, height = len(imagem[0]), len(imagem) 

    if prewitt:
        kernelx = choose_kernel(6)
        kernely = choose_kernel(5)
    else:
        kernelx = choose_kernel(4)
        kernely = choose_kernel(3)

    gx = apply_kernel(imagem, kernelx, clamp=False)
    gy = apply_kernel(imagem, kernely, clamp=False)

    output = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            mag = math.sqrt(gx[i][j][0]**2 + gy[i][j][0]**2)
            coiso = abs(max(0, min(255, round(mag))))

            output[i][j] = (coiso, coiso, coiso)

    return output

def mediana_dilate_erode(imagem, size, opt):
    width, height = len(imagem[0]), len(imagem) 
    border = size//2

    output = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]
    for x in range(border, height-border):
        for y in range(border, width-border):
            neighbour = []
            for i in range(size):
                for j in range(size):
                    neighbour.append(imagem[x+i-border][y+j-border][0])

            if opt == 0:
                neighbour.sort()
                mid = len(neighbour)//2
                coiso = neighbour[mid]
            elif opt == 1:
                coiso = max(neighbour)
            else:
                coiso = min(neighbour)

            output[x][y] = (coiso, coiso, coiso)

    return output

def open_close(imagem, size, open = True):
    if open:
        return mediana_dilate_erode(mediana_dilate_erode(imagem, size, 2), size, 1)
    else:
        return mediana_dilate_erode(mediana_dilate_erode(imagem, size, 1), size, 2)

print("Digite o nome da imagem de input: ")
name = str(input())

img = Image.open(name)
width, height = img.size
pixels = img.load()
imagem = [[pixels[x, y] for x in range(width)] for y in range(height)]

for i in range(height):
    for j in range(width):
        r, g, b = imagem[i][j]
        imagem[i][j] = grayify(r, g, b)

gray_image = image_from_matrix(imagem)
pixels = gray_image.load()
gray = [[pixels[x, y] for x in range(width)] for y in range(height)]

print("Digite o caminho para o arquivo de output: ")
path_output = str(input())

opt = 0

while True:
    print("Escolha o a operação a ser realizada:")
    print("1-Histograma")
    print("2-Escala de cinza")
    print("3-Limiarizar")
    print("4-Equalizar")
    print("5-Realçar")
    print("6-Bordas")
    print("7-Sobel")
    print("8-Prewitt")
    print("9-Emboss")
    print("10-Motion blur")
    print("11-Média")
    print("12-Mediana")
    print("13-Dilatação")
    print("14-Erosão")
    print("15-Abertura")
    print("16-Fechamento")
    print("17-Sair")

    opt = int(input())

    if opt == 1:
        h = histograma(gray)
        plt.bar(range(256), h)
        plt.title("Histograma")
        plt.show()

    elif opt == 2:
        gray_image.save(path_output+"output_gray.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 3:
        print("Digite o threshhold: ")
        threshold = int(input())
        thresh = thresholding(gray, threshold)
        thresh_image = image_from_matrix(thresh)
        thresh_image.save(path_output+"output_thresh.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 4:
        equal = equalizar(gray)
        equal_image = image_from_matrix(equal)
        equal_image.save(path_output+"output_equal.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 5:
        kernel = choose_kernel(1)
        sharpen = apply_kernel(gray, kernel)
        sharp_image = image_from_matrix(sharpen)
        sharp_image.save(path_output+"output_sharp.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 6:
        kernel = choose_kernel(2)
        border = apply_kernel(gray, kernel)
        border_image = image_from_matrix(border)
        border_image.save(path_output+"output_border.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 7:
        sob = sobel_prewitt(gray, prewitt=False)
        sob_image = image_from_matrix(sob)
        sob_image.save(path_output+"output_sobel.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 8:
        prewitt = sobel_prewitt(gray)
        prewitt_image = image_from_matrix(prewitt)
        prewitt_image.save(path_output+"output_prewitt.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 9:
        kernel = choose_kernel(7)
        emboss = apply_kernel(gray, kernel)
        emboss_image = image_from_matrix(emboss)
        emboss_image.save(path_output+"output_emboss.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 10:
        print("Digite a quantidade de motion blur (recomendado de 3 para cima): ")
        qtd = int(input())
        kernel = choose_kernel(8, size=qtd)
        motion_blur = apply_kernel(gray, kernel, k=qtd)
        motion_blur_image = image_from_matrix(motion_blur)
        motion_blur_image.save(path_output+"output_motion_blur.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 11:
        kernel = choose_kernel(0)
        soft = apply_kernel(gray, kernel)
        soft_image = image_from_matrix(soft)
        soft_image.save(path_output+"output_average.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 12:
        median = mediana_dilate_erode(gray, 3, 0)
        median_image = image_from_matrix(median)
        median_image.save(path_output+"output_median.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 13:
        thresh = thresholding(gray, 100)
        dilate = mediana_dilate_erode(thresh, 3, 1)
        dilate_image = image_from_matrix(dilate)
        dilate_image.save(path_output+"output_dilate.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 14:
        thresh = thresholding(gray, 100)
        erode = mediana_dilate_erode(thresh, 3, 2)
        erode_image = image_from_matrix(erode)
        erode_image.save(path_output+"output_erode.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 15:
        thresh = thresholding(gray, 100)
        opened = open_close(thresh, 3)
        opened_image = image_from_matrix(opened)
        opened_image.save(path_output+"output_open.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 16:
        thresh = thresholding(gray, 100)
        closed = open_close(thresh, 3, open=False)
        closed_image = image_from_matrix(closed)
        closed_image.save(path_output+"output_closed.jpg")
        print("Imagem salva com sucesso!")

    elif opt == 17:
        print("Tchau tchau!")
        break
