#version 330 core

in vec2 TexCoord;
in vec3 Normal;
in vec3 FragPos;

out vec4 FragColor;

uniform sampler2D textureSampler;

// Uniforms de Iluminação
uniform vec3 lightPos;       // Posição da Luz (0, 0, 0)
uniform vec3 viewPos;      // Posição da Câmera
uniform vec3 lightColor;   // Cor da Luz (Branco)
uniform float ambientStrength; // Força da luz ambiente
uniform int isSun; // <--- NOVO: 1 se for o sol, 0 se for um planeta

void main()
{
    // 1. Ler a cor da textura
    vec3 textureColor = vec3(texture(textureSampler, TexCoord));

    if (isSun == 1) {
        // Se for o SOL, desenha apenas a cor da textura no brilho total (emite luz)
        FragColor = vec4(textureColor, 1.0);
        return;
    }
    
    // 2. Componente Ambiente
    vec3 ambient = ambientStrength * lightColor * textureColor;

    // 3. Componente Difuso 
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor * textureColor;

    // 4. Componente Especular 
    vec3 specularColor = vec3(0.5);
    float shininess = 32.0; 

    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = specularColor * spec;
    
    // 5. Cor Final (Ambient + Diffuse + Specular)
    vec3 result = ambient + diffuse + specular;
    
    FragColor = vec4(result, 1.0);
}