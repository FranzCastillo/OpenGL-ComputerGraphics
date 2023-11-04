# Graphics Library Shader Language: GLSL

vertex_shader = """
    #version 450 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec2 texCoords;
    layout (location = 2) in vec3 normals;
    
    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    uniform float time;
    
    out vec2 UVs;
    out vec3 normal;
    
    void main() {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        UVs = texCoords;
        normal = normalize(
            (modelMatrix * vec4(normals, 0.0)).xyz
        );
    }
"""

fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        fragColor = texture(tex, UVs);
    }
"""

gourad_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    uniform vec3 directionalLight;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        float intensity = dot(normal, -directionalLight);
        fragColor = texture(tex, UVs) * intensity;
    }
"""

pixelated_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    uniform float time;
    uniform float fatness;
    
    in vec2 UVs;
    
    out vec4 fragColor;
    
    void main() {
        float pixelSize = 1.0 / 64.0;
        vec2 pixelUVs = floor(UVs / pixelSize) * pixelSize;
        fragColor = texture(tex, pixelUVs);
    }   
"""

tvStatic_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;

    uniform float time;
    uniform float fatness;
    
    in vec2 UVs;
    
    out vec4 fragColor;
    
    // A pseudo-random function from [^1^][1]
    float random (vec2 co) {
        return fract (sin (dot (co, vec2 (12.9898, 78.233))) * 43758.5453);
    }
    
    void main() {
        fragColor = texture(tex, UVs);
        float flash = sin(time * 5.0) * 0.7 + 0.5;
        if (flash > 0.9) {
            float r = random (vec2 (time, UVs.x));
            float g = random (vec2 (time, UVs.y));
            float b = random (vec2 (time, UVs.x + UVs.y));
            fragColor = vec4(r, g, b, 1.0);
        }
    }
"""