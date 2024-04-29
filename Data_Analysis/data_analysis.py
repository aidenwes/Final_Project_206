import matplotlib.pyplot as plt
import json

def open_daily_50():
    with open('daily_50_joined.json', 'r') as f:
        data = json.load(f)

