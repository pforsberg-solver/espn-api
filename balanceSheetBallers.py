import random
from espn_api.football import League

league = League(league_id=2131413492
                , year=2026
                , espn_s2='AEArWtxiccR7mRFrm39jJUIcvGMHKJfqpdLdzzhdEphCZwTWkosIbXFMFRSQ7hwsx3X7Neo3Sfr7SmNgY%2B6S3KG4thw1YNzpodGSayx%2Feb%2FiTtdECcLJGOguMh05JX56fy8PZdowGUhFZ8sjx9c3vHuiRECqYR2rL%2FAYjPX0Pg4xHZWA0WNYh61ucH9pTBcyJ30U7UjYXvLXX8UfoEZ2C%2FWQ1grRUqw181%2FMr4wQxucAdTGgzbJ7ES%2FZNK4r00GFEgSBa2%2BbAJyMaI8NlbMeH7NEkL3IBuW5I09gUHWT0N6WIJo%2F9NyY8mrAktWPqdltLLvtDnCx%2FZQbu5DeA2kmaRuQiv9WOYD5eWhYxbGEOtvmdg%3D%3D'
                , swid='{A7CA2027-1CE5-40B9-9968-8301C42A779B}'
                , debug=False
            )


# Target the current week or choose a specific week (e.g., week = 1)
target_week = 1 #league.current_week

# Comedic personality templates
# Tiered Roasts based on severity
mild_roasts = [
    "Not a fatal error, but definitely leaving money on the table.",
    "A minor lapse in judgment. We'll let it slide... for now.",
    "Left a few crumbs on the bench, but you'll survive."
]

severe_roasts = [
    "An absolute masterclass in self-sabotage. Shocking management.",
    "Rumor has it this manager sets their lineup by throwing darts blindfolded.",
    "This belongs in a museum of bad fantasy decisions. Truly tragic.",
    "Please hand your roster over to an AI. It literally cannot do worse than this.",
    "Leaving this many points on the bench should be a point-deductible offense.",
    "Did you forget to hit submit, or do you just actively hate winning?"
]

injury_commentary = [
    "is currently pursuing a full-time career as an orthopedic consultant.",
    "is contributing absolutely nothing except an expensive medical bill and bad vibes.",
    "has single-handedly tanking this team's insurance premiums.",
    "is providing elite emotional support from a motorized scooter.",
    "is listed as out with a severe case of 'not helping your fantasy team'.",
    "has an injury timeline longer than this franchise's future outlook."
]

print("=============================================================")
print(f"       🚫 WEEK {target_week} SHAME, ROASTS, & POWER RANKINGS 🚫       ")
print("=============================================================")

print("\n🚨 THE HALL OF SHAME (TRUE BENCH BLUNDERS - BY TEAM):")
print("-------------------------------------------------------------")

box_scores = league.box_scores(week=target_week)
has_blunders = False

# Variables to track the absolute worst move of the week
worst_move_team = None
worst_move_bench_player = ""
worst_move_start_player = ""
worst_move_diff = 0
worst_move_pos = ""
worst_move_bench_pts = 0
worst_move_start_pts = 0

# Dictionary to hold optimal point breakdowns
team_max_points_summary = {}

