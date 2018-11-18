---
id: doc5
title: Funciones
---

nadie quiere correr su codigo en una sola funcion (bueno es una mala practica) los programas deben ser creados de forma modular para que pueda ser utilizado otra ves y tambien reutilizar codigo.

toda funcion se delcara con la palabra `funcion` seguida por `:` y el `tipo de dato` y al final el id de la funcio que siempre se inicializa `~<ID>` y la tipica estrucutra de parentesis y corchetes

## Parametros

los tipos de datos soportados como parametros son solo enteros y decimales.
y son pasados como si fueras a declarar una variable pero sin la palabra var

## tipos de retorno

todas las funciones pueden generar un void donde solo queires que corra mas codigo, las funciones que regresan valores es para que hagan calculos, este se puede hacer declarando el tipo de retorno de dato que son enteros y deicmales, se tiene que declarar la palabra regresar para decir que valor quieres regresar.

### ejemplo void

```cpp
funcion : void ~print(&t : entero){
  si(&t>=1){
    imprimir &t;
    ~print(&t-1);
    imprimir &t;
  }
}
```

### ejemplo entero

```cpp
funcion : entero ~uno(&juan : entero, &pancho : entero){
  var &k : decimal;

  &k = 1 + 2 - -3 * (-3.0 - 4 + 5);

  si(&juan < &pancho){
    imprimir &i;
  } sino {
    imprimir &j;
  }

  regresar &i;
}
```

### ejemplo decimal

```cpp
funcion : decimal ~cero(){
  regresar 0.0;
}
```

## Recursion

soporta la recursion se funciones por ejemplo el factorial

```cpp
funcion : entero ~factorial(&ii : entero){
  var &tmp : entero;

  si(&ii >= 1){
    &tmp = &ii*~factorial(&ii-1);
  }sino{
    &tmp = 1;
  }

  regresar &tmp;
}
```
