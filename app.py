import pandas as pd
import joblib

from flask import Flask, render_template, request
from pydantic import BaseModel, Field

app = Flask(__name__)

model = joblib.load('batthealth.pkl')

class userInput(BaseModel):
    age: float = Field(...)
    usage: float = Field(...)
    gamer: float = Field(...)
    designCap: float = Field(...)
    cycles: float = Field(...)
    cpu: float = Field(...)
    gpu: float = Field(...)
    power: float = Field(...)
    temp: float = Field(...)

@app.route('/', methods=["GET", "POST"])
def loadAPI():
    print(request.form)
    return render_template("index.html")

@app.route('/predict', methods=["POST"])
def predictBattHealth():
    maxCapacity = float(request.form.get("designCap"));
    isGamer = 1 if request.form.getlist("gamer") == "isGamer" else 0
    print(isGamer)

    dataInput = pd.DataFrame([{
        "Battery Age": float(request.form.get("age")),
        "Daily Usage Hours": float(request.form.get("usage")),
        "Gaming User": float(isGamer),
        "Design Capacity": maxCapacity,
        "Cycle Count": float(request.form.get("cycles")),
        "CPU Usage": float(request.form.get("cpu")),
        "GPU Usage": float(request.form.get("gpu")),
        "Power Consumption": float(request.form.get("power")),
        "Average Temperature": float(request.form.get("temp"))
    }])

    currBattCapacity = int(model.predict(dataInput).item())

    batteryHealth = int((currBattCapacity / maxCapacity) * 100)
    comment = 'let me think...'

    if batteryHealth >= 95:
        comment = "Good for you"
    elif batteryHealth >= 80 and batteryHealth < 95:
        comment = "It's alright"
    elif batteryHealth >= 70 and batteryHealth < 80:
        comment = "That's uhh not good chief"
    elif batteryHealth < 70:
        comment = "💀"

    return render_template('results.jinja2', battHealth=batteryHealth, comment=comment, maxCap=int(maxCapacity), currCap=currBattCapacity)