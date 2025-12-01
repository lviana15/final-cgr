import numpy as np
import math


def generate_sphere(radius, stacks, sectors):
    """
    Gera vértices e índices para uma esfera UV.
    Retorna (vertices, indices) prontos para o OpenGL.
    Formato do vértice: [x, y, z, u, v, nx, ny, nz]
    """
    vertices = []
    indices = []

    # 1. Gerar Vértices
    for i in range(stacks + 1):
        stack_angle = math.pi / 2 - i * (math.pi / stacks)  # Latitude: de +90 a -90
        xy = radius * math.cos(stack_angle)
        z = radius * math.sin(stack_angle)

        for j in range(sectors + 1):
            sector_angle = j * (2 * math.pi / sectors)  # Longitude: 0 a 360

            # Posição (x, y, z)
            x = xy * math.cos(sector_angle)
            y = xy * math.sin(sector_angle)

            # Coordenadas de Textura (u, v)
            u = j / sectors
            v = i / stacks

            # Normais (nx, ny, nz) - Para esfera, a normal é a própria posição normalizada
            # Mas como nossa esfera está na origem (0,0,0), basta normalizar o vetor Posição.
            nx = x / radius
            ny = y / radius
            nz = z / radius

            vertices.extend([x, y, z, u, v, nx, ny, nz])

    # 2. Gerar Índices (Triângulos)
    # Conecta os vértices em triângulos para formar a malha
    for i in range(stacks):
        k1 = i * (sectors + 1)
        k2 = k1 + sectors + 1

        for j in range(sectors):
            if i != 0:
                indices.extend([k1, k2, k1 + 1])
            if i != (stacks - 1):
                indices.extend([k1 + 1, k2, k2 + 1])

            k1 += 1
            k2 += 1

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)
