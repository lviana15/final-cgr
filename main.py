# main.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
import glm
import ctypes

from utils import load_shader, load_texture # <--- Importando load_texture
from meshes import generate_sphere
from planet import Planet # <--- Importando a classe Planet


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sistema Solar - Fase 1: Esfera com Textura")

    glViewport(0, 0, 800, 600)
    glEnable(GL_DEPTH_TEST)

    try:
        shader = load_shader("shaders/basic.vert", "shaders/basic.frag")
        glUseProgram(shader)
    except Exception as e:
        print(e)
        pygame.quit()
        return

    # Carregar Texturas (Certifique-se que as imagens estão em 'assets/textures/')
    try:
        sun_tex = load_texture("assets/textures/sun.png")
        earth_tex = load_texture("assets/textures/earth.jpg")
        moon_tex = load_texture("assets/textures/moon.jpg")
    except FileNotFoundError as e:
        print(f"ERRO: Não foi possível carregar a textura. Verifique o caminho: {e}")
        pygame.quit()
        return

    # Gerar Malha da Esfera
    sphere_verts, sphere_inds = generate_sphere(radius=1.0, stacks=30, sectors=30)

    # Configurar Buffers (VAO, VBO, EBO)
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1)

    glBindVertexArray(VAO)

    # VBO: Envia os dados dos vértices
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, sphere_verts.nbytes, sphere_verts, GL_STATIC_DRAW)

    # EBO: Envia os índices
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(
        GL_ELEMENT_ARRAY_BUFFER, sphere_inds.nbytes, sphere_inds, GL_STATIC_DRAW
    )

    # Configurar os Atributos (Layout do Vertex Shader)
    stride = 8 * 4 # 8 floats (x,y,z, u,v, nx,ny,nz) * 4 bytes

    # Local 0: Posição (x, y, z)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Local 1: TexCoord (u, v) - Offset de 3 floats (12 bytes)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)

    # Local 2: Normal (nx, ny, nz) - Offset de 5 floats (20 bytes)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(5 * 4))
    glEnableVertexAttribArray(2)

    # Configuração das Matrizes (Câmera Fixa)
    projection = glm.perspective(glm.radians(45.0), 800 / 600, 0.1, 100.0)
    view = glm.lookAt(glm.vec3(0, 0, 8), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0)) # Câmera um pouco mais longe (Z=8)

    # Obter localizações Uniforms
    model_loc = glGetUniformLocation(shader, "model")
    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    tex_loc = glGetUniformLocation(shader, "textureSampler") # Localização da sampler

    # Enviar Projeção e View (Estáticas)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))
    
    # Dizer ao sampler que ele usará a Unidade de Textura 0
    glUniform1i(tex_loc, 0) 

    # Instanciar os Corpos Celestes (Agora com os IDs das Texturas)
    sun = Planet(
        radius=1.5,
        rotation_speed=5.0,
        orbit_radius=0.0,
        orbit_speed=0.0,
        parent=None,
        texture_id=sun_tex
    )

    # Instanciar os Corpos Celestes (CORRIGIDO O MAPEAMENTO DAS TEXTURAS)
    sun = Planet(
        radius=1.5,
        rotation_speed=5.0,
        orbit_radius=0.0,
        orbit_speed=0.0,
        parent=None,
        texture_id=sun_tex
    )

    earth = Planet(
        radius=0.5,
        rotation_speed=360.0,
        orbit_radius=4.0,
        orbit_speed=30.0,
        parent=sun,
        texture_id=earth_tex # <-- ID CORRETO: earth_tex para o objeto earth
    )

    moon = Planet(
        radius=0.15,
        rotation_speed=180.0,
        orbit_radius=1.0,
        orbit_speed=180.0,
        parent=earth,
        texture_id=moon_tex # <-- ID CORRETO: moon_tex para o objeto moon
    )

    all_planets = [sun, earth, moon]
    # Loop Principal
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
            ):
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Atualizar a Model Matrix (Rotação e Translação)
        time = pygame.time.get_ticks() / 1000.0
        
        for planet in all_planets:
            planet.update(time)
            
            # 1. Enviar a Model Matrix do planeta atual para o shader
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(planet.model))

            # 2. Bind da Textura do planeta (Muito Importante!)
            glActiveTexture(GL_TEXTURE0) # Ativa a unidade de textura 0
            glBindTexture(GL_TEXTURE_2D, planet.texture_id) # Faz o bind da textura
            
            # 3. Desenhar o planeta
            glBindVertexArray(VAO)
            glDrawElements(GL_TRIANGLES, len(sphere_inds), GL_UNSIGNED_INT, None)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()