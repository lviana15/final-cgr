import glm
import numpy as np
from OpenGL.GL import *
import ctypes


class Skybox:
    """
    Skybox como esfera invertida gigante.
    Renderiza um fundo de estrelas ao redor da câmera.
    """
    
    def __init__(self, radius=200.0, stacks=20, sectors=20):
        """
        Inicializa o Skybox (geometria gerada lazy na primeira renderização).
        
        Args:
            radius: Raio da esfera (deve ser muito grande)
            stacks: Divisões verticais da esfera
            sectors: Divisões horizontais da esfera
        """
        self.radius = radius
        self.stacks = stacks
        self.sectors = sectors
        self.shader = None
        self.texture_id = None
        self.VAO = None
        self.VBO = None
        self.EBO = None
        self.index_count = 0
        self.initialized = False
    
    def _generate_sphere(self):
        """
        Gera uma esfera invertida (normais apontam para dentro).
        Formato simplificado: apenas posição e UV.
        """
        vertices = []
        indices = []
        
        # Gerar vértices (esfera invertida: normais para dentro)
        for i in range(self.stacks + 1):
            stack_angle = np.pi / 2 - i * (np.pi / self.stacks)
            xy = self.radius * np.cos(stack_angle)
            z = self.radius * np.sin(stack_angle)
            
            for j in range(self.sectors + 1):
                sector_angle = j * (2 * np.pi / self.sectors)
                
                x = xy * np.cos(sector_angle)
                y = xy * np.sin(sector_angle)
                
                # UV coordinates
                u = j / self.sectors
                v = i / self.stacks
                
                # Para esfera invertida, negamos z para inverter normais
                vertices.extend([x, y, -z, u, v])
        
        # Gerar índices (ordem invertida para normais internas)
        for i in range(self.stacks):
            k1 = i * (self.sectors + 1)
            k2 = k1 + self.sectors + 1
            
            for j in range(self.sectors):
                # Primeiro triângulo (ordem invertida)
                if i != 0:
                    indices.extend([k1, k1 + 1, k2])
                
                # Segundo triângulo (ordem invertida)
                if i != (self.stacks - 1):
                    indices.extend([k1 + 1, k2 + 1, k2])
                
                k1 += 1
                k2 += 1
        
        self.index_count = len(indices)
        vertices = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)
        
        # Configurar VAO, VBO, EBO
        self.VAO = glGenVertexArrays(1)
        self.VBO = glGenBuffers(1)
        self.EBO = glGenBuffers(1)
        
        glBindVertexArray(self.VAO)
        
        # VBO
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        # EBO
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        # Layout: 5 floats por vértice (x, y, z, u, v)
        stride = 5 * 4
        
        # Posição
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # UV
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        
        glBindVertexArray(0)
    
    def set_texture(self, texture_id):
        """Define a textura do Skybox."""
        self.texture_id = texture_id
    
    def set_shader(self, shader_program):
        """Define o programa shader do Skybox."""
        self.shader = shader_program
    
    def render(self, view, projection, camera_position):
        """
        Renderiza o Skybox.
        
        Args:
            view: Matriz view da câmera
            projection: Matriz projection da câmera
            camera_position: Posição da câmera (para seguir movimento)
        """
        if self.shader is None or self.texture_id is None:
            return
        
        # Inicializar geometria na primeira renderização (com contexto OpenGL disponível)
        if not self.initialized:
            self._generate_sphere()
            self.initialized = True
        
        glUseProgram(self.shader)
        
        # Criar matriz model que segue a câmera
        model = glm.translate(glm.mat4(1.0), camera_position)
        
        # Remover componente de translação da view para que skybox fique estático
        view_no_translate = glm.mat4(1.0)
        for i in range(3):
            for j in range(3):
                view_no_translate[i][j] = view[i][j]
        
        # Enviar uniforms
        model_loc = glGetUniformLocation(self.shader, "model")
        view_loc = glGetUniformLocation(self.shader, "view")
        proj_loc = glGetUniformLocation(self.shader, "projection")
        tex_loc = glGetUniformLocation(self.shader, "textureSampler")
        
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view_no_translate))
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))
        glUniform1i(tex_loc, 0)
        
        # Desabilitar depth write para não ocluir nada
        glDepthMask(GL_FALSE)
        glDepthFunc(GL_LEQUAL)  # Desenhar até a profundidade máxima
        
        # Bind textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        
        # Renderizar
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, self.index_count, GL_UNSIGNED_INT, None)
        
        # Reabilitar depth write e restaurar função
        glDepthMask(GL_TRUE)
        glDepthFunc(GL_LESS)
        glBindVertexArray(0)
