#                       COG 2024 - IFSP Salto - Grupo 6
#       Renderização de Objetos 3D usando Projeções Ortogonais e Perspectivas

#   Nicolas Alberto Arvani Pereira
#   Isabella Bicudo de Souza
#   Erick Henrique de Araújo Moreira
#   Fernanda Miyuki Egawa
#   Gustavo Milan Cardoso
#   Maria Eduarda Guedes

# Utilização: py grupo6.py <objeto .obj>



import pygame
import sys
import math
from pygame.locals import *

# Inicialização do Pygame
pygame.init()
pygame.font.init()
h1 = pygame.font.SysFont("Arial", 18)
h2 = pygame.font.SysFont("Arial", 16)
h3 = pygame.font.SysFont("Arial", 14)
h4 = pygame.font.SysFont("Arial", 12)

# Variáveis globais
WIDTH, HEIGHT = 800, 600
SCALE = 50
CAM_DIST = WIDTH // 2 / SCALE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projeção Ortogonal vs Perspectiva")

# Variáveis para o objeto carregado
obj_points = []
obj_faces = []

# Função para carregar e processar o objeto .obj
def load_obj(filename):
    global obj_points, obj_faces

    # Definir as faces (Sem utilizar o pywavefront, pois ele triangula as faces automaticamente)
    # Ler o arquivo e pegar todas as linhas que começam com 'f'
    with open(filename, 'r') as f:
        lines = f.readlines()
    faces = []
    for line in lines:
        if line.startswith('v'):
            if(line.split()[0] != 'v'):
                continue
            vs = line.split()[1:4]
            for i in range(len(vs)):
                vs[i] = float(vs[i])
            obj_points.append(vs)

        elif line.startswith('f'):
            if(line.split()[0] != 'f'):
                continue
            vs = line.split()[1:]
            for i in range(len(vs)):
                vs[i] = int(vs[i].split('/')[0]) - 1 # indice comeca em 1 (._.)
            obj_faces.append(vs)

    print("Objeto carregado com sucesso!")



