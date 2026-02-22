## Actividad 4.2

### Programa 1

Este programa lee línea por línea y calcula sus estadísticas.

Archivos importantes

- `Actividad4.2/Programa1/compute_statistics.py`: script principal. Ejecutarlo así:

```bash
python Actividad1/Programa1/compute_statistics.py <ruta_al_archivo_de_entrada>
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

### Programa 3

Este programa cuenta palabras distintas en un archivo y reporta su
frecuencia. Implementa el conteo con algoritmos básicos y escribe los
resultados en pantalla y en `WordCountResults.txt`.

Archivos importantes

- `Actividad4.2/Programa3/word_count.py`: script principal. Ejecutarlo así:

```bash
python Actividad4.2/Programa3/word_count.py <ruta_al_archivo_de_entrada>
```

Notas de comportamiento

- Tokenización: el programa separa por espacios (whitespace) y acepta
	tokens alfanuméricos como válidos; tokens inválidos se reportan en
	consola y se ignoran en el conteo.
- Salida: cada línea del archivo de resultados contiene `Word<TAB>Count`.
- Escalabilidad: el procesamiento es por streaming (línea a línea) y
	mantiene únicamente un diccionario de conteos en memoria (adecuado
	para cientos o miles de palabras).
- Tiempo: al final se muestra y escribe en el archivo el tiempo
	transcurrido para el procesamiento.

Requisitos

- Python 3.6+
- No se requieren librerías externas; solo usa la biblioteca estándar.


## Actividad 6.2

### Programa 1

#### Evaluación del código

##### Activar el ambiente virtual

```bash
# Debe estar en la base del repositorio.
source venv/bin/activate
```

##### Flake8

Para evaluar el código utilizando Flake8, se utiliza este comando:

```bash
# Debe estar en la base del repositorio.
flake8 Actividad6.2/Programa1/src/
```

##### PyLint

Para evaluar el código utilizando PyLint, se utiliza este comando:

```bash
# Debe estar en la base del repositorio.
pylint Actividad6.2/Programa1/src/
```

##### Tests

Para correr los tests, se utiliza este comando:

```bash
# Debe estar en la base del repositorio.
python -m unittest discover -s Actividad6.2/Programa1/test/unit/src -p "test_*.py" -v
```

##### Coverage tests

Para correr coverage, se utiliza este comando:

```bash
# Debe estar en la base del repositorio.
coverage run --source=Actividad6.2/Programa1/src -m unittest discover -s Actividad6.2/Programa1/test/unit/src -p "test_*.py" && coverage report -m
```

#### CLI del sistema de reservas (Actividad 6.2)

Este repositorio incluye un pequeño CLI para gestionar hoteles, clientes y
reservaciones usando archivos JSON como almacenamiento. El CLI está en
`Actividad6.2/Programa1/src/main.py` y acepta tres archivos de entrada
(hoteles, clientes, reservaciones) como argumentos posicionales o mediante
las opciones `--hotels`, `--customers` y `--reservations`.

Forma básica de ejecución (ejemplo usando archivos de `sample_data`):

```bash
cd Actividad6.2/Programa1
python3 -m src.main sample_data/hotels.json sample_data/customers.json sample_data/reservations.json
cd ../../

```

También se pueden pasar los archivos por nombre:

```bash
cd Actividad6.2/Programa1
python3 -m src.main \
  --hotels sample_data/hotels.json \
  --customers sample_data/customers.json \
  --reservations sample_data/reservations.json
