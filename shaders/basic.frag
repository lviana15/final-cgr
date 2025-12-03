#version 330 core

in vec2 TexCoord;
in vec3 Normal;
in vec3 FragPos;

out vec4 FragColor;

// Adicionar a sampler para ler a textura
uniform sampler2D textureSampler;

void main()
{
    // 1. Ler a cor da textura
    vec3 textureColor = vec3(texture(textureSampler, TexCoord));

    // 2. Iluminação ambiente fake (a ser substituída pelo Phong)
    float ambientStrength = 0.5;
    vec3 lightColor = vec3(1.0, 1.0, 1.0);
    vec3 ambient = ambientStrength * lightColor;

    // A cor final é a luz ambiente * a cor da textura
    vec3 result = ambient * textureColor;
    
    FragColor = vec4(result, 1.0);
}