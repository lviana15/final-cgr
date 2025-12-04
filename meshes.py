import numpy as np
import math


def generate_sphere(radius, stacks, sectors):
    """
    Gera vértices e índices para uma esfera UV com Tangentes e Bitangentes.
    Retorna (vertices, indices) prontos para o OpenGL.
    Formato do vértice: [x, y, z, u, v, nx, ny, nz, tx, ty, tz, bx, by, bz]
    Total: 14 floats por vértice
    """
    vertices = []
    indices = []
    vertex_data = {}  # Dicionário para armazenar dados dos vértices

    # 1. Gerar Vértices com dados básicos
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
            nx = x / radius
            ny = y / radius
            nz = z / radius

            # Inicializar tangentes e bitangentes (serão calculados depois)
            vertex_idx = i * (sectors + 1) + j
            vertex_data[vertex_idx] = {
                'pos': np.array([x, y, z], dtype=np.float32),
                'uv': np.array([u, v], dtype=np.float32),
                'normal': np.array([nx, ny, nz], dtype=np.float32),
                'tangent': np.array([0.0, 0.0, 0.0], dtype=np.float32),
                'bitangent': np.array([0.0, 0.0, 0.0], dtype=np.float32),
            }

    # 2. Gerar Índices e calcular Tangentes/Bitangentes por triângulo
    for i in range(stacks):
        k1 = i * (sectors + 1)
        k2 = k1 + sectors + 1

        for j in range(sectors):
            # Primeiro triângulo (se não for topo)
            if i != 0:
                idx0, idx1, idx2 = k1, k2, k1 + 1
                indices.extend([idx0, idx1, idx2])
                _compute_triangle_tangents(vertex_data, idx0, idx1, idx2)

            # Segundo triângulo (se não for base)
            if i != (stacks - 1):
                idx0, idx1, idx2 = k1 + 1, k2, k2 + 1
                indices.extend([idx0, idx1, idx2])
                _compute_triangle_tangents(vertex_data, idx0, idx1, idx2)

            k1 += 1
            k2 += 1

    # 3. Normalizar tangentes e bitangentes (ortogonalização Gram-Schmidt)
    for vertex_idx in vertex_data:
        data = vertex_data[vertex_idx]
        normal = data['normal']
        tangent = data['tangent']

        # Gram-Schmidt: T = T - (T·N)N
        tangent = tangent - np.dot(tangent, normal) * normal
        tangent = tangent / (np.linalg.norm(tangent) + 1e-8)  # Normalizar

        # B = N × T (garantir ortogonalidade)
        bitangent = np.cross(normal, tangent)

        data['tangent'] = tangent
        data['bitangent'] = bitangent

    # 4. Montar array final de vértices [x,y,z, u,v, nx,ny,nz, tx,ty,tz, bx,by,bz]
    for i in range((stacks + 1) * (sectors + 1)):
        if i in vertex_data:
            data = vertex_data[i]
            vertices.extend(data['pos'])      # 3 floats
            vertices.extend(data['uv'])       # 2 floats
            vertices.extend(data['normal'])   # 3 floats
            vertices.extend(data['tangent'])  # 3 floats
            vertices.extend(data['bitangent'])# 3 floats

    return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32)


def _compute_triangle_tangents(vertex_data, idx0, idx1, idx2):
    """
    Calcula e acumula tangentes/bitangentes para um triângulo.
    Usa a fórmula: T = f * (dV2*E1 - dV1*E2), B = f * (-dU2*E1 + dU1*E2)
    """
    # Obter dados dos vértices
    p0 = vertex_data[idx0]['pos']
    p1 = vertex_data[idx1]['pos']
    p2 = vertex_data[idx2]['pos']

    uv0 = vertex_data[idx0]['uv']
    uv1 = vertex_data[idx1]['uv']
    uv2 = vertex_data[idx2]['uv']

    # Calcular arestas
    e1 = p1 - p0
    e2 = p2 - p0

    duv1 = uv1 - uv0
    duv2 = uv2 - uv0

    # Calcular determinante
    f = 1.0 / (duv1[0] * duv2[1] - duv2[0] * duv1[1] + 1e-8)

    # Calcular tangente e bitangente
    tangent = f * (duv2[1] * e1 - duv1[1] * e2)
    bitangent = f * (-duv2[0] * e1 + duv1[0] * e2)

    # Acumular nos vértices do triângulo
    vertex_data[idx0]['tangent'] += tangent
    vertex_data[idx1]['tangent'] += tangent
    vertex_data[idx2]['tangent'] += tangent

    vertex_data[idx0]['bitangent'] += bitangent
    vertex_data[idx1]['bitangent'] += bitangent
    vertex_data[idx2]['bitangent'] += bitangent
