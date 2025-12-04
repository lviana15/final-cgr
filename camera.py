import glm
import math


class Camera:
    """
    Câmera em estilo FPS com controles de teclado (WASD/Setas) e mouse.
    
    Usa ângulos de Euler (yaw, pitch) para rotação.
    Movimento baseado em delta time para frame-rate independência.
    """
    
    def __init__(self, position=glm.vec3(0, 0, 8), fov=45.0, aspect_ratio=800/600, 
                 speed=5.0, mouse_sensitivity=0.1):
        """
        Inicializa a câmera.
        
        Args:
            position: Posição inicial da câmera no mundo
            fov: Campo de visão em graus
            aspect_ratio: Proporção largura/altura
            speed: Velocidade de movimento em unidades/segundo
            mouse_sensitivity: Sensibilidade do mouse (radianos por pixel)
        """
        self.position = position
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.speed = speed
        self.mouse_sensitivity = mouse_sensitivity
        
        # Ângulos de Euler (em graus) - mais intuitivo para mapeamento do mouse
        self.yaw = -90.0    # Começa mirando para +Z (graus)
        self.pitch = 0.0    # Começando horizontalmente (graus)
        
        # Vetores da câmera (calculados a partir dos ângulos)
        self.front = glm.vec3(0.0, 0.0, 1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.world_up = glm.vec3(0.0, 1.0, 0.0)
        
        # Limites de câmera (opcional)
        self.min_distance = 0.1
        self.max_distance = 100.0
        
        self._update_camera_vectors()
    
    def _update_camera_vectors(self):
        """
        Recalcula os vetores front, right, up baseado em yaw e pitch.
        Deve ser chamado sempre que yaw ou pitch mudam.
        """
        # Calcular o novo vetor front usando trigonometria esférica
        # Converter ângulos para radianos para uso nas funções trigonométricas
        yaw_rad = math.radians(self.yaw)
        pitch_rad = math.radians(self.pitch)

        front = glm.vec3(
            math.cos(yaw_rad) * math.cos(pitch_rad),
            math.sin(pitch_rad),
            math.sin(yaw_rad) * math.cos(pitch_rad)
        )
        self.front = glm.normalize(front)
        
        # Calcular right vector
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        
        # Recalcular up vector (garantir ortogonalidade)
        self.up = glm.normalize(glm.cross(self.right, self.front))
    
    def update(self, keys, mouse_delta, delta_time):
        """
        Atualiza a câmera baseado em entrada do teclado e mouse.
        
        Args:
            keys: Dict de teclas pressionadas (de pygame.key.get_pressed())
            mouse_delta: Tupla (dx, dy) de movimento do mouse
            delta_time: Tempo decorrido desde o último frame em segundos
        """
        # Movimento com teclado (WASD)
        if keys.get('w'):  # Avançar
            self.position += self.front * self.speed * delta_time
        if keys.get('s'):  # Recuar
            self.position -= self.front * self.speed * delta_time
        if keys.get('a'):  # Esquerda
            self.position -= self.right * self.speed * delta_time
        if keys.get('d'):  # Direita
            self.position += self.right * self.speed * delta_time
        
        # Movimento com setas (também suportado)
        if keys.get('up'):
            self.position += self.front * self.speed * delta_time
        if keys.get('down'):
            self.position -= self.front * self.speed * delta_time
        if keys.get('left'):
            self.position -= self.right * self.speed * delta_time
        if keys.get('right'):
            self.position += self.right * self.speed * delta_time
        
        # Rotação com mouse
        if mouse_delta[0] != 0 or mouse_delta[1] != 0:
            dx, dy = mouse_delta

            # Proteção: limitar deltas muito grandes (ex.: quando o mouse entra/volta à janela)
            max_delta = 60.0
            if dx > max_delta:
                dx = max_delta
            if dx < -max_delta:
                dx = -max_delta
            if dy > max_delta:
                dy = max_delta
            if dy < -max_delta:
                dy = -max_delta

            # Atualizar yaw (rotação horizontal)
            # Agora tratamos sensibilidade como graus por pixel
            self.yaw += dx * self.mouse_sensitivity

            # Atualizar pitch (rotação vertical)
            self.pitch -= dy * self.mouse_sensitivity
            
            # Limitar pitch para evitar flip de câmera (gimbal lock)
            # Limitar pitch em graus para evitar flip de câmera (gimbal lock)
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
            
            # Recalcular vetores da câmera
            self._update_camera_vectors()
        
        # Limites de distância da origem (opcional)
        distance = glm.length(self.position)
        if distance < self.min_distance:
            self.position = glm.normalize(self.position) * self.min_distance
        if distance > self.max_distance:
            self.position = glm.normalize(self.position) * self.max_distance
    
    def get_view(self):
        """
        Retorna a matriz View calculada com glm.lookAt.
        
        Returns:
            glm.mat4: Matriz view para passar ao shader
        """
        return glm.lookAt(self.position, self.position + self.front, self.up)
    
    def get_projection(self):
        """
        Retorna a matriz Projection.
        
        Returns:
            glm.mat4: Matriz projection para passar ao shader
        """
        return glm.perspective(glm.radians(self.fov), self.aspect_ratio, 0.1, 500.0)
