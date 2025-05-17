from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
import re
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to identify and extract parameters from ticket status query
def parse_ticket_status(query):
    match = re.search(r'ticket\s+(\d+)', query, re.IGNORECASE)
    if match and "status" in query.lower():
        ticket_id = int(match.group(1))
        return {
            "name": "get_ticket_status",
            "arguments": json.dumps({"ticket_id": ticket_id})
        }
    return None


# Function to identify and extract parameters from meeting scheduling query
def parse_schedule_meeting(query):
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', query)
    time_match = re.search(r'(\d{2}:\d{2})', query)
    room_match = re.search(r'(Room\s+\w+|Conf\d+|Meeting Room)', query, re.IGNORECASE)

    if date_match and time_match and room_match:
        return {
            "name": "schedule_meeting",
            "arguments": json.dumps({
                "date": date_match.group(1),
                "time": time_match.group(1),
                "meeting_room": room_match.group(1).strip()
            })
        }
    return None


# Function to identify and extract parameters from expense balance query
def parse_expense_balance(query):
    match = re.search(r'(?:employee|emp)\s+(\d+)', query, re.IGNORECASE)
    if match and re.search(r'expense|expenses|reimbursement', query, re.IGNORECASE):
        return {
            "name": "get_expense_balance",
            "arguments": json.dumps({"employee_id": int(match.group(1))})
        }
    return None


# Function to identify and extract parameters from performance bonus query
def parse_performance_bonus(query):
    emp_match = re.search(r'(?:employee|emp)\s+(\d+)', query, re.IGNORECASE)
    year_match = re.search(r'(\d{4})', query)
    if emp_match and year_match and re.search(r'bonus', query, re.IGNORECASE):
        return {
            "name": "calculate_performance_bonus",
            "arguments": json.dumps({
                "employee_id": int(emp_match.group(1)),
                "current_year": int(year_match.group(1))
            })
        }
    return None


# Function to identify and extract parameters from office issue report query
def parse_office_issue(query):
    issue_match = re.search(r'issue\s+(\d+)', query, re.IGNORECASE)
    dept_match = re.search(r'(?:for|in)\s+(?:the\s+)?(\w+)(?:\s+dept|artment)?', query, re.IGNORECASE)
    
    if issue_match and dept_match:
        return {
            "name": "report_office_issue",
            "arguments": json.dumps({
                "issue_code": int(issue_match.group(1)),
                "department": dept_match.group(1)
            })
        }
    return None


@app.get("/execute")
async def execute_query(request: Request, q: str = Query(..., description="The query to execute")):
    logger.debug(f"Received query: {q}")
    logger.debug(f"Request headers: {request.headers}")
    
    # List of parser functions to try
    parsers = [
        parse_ticket_status,
        parse_schedule_meeting,
        parse_expense_balance,
        parse_performance_bonus,
        parse_office_issue
    ]
    
    # Try each parser until one returns a result
    for parser in parsers:
        result = parser(q)
        if result:
            logger.debug(f"Returning result: {result}")
            return result
    
    # If no parser matched
    logger.warning(f"Could not parse query: {q}")
    return {"error": "Could not parse query"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server at http://127.0.0.1:8810")
    uvicorn.run(app, host="127.0.0.1", port=8810, log_level="debug") 