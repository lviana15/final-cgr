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
        
        # 2. Translação (Órbita em torno do Pai)
        translation_matrix = glm.mat4(1.0)
        
        if self.parent:
            # Rotação de órbita em torno do pai
            orbit_angle = glm.radians(time * self.orbit_speed)
            orbit_rotation = glm.rotate(glm.mat4(1.0), orbit_angle, glm.vec3(0.0, 1.0, 0.0))
            
            # A translação total do planeta é:
            # M_parent * R_orbita * T_inicial * R_propria * S_escala
            
            # Pega a posição do planeta pai
            translation_matrix = self.parent.model * orbit_rotation
            
        # 3. Escala
        scale_matrix = glm.scale(glm.mat4(1.0), glm.vec3(self.radius))
        
        # 4. Cálculo da Matriz Model final
        # Ordem de Transformação:
        # PosiçãoGlobal(Parent) * RotaçãoÓrbita * PosiçãoInicialNaÓrbita * RotaçãoPrópria * Escala
        
        self.model = translation_matrix * self.initial_translation * rotation_matrix * scale_matrix