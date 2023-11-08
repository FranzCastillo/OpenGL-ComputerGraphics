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
# Makes a glitching effect on all the vertices
glitch_vertex_shader = """
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
        
        if (fract(time * 5.0) > 0.5) {
            gl_Position.x += sin(time * 1000.0);
            gl_Position.y += cos(time * 1000.0);
        }
    }
"""

# Vertex shader that makes the vertices look like a beating heart
heart_vertex_shader = """
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
        
        float beat = sin(time * 5.0) * 0.5 + 0.5;
        gl_Position.x *= beat;
        gl_Position.y *= beat;
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
# Implements a fragment shader that imitates a normal map
random_normal_map_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    uniform float time;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    // A pseudo-random function from [^1^][1]
    float random (vec2 co) {
        return fract (sin (dot (co, vec2 (12.9898, 78.233))) * 43758.5453);
    }
    
    void main() {
        vec3 n = normalize(normal);
        vec3 r = vec3(random(UVs), random(UVs + 0.1), random(UVs + 0.2));
        vec3 newNormal = normalize(n + r);
        fragColor = vec4(newNormal, 1.0);
    }
"""

rainbow_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    uniform float time;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        vec3 n = normalize(normal);
        vec3 r = vec3(sin(time), sin(time + 2.0), sin(time + 4.0));
        vec3 newNormal = normalize(n + r);
        float intensity = dot(newNormal, -vec3(0.0, 0.0, 1.0));
        fragColor = vec4(newNormal, 1.0) * intensity;
    }
"""

ripple_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    uniform float time;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        vec2 center = vec2(0.5, 0.5);
        float distance = length(center - UVs);
        float intensity = sin(distance * 100.0 - time * 10.0) * 0.5 + 0.5;
        fragColor = texture(tex, UVs) * intensity;
    }
"""

grayscale_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    uniform float time;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        vec4 color = texture(tex, UVs);
        float luminance = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));
        fragColor = vec4(luminance, luminance, luminance, 1.0);
    }
"""

fire_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    uniform float time;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    // A pseudo-random function from [^1^][1]
    float random (vec2 co) {
        return fract (sin (dot (co, vec2 (12.9898, 78.233))) * 43758.5453);
    }
    
    void main() {
        vec4 color = texture(tex, UVs);
        float noise = random(UVs + time);
        float intensity = dot(normal, vec3(0.0, 0.0, 1.0));
        fragColor = color * intensity * noise;
    }
"""

blur_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    uniform float time;
    
    in vec2 UVs;
    in vec3 normal;
    
    out vec4 fragColor;
    
    void main() {
        vec4 color = vec4(0.0);
        float weight = 1.0 / 9.0;
        for (int x = -1; x <= 1; x++) {
            for (int y = -1; y <= 1; y++) {
                color += texture(tex, UVs + vec2(x, y) * 0.001) * weight;
            }
        }
        fragColor = color;
    }
"""

glitch_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform float time;

    in vec2 UVs;
    in vec3 normal;

    out vec4 fragColor;

    void main() {
        vec4 color = texture(tex, UVs);
        if (fract(time * 5.0) > 0.5) {
            color.r = 1.0 - color.r;
            color.g = 1.0 - color.g;
            color.b = 1.0 - color.b;
        }
        fragColor = color;
    }
"""

heart_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;

    uniform float time;

    in vec2 UVs;
    in vec3 normal;

    out vec4 fragColor;

    void main() {
        vec4 color = texture(tex, UVs);
        float beat = sin(time * 5.0) * 0.5 + 0.5;
        fragColor = color * beat;
    }
"""