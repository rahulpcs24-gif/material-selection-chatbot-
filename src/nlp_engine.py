import re

class NLPEngine:
    def __init__(self):
        # Define mappings for keywords to property values
        # Aiming for extensive vocabulary coverage (>50 keywords)
        self.property_map = {
            # Mechanical Properties
            "strength": {
                "high": ["high strength", "strong", "tough", "durable", "high tensile", "unbreakable", "robust", "hard-wearing", "reinforced", "sturdy"],
                "medium": ["medium strength", "moderate strength", "average strength"],
                "low": ["low strength", "weak", "delicate", "brittle"]
            },
            "stiffness": {
                "high": ["stiff", "rigid", "high stiffness", "non-deformable", "inflexible", "modulus"],
                "low": ["flexible", "low stiffness", "elastic", "pliable", "bendable", "compliant"]
            },
            "hardness": {
                "high": ["hard", "high hardness", "scratch resistant", "wear resistant", "abrasion resistant"],
                "low": ["soft", "low hardness", "malleable"] # Malleable often implies softer than hardened steel
            },
            "ductility": {
                "high": ["ductile", "formable", "malleable", "plasticity", "bendable", "drawable"],
                "low": ["brittle", "non-ductile"]
            },
            
            # Physical Properties
            "weight": {
                "low": ["lightweight", "light", "low weight", "ultralight", "portable", "featherweight", "low density"],
                "high": ["heavy", "high weight", "dense", "massive", "high density"]
            },
            "transparency": {
                "yes": ["transparent", "clear", "see-through", "translucent", "optical", "glass-like"],
                "no": ["opaque", "solid color", "non-transparent"]
            },
            
            # Thermal Properties
            "thermal_conductivity": {
                "high": ["thermally conductive", "heat conductor", "conducts heat", "heat sink", "dissipates heat", "cooling"],
                "low": ["thermal insulator", "heat insulator", "insulating", "insulation", "keeps warm", "heat resistant"] # Context dependent, but usually insulation
            },
            "max_temp": {
                "high": ["heat resistant", "high temperature", "refractory", "fire resistant", "high melting point", "withstands heat"],
                "low": ["low melting point", "low temperature"]
            },

            # Electrical Properties
            "electrical_conductivity": {
                "high": ["conductive", "electrical conductor", "conducts electricity", "conducts current"],
                "low": ["electrical insulator", "dielectric", "non-conductive", "insulates electricity"]
            },

            # Chemical/Environmental
            "corrosion_resistance": {
                "excellent": ["excellent corrosion resistance", "rust proof", "marine", "outdoor", "chemical resistant", "weather resistant", "stainless", "anti-corrosive", "non-rusting", "inert", "acid resistant"],
                "good": ["good corrosion resistance", "corrosion resistant"],
                "poor": ["poor corrosion resistance", "rusts", "oxidizes"]
            },
            "toxicity": {
                "low": ["biocompatible", "non-toxic", "food safe", "medical grade", "safe", "inert"],
                "high": ["toxic", "hazardous"]
            },

            # Economic
            "cost": {
                "low": ["cheap", "low cost", "inexpensive", "affordable", "economical", "budget", "low price", "value"],
                "high": ["expensive", "high cost", "premium", "costly", "high price", "luxury"]
            }
        }

    def process_query(self, query):
        """
        Analyzes the user query and returns a dictionary of extracted constraints.
        Example output: {'strength': 'high', 'cost': 'low'}
        """
        query = query.lower()
        constraints = {}

        for prop, values_map in self.property_map.items():
            for level, keywords in values_map.items():
                for keyword in keywords:
                    if keyword in query:
                        # If a more specific constraint was not already found (or overwrite)
                        constraints[prop] = level
                        break # Found a match for this property level
        
        return constraints
