import pygame as pg

class World:
    def __init__(self, data, map_image):
        self.level_data = data
        self.image = map_image
        self.waypoints = []  # Inicializa a lista de waypoints aqui
        print(f"Waypoints inicializados: {self.waypoints}")  # Debug para confirmar inicialização
        
    def process_data(self):
        print("Iniciando o processamento de dados...")
        for layer in self.level_data["layers"]:
            print(f"Analisando camada: {layer['name']}")  # Debug
            if layer["name"] == "waypoints":
                for obj in layer["objects"]:
                    waypoint_data = obj.get("polyline", [])
                    print(f"Waypoints encontrados: {waypoint_data}")  # Debug
                    self.process_waypoints(waypoint_data)
                        
    def process_waypoints(self, data):
        print("Processando waypoints...")
        for point in data:
            temp_x = point.get("x")
            temp_y = point.get("y")
            print(f"Adicionando waypoint: ({temp_x}, {temp_y})")  # Debug
            self.waypoints.append((temp_x, temp_y))  # Adiciona os waypoints corretamente
        
    def draw(self, surface):
        surface.blit(self.image, (0, 0))
