import pygame
import sys
import numpy as np
import networkx as nx
import random
from vmi import move, mark_edge, Trémaux


size = (20, 20)
G = nx.grid_2d_graph(size[0], size[1])
start, goal = (0,0), (19, 19)




########## Labirintusgenerálás
def random_DFS_tree(G, start, goal):
    T_edges = []
    discovered = set()
    visited = [start]

    goal_reached = False
    solution = [start] 

    while visited:
        v = visited.pop()
        
        if v == goal and not goal_reached:
            goal_reached = True
            discovered.add(goal)
            continue

        nexts = list(set(G[v].keys())-discovered-set(visited))
        
        if nexts:
            next = random.choice(nexts)
            nexts.remove(next)
            
            if nexts:
                visited.append(v)
            else:
                discovered.add(v)
            
            T_edges.append((v, next))
            if not goal_reached:
                
                i  = 0
                while solution[-1] != v:
                    solution.append(solution[i])
                    i -= 2
                
                solution.append(next)

            visited.append(next)
        else:
            discovered.add(v)

    return T_edges, solution


tree_edges, sol = random_DFS_tree(G, start, goal)
T = nx.from_edgelist(tree_edges)




########## DFS megoldás

def sub_list(list_1, list_2):
    sub = []
    for i in list_1:
        if i not in list_2:
            sub.append(i)
    return sub

def DFS_solve(G, start, goal):
    v_level = dict()
    for vertex in G:
        v_level[vertex] = -1
    v_level[start] = 0
    
    visited = []
    solution = []
    v = start

    while True:
        solution.append(v)
        if v not in visited:
            visited.append(v)
        
        if v == goal:
            break
        
        nexts = sub_list(list(G[v].keys()), visited)

        if nexts:
            next = nexts[0]
            v_level[next] = v_level[v] + 1
            v = next
        else:    
            while not sub_list(list(G[v].keys()), visited):
                for i in list(G[v].keys()):
                    if v_level[i] == v_level[v] - 1:
                        v = i
                        solution.append(v)
                        break
            solution.pop()

    return solution
                 






########## Balkézszabály megoldás
def left_hand_rule(G, start, goal):
    done = False
    v = start
    r = (0, 1)
    l = (0, -1)
    u = (-1, 0)
    d = (1, 0)
    r = np.array(r)
    l = np.array(l)
    u = np.array(u)
    d = np.array(d)
    start = np.array(start)
    goal = np.array(goal)
    route = [start]
    if (tuple(start), tuple(start+d)) in G.edges():
        v = start+d
        direction = 'd'  #egy csúcsba fentről jövök le
        route.append(v) 
    else:
        v = start+r 
        direction = 'r' #egy csúcsba balról jövök be
        route.append(v)
    while not done:
        if direction == 'r':
            if (tuple(v), tuple(v+d)) in G.edges():
                v = v+d
                direction = 'd'
                route.append(v)
            elif (tuple(v), tuple(v+r)) in G.edges():
                v = v+r
                direction = 'r'
                route.append(v)
            elif (tuple(v), tuple(v+u)) in G.edges():
                v = v+u
                direction = 'u'
                route.append(v)
            else:
                direction = 'l'
                v = v+l
                route.append(v)
        elif direction == 'l':
            if (tuple(v), tuple(v+u)) in G.edges():
                v = v+u
                direction = 'u'
                route.append(v)
            elif (tuple(v), tuple(v+l)) in G.edges():
                v = v+l
                direction = 'l'
                route.append(v)
            elif (tuple(v), tuple(v+d)) in G.edges():
                v = v+d
                direction = 'd'
                route.append(v)
            else:
                direction = 'r'
                v = v+r
                route.append(v)
        elif direction == 'u':
            if (tuple(v), tuple(v+r)) in G.edges():
                v = v+r
                direction = 'r'
                route.append(v)
            elif (tuple(v), tuple(v+u)) in G.edges():
                v = v+u
                direction = 'u'
                route.append(v)
            elif (tuple(v), tuple(v+l)) in G.edges():
                v = v+l
                direction = 'l'
                route.append(v)
            else:
                direction = 'd'
                v = v+d
                route.append(v)
        elif direction == 'd':
            if (tuple(v), tuple(v+l)) in G.edges():
                v = v+l
                direction = 'l'
                route.append(v)
            elif (tuple(v), tuple(v+d)) in G.edges():
                v = v+d
                direction = 'd'
                route.append(v)
            elif (tuple(v), tuple(v+r)) in G.edges():
                v = v+r
                direction = 'r'
                route.append(v)
            else:
                direction = 'u'
                v = v+u
                route.append(v)

        if tuple(v) == tuple(goal):
            done = True
    return route



