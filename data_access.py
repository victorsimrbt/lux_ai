from kaggle_environments import make
import numpy as np

def get_game_data(gs):
    game_map = gs.map.map
    resource_matrix = []
    citytile_matrix = []
    road_matrix = []

    for row in game_map:
        for cell in row:
            resource_matrix.append(cell.resource)
            citytile_matrix.append(cell.citytile)
            road_matrix.append(cell.road)

    sqrt = np.sqrt(len(resource_matrix)).astype(int)
    resource_matrix = np.array(resource_matrix).reshape(sqrt,sqrt)
    citytile_matrix = np.array(citytile_matrix).reshape(sqrt,sqrt)
    road_matrix = np.array(road_matrix).reshape(sqrt,sqrt)
    
    resource_dict = {
    'wood':1,
    'coal':2,
    'uranium':3
}
    resourcetype_matrix = np.array([resource.type 
                                    if resource 
                                    else None 
                                    for resource in resource_matrix.flatten()]).reshape(sqrt,sqrt)
    resourcetype_matrix = np.where(resourcetype_matrix==None, 0, resourcetype_matrix)

    for value in resource_dict.keys():
        resourcetype_matrix = np.where(resourcetype_matrix==value, resource_dict[value], resourcetype_matrix)
        
    resourceamount_matrix = np.array([resource.amount
                                    if resource 
                                    else None 
                                    for resource in resource_matrix.flatten()]).reshape(sqrt,sqrt)
    resourceamount_matrix = np.where(resourceamount_matrix==None, 0, resourceamount_matrix)
    
    player1,player2 = gs.players
    units = [player1.units,player2.units]
    cities = [player1.cities.values(),player2.cities.values()]

    coal = [player1.researched_coal(),player2.researched_coal()]
    uranium = [player2.researched_uranium(),player2.researched_uranium()]
    research_points = [player1.research_points,player2.research_points]
    
    def fill_bitmatrix(val):
        a = np.zeros((sqrt,sqrt))
        a.fill(val)
        return a

    coal_research_matrices = list(map(fill_bitmatrix,coal))
    uranium_research_matrices = list(map(fill_bitmatrix,uranium))
    research_matrices = list(map(fill_bitmatrix,research_points))
    
    def fuel_matrix(cities):
        matrix = np.zeros((sqrt,sqrt))
        for city in cities:
            fuel = city.fuel
            for citytiles in city.citytiles:
                pos = (citytiles.pos.x,citytiles.pos.y)
                matrix[pos] = fuel
        return matrix

    def lightupkeep_matrix(cities):
        matrix = np.zeros((sqrt,sqrt))
        for city in cities:
            light = city.get_light_upkeep()
            for citytiles in city.citytiles:
                pos = (citytiles.pos.x,citytiles.pos.y)
                matrix[pos] = light
        return matrix

    citytileteam_matrix = []
    for citytile in citytile_matrix.flatten():
        if citytile:
            if citytile.team == 0:
                citytileteam_matrix.append(-1)
            else:
                citytileteam_matrix.append(citytile.team)
        else:
            citytileteam_matrix.append(0)
    citytileteam_matrix = np.array(citytileteam_matrix).reshape(sqrt,sqrt)

    citytilecooldown_matrix = np.array([citytile.cooldown
                                    if citytile
                                    else 0
                                    for citytile in citytile_matrix.flatten()]).reshape(sqrt,sqrt)
                

    fuel_matrices = list(map(fuel_matrix,cities))
    lightupkeep_matrices= list(map(lightupkeep_matrix,cities))
    
    def cooldown_matrix(units):
        matrix = np.zeros((sqrt,sqrt))
        for unit in units:
            cooldown = unit.cooldown
            pos = (unit.pos.x,unit.pos.y)
            matrix[pos] = cooldown
        return matrix

    def cargo_matrix(units):
        wood_matrix = np.zeros((sqrt,sqrt))
        coal_matrix = np.zeros((sqrt,sqrt))
        uranium_matrix = np.zeros((sqrt,sqrt))
        for unit in units:
            wood = unit.cargo.wood
            coal = unit.cargo.coal
            uranium = unit.cargo.uranium
            
            pos = (unit.pos.x,unit.pos.y)
            
            wood_matrix[pos] = wood
            coal_matrix[pos] = coal
            uranium_matrix[pos] = uranium
        return [wood_matrix,coal_matrix,uranium_matrix]

    cooldown_matrices = list(map(cooldown_matrix,units))
    cargo_matrices = list(map(cargo_matrix,units))
    
    data_matrices = np.array([resourcetype_matrix,resourceamount_matrix,
                 road_matrix,
                 coal_research_matrices[0],coal_research_matrices[1],
                 uranium_research_matrices[0],uranium_research_matrices[1],
                 research_matrices[0], research_matrices[1],
                 citytileteam_matrix,citytilecooldown_matrix,
                 fuel_matrices[0],fuel_matrices[1],
                 lightupkeep_matrices[0],fuel_matrices[1],
                 cooldown_matrices[0],cooldown_matrices[1],
                 cargo_matrices[0][0],cargo_matrices[0][1],cargo_matrices[0][2],
                 cargo_matrices[1][0],cargo_matrices[1][1],cargo_matrices[1][2]
                 ])
    
    return data_matrices