for match in box_scores:
    matchups_to_check = [
        {"team": match.home_team, "lineup": match.home_lineup, "actual_score": match.home_score},
        {"team": match.away_team, "lineup": match.away_lineup, "actual_score": match.away_score}
    ]
    
    for game in matchups_to_check:
        squad = game["team"]
        lineup = game["lineup"]
        actual_score = game["actual_score"]
        
        if not squad or not lineup:
            continue
            
        # Separate ALL rostered players strictly by true football position
        all_qbs = sorted([p for p in lineup if p.position == 'QB'], key=lambda p: getattr(p, 'points', 0), reverse=True)
        all_rbs = sorted([p for p in lineup if p.position == 'RB'], key=lambda p: getattr(p, 'points', 0), reverse=True)
        all_wrs = sorted([p for p in lineup if p.position == 'WR'], key=lambda p: getattr(p, 'points', 0), reverse=True)
        all_tes = sorted([p for p in lineup if p.position == 'TE'], key=lambda p: getattr(p, 'points', 0), reverse=True)
        all_dst = sorted([p for p in lineup if p.position in ['D/ST', 'DEF']], key=lambda p: getattr(p, 'points', 0), reverse=True)
        all_ks = sorted([p for p in lineup if p.position == 'K'], key=lambda p: getattr(p, 'points', 0), reverse=True)

        # --- DYNAMIC MAXIMUM POINTS CALCULATION ---
        opt_qb = all_qbs[0].points if all_qbs else 0
        opt_te = all_tes[0].points if all_tes else 0
        opt_dst = all_dst[0].points if all_dst else 0
        opt_k = all_ks[0].points if all_ks else 0

        opt_rbs = all_rbs[:2]
        opt_wrs = all_wrs[:2]
        
        remaining_rbs = all_rbs[2:]
        remaining_wrs = all_wrs[2:]
        remaining_tes = all_tes[1:]
        
        flex_pool = sorted(remaining_rbs + remaining_wrs + remaining_tes, key=lambda p: getattr(p, 'points', 0), reverse=True)
        opt_flex = flex_pool[0].points if flex_pool else 0

        max_possible_score = round(opt_qb + sum(p.points for p in opt_rbs) + sum(p.points for p in opt_wrs) + opt_te + opt_flex + opt_dst + opt_k, 1)
        efficiency = round((actual_score / max_possible_score) * 100, 1) if max_possible_score > 0 else 100

        team_max_points_summary[squad.team_name] = {
            "actual": actual_score,
            "max": max_possible_score,
            "efficiency": efficiency
        }

        # --- TRUE LINEUP BLUNDER DETECTION ---
        starters_by_pos = {
            'QB': [p for p in lineup if p.slot_position == 'QB'],
            'RB': [p for p in lineup if p.slot_position in ['RB', 'FLEX']],
            'WR': [p for p in lineup if p.slot_position in ['WR', 'FLEX']],
            'TE': [p for p in lineup if p.slot_position == 'TE'],
            'D/ST': [p for p in lineup if p.slot_position in ['D/ST', 'DEF']],
            'K': [p for p in lineup if p.slot_position == 'K']
        }
        
        bench_by_pos = {
            'QB': [p for p in lineup if p.slot_position == 'BE' and p.position == 'QB'],
            'RB': [p for p in lineup if p.slot_position == 'BE' and p.position == 'RB'],
            'WR': [p for p in lineup if p.slot_position == 'BE' and p.position == 'WR'],
            'TE': [p for p in lineup if p.slot_position == 'BE' and p.position == 'TE'],
            'D/ST': [p for p in lineup if p.slot_position == 'BE' and p.position == 'D/ST'],
            'K': [p for p in lineup if p.slot_position == 'BE' and p.position == 'K']
        }
        
        team_blunders = []
        total_missed_points = 0
        
        for pos in ['QB', 'RB', 'WR', 'TE', 'D/ST', 'K']:
            starts = starters_by_pos[pos]
            bench = bench_by_pos[pos]
            
            if starts and bench:
                worst_starter = min(starts, key=lambda p: getattr(p, 'points', 0))
                best_bench = max(bench, key=lambda p: getattr(p, 'points', 0))
                
                if best_bench.points > worst_starter.points:
                    diff = round(best_bench.points - worst_starter.points, 1)
                    total_missed_points += diff
                    team_blunders.append({
                        "pos": pos,
                        "bench_name": best_bench.name,
                        "bench_pts": best_bench.points,
                        "start_name": worst_starter.name,
                        "start_pts": worst_starter.points,
                        "diff": diff
                    })
                    
                    if diff > worst_move_diff:
                        worst_move_diff = diff
                        worst_move_team = squad.team_name
                        worst_move_bench_player = best_bench.name
                        worst_move_start_player = worst_starter.name
                        worst_move_pos = pos
                        worst_move_bench_pts = best_bench.points
                        worst_move_start_pts = worst_starter.points

        if team_blunders:
            has_blunders = True
            print(f"❌ Team: {squad.team_name}")
            for blunder in team_blunders:
                print(f"   👉 [{blunder['pos']}] Benched {blunder['bench_name']} ({blunder['bench_pts']} pts) "
                      f"for {blunder['start_name']} ({blunder['start_pts']} pts). Lost out on +{blunder['diff']} pts.")
            
            chosen_roast = random.choice(severe_roasts) if total_missed_points >= 15 else random.choice(mild_roasts)
            print(f"   🔥 Total Left on the bench: {round(total_missed_points, 1)} pts. {chosen_roast}\n")

if not has_blunders:
    print(" 🌟 Wow. No bench blunders found. Everyone managed their rosters flawlessly... boring.\n")

print("🏥 THE ER WAITING ROOM (INJURY REPORT):")
print("-------------------------------------------------------------")
has_injuries = False

for team in league.teams:
    ir_players = [
        p for p in team.roster 
        if getattr(p, 'injuryStatus', 'HEALTHY') in ['OUT', 'IR', 'INJURED_RESERVE', 'DOUBTFUL']
    ]
    
    if ir_players:
        has_injuries = True
        print(f"🤕 {team.team_name}:")
        for player in ir_players:
            print(f"   • {player.name} {random.choice(injury_commentary)}")
        print("")

if not has_injuries:
    print(" 🎉 Medical miracle! No notable players are currently tagged out on injuries.\n")

print("=============================================================")
print("📊 ROSTER EFFICIENCY & MAX POSSIBLE POINTS BREAKDOWN")
print("=============================================================")
for name, data in sorted(team_max_points_summary.items(), key=lambda item: item[1]['efficiency'], reverse=True):
    print(f" 📈 {name:<25} | Actual: {data['actual']:>5} pts | Max Potential: {data['max']:>5} pts | Efficiency: {data['efficiency']}%")

# --- NEW SECTION: LIVE OFFICIAL STANDINGS & TOP/BOTTOM ROASTS ---
print("=============================================================")
print(f"       🏆 OFFICIAL LEAGUE STANDINGS (POST-MNF FINAL)        ")
print("=============================================================")

# Sort the official teams array by league standing placement index
sorted_standings = sorted(league.teams, key=lambda t: getattr(t, 'standing', 99))

for index, team in enumerate(sorted_standings, start=1):
    record_str = f"({team.wins}-{team.losses})"
    comment = ""
    
    # Specific targeted custom roasts based on true standing ranks
    if index == 1:
        comment = "👑 #1: Enjoying a fluke run. Don't worry, regression is actively hunting you down."
    elif index == 2:
        comment = "🥈 #2: Sitting comfortably in the shadow of #1. The ultimate bridesmaid roster."
    elif index == len(sorted_standings):
        comment = "🤡 DEAD LAST: The definitive league doormat. Statistically, coin flips choose better lineups."
    elif index == 3:
         comment = "🥉 #3: Smells like bronze in here. So close to relevance, yet so far away."
    elif index == len(sorted_standings):
        comment = "🤡 DEAD LAST: The definitive league doormat. Statistically, coin flips choose better lineups."
        
    print(f" Rank {index:<2} | {team.team_name:<23} {record_str:<7} | {comment}")