# Função para projeção ortogonal
def orthogonal_projection(point):
    # Ignora o z e apenas escala o x e o y
    x, y, z = point
    return (WIDTH // 2 + x * SCALE, HEIGHT // 2 - y * SCALE)

# Função para projeção em perspectiva
def perspective_projection(point):
    # Não posso ignorar o Z
    x, y, z = point
    factor = CAM_DIST / (CAM_DIST + z)          # Fator de zoom da camera
    
    # Projeção em perspectiva (usando o fator de zoom da camera) 
    x_proj = x * SCALE * factor + WIDTH // 2    
    y_proj = -y * SCALE * factor + HEIGHT // 2  
    
    # Retorno um ponto 2D
    return (x_proj, y_proj)

# Função de rotação dos pontos 3D
def rotate(point, angle_x, angle_y, angle_z, obj_points):
    x, y, z = point
    
    # Rotação utilizando o centro do objeto
    obj_center = (sum(x for x, y, z in obj_points) / len(obj_points), sum(y for x, y, z in obj_points) / len(obj_points), sum(z for x, y, z in obj_points) / len(obj_points))
    x, y, z = x - obj_center[0], y - obj_center[1], z - obj_center[2]

    # Rotação em torno do eixo X
    cos_x = math.cos(angle_x)
    sin_x = math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x

    # Rotação em torno do eixo Y
    cos_y = math.cos(angle_y)
    sin_y = math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y

    # Rotação em torno do eixo Z
    cos_z = math.cos(angle_z)
    sin_z = math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z

    x, y, z = x + obj_center[0], y + obj_center[1], z + obj_center[2]

    return (x, y, z)

# Função para desenhar o cubo com projeção e opção de preenchimento com transparência
def draw_cube(points, projection_func, fill_mode=False, line_mode=True, point_mode=True, color=(100, 100, 255, 128), line_color=(255, 255, 255)):
    # Superfície transparente para desenhar as faces preenchidas (preciso usar uma superficie com alfa para o preenchimento)
    fill_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # Desenhar as faces com preenchimento transparente, se `fill_mode` estiver ativo
    if fill_mode:
        for face in obj_faces:  # Desenhar as faces
            face_points = [projection_func(points[i]) for i in face]
            pygame.draw.polygon(fill_surface, color, face_points)  # Cor de preenchimento com transparência

    if line_mode:
        for face in obj_faces:  # Para cada face vou desenhar as linhas dela
            for i in range(len(face)):
                start, end = face[i], face[(i + 1) % len(face)] # Primeiro vertice e o proximo (desenhar as linhas)
                pygame.draw.line(screen, line_color, projection_func(points[start]), projection_func(points[end]), 1)

    # Desenhar os pontos do cubo
    if point_mode:
        for point in points:
            x, y = projection_func(point)
            pygame.draw.circle(screen, line_color, (x, y), 3)

        # Desenhar o ponto central do objeto
        ponto_central = (sum(x for x, y, z in points) / len(points), sum(y for x, y, z in points) / len(points), sum(z for x, y, z in points) / len(points))
        pygame.draw.circle(screen, line_color, projection_func(ponto_central), 3)

    # Sobrepor a superfície transparente na tela principal
    screen.blit(fill_surface, (0, 0))

def draw_background():
    # Grade para visualizar as projeções
    color = (25, 25, 25)

    for x in range(-10, 11):
        pygame.draw.line(screen, color, orthogonal_projection((x, -10, 0)), orthogonal_projection((x, 10, 0)))
    for y in range(-10, 11):
        pygame.draw.line(screen, color, orthogonal_projection((-10, y, 0)), orthogonal_projection((10, y, 0)))

# Pegar o primeiro argumento do programa e abrir o arquivo obj
load_obj(sys.argv[1])

clock = pygame.time.Clock()
angle_x, angle_y, angle_z = 0, 0, 0  # Ângulos de rotação para cada eixo

# Configurações iniciais
fill_mode = True  # Modo de preenchimento ativo por padrão
line_mode = True
point_mode = True

# Distância dos objetos
dist_between = 2
dist_x = 0
dist_y = 0

rotating = False

shift = False

# Configurações de projeção
projecao_ortogonal = True
projecao_perspectiva = True
while True:
    screen.fill((0, 0, 0))

    # Tratamento de eventos
    for event in pygame.event.get():
        if event.type == QUIT: # Sair do programa
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL: # Scroll do mouse - alterar zoom
            # Calculando o zoom da camera
            SCALE = max(2, SCALE + event.y * 0.5)
            CAM_DIST = WIDTH // 2 / SCALE

        elif event.type == KEYDOWN: # Tratamento de teclado
            if event.key == K_f:
                fill_mode = not fill_mode   # Alterna o modo de preenchimento
            elif event.key == K_l:
                line_mode = not line_mode   # Alterna o modo de linhas
            elif event.key == K_r:
                if shift:    # R maiusculo para resetar a rotação
                    angle_x, angle_y, angle_z = 0, 0, 0
                else:        # R (sem shift) para alternar o modo de rotação
                    rotating = not rotating
            elif event.key == K_RSHIFT or event.key == K_LSHIFT: # Habilitar o shift
                shift = True
                
            elif event.key == K_p:      # P para alternar o modo de pontos
                point_mode = not point_mode

            # Posição do objeto
            elif event.key == K_LEFT:
                dist_x = dist_x - 0.1
            elif event.key == K_RIGHT:
                dist_x = dist_x + 0.1
            elif event.key == K_UP:
                dist_y += 0.1
            elif event.key == K_DOWN:
                dist_y -= 0.1

            # Alterar distância entre os objetos
            elif event.key == K_COMMA:
                dist_between = dist_between - 0.10
            elif event.key == K_PERIOD:
                dist_between = dist_between + 0.10

            # Exibição de cada projeção
            elif event.key == K_1:
                projecao_ortogonal = not projecao_ortogonal
            elif event.key == K_2:
                projecao_perspectiva = not projecao_perspectiva
                
            # Posicionamento automático dos objetos
            elif event.key in [K_KP0, K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9]:
                if event.key == K_KP0:      # centro
                    dist_x, dist_y = 0, 0
                elif event.key == K_KP1:    # inferior esquerda
                    dist_x, dist_y = -3, -3
                elif event.key == K_KP2:    # inferior centro
                    dist_x, dist_y = 0, -3
                elif event.key == K_KP3:    # inferior direita
                    dist_x, dist_y = 3, -3
                elif event.key == K_KP4:    # centro esquerda
                    dist_x, dist_y = -3, 0
                elif event.key == K_KP5:    # centro
                    dist_x, dist_y = 0, 0
                elif event.key == K_KP6:    # centro direita
                    dist_x, dist_y = 3, 0
                elif event.key == K_KP7:    # superior esquerda
                    dist_x, dist_y = -3, 3
                elif event.key == K_KP8:    # superior centro
                    dist_x, dist_y = 0, 3
                elif event.key == K_KP9:    # superior direita
                    dist_x, dist_y = 3, 3

            # Alterações de ângulos
            elif event.key == K_PLUS or event.key == K_KP_PLUS:
                angle_x += 0.1
                angle_y += 0.1
                angle_z += 0.1
            elif event.key == K_MINUS or event.key == K_KP_MINUS:
                angle_x -= 0.1
                angle_y -= 0.1
                angle_z -= 0.1
        
        elif event.type == KEYUP: # Só tratamento do shift
            if event.key == K_RSHIFT or event.key == K_LSHIFT:
                shift = False

    # Atualiza ângulos de rotação para animação contínua
    if(rotating):
        angle_x += 0.01
        angle_y += 0.01
        angle_z += 0.01

    # Rotaciona o objeto
    rotated_points = [rotate(point, angle_x, angle_y, angle_z, obj_points) for point in obj_points]

    # Cor do objeto
    o_color = (100, 100, 255, 128)
    p_color = (255, 100, 100, 128)

    # Cor da linha
    ol_color = (0, 0, 255)
    pl_color = (255, 0, 0)

    # Desenha o plano de fundo
    draw_background()

    # Desenha o cubo usando as duas projeções, com ou sem preenchimento
    if projecao_ortogonal:
        draw_cube([(x + dist_x - dist_between, y + dist_y, z) for x, y, z in rotated_points], orthogonal_projection, fill_mode, line_mode, point_mode, o_color, ol_color)  # Projeção ortogonal
    if projecao_perspectiva:
        draw_cube([(x + dist_x + dist_between, y + dist_y, z) for x, y, z in rotated_points], perspective_projection, fill_mode, line_mode, point_mode, p_color, pl_color)  # Projeção em perspectiva

    # Desenhando os textos com informações de distância e rotação
    text_surface = h2.render(f"Distância dos objetos: X: {dist_x:.2f} | Y: {dist_y:.2f}", True, (255, 255, 255))
    screen.blit(text_surface, (10, 10))
    
    text_surface = h2.render(f"Rotação Atual: X: {angle_x:.2f} | Y: {angle_y:.2f} | Z: {angle_z:.2f}", True, (255, 255, 255))
    screen.blit(text_surface, (10, 30))
    
    text_surface = h3.render(f"Modos: Fill: {fill_mode} | Line: {line_mode} | Rotação: {rotating} | Ponto: {point_mode}", True, (255, 255, 255))
    
    left_edge = WIDTH - text_surface.get_width() - 10 # calcular a distancia para aparecer o texto na direita
    screen.blit(text_surface, (left_edge, 10))

    # Desenhando os textos de ajuda
    text_surface = h4.render("Pressione 'P' para alternar o modo de pontos", True, (255, 255, 255))
    left_edge = WIDTH - text_surface.get_width() - 10
    screen.blit(text_surface, (left_edge, HEIGHT - text_surface.get_height() - 70))
    
    text_surface = h4.render("Pressione 'R' para alternar o modo de rotação", True, (255, 255, 255))
    left_edge = WIDTH - text_surface.get_width() - 10
    screen.blit(text_surface, (left_edge, HEIGHT - text_surface.get_height() - 50))

    text_surface = h4.render("Pressione 'L' para alternar o modo de linhas", True, (255, 255, 255))
    left_edge = WIDTH - text_surface.get_width() - 10
    screen.blit(text_surface, (left_edge, HEIGHT - text_surface.get_height() - 30))

    text_surface = h4.render("Pressione 'F' para alternar o modo de preenchimento", True, (255, 255, 255))
    left_edge = WIDTH - text_surface.get_width() - 10
    screen.blit(text_surface, (left_edge, HEIGHT - text_surface.get_height() - 10))

    # Desenhando os textos sobre o trabalho
    text_surface = h4.render("Projeção Ortogonal vs Perspectiva", True, (255, 255, 255))
    screen.blit(text_surface, (10, HEIGHT - text_surface.get_height() - 25))

    text_surface = h3.render("Grupo 6 - Renderização de Objetos 3D usando Projeções Ortogonais e Perspectivas", True, (255, 255, 255))
    screen.blit(text_surface, (10, HEIGHT - text_surface.get_height() - 10))


    pygame.display.flip()
    clock.tick(60)
