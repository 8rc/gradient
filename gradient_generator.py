def interpolate_color(colors, factor: float):
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(rgb_color):
        return "#{:02x}{:02x}{:02x}".format(*rgb_color)
    
    num_colors = len(colors)
    
    if num_colors == 1:
        return colors[0]
    elif num_colors == 2:
        c1 = hex_to_rgb(colors[0])
        c2 = hex_to_rgb(colors[1])
        interpolated = tuple(int(c1[i] + (c2[i] - c1[i]) * factor) for i in range(3))
        return rgb_to_hex(interpolated)
    else:
        segment = 1 / (num_colors - 1)
        segment_index = int(factor / segment)
        if segment_index >= num_colors - 1:
            return colors[-1]
        else:
            sub_factor = (factor - segment_index * segment) / segment
            c1 = hex_to_rgb(colors[segment_index])
            c2 = hex_to_rgb(colors[segment_index + 1])
            interpolated = tuple(int(c1[i] + (c2[i] - c1[i]) * sub_factor) for i in range(3))
            return rgb_to_hex(interpolated)

def generate_gradient(text, *colors):
    lines = text.split('\n')
    max_length = max(len(line) for line in lines)
    gradient_text = []
    
    for i, line in enumerate(lines):
        new_line = []
        for j, char in enumerate(line):
            factor = j / max_length if max_length > 0 else 0
            color = interpolate_color(colors, factor)
            
            r, g, b = tuple(int(color[1:][i:i+2], 16) for i in (0, 2, 4))
            new_line.append(f"\033[38;2;{r};{g};{b}m{char}\033[0m")
        gradient_text.append(''.join(new_line))
    
    gradient_text.append('')
    
    return '\n'.join(gradient_text)