cd ../../
```

Después de los archivos de entrada, se pueden ejecutar las siguientes
opciones/acciones. Para las operaciones que crean o modifican entidades se
espera un archivo JSON con un único objeto (ej.: un solo hotel o cliente).

Formato JSON mínimo (ejemplos):

- Hotel:

```json
{
	"hotel_id": 1,
	"name": "Hotel Central",
	"address": "Calle Falsa 123",
	"rooms": {"101": 2, "102": 2, "201": 3}
}
```

- Customer:

```json
{
	"customer_id": 1,
	"name": "Juan Perez",
	"email": "juan@example.com",
	"phone": "555-1234"
}
```

- Reservation:

```json
{
	"reservation_id": 1,
	"customer_id": 1,
	"hotel_id": 1,
	"room_number": "101",
	"start_date": "2026-03-01",
	"end_date": "2026-03-05"
}
```

Comandos y opciones disponibles

1. Hotels

	a. Create Hotel

		 - Opción: `--create-hotel <path>`
		 - Descripción: Crea un hotel leyendo un único objeto JSON desde `<path>`.
			 El objeto debe contener `hotel_id`, `name`, `address` y `rooms`.

		 - Ejemplo:

		 cd Actividad6.2/Programa1
		 python3 -m src.main sample_data/hotels.json \
			 sample_data/customers.json sample_data/reservations.json \
			 --create-hotel sample_data/new_hotel.json
		 cd ../../

	b. Delete Hotel

		 - Opción: `--delete-hotel <id>`
		 - Descripción: Borra el hotel con identificador `<id>` si existe. Imprime
			 si se borró o si no se encontró.

		 - Ejemplo: `--delete-hotel 2`

	c. Display Hotel information

		 - Opción: `--show-hotel <id>`
		 - Descripción: Muestra la representación JSON del hotel solicitado.

	d. Modify Hotel Information

		 - Opción: `--modify-hotel <path>`
		 - Descripción: Lee un objeto hotel desde `<path>` y reemplaza la entrada
			 existente con el mismo `hotel_id`. Imprime si se actualizó o no se
			 encontró.

	e. Reserve a Room

		 - Opción: `--create-reservation <path>`
		 - Descripción: Crea una reservación leyendo un objeto Reservation desde
			 `<path>` (debe incluir `reservation_id`, `customer_id`, `hotel_id`,
			 `room_number`, `start_date`, `end_date`). Devuelve éxito o fallo si
			 hay conflicto de fechas o referencias inválidas.

	f. Cancel a Reservation

		 - Opción: `--cancel-reservation <id>`
		 - Descripción: Cancela (borra) la reservación con id `<id>` si existe.

2. Customer

	a. Create Customer

		 - Opción: `--create-customer <path>`
		 - Descripción: Añade un cliente leyendo un único objeto Customer desde
			 `<path>` (campos mínimos: `customer_id`, `name`, `email`, `phone`).

	b. Delete a Customer

		 - Opción: `--delete-customer <id>`
		 - Descripción: Borra el cliente con id `<id>` si existe.

	c. Display Customer Information

		 - Opción: `--show-customer <id>`
		 - Descripción: Muestra la representación JSON del cliente solicitado.

	d. Modify Customer Information

		 - Opción: `--modify-customer <path>`
		 - Descripción: Lee un objeto Customer desde `<path>` y reemplaza la
			 entrada existente con el mismo `customer_id`.

3. Reservation

	a. Create a Reservation (Customer, Hotel)

		 - Opción: `--create-reservation <path>` (igual que 1.e)
		 - Descripción: Crea una reservación ligada a un cliente y un hotel. El
			 sistema valida que `customer_id` y `hotel_id` existan y que la habitación
			 no esté reservada en el rango de fechas indicado.

	b. Cancel a Reservation

		 - Opción: `--cancel-reservation <id>` (igual que 1.f)
		 - Descripción: Cancela la reservación indicada.

Notas adicionales

- El CLI intentará leer los tres archivos iniciales (hoteles, clientes,
	reservaciones). Si alguno no existe o contiene JSON inválido, el sistema
	lo reporta y continúa cuando es posible.
- Para operaciones que leen un objeto JSON (create/modify), si el JSON no es
	válido se imprimirá un error y el CLI devolverá código de salida 2.
- Después de ejecutar las acciones, el CLI imprime un resumen con los conteos
	actuales de hoteles, clientes y reservaciones.

