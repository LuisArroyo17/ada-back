import matplotlib
matplotlib.use('Agg')  # Establece el backend no interactivo antes de importar pyplot
import matplotlib.pyplot as plt
import os

def generar_grafico(nombre, tiempos_por_codigo):
    tamaños_entrada = [5, 10, 15]

    img_folder = os.path.join("static", "img")
    os.makedirs(img_folder, exist_ok=True)

    plt.figure()
    for codigo_nombre, tiempos in tiempos_por_codigo.items():
        tamaños = tamaños_entrada[:len(tiempos)]
        plt.plot(tamaños, tiempos, marker='o', label=codigo_nombre)

    plt.xlabel("Tamaño de Entrada")
    plt.ylabel("Tiempo de Ejecución (segundos)")
    plt.title(f"Análisis de Tiempo - {nombre}")
    plt.legend()
    plt.grid(True)

    grafico_filename = f"{nombre}_grafico.png"
    grafico_path = os.path.join(img_folder, grafico_filename)
    plt.savefig(grafico_path)
    plt.close()
    return grafico_filename

def determinar_tiempos_de_ejecucion(codigos):
    import time

    tiempos = {}
    tamaños_entrada = [5, 10, 15]

    for nombre, contenido in codigos.items():
        tiempos[nombre] = []

        for tamaño in tamaños_entrada:
            start_time = time.time()

            try:
                local_vars = {}
                exec(contenido, {}, local_vars)
                if "solve" in local_vars:
                    local_vars["solve"](tamaño)
                else:
                    raise ValueError(f"No se encontró la función 'solve' en {nombre}")

                elapsed_time = time.time() - start_time
                tiempos[nombre].append(elapsed_time)

            except Exception as e:
                print(f"Error ejecutando {nombre} con entrada {tamaño}: {e}")
                tiempos[nombre].append(None)

    return tiempos
