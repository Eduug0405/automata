import csv

def generar_csv(patrones):
    """Genera un archivo CSV con los patrones encontrados por el autómata."""
    filename = "patrones_automata.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Patrones"])  # Encabezado
        for patron in patrones:
            writer.writerow([patron])
    return filename
