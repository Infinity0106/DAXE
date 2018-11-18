---
id: doc6
title: Dibujos
---

El valor adicional de este lenguaje es que puedes generar tus propias imagenes por medio de un lapiz que esta centrado en el centro de la pantalla.

el finalizar la ejecucion del programa, se creara un archivo con extension svg para poder tener tu dibujo por siempre, pero recureda que si lo corres otra ves se sobre escribira la imagen anterior asi que es recomendable cambiar el nombre del archivo al finalizar cada corrida

## Lapiz

### adelante

toma como parametros un numero entero o decimal para poder moverse. dependiendo donde este apuntando el angulo de rotacion se dibujara hacia adelante, tambien acepta numero negativos para dibujar hacia atras

```cpp
adelante 1;
```

### rotar

Toma como parametros un numero entero o decimal para poder apuntar a otro lado, son angulos de rotacion este rotara en contras de las manecillas del reloj

```cpp
rotar 20;
```

## Cuadrado

toma los siguientes parametros `cuadrado x, y, lado, color, grosor`

| parametro | valor                   |
| --------- | ----------------------- |
| x         | numero entero o decimal |
| y         | numero entero o decimal |
| lado      | numero entero o decimal |
| color     | string rgb format       |
| grosor    | numero entero o decimal |

### ejemplo

```cpp
cuadrado 100, 60, 19, rgb(10, 34, 255), 5;
```

## Circulo
tiene el siguiente formato `circulo x, y, radio, color, grosor` para poder dibujar un circulo

| parametro | valor                   |
| --------- | ----------------------- |
| x         | numero entero o decimal |
| y         | numero entero o decimal |
| radio     | numero entero o decimal |
| color     | string rgb format       |
| grosor    | numero entero o decimal |

### ejemplo
```cpp
circulo -100, -60, 10, rgb(10,34,23), 2;
```

## Triangulo
tiene el siguiente formato `triangulo x, y, base, altura, color, grosor` para poder dibujar un triangulo

| parametro | valor                   |
| --------- | ----------------------- |
| x         | numero entero o decimal |
| y         | numero entero o decimal |
| base      | numero entero o decimal |
| altura    | numero entero o decimal |
| color     | string rgb format       |
| grosor    | numero entero o decimal |

### ejemplo
```cpp
triangulo &j, 10, ~uno(60, ~tres(1,-3)), 5, rgb(10, 34, 255), 2;
```

## Texto
tiene el siguiente formato `texto x, y, texto, color, tamaño letra` para poder crear un label de texto
| parametro    | valor                        |
| ------------ | ---------------------------- |
| x            | numero entero o decimal      |
| y            | numero entero o decimal      |
| texto        | texto entre comillas simples |
| color        | string rgb format            |
| tamaño letra | numero entero o decimal      |

### ejemplo
```cpp
texto -100, 60, 'juancho', rgb(255,34,23), 24;
```
