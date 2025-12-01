from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL.shaders import compileProgram, compileShader


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
