import requests
import json
import subprocess

# 1. Generar historias de usuario
def generar_historias_usuario(nombre_proyecto, descripcion, token):
    prompt_hu = {
        "model": "meta-llama/llama-3.3-8b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Dame historias de usuario enumeradas con HU y el número secuencial para un proyecto de software llamado '{nombre_proyecto}' y con la siguiente descripcion '{descripcion}'. "
                    "Con la estructura: Como, Quiero, Para. No le des formato a la respuesta. Ni uses lenguaje tecnico."
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
        return data['choices'][0]['message']['content']
    else:
        raise Exception(f"Error al generar historias: {response.status_code} {response.text}")

# 2. Generar diagrama de flujo
def generar_diagrama_de_flujo(historia_usuario_texto, token):
    prompt_diagrama = (
        "Genera un solo diagrama de flujo donde estén todos los usuarios en ese mismo diagrama usando la sintaxis Markdown de Mermaid basado en las siguientes historias de usuario:\n\n"
        f"{historia_usuario_texto}\n\n"
        "El diagrama debe mostrar el flujo principal de acciones y decisiones descritas en las historias, "
        "incluyendo un solo inicio, pasos de cada uno de los actores, decisiones y finalización. Usa nodos claros y conecta con flechas para mostrar el flujo.\n\n"
        "Devuelve sólo el bloque de código con sintaxis Mermaid listo para copiar y pegar, sin texto adicional ni explicaciones.\n\n"
        "Ejemplo de formato:\n"
        "Ten en cuenta no empezar con backticks ni terminar con backticks, ni empezar con la palabra mermaid, además no uses paréntesis en dentro de la sintaxis\n"
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
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Error al generar diagrama de flujo: {response.status_code} {response.text}")

# 3. Generar diagrama de clases
def generar_diagrama_clases(texto, token):
    prompt = (
        "Genera un diagrama de clases en sintaxis Mermaid basado en el siguiente texto:\n\n"
        f"{texto}\n\n"
        "Incluye las siguientes características:\n"
        "- Clases con nombres claros.\n"
        "- Atributos con tipo y visibilidad (+ público, - privado, # protegido).\n"
        "- Métodos con parámetros y visibilidad.\n"
        "- Relaciones entre clases: herencia (<|--), asociación (--), composición (*--), agregación (o--).\n"
        "- Multiplicidades en las relaciones cuando corresponda.\n"
        "Ejemplo:\n"
        "Ten en cuenta no empezar con backticks ni terminar con backticks, ni empezar con la palabra mermaid, además no uses paréntesis en dentro de la sintaxis\n"
        "Adema siempre se empezara la primera linea con esta linea: classDiagram\n"
        "classDiagram\n"
        "    class Usuario {\n"
        "        +nombre: String\n"
        "        +login()\n"
        "    }\n"
        "    class Cliente {\n"
        "        +id: Int\n"
        "        +realizarCompra()\n"
        "    }\n"
        "    Usuario <|-- Cliente\n"
        "    Cliente *-- Pedido : realiza\n"
        "    Pedido o-- Producto : contiene\n"
    )
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({
            "model": "meta-llama/llama-3.3-8b-instruct:free",
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Error al generar diagrama de clases: {response.status_code} {response.text}")

# 4. Generar diagrama entidad-relación (ER)
def generar_diagrama_er(texto, token):
    prompt = (
        "Genera un diagrama entidad-relación (ER) en sintaxis Mermaid basado en el siguiente texto:\n\n"
        f"{texto}\n\n"
        "Por favor, sigue estas indicaciones para la sintaxis del diagrama ER en Mermaid:\n"
        "- Define entidades con sus atributos claramente.\n"
        "- Usa sólo los siguientes símbolos para las relaciones y cardinalidades:\n"
        "  || para 'uno y solo uno' (1)\n"
        "  |o para 'cero o uno' (0..1)\n"
        "  }o para 'cero o muchos' (0..*)\n"
        "  }| para 'uno o muchos' (1..*)\n"
        "- No uses flechas, símbolos con '>' ni otros símbolos no válidos en Mermaid ER.\n"
        "- No uses paréntesis ni el símbolo '&' en la sintaxis.\n"
        "- Devuelve sólo el código Mermaid listo para usar, sin backticks ni la palabra 'mermaid'.\n\n"
        "Ejemplo válido de diagrama ER Mermaid:\n"
        "erDiagram\n"
        "    CLIENTE {\n"
        "        int id\n"
        "        string nombre\n"
        "        string telefono\n"
        "    }\n"
        "    PEDIDO {\n"
        "        int id\n"
        "        date fecha\n"
        "    }\n"
        "    CLIENTE ||--o{ PEDIDO : realiza\n"
        "    PEDIDO }o--|| PRODUCTO : contiene\n"
    )

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {token}"},
        data=json.dumps({
            "model": "meta-llama/llama-3.3-8b-instruct:free",
            "messages": [{"role": "user", "content": prompt}]
        })
    )
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"Error al generar diagrama ER: {response.status_code} {response.text}")

# 5. Generar imagen PNG desde código Mermaid usando Mermaid CLI
def generar_imagen_mermaid(archivo_entrada, archivo_salida, ruta_mmdc=r"C:\Program Files\nodejs\mmdc.cmd"):
    result = subprocess.run([ruta_mmdc, "-i", archivo_entrada, "-o", archivo_salida])
    if result.returncode == 0:
        print(f"Imagen {archivo_salida} generada correctamente.")
    else:
        print(f"Error al generar la imagen {archivo_salida}.")

# Main integrando todo
def main():
    token = "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"
    nombre_proyecto = input("Ingresa el nombre del proyecto de software: ")
    descripcion_proyecto = input("Ingresa una breve descripción del proyecto: ")

    print("\nGenerando historias de usuario...\n")
    historias = generar_historias_usuario(nombre_proyecto, descripcion_proyecto, token)
    print(historias)

    print("\nGenerando diagrama de flujo...\n")
    diagrama_flujo = generar_diagrama_de_flujo(historias, token)
    print(diagrama_flujo)
    with open("diagram_flujo.mmd", "w", encoding="utf-8") as f:
        f.write(diagrama_flujo)
    generar_imagen_mermaid("diagram_flujo.mmd", "diagram_flujo.png")

    print("\nGenerando diagrama de clases...\n")
    diagrama_clases = generar_diagrama_clases(historias, token)
    print(diagrama_clases)
    with open("diagram_clases.mmd", "w", encoding="utf-8") as f:
        f.write(diagrama_clases)
    generar_imagen_mermaid("diagram_clases.mmd", "diagram_clases.png")

    print("\nGenerando diagrama ER...\n")
    diagrama_er = generar_diagrama_er(historias, token)
    print(diagrama_er)
    with open("diagram_er.mmd", "w", encoding="utf-8") as f:
        f.write(diagrama_er)
    generar_imagen_mermaid("diagram_er.mmd", "diagram_er.png")

if __name__ == "__main__":
    main()

