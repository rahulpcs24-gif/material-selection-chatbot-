import json
import random
import os

def get_base_properties(mat_type):
    # Returns base properties and ranges for different families
    if mat_type == "Steel":
        return {
            "type": "Metal",
            "strength": ["high", "very high"],
            "weight": ["high"],
            "cost": ["low", "medium"],
            "corrosion_resistance": ["poor", "medium", "good"], # Depends on stainless or carbon
            "stiffness": ["high"],
            "hardness": ["high", "very high"],
            "ductility": ["medium", "high"],
            "thermal_conductivity": ["medium"],
            "electrical_conductivity": ["medium"],
            "transparency": ["no"],
            "toxicity": ["low"],
            "max_temp": ["high", "very high"]
        }
    elif mat_type == "Aluminum":
        return {
            "type": "Metal",
            "strength": ["medium", "high"],
            "weight": ["low"],
            "cost": ["medium"],
            "corrosion_resistance": ["good", "excellent"],
            "stiffness": ["medium"],
            "hardness": ["medium"],
            "ductility": ["high"],
            "thermal_conductivity": ["high", "very high"],
            "electrical_conductivity": ["high"],
            "transparency": ["no"],
            "toxicity": ["low"],
            "max_temp": ["medium"]
        }
    elif mat_type == "Polymer":
        return {
            "type": "Polymer",
            "strength": ["low", "medium"],
            "weight": ["low"],
            "cost": ["low", "medium"],
            "corrosion_resistance": ["good", "excellent"],
            "stiffness": ["low", "medium"],
            "hardness": ["low", "medium"],
            "ductility": ["high", "very high"],
            "thermal_conductivity": ["low"],
            "electrical_conductivity": ["low"],
            "transparency": ["yes", "no"], # Varies
            "toxicity": ["low", "medium"],
            "max_temp": ["low"]
        }
    elif mat_type == "Ceramic":
        return {
            "type": "Ceramic",
            "strength": ["high", "very high"], # compressive
            "weight": ["medium"],
            "cost": ["low", "high"],
            "corrosion_resistance": ["excellent"],
            "stiffness": ["very high"],
            "hardness": ["very high"],
            "ductility": ["low"], # Brittle
            "thermal_conductivity": ["low", "high"], # Varies (alumina vs zirconia)
            "electrical_conductivity": ["low"],
            "transparency": ["no", "yes"], # Glass
            "toxicity": ["low"],
            "max_temp": ["very high"]
        }
    elif mat_type == "Composite":
        return {
            "type": "Composite",
            "strength": ["high", "very high"],
            "weight": ["low", "medium"],
            "cost": ["high", "very high"],
            "corrosion_resistance": ["excellent"],
            "stiffness": ["high", "very high"],
            "hardness": ["high"],
            "ductility": ["low", "medium"],
            "thermal_conductivity": ["low", "medium"],
            "electrical_conductivity": ["low", "medium"], # Carbon fiber conducts
            "transparency": ["no"],
            "toxicity": ["low"],
            "max_temp": ["medium", "high"]
        }
    # Default fallback
    return {}

