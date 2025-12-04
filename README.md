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
- [x] Criar o script principal (main.py) com a abertura da janela e o loop principal (Game Loop).
- [x] Implementar função para ler, compilar e linkar Shaders (Vertex e Fragment).
- [x] Implementar função para carregar texturas (Diffuse e Normal maps) usando Pillow para o OpenGL.
- [x] Criar algoritmo de geração de malha de Esfera que retorne arrays numpy para: Vértices, UVs, Normais e Tangentes.
- [x] Configurar os buffers do OpenGL (VAO, VBO, EBO) para enviar os dados da esfera para a GPU.
- [x] Escrever o Vertex Shader básico (transformação Projection * View * Model).
- [x] Escrever o Fragment Shader básico (apenas aplicação de textura de cor).
- [ ] Implementar classe de Câmera utilizando PyGLM para gerenciar as matrizes de View e Projection.
- [ ] Adicionar controle de input (teclado/mouse) para mover a câmera pela cena.
- [x] Criar classe Planet que armazena posição, rotação, escala, textura e referência ao planeta "pai".
- [x] Implementar lógica de atualização de órbita (translação e rotação) baseada no tempo (time.get_ticks).
- [x] Instanciar o Sol, a Terra e a Lua com suas respectivas texturas e tamanhos.
- [ ] Atualizar o Vertex Shader para calcular a Matriz TBN (Tangent, Bitangent, Normal).
- [x] Atualizar o Fragment Shader para implementar o modelo de iluminação Phong (Ambient + Diffuse + Specular).
- [ ] Atualizar o Fragment Shader para ler a textura de Normal Map e alterar a normal da superfície para criar o efeito de rugosidade.
- [ ] Adicionar um Skybox (cubo ou esfera gigante invertida com textura de estrelas) para o fundo.
- [ ] Revisar o código, remover prints de debug e organizar comentários finais.
