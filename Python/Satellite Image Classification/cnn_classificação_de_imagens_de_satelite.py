# -*- coding: utf-8 -*-
"""CNN - Classificação de imagens de satelite.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1m2YY_n0WwH0qoRnq8023PD1ZFmSxeo03

# Rede Neural Convolucional - Classificação de imagens de Satélite

![](https://as1.ftcdn.net/v2/jpg/04/74/61/94/1000_F_474619433_0aVlKtdw2H3g6rYg4P7b2PzkKxq6IYza.jpg)

**Descrição** 

Conjunto de dados de classificação de imagem de satélite-RSI-CB256, este conjunto de dados tem 4 classes diferentes misturadas de sensores e instantâneo do mapa do google.



**Conteúdo**

Os últimos anos testemunharam um grande progresso na interpretação de imagens de sensoriamento remoto (RS) e suas amplas aplicações. Com as imagens RS se tornando mais acessíveis do que nunca, há uma demanda crescente pela interpretação automática dessas imagens. Nesse contexto, os conjuntos de dados de referência servem como pré-requisitos essenciais para desenvolver e testar algoritmos de interpretação inteligentes. Depois de revisar os conjuntos de dados de referência existentes na comunidade de pesquisa de interpretação de imagens RS, este artigo discute o problema de como preparar eficientemente um conjunto de dados de referência adequado para interpretação de imagens RS. Especificamente, primeiro analisamos os desafios atuais de desenvolver algoritmos inteligentes para interpretação de imagens RS com investigações bibliométricas. Em seguida, apresentamos a orientação geral sobre como criar conjuntos de dados de referência de maneira eficiente. Seguindo a orientação apresentada, também fornecemos um exemplo de construção de conjunto de dados de imagem RS, ou seja, Million-AID, um novo conjunto de dados de referência de grande escala contendo um milhão de instâncias para classificação de cena de imagem RS. Vários desafios e perspectivas na anotação de imagens RS são finalmente discutidos para facilitar a pesquisa na construção de conjuntos de dados de referência. Esperamos que este artigo forneça à comunidade RS uma perspectiva geral sobre a construção de conjuntos de dados de imagens práticos e em larga escala para pesquisas futuras, especialmente as baseadas em dados.


**Reconhecimentos**

Conjuntos de dados anotados para interpretação de imagens RS
A interpretação de imagens RS vem desempenhando um papel cada vez mais importante em uma grande diversidade de aplicações e, portanto, tem atraído notáveis atenções de pesquisa. Consequentemente, vários conjuntos de dados foram construídos para avançar no desenvolvimento de algoritmos de interpretação para imagens RS. Cobrindo a literatura publicada na última década, realizamos uma revisão sistemática dos conjuntos de dados de imagens RS existentes sobre o atual fluxo principal de tarefas de interpretação de imagens RS, incluindo classificação de cena, detecção de objetos, segmentação semântica e detecção de alterações.

- Aprendizado Profundo, Imagem de Satélite
"""

import cv2
import keras
import numpy as np
import tensorflow as tf 
import seaborn as sns
import matplotlib.pyplot as plt

from tensorflow.keras import layers

from google.colab import drive
drive.mount('/content/drive')

# Versão CUDA
# NVIDIA

print("Versão Tensorflow-GPU", tf.__version__)
gpu = len(tf.config.list_physical_devices('GPU'))>0
print("GPU está", "disponivel" if gpu else "Não disponivel")
print()
!nvidia-smi

# Dataset - imagens
img_total = "data"

# Pré-processamento dataset

data_train = tf.keras.preprocessing.image_dataset_from_directory(img_total,
                                                                image_size = (64, 64),
                                                                label_mode = "categorical",
                                                                batch_size=32,
                                                                validation_split=0.20,
                                                                seed = 42,
                                                                subset="training")
print()

data_test = tf.keras.preprocessing.image_dataset_from_directory(img_total,
                                                                image_size = (64,64),
                                                                label_mode = "categorical",
                                                                batch_size = 32,
                                                                seed = 42,
                                                                validation_split = 0.20,
                                                                subset = "validation"
                                                                )

# Classes das imagens

label_classe = data_train.class_names
label_classe

imag1 = cv2.imread("/content/drive/MyDrive/Machine learning e deep learning/CNN - Projetos/Satellite Image Classification/data/desert/desert(1007) (1).jpg")
imag2 = cv2.imread("/content/drive/MyDrive/Machine learning e deep learning/CNN - Projetos/Satellite Image Classification/data/green_area/Forest_1488.jpg")
plt.imshow(imag1)

