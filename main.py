import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


def main():
    # 1. Inicialização do Pygame e Janela
    pygame.init()
    display = (800, 600)

    # Cria a janela com buffer duplo (DOUBLEBUF) e contexto OpenGL
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Sistema Solar - Projeto Final CG")

    # 2. Configurações Iniciais do OpenGL
    glViewport(0, 0, 800, 600)
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Cor de fundo (Cinza escuro)

    # 3. Game Loop (Loop Principal)
    running = True
    while running:
        # A. Tratamento de Eventos (Input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # B. Renderização (Desenhar as coisas)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # --- AQUI É ONDE VAMOS DESENHAR OS PLANETAS DEPOIS ---

        # C. Atualizar a tela
        pygame.display.flip()

        # Limita a 60 FPS para não fritar a CPU
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
