import sys
import os


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.database import MaterialDatabase
from src.nlp_engine import NLPEngine
from src.recommender import Recommender

def main():
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'materials.json')

    
    try:
        db = MaterialDatabase(data_path)
    except Exception as e:
        print(f"Error loading database: {e}")
        return

    nlp = NLPEngine()
    recommender = Recommender(db)

    print("=====================================================")
    print("      Material Selection Chatbot           ")
    print("=====================================================")
    print("Hello! Describe your requirements (e.g., 'lightweight, low cost').")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break

       
        constraints = nlp.process_query(user_input)
        if not constraints:
            print("Bot: I couldn't detect specific material requirements. Try mentioning properties like strength, weight, cost, or corrosion resistance.")
            continue
        
        print(f"   (Detected constraints: {constraints})")

        
        results = recommender.recommend(constraints)

       
        if results:
            top_choice = results[0]
            mat = top_choice['material']
            print(f"\nBot: I recommend **{mat['name']}**.")
            print(f"     Type: {mat['type']}")
            # Pretty print properties
            print("     Properties:")
            # Filter to show only relevant or all properties in a clean way
            for k, v in mat['properties'].items():
                if k in constraints:
                    print(f"       * {k.ljust(25)} : {v} (Matched)")
                else:
                    # Optional: Don't show everything to avoid clutter, or show subset
                    # For now show all but indented
                    print(f"         {k.ljust(25)} : {v}")

            print(f"     Reason: {', '.join(top_choice['reasons'])}")
            print(f"     Description: {mat['description']}")
            
            if len(results) > 1:
                print("\n     Alternatives:")
                for alt in results[1:3]:
                    print(f"     - {alt['material']['name']} (Score: {alt['score']})")
        else:
            print("\nBot: Sorry, I couldn't find a material that perfectly matches all those constraints. Try relaxing one requirement.")
        
        print("-" * 50)

if __name__ == "__main__":
    main()
