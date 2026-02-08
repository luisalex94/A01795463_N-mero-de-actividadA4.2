Proyecto: Cálculo de estadísticas básicas desde archivos de texto

Este repositorio contiene una solución en Python para leer archivos de texto con valores numéricos (uno por línea), detectar tokens inválidos y calcular estadísticas descriptivas básicas (media, mediana, moda, varianza muestral y desviación estándar).

Archivos importantes

- `Actividad1/compute_statistics.py`: script principal. Ejecutarlo así:

```bash
python Actividad1/compute_statistics.py <ruta_al_archivo_de_entrada>
```

El script imprimirá los resultados por consola y escribirá un archivo `StatisticsResults.txt` en el mismo directorio que el archivo de entrada.

Notas de comportamiento

- Tokenización: el programa considera que cada línea del archivo representa un elemento (se limpia con `strip()`). Si una línea no es un número válido, se registra como "invalid token" y la ejecución continúa.
- Parseo numérico: intenta convertir a `int` primero (por ejemplo, `3.00` se tratará como `3`). Si no es posible, usa `float`.
- Moda: si hay un empate a la máxima frecuencia, se devuelve el valor que aparece primero en el archivo (política determinista).
- Salida: para evitar notación científica en números muy grandes, la salida convierte floats enteros a enteros y formatea con hasta 12 decimales, eliminando ceros finales.

Requisitos

- Python 3.6+
- No se requieren librerías externas; solo usa la biblioteca estándar.
