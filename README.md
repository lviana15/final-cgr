### Como executar o projeto

- Criar ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate
```

- Instalar dependencias
```
python3 install -r requirements.txt
```

- Executar o progama
```
python3 main.py
```

### Roadmap
- [ ] Criar o script principal (main.py) com a abertura da janela e o loop principal (Game Loop).
- [ ] Implementar função para ler, compilar e linkar Shaders (Vertex e Fragment).
- [ ] Implementar função para carregar texturas (Diffuse e Normal maps) usando Pillow para o OpenGL.
- [ ] Criar algoritmo de geração de malha de Esfera que retorne arrays numpy para: Vértices, UVs, Normais e Tangentes.
- [ ] Configurar os buffers do OpenGL (VAO, VBO, EBO) para enviar os dados da esfera para a GPU.
- [ ] Escrever o Vertex Shader básico (transformação Projection * View * Model).
- [ ] Escrever o Fragment Shader básico (apenas aplicação de textura de cor).
- [ ] Implementar classe de Câmera utilizando PyGLM para gerenciar as matrizes de View e Projection.
- [ ] Adicionar controle de input (teclado/mouse) para mover a câmera pela cena.
- [ ] Criar classe Planet que armazena posição, rotação, escala, textura e referência ao planeta "pai".
- [ ] Implementar lógica de atualização de órbita (translação e rotação) baseada no tempo (time.get_ticks).
- [ ] Instanciar o Sol, a Terra e a Lua com suas respectivas texturas e tamanhos.
- [ ] Atualizar o Vertex Shader para calcular a Matriz TBN (Tangent, Bitangent, Normal).
- [ ] Atualizar o Fragment Shader para implementar o modelo de iluminação Phong (Ambient + Diffuse + Specular).
- [ ] Atualizar o Fragment Shader para ler a textura de Normal Map e alterar a normal da superfície para criar o efeito de rugosidade.
- [ ] Adicionar um Skybox (cubo ou esfera gigante invertida com textura de estrelas) para o fundo.
- [ ] (Opcional - Risco Alto) Criar Framebuffer Object (FBO) para capturar o mapa de profundidade (Shadow Map).
- [ ] (Opcional - Risco Alto) Implementar o "Render Pass" de sombras (renderizar a cena da visão do Sol).
- [ ] (Opcional - Risco Alto) Aplicar o cálculo de sombra no Fragment Shader principal comparando a profundidade.
- [ ] Revisar o código, remover prints de debug e organizar comentários finais.
