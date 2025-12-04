# planet.py
import glm
import pygame

class Planet:
    def __init__(self, radius, rotation_speed, orbit_radius, orbit_speed, parent=None, texture_id=0):
        """
        Inicializa um corpo celeste (Planeta, Lua ou Sol).

        Args:
            radius (float): Raio/escala do planeta.
            rotation_speed (float): Velocidade de rotação em torno do próprio eixo (graus/seg).
            orbit_radius (float): Raio da órbita em torno do 'parent'. (0 para o Sol).
            orbit_speed (float): Velocidade de translação em torno do 'parent' (graus/seg).
            parent (Planet, optional): O planeta que ele orbita. None para o Sol.
            texture_id (int): O ID da textura do OpenGL (A ser implementado).
        """
        self.radius = radius
        self.rotation_speed = rotation_speed
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.parent = parent
        self.texture_id = texture_id
        
        # Matrizes de Transformação
        self.model = glm.mat4(1.0)
        self.initial_translation = glm.translate(glm.mat4(1.0), glm.vec3(orbit_radius, 0.0, 0.0))
        
    def update(self, time):
        """
        Calcula e atualiza a matriz de transformação (Model Matrix) 
        baseada na rotação e translação (órbita).
        
        Args:
            time (float): Tempo total em segundos desde o início da aplicação.
        """
        # 1. Rotação Própria (Giro do planeta em seu próprio eixo)
        # O ângulo de rotação é baseado no tempo e na velocidade de rotação.
        rotation_angle = glm.radians(time * self.rotation_speed)
        rotation_matrix = glm.rotate(glm.mat4(1.0), rotation_angle, glm.vec3(0.0, 1.0, 0.0))
        
        # 2. Escala
        scale_matrix = glm.scale(glm.mat4(1.0), glm.vec3(self.radius))
        
        # 3. Translação (Órbita em torno do Pai)
        if self.parent:
            # Rotação de órbita em torno do pai (eixo Y)
            orbit_angle = glm.radians(time * self.orbit_speed)
            orbit_rotation = glm.rotate(glm.mat4(1.0), orbit_angle, glm.vec3(0.0, 1.0, 0.0))
            
            # Translação inicial para a órbita (posiciona o planeta no raio de órbita)
            initial_orbit_pos = glm.translate(glm.mat4(1.0), glm.vec3(self.orbit_radius, 0.0, 0.0))
            
            # Ordem de Transformação:
            # Posição_Pai * Rotação_Órbita * Translação_Inicial * Rotação_Própria * Escala
            self.model = self.parent.model * orbit_rotation * initial_orbit_pos * rotation_matrix * scale_matrix
        else:
            # Se for o Sol (sem pai), apenas rotação própria e escala
            # Ordem: Rotação_Própria * Escala
            self.model = rotation_matrix * scale_matrix