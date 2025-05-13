from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET"],  # Only allow GET requests
    allow_headers=["*"],
)

# Load the CSV file
df = pd.read_csv("q-fastapi.csv")

# Convert DataFrame to the expected format
def get_students_data(class_filters=None):
    # If class filters are provided, filter the dataframe
    if class_filters:
        filtered_df = df[df['class'].isin(class_filters)]
    else:
        filtered_df = df
    
    # Convert to list of dictionaries
    students = []
    for _, row in filtered_df.iterrows():
        students.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })
    
    return students

@app.get("/api")
async def get_students(class_param: Optional[List[str]] = Query(None, alias="class")):
    """
    Get student data.
    Optional query parameter 'class' to filter by class (can be used multiple times).
    Example: /api?class=1A&class=1B
    """
    students = get_students_data(class_param)
    return {"students": students}

@app.get("/")
async def root():
    return {"message": "Student API is running. Use /api endpoint to get student data."}

# Run the application directly if executed as a script
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True) 