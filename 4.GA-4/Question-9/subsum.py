import pdfplumber
import pandas as pd

def get_user_inputs():
    pdf_path = input("Enter PDF file path: ").strip()
    start_group = int(input("Enter start group number (e.g., 1): "))
    end_group = int(input("Enter end group number (e.g., 24): "))
    filter_subject = input("Enter subject to filter by (e.g., Maths): ").strip()
    filter_threshold = int(input(f"Enter minimum marks for {filter_subject} (e.g., 55): "))
    sum_subject = input("Enter subject to sum marks for (e.g., Physics): ").strip()
    return pdf_path, start_group, end_group, filter_subject, filter_threshold, sum_subject

def extract_and_calculate(pdf_path, start_group, end_group, filter_subject, filter_threshold, sum_subject):
    all_rows = []
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        # Validate group range against pages
        if not (1 <= start_group <= total_pages and 1 <= end_group <= total_pages):
            raise ValueError(f"Group numbers must be between 1 and {total_pages}")

        for page_num in range(start_group - 1, end_group):
            page = pdf.pages[page_num]
            table = page.extract_table()
            if not table:
                continue
            headers = table[0]
            rows = table[1:]
            for row in rows:
                if len(row) != len(headers):
                    continue
                try:
                    data = dict(zip(headers, row))
                    # Convert marks to int
                    for key in data:
                        data[key] = data[key].strip()
                    data[filter_subject] = int(data[filter_subject])
                    data[sum_subject] = int(data[sum_subject])
                    all_rows.append(data)
                except Exception:
                    continue

    df = pd.DataFrame(all_rows)
    filtered_df = df[df[filter_subject] >= filter_threshold]

    total_sum = filtered_df[sum_subject].sum()
    return total_sum

if __name__ == "__main__":
    pdf_path, start_group, end_group, filter_subject, filter_threshold, sum_subject = get_user_inputs()
    total = extract_and_calculate(pdf_path, start_group, end_group, filter_subject, filter_threshold, sum_subject)
    print(f"\nTotal {sum_subject} marks of students who scored ≥{filter_threshold} in {filter_subject} in groups {start_group}-{end_group}: {total}")
