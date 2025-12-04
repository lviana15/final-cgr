# main.py
import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
import glm
import ctypes

from utils import load_shader, load_texture, generate_starfield_texture
from meshes import generate_sphere
from planet import Planet
from camera import Camera
from skybox import Skybox

# Escala de Tempo para acelerar as órbitas e rotações
TIME_SCALE = 8000.0

# Períodos Reais (em segundos para o cálculo de velocidades)
EARTH_ORBITAL_PERIOD = 365.25636 * 86400
MOON_ORBITAL_PERIOD = 27.321661 * 86400 
EARTH_ROTATION_PERIOD = 23.9344696 * 3600
MOON_ROTATION_PERIOD = 27.321661 * 86400
SUN_ROTATION_PERIOD = 25.05 * 86400

SUN_ROTATION_SPEED = (360.0 / SUN_ROTATION_PERIOD) * TIME_SCALE
EARTH_ROTATION_SPEED = (360.0 / EARTH_ROTATION_PERIOD) * TIME_SCALE
MOON_ROTATION_SPEED = (360.0 / MOON_ROTATION_PERIOD) * TIME_SCALE

EARTH_ORBITAL_SPEED = (360.0 / EARTH_ORBITAL_PERIOD) * TIME_SCALE
MOON_ORBITAL_SPEED = (360.0 / MOON_ORBITAL_PERIOD) * TIME_SCALE


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sistema Solar - Fase 1: Esfera com Textura")

    glViewport(0, 0, 800, 600)
    glEnable(GL_DEPTH_TEST)
    # Capturar mouse para controle FPS: ocultar cursor e prender dentro da janela
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)
    # Limpar movimento relativo inicial
    pygame.mouse.get_rel()

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

    # Carregar Normal Maps (Opcional - se não existirem, usaremos normal padrão)
    sun_normal = None
    earth_normal = None
    moon_normal = None
    
    try:
        sun_normal = load_texture("assets/textures/sun_normal.png")
        print("Normal map do Sol carregado com sucesso")
    except FileNotFoundError:
        print("Normal map do Sol não encontrado - usando normal padrão")

    try:
        earth_normal = load_texture("assets/textures/earth_normal.jpg")
        print("Normal map da Terra carregado com sucesso")
    except FileNotFoundError:
        print("Normal map da Terra não encontrado - usando normal padrão")

    try:
        moon_normal = load_texture("assets/textures/moon_normal.jpg")
        print("Normal map da Lua carregado com sucesso")
    except FileNotFoundError:
        print("Normal map da Lua não encontrado - usando normal padrão")

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
    # Novo formato: 14 floats por vértice [x,y,z, u,v, nx,ny,nz, tx,ty,tz, bx,by,bz]
    stride = 14 * 4  # 14 floats * 4 bytes

    # Local 0: Posição (x, y, z) - Offset 0
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # Local 1: TexCoord (u, v) - Offset de 3 floats (12 bytes)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
    glEnableVertexAttribArray(1)

    # Local 2: Normal (nx, ny, nz) - Offset de 5 floats (20 bytes)
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(5 * 4))
    glEnableVertexAttribArray(2)

    # Local 3: Tangent (tx, ty, tz) - Offset de 8 floats (32 bytes)
    glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(8 * 4))
    glEnableVertexAttribArray(3)

    # Local 4: Bitangent (bx, by, bz) - Offset de 11 floats (44 bytes)
    glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(11 * 4))
    glEnableVertexAttribArray(4)

    # Instanciar Câmera com controle FPS
    # Ajustei a sensibilidade do mouse para 0.15 (graus por pixel) para resposta mais perceptível
    camera = Camera(position=glm.vec3(0, 0, 8), fov=45.0, aspect_ratio=800/600, speed=8.0, mouse_sensitivity=0.15)

    # Obter localizações Uniforms
    model_loc = glGetUniformLocation(shader, "model")
    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    tex_loc = glGetUniformLocation(shader, "textureSampler")  # Localização da sampler
    normal_map_loc = glGetUniformLocation(shader, "normalMapSampler")  # Localização do normal map

    # Obter localizações Uniforms de Iluminação
    lightPos_loc = glGetUniformLocation(shader, "lightPos")
    viewPos_loc = glGetUniformLocation(shader, "viewPos")
    lightColor_loc = glGetUniformLocation(shader, "lightColor")
    ambientStrength_loc = glGetUniformLocation(shader, "ambientStrength")
    isSun_loc = glGetUniformLocation(shader, "isSun")
    useNormalMap_loc = glGetUniformLocation(shader, "useNormalMap")  # Flag para usar normal map

    # Configurações de Luz (Sol) e Ambiente
    light_pos = glm.vec3(0.0, 0.0, 0.0)  # O Sol está na origem
    light_color = glm.vec3(1.0, 1.0, 1.0)  # Luz branca
    ambient_strength = 0.25  # Diminuímos a luz ambiente para realçar o efeito difuso

    # Enviar Uniforms de Luz (Estáticas)
    glUniform3fv(lightPos_loc, 1, glm.value_ptr(light_pos))
    glUniform3fv(lightColor_loc, 1, glm.value_ptr(light_color))
    glUniform1f(ambientStrength_loc, ambient_strength)

    # Enviar Projeção (estática)
    projection = camera.get_projection()
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))

    # Inicializar Clock para delta time
    clock = pygame.time.Clock()

    # Estado do controle do mouse (prendido / liberado). TAB alterna.
    mouse_enabled = True

    # Dizer aos samplers que vão usar as Unidades de Textura 0 e 1
    glUniform1i(tex_loc, 0)        # Textura difusa na unidade 0
    glUniform1i(normal_map_loc, 1) # Normal map na unidade 1

    # Criar e configurar Skybox
    skybox = Skybox(radius=200.0, stacks=20, sectors=20)
    skybox_shader = load_shader("shaders/skybox.vert", "shaders/skybox.frag")
    starfield_texture = generate_starfield_texture(width=1024, height=1024, star_density=0.01)
    skybox.set_shader(skybox_shader)
    skybox.set_texture(starfield_texture)

    # Instanciar os Corpos Celestes com velocidades baseadas em períodos reais
    sun = Planet(
        radius=1.5,
        rotation_speed=SUN_ROTATION_SPEED,
        orbit_radius=0.0,
        orbit_speed=0.0,
        parent=None,
        texture_id=sun_tex,
        normal_map_id=sun_normal,
    )

    earth = Planet(
        radius=0.5,
        rotation_speed=EARTH_ROTATION_SPEED,
        orbit_radius=4.0,
        orbit_speed=EARTH_ORBITAL_SPEED,
        parent=sun,
        texture_id=earth_tex,
        normal_map_id=earth_normal,
    )

    moon = Planet(
        radius=0.15,
        rotation_speed=MOON_ROTATION_SPEED,
        orbit_radius=1.0,
        orbit_speed=MOON_ORBITAL_SPEED,
        parent=earth,
        texture_id=moon_tex,
        normal_map_id=moon_normal,
    )

    all_planets = [sun, earth, moon]
    # Loop Principal
    running = True
    while running:
        # Calcular delta time
        delta_time = clock.tick(60) / 1000.0
        
        # Capturar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == KEYDOWN and event.key == K_ESCAPE
            ):
                running = False

            # Alternar captura do mouse com TAB (prender/soltar)
            if event.type == KEYDOWN and event.key == K_TAB:
                mouse_enabled = not mouse_enabled
                if mouse_enabled:
                    pygame.mouse.set_visible(False)
                    pygame.event.set_grab(True)
                    # limpar delta residual
                    pygame.mouse.get_rel()
                else:
                    pygame.mouse.set_visible(True)
                    pygame.event.set_grab(False)
                    pygame.mouse.get_rel()
        
        # Capturar entrada (teclado e mouse)
        keys_pressed = pygame.key.get_pressed()
        keys = {
            'w': keys_pressed[K_w],
            's': keys_pressed[K_s],
            'a': keys_pressed[K_a],
            'd': keys_pressed[K_d],
            'up': keys_pressed[K_UP],
            'down': keys_pressed[K_DOWN],
            'left': keys_pressed[K_LEFT],
            'right': keys_pressed[K_RIGHT],
        }
        # Obter delta do mouse apenas se o mouse estiver habilitado
        if mouse_enabled:
            mouse_delta = pygame.mouse.get_rel()
        else:
            # consumir movimento, garantir zeros
            pygame.mouse.get_rel()
            mouse_delta = (0, 0)
        
        # Atualizar câmera
        camera.update(keys, mouse_delta, delta_time)
        
        # Enviar matrizes de câmera atualizadas
        view = camera.get_view()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        
        # Enviar posição da câmera para o cálculo de iluminação Phong
        glUniform3fv(viewPos_loc, 1, glm.value_ptr(camera.position))
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Atualizar a Model Matrix (Rotação e Translação)
        time = pygame.time.get_ticks() / 1000.0

        # Renderizar Skybox primeiro
        skybox.render(view, projection, camera.position)
        
        # Voltar ao shader principal para renderizar planetas
        glUseProgram(shader)

        for planet in all_planets:
            # 1. Definir se o objeto é o Sol ou um Planeta
            if planet == sun:
                glUniform1i(isSun_loc, 1)  # É o Sol (DESLIGA O PHONG)
            else:
                glUniform1i(isSun_loc, 0)  # É um Planeta (LIGA O PHONG)

            planet.update(time)

            # Enviar Model Matrix
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(planet.model))
            
            # Bind da textura difusa (unidade 0)
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, planet.texture_id)
            
            # Bind do normal map (unidade 1) - se existir
            glActiveTexture(GL_TEXTURE1)
            if planet.normal_map_id is not None:
                glBindTexture(GL_TEXTURE_2D, planet.normal_map_id)
                glUniform1i(useNormalMap_loc, 1)  # Usar normal map
            else:
                glUniform1i(useNormalMap_loc, 0)  # Não usar normal map
            
            # Desenhar o planeta
            glBindVertexArray(VAO)
            glDrawElements(GL_TRIANGLES, len(sphere_inds), GL_UNSIGNED_INT, None)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