########## A felhasználó algoritmust választ
choice = input("Melyik megoldást választod? Trémaux-T, Balkéz szabály-B, DFS-D: ").strip().upper()

########## Megoldás az input alapján
if choice == 'T':
    solutionn = Trémaux(T, start, goal)
elif choice == 'B':
    solutionn = left_hand_rule(T, start, goal)
elif choice == 'D':
    solutionn = DFS_solve(T, start, goal)
else:
    print("Nem érvényes választás, marad a Trémaux.")
    solution = Trémaux(T, start, goal)


########## Az algoritmus általi mozgás irányai, listába szervezve

def listamaker(inp):
    out = []
    for i in range(len(inp)-1):
        out.append((inp[i+1][0]-inp[i][0], inp[i+1][1]-inp[i][1]))
    return out

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)
    x_coordinate, y_coordinate = 10, 10
    lista = np.array(listamaker(solutionn))*20
    i = 0
    edges = tree_edges
    y=0

    
    while True:
        drawGrid()
        draw_lines()
        draw_exit_entrance()
        ########## A falak kirajzolása
        for j in range(len(edges)):
            if edges[j][0][0] == edges[j][1][0]:
                y = min(edges[j][0][1], edges[j][1][1])
                draw_wall((edges[j][0][0]*20, y*20+20-1), (edges[j][0][0]*20+20, y*20+20-1))
            else:
                x = min(edges[j][0][0], edges[j][1][0])
                draw_wall((x*20+20-1, edges[j][0][1]*20), (x*20+20-1, edges[j][0][1]*20+20))
        
        
        ########## Mozgás
        x_old, y_old, x_coordinate, y_coordinate = move(x_coordinate, y_coordinate, lista[i])
        drawpoint(x_coordinate, y_coordinate)
        delete(x_old, y_old)
        i += 1
        if i == len(lista)+1:
            print(lista[-1])
            CLOCK.tick(1)
            pygame.quit()
            sys.exit()
        
        CLOCK.tick(8)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        

########## Labirintus, kijárat, bejárat, mozgó pont, falak megrajzolása

def drawGrid():
    blockSize = 20 
    for x in range(0, WINDOW_WIDTH, blockSize):
        for y in range(0, WINDOW_HEIGHT, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(SCREEN, WHITE, rect, 2)

def draw_exit_entrance():
    pygame.draw.rect(SCREEN, 'green', (385, 385, 12, 12))
    pygame.draw.rect(SCREEN, 'green', (5, 3, 12, 12))
def drawpoint(x, y):
    pygame.draw.circle(SCREEN, 'white', (x, y), 5)
def delete(x,y):
    pygame.draw.circle(SCREEN, BLACK, (x, y), 5)

def draw_lines():
    pygame.draw.lines(SCREEN, 'red', True, [(0, 0), (398, 0), (398, 398),(0, 398)], 2)
    pygame.draw.line(SCREEN, 'white', (0, 0),(20, 0), 2)
    pygame.draw.line(SCREEN, 'white', (378, 398),(398, 398), 2)


def move(x, y, direction):
    x_new = x + direction[0]
    y_new = y + direction[1]
    return x, y, x_new, y_new


def draw_wall(start, end):
    pygame.draw.line(SCREEN, 'black', start, end, 4)

def graph():
    return nx.grid_2d_graph(20,20)




main()

