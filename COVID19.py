# Libraries
from io import BytesIO
import pandas as pd
import numpy as np
import requests
import json
import sqlite3
import matplotlib.pyplot as plt
from flask import Flask, app, render_template, request, send_file

# ----------------------------
# Connect to DB
# ----------------------------
conn = sqlite3.connect('covid_data.db')
df = pd.read_sql('SELECT * FROM data', conn)
conn.close()
print("SQLite table converted back to DataFrame:")
print(df)

print("Shape of new df")
print(df.shape)

# -----------------------------
# Explore Data
# -----------------------------
# Time span
start_date = min(df['date'])
end_date = max(df['date'])
print("Data reported from", start_date, "to", end_date)

# Column "states"?
states = df['states']
#print(states)
print(max(states))
print(min(states))
print(df.columns)

# -------------------------------------
# Query DB by data
# -------------------------------------

#conn = sqlite3.connect('covid_data.db')
#curs = conn.cursor()
#range = curs.execute("select * from data where date >= 20200307 and date <= 20210307")
#rangeDF = pd.DataFrame(range)
#print(rangeDF)

app = Flask(__name__)

# -----------------------------------
# Display Data Function
# -----------------------------------
def display(date1, date2):
    conn = sqlite3.connect('covid_data.db')
    # Use parameterized query to pass date1 and date2
    query = 'SELECT * FROM data WHERE date >= ? AND date <= ?'
    df = pd.read_sql(query, conn, params=(date1, date2))
    conn.close()

    # Plot deaths and hospitalizations over time
    plt.figure(figsize=(10, 6))
    # Line for deaths
    plt.plot(df['date'], df['death'], label='Deaths', color='red', marker='o')
    # Line for hospitalizations
    plt.plot(df['date'], df['hospitalized'], label='Hospitalizations', color='blue', marker='x')


    # Adding labels and title
    plt.xlabel('Date')
    plt.ylabel('Count')
    title = ('COVID-19 Deaths and Hospitalizations From {} to {}').format(date1, date2)
    plt.title(title)

    # Show legend
    plt.legend()
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    # Display the plot
    plt.tight_layout()  
    # Save plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    
    return img

# Route to display the form and the plot
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date1 = request.form.get("date1")
        date2 = request.form.get("date2")
        img = display(date1, date2)
        return send_file(img, mimetype='image/png')
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)