from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from datetime import datetime
from typing import Optional
from memory import init_db, store_user_and_plan
from llm import generate_plan
from prompt import build_fitness_prompt

app = FastAPI(title="AI Fitness API")

@app.on_event("startup")
def startup_event():
    init_db()

class UserProfile(BaseModel):
    name: str
    age: Optional[int] = None
    sex: str
    weight: Optional[float] = None
    height: Optional[float] = None
    purpose: str
    # The new medical fields:
    bloodPressure: str
    pulse: Optional[int] = None
    hasDiabetes: bool
    hasThyroid: bool
    otherConditions: str

class PlanResponse(BaseModel):
    bmi: float
    bmi_category: str
    plan: str

def calculate_bmi(weight_kg: float, height_cm: float):
    # Safety check so we don't divide by zero if height is empty!
    if not weight_kg or not height_cm or height_cm == 0:
        return 0.0, "N/A"
        
    bmi = weight_kg / ((height_cm / 100) ** 2)
    if bmi < 18.5: cat = "Underweight"
    elif bmi < 24.9: cat = "Normal weight"
    elif bmi < 29.9: cat = "Overweight"
    else: cat = "Obese"
    return round(bmi, 1), cat

@app.post("/generate-plan", response_model=PlanResponse)
async def create_plan(user: UserProfile):
    try:
        # Get the exact current date/time to force Gemini to make it for TODAY only
        current_time = datetime.now().strftime("%A, %B %d, %Y")
        
        # 1. Pass ALL 11 fields + the time to the prompt builder
        prompt = build_fitness_prompt(
            user.name, user.age, user.sex, user.weight, user.height, user.purpose,
            user.bloodPressure, user.pulse, user.hasDiabetes, user.hasThyroid, user.otherConditions,
            current_time
        )
        
        # 2. Ask Gemini for the plan
        plan = generate_plan(prompt)
        
        # 3. Pass ALL 11 fields + the plan to the database
        store_user_and_plan(
            user.name, user.age, user.sex, user.weight, user.height, user.purpose,
            user.bloodPressure, user.pulse, user.hasDiabetes, user.hasThyroid, user.otherConditions,
            plan
        )
        
        bmi_val, bmi_cat = calculate_bmi(user.weight, user.height)
        
        return PlanResponse(bmi=bmi_val, bmi_category=bmi_cat, plan=plan)
        
    except Exception as e:
        # This will print the exact crash reason in your VS Code terminal!
        print(f"CRASH DETAILS: {repr(e)}") 
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)