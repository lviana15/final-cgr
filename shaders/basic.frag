#version 330 core

in vec2 TexCoord;
in vec3 Normal;
in vec3 FragPos;

out vec4 FragColor;

void main()
{
    // Cor temporária (Laranja) para debug
    vec3 objectColor = vec3(1.0, 0.5, 0.31);
    
    // Iluminação ambiente fake bem simples para não ficar tudo chapado
    float ambientStrength = 0.5;
    vec3 lightColor = vec3(1.0, 1.0, 1.0);
    vec3 ambient = ambientStrength * lightColor;

    vec3 result = ambient * objectColor;
    FragColor = vec4(result, 1.0);
}
