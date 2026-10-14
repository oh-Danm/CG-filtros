# Programa de aplicação de filtros em uma imagem

## Sobre
Esse programa em python permite com que você selecione uma imagem e aplique diversos filtros nela.

## Funcionamento
Para executar o programa basta compilá-lo com o python3 instalado com o comando:

```
python3 <nome-do-arquivo(photo.py)>
```

*Nota: o código foi feito na versão 3.10.12 do Python, então verifique se sua versão do Python é compatível.*

### Execução
Ao executar, o programa e irá pedir o nome da imagem, você pode digitar o nome da imagem somente, se ela estiver no mesmo diretório do programa ou você pode indicar um caminho para a imagem.

```
Digite o nome da imagem de input: <nome-da-imagem>
```

##### *Nota: o programa reconhece múltiplos formatos de imagem, porém não permite imagens animadas.*



Depois, o programa pede para digitar o caminho para a saída do arquivo com o filtro aplicado, o programa não altera a imagem original, você pode opta por gerar os arquivos no diretório que o programa estiver ao apertar enter sem digitar nada.

```
Digite o caminho para o arquivo de output: <caminho-para-gerar-imagem>
```

E por fim, o programa abrirá um "menu" para selecionar o filtro que deseja aplicar.

```
Escolha o a operação a ser realizada:
1-Histograma
2-Escala de cinza
3-Limiarizar
4-Equalizar
5-Realçar
6-Bordas
7-Sobel
8-Prewitt
9-Emboss
10-Motion blur
11-Média
12-Mediana
13-Dilatação
14-Erosão
15-Abertura
16-Fechamento
17-Sair
```

Basta então selecionar o filtro desejado que o programa irá gerar uma imagem com o filtro aplicado no caminho especificado.

##### *Obs.: por conta do algoritmo utilizado, os filtros só podem ser utilizados em imagens em escala de cinza, felizmente, a imagem já é convertida em escala de cinza automaticamente, porém o resultado não é uma imagem com cores.*