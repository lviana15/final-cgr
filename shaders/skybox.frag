#version 330 core

in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D textureSampler;

void main()
{
    // Simplesmente aplica a textura de estrelas
    vec3 starColor = vec3(texture(textureSampler, TexCoord));
    FragColor = vec4(starColor, 1.0);
}
