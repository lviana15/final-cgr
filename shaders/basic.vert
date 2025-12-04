#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;
layout (location = 2) in vec3 aNormal;
layout (location = 3) in vec3 aTangent;
layout (location = 4) in vec3 aBitangent;

out vec2 TexCoord;
out vec3 Normal;
out vec3 FragPos;

// Vetores transformados para espaço tangente
out vec3 TangentLightPos;
out vec3 TangentViewPos;
out vec3 TangentFragPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

// Uniforms de iluminação (em world space)
uniform vec3 lightPos;
uniform vec3 viewPos;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    
    FragPos = vec3(model * vec4(aPos, 1.0));
    TexCoord = aTexCoord;
    
    // Transformar normais, tangentes e bitangentes para world space
    vec3 T = normalize(vec3(model * vec4(aTangent, 0.0)));
    vec3 B = normalize(vec3(model * vec4(aBitangent, 0.0)));
    vec3 N = normalize(vec3(model * vec4(aNormal, 0.0)));
    
    // Re-ortogonalizar usando Gram-Schmidt (T = T - (T·N)N)
    T = normalize(T - dot(T, N) * N);
    // B = N × T
    B = cross(N, T);
    
    // Matriz TBN para transformar do world space para tangent space
    mat3 TBN = transpose(mat3(T, B, N));
    
    // Transformar posições e vetores para espaço tangente
    TangentLightPos = TBN * lightPos;
    TangentViewPos = TBN * viewPos;
    TangentFragPos = TBN * FragPos;
    
    Normal = N;
}