plt.imshow(imag2)

# Visualizando dados de treino

plt.figure(figsize=(20,14))

for img, x in data_train.take(1):
  
  for i in range(16):
    plt.subplot(6,3,i+1)
    plt.imshow(img[i].numpy().astype("uint8"))
    plt.title(label_classe[tf.argmax(x[i])]) 
    plt.axis("off")

# Modelo CNN
# Rede neural pré treinada
# Um modelo de classificação de imagem Keras, opcionalmente carregado com pesos pré-treinados no ImageNet.

model_cnn = tf.keras.applications.EfficientNetB5(include_top=False)
model_cnn.trainable = False

# Entrada da rede neural 

input_s = tf.keras.Input(shape=(64,64,3))

x = model_cnn(input_s)
x = layers.GlobalAveragePooling2D()(x)

output_s = layers.Dense(4, activation="softmax")(x)
model_cnn = tf.keras.Model(input_s, output_s)
model_cnn.summary()

# Otimizador do modelo 
model_cnn.compile(
    loss = tf.keras.losses.categorical_crossentropy,
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001),
    metrics = ["accuracy"]
)

# Fit rede neural
model_fit_hit = model_cnn.fit(data_train,
             epochs=105,
             steps_per_epoch = len(data_train),
             validation_data = data_test,
             validation_steps = len(data_test))

# Avaliação do modelo
evaluation_model = model_cnn.evaluate(data_test)

# Accuarcy CNN
print(f"Accuarcy CNN: {evaluation_model[1] * 100 : 0.2f} %")

# Avaliação do modelo
plt.plot(model_fit_hit.history['loss'], model_fit_hit.history["val_loss"])
plt.title('Model Loss Progress During Training')
plt.xlabel('Epoch')
plt.ylabel('Training and Validation Loss')
plt.legend(['Training Loss']);

plt.plot(model_fit_hit.history['accuracy'], model_fit_hit.history["val_accuracy"])
plt.title('Model accuracy During Training')
plt.xlabel('Epoch')
plt.ylabel('Training and accuracy')
plt.legend(['Accuracy', "val_accuracy"]);

# Previsão das imagens com dados test
img_pred = model_cnn.predict(data_test)
img_pred

# Previsão das imagens 

plt.figure(figsize=(16,16))

for img, x in data_test.take(1):
  for i in range(18):
    plt.subplot(6,3,i+1)
    plt.imshow(img[i].numpy().astype("uint8"))
    plt.title(f"Prediction: {label_classe[tf.argmax(img_pred[i])]} \nOriginal : {label_classe[tf.argmax(x[i])]}")
    plt.subplots_adjust(top = 1.25)
    plt.axis("off")

"""# **Rede neural segundo modelo**"""

# Modelo 02

# Treinamento do modelo
model_cnn.trainable = True
for layer in model_cnn.layers[:-3]:
  model_cnn.trainable = False

# Compilando modelo
model_cnn.compile(
    loss = tf.keras.losses.categorical_crossentropy,
    optimizer = tf.keras.optimizers.Adam(learning_rate= 0.001),
    metrics = ["accuracy"])

# Súmario da CNN
model_cnn.summary()

# Rodando rede neural
model_fit_hist2 = model_cnn.fit(
    data_train,
    epochs = 105,
    steps_per_epoch = len(data_train),
    validation_data = data_test,
    validation_steps = len(data_test))

# Previsão das imagens com dados test
img_pred2 = model_cnn.predict(data_test)
img_pred2

# Avaliação do modelo
evaluation_model2 = model_cnn.evaluate(data_test)
evaluation_model2

# Accuarcy CNN
print(f"Accuarcy CNN 2: {evaluation_model2[1] * 100 : 0.2f} %")

# Previsão das imagens com dados test
img_pred2 = model_cnn.predict(data_test)
img_pred2

# Previsão das imagens geral
plt.figure(figsize=(16,16))

for image, label in data_test.take(1):
  for i in range(18):
    plt.subplot(6,3,i+1)
    plt.imshow(image[i].numpy().astype("uint8"))
    plt.title(f"Prediction: {label_classe[tf.argmax(img_pred2[i])]} \nOriginal : {label_classe[tf.argmax(label[i])]}")
    plt.subplots_adjust(top = 1.25)
    plt.axis("off")

# Salvando modelo CNN
CNN = model_cnn.save('satelite_imgens_CNN.h5')
CNN

