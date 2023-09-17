def scrutinize_team(teams,team_id):
    if team_id == 100:
        ally_team = teams[0]
        enemy_team = teams[1]
    else:
        ally_team = teams[1]
        enemy_team = teams[0]
    ally_team_turret = ally_team['objectives']['tower']['kills']
    enemy_team_turret = enemy_team['objectives']['tower']['kills']
    ally_team_inhibitor = ally_team['objectives']['inhibitor']['kills']
    enemy_team_inhibitor = enemy_team['objectives']['inhibitor']['kills']
    ally_team_baron = ally_team['objectives']['baron']['kills']
    enemy_team_baron = enemy_team['objectives']['baron']['kills']
    ally_team_dragon = ally_team['objectives']['dragon']['kills']
    enemy_team_dragon = enemy_team['objectives']['dragon']['kills']
    ally_team_rift = ally_team['objectives']['riftHerald']['kills']
    enemy_team_rift = enemy_team['objectives']['riftHerald']['kills']
    ally_team_kills = ally_team['objectives']['champion']['kills']
    enemy_team_kills = enemy_team['objectives']['champion']['kills']
    return {'ally_tower_kills':ally_team_turret,'enemy_tower_kills':enemy_team_turret,'ally_inhibitor_kills':ally_team_inhibitor,'enemy_inhibitor_kills':enemy_team_inhibitor,
        'ally_baron_kills':ally_team_baron,'enemy_baron_kills':enemy_team_baron,'ally_dragon_kills':ally_team_dragon,'enemy_dragon_kills':enemy_team_dragon,
        'ally_rift_kills':ally_team_rift,'enemy_rift_kills':enemy_team_rift,'ally_kills':ally_team_kills,'enemy_kills':enemy_team_kills}

