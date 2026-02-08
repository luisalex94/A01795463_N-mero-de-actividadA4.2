## Actividad 4.2

### Programa 1

Este programa lee línea por línea y calcula sus estadísticas.

Archivos importantes

- `Actividad4.2/Programa1/compute_statistics.py`: script principal. Ejecutarlo así:

```bash
python Actividad1/compute_statistics.py <ruta_al_archivo_de_entrada>
```

El script imprimirá los resultados por consola y escribirá un archivo `StatisticsResults.txt` en el mismo directorio que el archivo de entrada.

Notas de comportamiento

- Tokenización: el programa considera que cada línea del archivo representa un elemento (se limpia con `strip()`). Si una línea no es un número válido, se registra como "invalid token" y la ejecución continúa.
- Parseo numérico: intenta convertir a `int` primero (por ejemplo, `3.00` se tratará como `3`). Si no es posible, usa `float`.
- Moda: si hay un empate a la máxima frecuencia, se devuelve el valor que aparece primero en el archivo (política determinista).
- Salida: para evitar notación científica en números muy grandes, la salida convierte floats enteros a enteros y formatea con hasta 12 decimales, eliminando ceros finales.

### Programa 2

Este programa convierte números enteros leídos desde un archivo a sus representaciones en binario y hexadecimal usando algoritmos básicos (no se emplean `bin()` ni `hex()` internamente).

Archivos importantes

- `Actividad4.2/Programa2/convert_numbers.py`: script principal. Ejecutarlo así:

```bash
python Actividad4.2/Programa2/convert_numbers.py <ruta_al_archivo_de_entrada>
```

Notas de comportamiento

- Salida por consola y archivo `ConvertionResults.txt` en el directorio de ejecución. Cada línea tiene el formato: `indice<TAB>valor<TAB>binario<TAB>hex`.
- Datos inválidos se reportan en consola y aparecen como `#VALUE!` en el archivo de resultados; la ejecución continúa.
- Los enteros negativos se representan en complemento a dos de 32 bits para la salida binaria y hexadecimal (ej.: `-39` → binario 32-bit y hex `FFFFFFD9`).
- Escalabilidad: el procesamiento se realiza en streaming (línea a línea) para soportar archivos de cientos o miles de elementos.
- Tiempo: al final de la ejecución se muestra y escribe en el archivo el tiempo transcurrido para el cálculo.

Requisitos

- Python 3.6+
- No se requieren librerías externas; solo usa la biblioteca estándar.