def generate_materials():
    materials = []
    
    # --- Definition of specific materials to generate ---
    
    # 1. Steels (50 variants)
    for i in range(1001, 1051):
        materials.append(create_material(f"AISI Carbon Steel {i}", "Steel", "standard carbon steel", 
                                       strength="high", corrosion="poor", cost="low"))
    for i in range(301, 351):
        materials.append(create_material(f"Stainless Steel {i}", "Steel", "corrosion resistant steel", 
                                       strength="medium", corrosion="excellent", cost="medium"))

    # 2. Aluminums (30 variants)
    series = [1000, 2000, 3000, 5000, 6000, 7000]
    for s in series:
        for i in range(5):
            name = f"Aluminum Alloy {s + i*10}"
            desc = f"Series {s} aluminum alloy."
            if s == 7000: strength="high"; cost="medium"
            elif s == 1000: strength="low"; cost="low"
            else: strength="medium"; cost="medium"
            materials.append(create_material(name, "Aluminum", desc, strength=strength, cost=cost))

    # 3. Polymers (40 variants)
    polymers = ["Polyethylene", "Polypropylene", "PVC", "Polystyrene", "Nylon", "ABS", "Polycarbonate", "Acrylic", "PET", "Teflon"]
    grades = ["LD", "HD", "Ultra High MW", "Glass Filled", "High Impact"]
    for p in polymers:
        for g in grades[:4]: # 4 variants each approx
            name = f"{p} ({g})"
            desc = f"Grade {g} of {p}."
            is_transp = "yes" if p in ["Acrylic", "Polycarbonate", "PET", "Polystyrene"] else "no"
            materials.append(create_material(name, "Polymer", desc, transparency=is_transp))

    # 4. Ceramics (20 variants)
    ceramics = ["Alumina", "Zirconia", "Silicon Carbide", "Silicon Nitride", "Boron Carbide", "Glass (Soda-Lime)", "Glass (Borosilicate)", "Porcelain"]
    for c in ceramics:
        for g in ["Grade A", "Industrial", "High Purity"]:
            materials.append(create_material(f"{c} {g}", "Ceramic", "Technical ceramic."))

    # 5. Composites (20 variants)
    matrices = ["Epoxy", "Polyester", "PEEK"]
    fibers = ["Carbon Fiber", "Glass Fiber", "Aramid"]
    for m in matrices:
        for f in fibers:
            for o in ["d", "w"]: # dummy variants
                name = f"{f}/{m} Composite ({'UD' if o=='d' else 'Woven'})"
                materials.append(create_material(name, "Composite", "High performance composite."))
                
    # 6. Copper & Alloys (20 variants)
    copper_alloys = ["Pure Copper", "Brass (Cu-Zn)", "Bronze (Cu-Sn)", "Beryllium Copper", "Cupronickel"]
    for c in copper_alloys:
        for t in ["Annealed", "Hardened", "Spring Temper"]:
            materials.append(create_material(f"{c} - {t}", "Metal", "Copper based alloy with high conductivity.", 
                                           electrical_conductivity="high", thermal_conductivity="high"))

    # 8. Magnesium Alloys (10 variants)
    for i in ["AZ31", "AZ91", "ZK60", "WE43", "Elektron 43", "Magnesium-Lithium", "AM60", "AM50", "EZ33", "ZE41"]:
        materials.append(create_material(f"Magnesium Alloy {i}", "Metal", "Ultra-lightweight structural metal.", 
                                       weight="low", strength="medium", corrosion="poor"))

    # 9. Nickel Superalloys (10 variants)
    for i in ["Inconel 718", "Inconel 625", "Hastelloy X", "Waspaloy", "Monel 400", "Nimonic 90", "Rene 41", "Haynes 230", "Incoloy 800", "Nichrome"]:
        materials.append(create_material(f"Nickel Superalloy {i}", "Metal", "High-temperature superalloy.", 
                                       max_temp="very high", strength="very high", corrosion="excellent", cost="very high"))

    # 10. Refractory Metals (10 variants)
    refractories = ["Tungsten", "Molybdenum", "Tantalum", "Niobium", "Rhenium"]
    for r in refractories:
        for f in ["Pure", "Alloy"]:
            materials.append(create_material(f"{r} ({f})", "Metal", "Refractory metal with extremely high melting point.", 
                                           max_temp="very high", hardness="high", weight="high"))

    # 11. Natural Materials (10 variants)
    naturals = ["Oak Wood", "Pine Wood", "Bamboo", "Cork", "Natural Rubber", "Leather", "Wool Felt", "Cotton", "Hemp Composite", "Balsa Wood"]
    for n in naturals:
        desc = "Sustainable natural material."
        w = "low"
        # customized logic for naturals
        s = "low" if "Cork" in n or "Cotton" in n else "medium"
        materials.append(create_material(n, "Natural", desc, weight=w, strength=s, corrosion="good", cost="low", electrical_conductivity="low"))

    # 12. Precious Metals (5 variants)
    for p in ["Gold", "Silver", "Platinum", "Palladium", "Rhodium"]:
        materials.append(create_material(p, "Metal", "Precious metal, excellent conductor.", 
                                       cost="very high", electrical_conductivity="very high", corrosion="excellent"))

    # 13. Construction Materials (5 variants)
    for c in ["Concrete (High Strength)", "Portland Cement", "Granite", "Marble", "Limestone"]:
        materials.append(create_material(c, "Ceramic", "Construction material.", 
                                       strength="high", weight="high", cost="low", ductility="low"))
                                       
    # 14. Smart Materials (5 variants)
    smart_mats = ["Nitinol (Shape Memory)", "Piezoelectric Ceramic", "Magnetostrictive Alloy", "Thermochromic Polymer", "Self-Healing Polymer"]
    for sm in smart_mats:
        materials.append(create_material(sm, "Smart Material", "Advanced material with responsive usage.", 
                                       cost="high"))

    # 15. Tool Steels (20 variants)
    # High hardness and wear resistance
    tool_steels = ["D2", "A2", "O1", "M2", "M4", "H13", "S7", "P20", "W1", "L6"]
    for ts in tool_steels:
        for state in ["Annealed", "Hardened"]:
            materials.append(create_material(f"Tool Steel {ts} ({state})", "Metal", "High hardness tool steel for cutting/forming.", 
                                           hardness="very high", strength="high", ductility="low"))

    # 16. Electronic/Semiconductors (15 variants)
    semis = ["Silicon (Si)", "Germanium (Ge)", "Gallium Arsenide (GaAs)", "Indium Phosphide (InP)", "Silicon Carbide (SiC electronic grade)", "Gallium Nitride (GaN)"]
    for s in semis:
        for doped in ["Pure", "N-doped", "P-doped"]:
             materials.append(create_material(f"{s} - {doped}", "Ceramic", "Semiconductor material.", 
                                            electrical_conductivity="medium", thermal_conductivity="medium", transparency="no"))

    # 17. Magnetic Materials (10 variants)
    magnets = ["Neodymium (NdFeB)", "Samarium Cobalt", "Ferrite", "Alnico", "Permalloy", "Soft Iron", "Mu-Metal"]
    for m in magnets:
        materials.append(create_material(m, "Metal", "Magnetic material.", 
                                       strength="medium", electrical_conductivity="medium"))

    # 18. Biomedical Alloys (10 variants)
    bio_mats = ["Cobalt-Chrome", "Stainless Steel 316LVM", "Nitinol (Medical)", "Tantalum (Porous)", "Magnesium (Biodegradable)"]
    for b in bio_mats:
        for form in ["Implant", "Stent"]:
             materials.append(create_material(f"{b} {form}", "Metal", "Biocompatible medical alloy.", 
                                            toxicity="low", corrosion="excellent"))

    # 19. Metal Matrix Composites (10 variants)
    mmcs = ["Al-SiC", "Al-Al2O3", "Ti-SiC", "Mg-SiC", "Cu-Graphite"]
    for mmc in mmcs:
        for vol in ["10%", "20%"]:
             materials.append(create_material(f"{mmc} ({vol} vol)", "Composite", "Metal matrix reinforced composite.", 
                                            strength="high", stiffness="high", thermal_conductivity="medium"))
    
    # 20. Expanded Aluminum Series (Adding 40 more specific alloys)
    for i in range(40):
         materials.append(create_material(f"Aluminum Alloy Experimental-{i+8000}", "Aluminum", "Experimental high-strength alloy.", 
                                        strength="high", weight="low"))

    # Ensure unique IDs
    for idx, mat in enumerate(materials):
        mat['id'] = f"mat_{idx+1000}"

    return materials

def create_material(name, family, base_desc, **overrides):
    base_props = get_base_properties(family)
    props = {}
    
    # Resolve list ranges to single values for base properties
    for k, v in base_props.items():
        if isinstance(v, list):
            # Deterministic "pseudorandom" based on name hash to stay consistent
            seed = sum(ord(c) for c in name + k)
            props[k] = v[seed % len(v)]
        else:
            props[k] = v
            
    # Apply specific overrides (e.g. if we know Steel 304 is excellent corrosion)
    for k, v in overrides.items():
        if v is not None:
            props[k] = v
            
    # Clean up non-dict keys from properties if any leaked
    final_props = {k:v for k,v in props.items() if k != "type"}
    
    return {
        "id": "temp",
        "name": name,
        "type": base_props.get("type", "Material"),
        "properties": final_props,
        "description": base_desc,
        "applications": ["general engineering", "structural"] # Generic for bulk gen
    }

if __name__ == "__main__":
    mats = generate_materials()
    print(f"Generated {len(mats)} materials.")
    
    # Save
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base_dir, 'data', 'materials.json')
    
    with open(out_path, 'w') as f:
        json.dump(mats, f, indent=2)
    print(f"Saved to {out_path}")
