#version 330 core

in vec2 TexCoord;
in vec3 Normal;
in vec3 FragPos;

// Vetores em espaço tangente
in vec3 TangentLightPos;
in vec3 TangentViewPos;
in vec3 TangentFragPos;

out vec4 FragColor;

uniform sampler2D textureSampler;
uniform sampler2D normalMapSampler;

// Uniforms de Iluminação
uniform vec3 lightColor;
uniform float ambientStrength;
uniform int isSun;
uniform int useNormalMap; // 1 para usar normal map, 0 para usar normal padrão

void main()
{
    // 1. Ler a cor da textura
    vec3 textureColor = vec3(texture(textureSampler, TexCoord));

    if (isSun == 1) {
        // Se for o SOL, desenha apenas a cor da textura no brilho total (emite luz)
        FragColor = vec4(textureColor, 1.0);
        return;
    }
    
    // 2. Determinar a normal a usar (com ou sem normal map)
    vec3 normal;
    vec3 lightDir;
    vec3 viewDir;
    
    if (useNormalMap == 1) {
        // Usar normal map (espaço tangente)
        vec3 normalMapColor = texture(normalMapSampler, TexCoord).rgb;
        normal = normalize(normalMapColor * 2.0 - 1.0);
        lightDir = normalize(TangentLightPos - TangentFragPos);
        viewDir = normalize(TangentViewPos - TangentFragPos);
    } else {
        // Usar normal padrão (world space)
        normal = normalize(Normal);
        lightDir = normalize(TangentLightPos - FragPos);
        viewDir = normalize(TangentViewPos - FragPos);
    }
    
    // 3. Componente Ambiente
    vec3 ambient = ambientStrength * lightColor * textureColor;

    // 4. Componente Difuso
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * lightColor * textureColor;

    // 5. Componente Especular
    vec3 specularColor = vec3(0.5);
    float shininess = 32.0;
    
    vec3 reflectDir = reflect(-lightDir, normal);
    
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    vec3 specular = specularColor * spec;
    
    // 6. Cor Final (Ambient + Diffuse + Specular)
    vec3 result = ambient + diffuse + specular;
    
    FragColor = vec4(result, 1.0);
}