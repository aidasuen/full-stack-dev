def calculate_team_performance(results):
   
    wins = results.count('win')
    
    if wins > len(results) / 2:
        return wins + 2 
    else:
        return wins
    
def player_performance(scores):
    total_score = 0
    for score in scores:
        if score > 30:
            total_score += score + 5 
        else:
            total_score += score
            
    average_score = total_score / len(scores) 
    return average_score

def final_report(team_results, player_scores):
  
    team_performance = calculate_team_performance(team_results)
    
    average_player_score = sum(player_scores) / len(player_scores)
    
    if team_performance >= 5 and average_player_score >= 20:
        return "Отличная команда"
    else:
        return "Можно и лучше"
    
team_results = ['win', 'loss', 'win', 'win', 'loss']
player_scores = [25, 35, 18, 40, 28]

team_performance = calculate_team_performance(team_results)
print(f"Итоговый результат команды: {team_performance}")

average_score = player_performance(player_scores)
print(f"Средний результат игрока: {average_score:.2f}")

report = final_report(team_results, player_scores)
print(f"Отчет: {report}")



