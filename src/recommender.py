class Recommender:
    def __init__(self, database):
        self.db = database

    def recommend(self, constraints):
        """
        Finds materials matching the constraints.
        Returns a list of tuples: (material, score, reasons)
        """
        materials = self.db.get_all_materials()
        recommendations = []

        # properties where 'high' is generally better than 'medium' if 'medium' is requested
        # OR where 'very high' satisfies 'high'
        performance_props = ['strength', 'stiffness', 'corrosion_resistance', 'hardness', 'ductility', 'max_temp', 'thermal_conductivity', 'electrical_conductivity']

        for mat in materials:
            score = 0
            reasons = []
            mismatch = False
            
            for prop, required_val in constraints.items():
                mat_val = mat['properties'].get(prop, 'unknown').lower()
                
                # 1. Exact Match
                if mat_val == required_val:
                    score += 2
                    reasons.append(f"Matches {prop} ({mat_val})")
                
                # 2. "Better" than asked (e.g. asked for Medium, got High)
                elif required_val == 'medium' and mat_val in ['high', 'very high'] and prop in performance_props:
                    score += 2  # Treat as full match or bonus
                    reasons.append(f"Exceeds {prop} requirement ({mat_val})")
                
                # 3. "Acceptable" fallback (e.g. asked for High, got Very High - handled above, but what about High vs Medium?)
                # If asked for High, and got Medium --> Partial Score?
                elif required_val in ['high', 'very high'] and mat_val == 'medium' and prop in performance_props:
                    score += 1
                    reasons.append(f"Acceptable {prop} ({mat_val})")

                # 4. Mismatch Checks (Critical failures)
                # Cost: Wanted Low, got High
                elif required_val == 'low' and mat_val in ['high', 'very high'] and prop == 'cost':
                    mismatch = True
                # Weight: Wanted Low, got High
                elif required_val == 'low' and mat_val in ['high', 'very high'] and prop == 'weight':
                    mismatch = True
                # Performance: Wanted High, got Low (Critical for engineering)
                elif required_val in ['high', 'very high'] and mat_val == 'low' and prop in performance_props:
                   # Penalize heavily or mark mismatch
                   score -= 2 # Penalize but don't strictly filter out unless critical?
                   # Let's simple filter out if it directly contradicts the core request
                   # mismatch = True # Stricter
                   pass

            if not mismatch:
                # If we have at least one match or the score is decent
                if score > 0:
                    recommendations.append({
                        "material": mat,
                        "score": score,
                        "reasons": reasons
                    })
        
        # Sort by score descending
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations
