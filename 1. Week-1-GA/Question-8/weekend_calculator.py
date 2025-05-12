from datetime import datetime, timedelta

# Set your date range here (format: YYYY-MM-DD)
START_DATE = "1989-12-19"
END_DATE = "2007-07-03"
IS_INCLUSIVE = True  # Set to False if end date is exclusive

def validate_dates(start_str, end_str):
    """Validate the date format and range."""
    try:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
        if start > end:
            raise ValueError("Start date cannot be after end date")
        return start, end
    except ValueError as e:
        if "strptime" in str(e):
            print("\nError: Invalid date format. Please use YYYY-MM-DD")
        else:
            print(f"\nError: {e}")
        exit(1)

def count_weekend_days(start_str, end_str, inclusive=True):
    """Count weekend days between two dates.
    Args:
        start_str: Start date in YYYY-MM-DD format
        end_str: End date in YYYY-MM-DD format
        inclusive: If True, includes both start and end dates
                  If False, includes start date but not end date
    """
    start, end = validate_dates(start_str, end_str)
    if not inclusive:
        end = end - timedelta(days=1)
    days = (end - start).days + 1
    weeks, remainder = divmod(days, 7)
    weekend_days = weeks * 2
    start_weekday = start.weekday()
    for i in range(remainder):
        if (start_weekday + i) % 7 >= 5:
            weekend_days += 1
    return weekend_days

if __name__ == "__main__":
    total_weekends = count_weekend_days(START_DATE, END_DATE, IS_INCLUSIVE)
    
    print(f"\nDate Range: {START_DATE} to {END_DATE}")
    print(f"Range Type: {'Inclusive' if IS_INCLUSIVE else 'Exclusive'}")
    print(f"Total Weekend Days: {total_weekends}")
    print("\nNote: Weekend days include both Saturdays and Sundays")
    if not IS_INCLUSIVE:
        print("Note: End date is exclusive (not counted in the result)") 