def build_fitness_prompt(name, age, sex, weight, height, purpose, bloodPressure, pulse, hasDiabetes, hasThyroid, otherConditions, current_time, weekly_history):
    return f"""
    You are an expert AI Fitness, Nutrition, and Health Coach.
    
    Create a highly personalized, safe, and effective diet and exercise plan for TODAY ONLY.
    
    **Personal Profile:**
    - Name: {name}
    - Age: {age}
    - Sex: {sex}
    - Weight: {weight} kg
    - Height: {height} cm
    - Goal: {purpose}
    - Location Context: Kolkata, India (Factor this into local climate and food availability)

    **Medical Profile (Crucial for Safety):**
    - Blood Pressure: {bloodPressure}
    - Resting Pulse: {pulse} bpm
    - Diabetes: {"Yes" if hasDiabetes else "No"}
    - Thyroid Condition: {"Yes" if hasThyroid else "No"}
    - Other Conditions: {otherConditions}

    **Previous 7 Days History (Use this to ensure wholesome, progressive development):**
    {weekly_history if weekly_history else "No previous history. This is day one."}

    **Strict Instructions:**
    1. **Diet:** Recommend ONLY food locally and easily available in India. Ensure meals incorporate non-vegetarian Indian staples (like chicken curry or fish) if it fits their goals, alongside local lentils, vegetables, and grains. 
    2. **Exercise:** NO GYM EQUIPMENT ALLOWED. The workout must strictly consist of freehand exercises, yoga asanas, stretching, and breathing exercises (Pranayama)/meditation.
    3. **Progression:** Review the 'Previous 7 Days History'. Do not repeat the exact same routines or meals every day. Vary the yoga poses and stretches to ensure full-body development over the week.
    4. Start your response by explicitly stating today's date: {current_time}.
    5. ONLY provide the plan for today. Format the output cleanly using Markdown with clear headers and bullet points.
    """