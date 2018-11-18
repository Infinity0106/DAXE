---
id: doc2
title: Variables
---

todas las variables son declaradas con `&<ID>` seguidas por `:` y el `tipo de dato`,
toda variable debe ser inicializada si no mercara error en variable no inicializada

## Globales

las variables globales pueden ser accesadas por todo el programa y se delcaran de esta manaera

```cpp
programa "prueba";

var &global : entero; //VARIABLE GLOBAL

dibujar(){

}
```

## Locales

las variables locales solo son accesadas en el scope donde se encuetnren ya sea en la funcion dibujar o en los modulos delcarados

```cpp
programa "prueba";

dibujar(){
  var &local : decimal; // VARIABLE LOCAL
}
```

## Tipos de dato
| Nombre    | Ejemplo                        | Valor  |
| --------- | ------------------------------ | ------ |
| entero    | var &entero : entero;          | 1      |
| decimal   | var &decimal : decimal;        | 3.1416 |
| entero[]  | var &ArrEntero : entero[10];   | 1      |
| decimal[] | var &ArrDecimal : decimal[10]; | 3.1416 |

## Accessar arreglos

Los arreglos son conjutos de valores enteros en una sola variable 

```cpp
var &arr : decimal[10];

//INICIALIZACION
&arr[2] = 3.1;

imprimir &arr[2];
```