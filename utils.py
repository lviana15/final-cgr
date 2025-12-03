from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import (
    GL_TEXTURE_2D, GL_RGBA, GL_UNSIGNED_BYTE, 
    GL_CLAMP_TO_EDGE, GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR, 
    GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, 
    glGenTextures, glBindTexture, glTexParameteri, glTexImage2D, glGenerateMipmap
)
from PIL import Image 


def load_shader(vertex_path, fragment_path):
    """
    Lê os arquivos, compila e linka o programa de shader.
    Retorna o ID do programa OpenGL ou lança erro.
    """
    with open(vertex_path, "r") as f:
        vertex_src = f.read()

    with open(fragment_path, "r") as f:
        fragment_src = f.read()

    try:
        shader_vertex = compileShader(vertex_src, GL_VERTEX_SHADER)
    except RuntimeError as e:
        print(f"ERRO ao compilar Vertex Shader ({vertex_path}):\n{e}")
        raise

    try:
        shader_fragment = compileShader(fragment_src, GL_FRAGMENT_SHADER)
    except RuntimeError as e:
        print(f"ERRO ao compilar Fragment Shader ({fragment_path}):\n{e}")
        raise

    shader_program = compileProgram(shader_vertex, shader_fragment)

    return shader_program


def load_texture(texture_path):
    """
    Carrega uma imagem usando Pillow, envia os dados para uma textura OpenGL.
    Retorna o ID da textura.
    """
    # 1. Abre a imagem
    img = Image.open(texture_path)
    img_data = img.convert("RGBA").tobytes() # Converte para formato RGBA
    
    # 2. Gera a ID de Textura no OpenGL
    texture_id = glGenTextures(1)
    
    # 3. Faz o bind e configura a textura
    glBindTexture(GL_TEXTURE_2D, texture_id)
    
    # Parâmetros de Wrapping (Repetição)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    
    # Parâmetros de Filtering (Resolução)
    
    # 3.1. Filtro de Magnificação (Objeto Perto) - SÓ ACEITA GL_LINEAR ou GL_NEAREST
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR) # <--- CORRIGIDO
    
    # 3.2. Filtro de Minificação (Objeto Longe) - Aceita Mipmaps
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR) 
    
    # 4. Envia os dados da imagem para a GPU
    glTexImage2D(
        GL_TEXTURE_2D, 
        0, 
        GL_RGBA, 
        img.width, 
        img.height, 
        0, 
        GL_RGBA, 
        GL_UNSIGNED_BYTE, 
        img_data
    )
    
    # 5. Gera Mipmaps
    glGenerateMipmap(GL_TEXTURE_2D)
    
    # 6. Desfaz o bind e retorna o ID
    glBindTexture(GL_TEXTURE_2D, 0)
    return texture_id