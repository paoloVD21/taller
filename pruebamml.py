import requests
import json
import subprocess

# 1. Función para generar historias de usuario
def generar_historias_usuario(nombre_proyecto, descripcion, token):
    prompt_hu = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Dame historias de usuario enumeradas con HU y el número secuencial para un proyecto de software llamado '{nombre_proyecto}' y con la siguiente descripcion '{descripcion}'. "
                    "Con la estructura: Como, Quiero, Para. No le des formato a la respuesta. Ni uses lenguaje tecnico. Usa lenguaje de usuario"
                )
            }
        ]
    }

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps(prompt_hu)
    )

    if response.status_code == 200:
        data = response.json()
        historias = data['choices'][0]['message']['content']
        return historias
    else:
        raise Exception(f"Error al generar historias: {response.status_code} {response.text}")


# 2. Función para generar diagrama de flujo en Markdown (Mermaid) basado en historias
def generar_diagrama_de_flujo(historia_usuario_texto, token):
    prompt_diagrama = (
        "Genera un solo diagrama de flujo donde estén todos los usuarios en ese mismo diagrama usando la sintaxis Markdown de Mermaid basado en las siguientes historias de usuario:\n\n"
        f"{historia_usuario_texto}\n\n"
        "El diagrama debe mostrar el flujo principal de acciones y decisiones descritas en las historias, "
        "incluyendo un solo inicio, pasos de cada uno de los actores, decisiones y finalización. Usa nodos claros y conecta con flechas para mostrar el flujo.\n\n"
        "Devuelve sólo el bloque de código con sintaxis Mermaid listo para copiar y pegar, sin texto adicional ni explicaciones.\n\n"
        "Ejemplo de formato:\n"
        "Ten encuenta no empezar con backticks ni terminar con bacticks, ni empezar con la palabra mermaid\n"
        "flowchart TD\n"
        "    A[Inicio] --> B[Primer paso]\n"
        "    B --> C{¿Decisión?}\n"
        "    C -->|Sí| D[Acción 1]\n"
        "    C -->|No| E[Acción 2]\n"
        "    D --> F[Fin]\n"
        "    E --> F[Fin]\n"
    )

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({
            "model": "meta-llama/llama-3.3-8b-instruct:free",
            "messages": [{"role": "user", "content": prompt_diagrama}]
        })
    )

    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        raise Exception(f"Error en la petición: {response.status_code} {response.text}")


# 3. Función para generar la imagen a partir del código Mermaid
def generar_imagen_mermaid():
    # Usa la ruta completa a mmdc.cmd
    ruta_mmdc = r"C:\Program Files\nodejs\mmdc.cmd"  # Modifica <TuUsuario> con tu nombre de usuario

    # Ejecutar Mermaid CLI (mmdc) para generar la imagen
    result = subprocess.run([ruta_mmdc, "-i", "diagram.mmd", "-o", "diagram.png"])

    if result.returncode == 0:
        print("Imagen diagram.png generada correctamente.")
    else:
        print("Error al generar la imagen.")

def generar_diagrama_clases(descripcion_proyecto, token):
    prompt_diagrama_clases = (
        f"Genera un diagrama de clases en sintaxis Mermaid para un proyecto de software con la siguiente descripción:\n\n"
        f"{descripcion_proyecto}\n\n"
        "Incluye las clases principales, sus atributos y métodos, y las relaciones (herencia, asociación) entre ellas.\n"
        "Devuelve sólo el bloque de código Mermaid para diagrama de clases, sin backticks ni texto adicional.\n\n"
        "Ejemplo de sintaxis Mermaid para diagrama de clases:\n"
        "classDiagram\n"
        "    class Usuario {\n"
        "        +nombre\n"
        "        +email\n"
        "        +login()\n"
        "    }\n"
        "    class Producto {\n"
        "        +id\n"
        "        +nombre\n"
        "        +precio\n"
        "    }\n"
        "    Usuario <|-- Cliente\n"
        "    Usuario <|-- Administrador\n"
        "    Cliente --> Producto : compra\n"
    )
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({
            "model": "meta-llama/llama-3.3-8b-instruct:free",
            "messages": [{"role": "user", "content": prompt_diagrama_clases}]
        })
    )
    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        raise Exception(f"Error al generar diagrama de clases: {response.status_code} {response.text}")

def generar_diagrama_er(descripcion_proyecto, token):
    prompt_diagrama_er = (
        f"Genera un diagrama entidad-relación (ER) en sintaxis Mermaid para un proyecto de software con la siguiente descripción:\n\n"
        f"{descripcion_proyecto}\n\n"
        "Incluye las entidades principales, sus atributos y las relaciones entre ellas con cardinalidades.\n"
        "Devuelve sólo el bloque de código Mermaid para diagrama ER, sin backticks ni texto adicional.\n\n"
        "Ejemplo de sintaxis Mermaid para diagrama ER:\n"
        "erDiagram\n"
        "    CLIENTE ||--o{ PEDIDO : realiza\n"
        "    PEDIDO ||--|{ DETALLE_PEDIDO : contiene\n"
        "    PRODUCTO ||--o{ DETALLE_PEDIDO : incluye\n"
        "    CLIENTE {\n"
        "        string nombre\n"
        "        string direccion\n"
        "    }\n"
        "    PRODUCTO {\n"
        "        string nombre\n"
        "        float precio\n"
        "    }\n"
    )
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({
            "model": "meta-llama/llama-3.3-8b-instruct:free",
            "messages": [{"role": "user", "content": prompt_diagrama_er}]
        })
    )
    if response.status_code == 200:
        data = response.json()
        return data['choices'][0]['message']['content']
    else:
        raise Exception(f"Error al generar diagrama ER: {response.status_code} {response.text}")



def main():
    token = "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"
    nombre_proyecto = input("Ingresa el nombre del proyecto de software: ")
    descripcion_proyecto = input("Ingresa una breve descripción del proyecto: ")

    print("\nGenerando historias de usuario...\n")
    historias = generar_historias_usuario(nombre_proyecto, descripcion_proyecto, token)
    print("Historias de usuario generadas:\n")
    print(historias)

    print("\nGenerando diagrama de flujo basado en las historias...\n")
    diagrama = generar_diagrama_de_flujo(historias, token)
    print("Diagrama Mermaid generado:\n")
    print(diagrama)

    # Guardar el contenido de la variable 'diagrama' en un archivo de texto
    with open("diagrama_flujo.txt", "w", encoding="utf-8") as archivo:
        print(diagrama, file=archivo) 

    # Guardar el código Mermaid en un archivo sin los backticks triples ni la palabra "mermaid"
    with open("diagram.mmd", "w") as f:
        f.write(diagrama)

    # Llamar la función para generar la imagen
    generar_imagen_mermaid()


if __name__ == "__main__":
    main()
