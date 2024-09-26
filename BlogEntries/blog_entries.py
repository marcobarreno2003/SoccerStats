import os
from datetime import datetime

def create_blog_entry():
    # Solicitar detalles de la entrada
    title = input("Título de la entrada: ")
    content = input("Escribe el contenido de la entrada: ")
    
    # Crear la estructura de la entrada
    current_date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{current_date}-{title.replace(' ', '_')}.md"
    entry_content = f"# {title}\n\n**Fecha:** {current_date}\n\n{content}\n"

    # Guardar la entrada en un archivo .md
    blog_directory = 'blog_entries'
    if not os.path.exists(blog_directory):
        os.makedirs(blog_directory)
    
    with open(os.path.join(blog_directory, filename), 'w', encoding='utf-8') as file:
        file.write(entry_content)
    
    print(f"Entrada '{title}' guardada como {filename} en {blog_directory}/")

if __name__ == "__main__":
    create_blog_entry()
