import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from clients import Client
import services  # Import the updated services module

# Google Sheets API settings
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "config/credentials.json"  # Ensure this file is properly configured
SPREADSHEET_NAME = "YOUR_SPREADSHEET_NAME"  # Replace with your actual spreadsheet name


def setup_google_sheets():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPES)
    client = gspread.authorize(creds)
    return client.open(SPREADSHEET_NAME)


def fetch_google_sheet(sheet_name):
    """Fetch data from a specific sheet and return as DataFrame, skipping the first line."""
    try:
        spreadsheet = setup_google_sheets()
        sheet = spreadsheet.worksheet(sheet_name)
        all_values = sheet.get_all_values()
        if len(all_values) > 1:
            header = all_values[0]
            data = all_values[1:]
            df = pd.DataFrame(data, columns=header)
            df.rename(columns={
                'ID': 'id', 'Full Name': 'full_name', 'Service': 'service',
                'Payment': 'payment', 'Paid': 'paid', 'Code': 'code', 'Solde': 'solde'
            }, inplace=True)
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"Error fetching {sheet_name}: {str(e)}")
        return pd.DataFrame()


def append_to_google_sheet(sheet_name, new_row_data):
    try:
        spreadsheet = setup_google_sheets()
        sheet = spreadsheet.worksheet(sheet_name)
        sheet.append_row([
            new_row_data.get('id'), new_row_data.get('full_name'), new_row_data.get('service'),
            new_row_data.get('payment'), new_row_data.get('paid'), new_row_data.get('code'), new_row_data.get('solde')
        ])
        services.notify_client_saved()
        if new_row_data.get("code"):
            services.notify_registration_with_code(new_row_data.get("full_name"), new_row_data.get("payment"))
        print(f"Data saved to {sheet_name}!")
    except Exception as e:
        print(f"Error while appending to {sheet_name}: {str(e)}")


def add_client(sheet_name, min_clients, solde_percentage):
    num_clients = int(input(f"Enter number of clients (minimum {min_clients}): "))
    if num_clients < min_clients:
        print(f"Minimum {min_clients} clients required!")
        return

    client_id = input("Enter ID: ").upper()
    service = input("Enter service: ")
    payment = float(input("Enter payment fee: "))
    paid = int(input("Enter paid (0-1): "))
    code = input("Enter code (optional): ") or None

    for _ in range(num_clients):
        full_name = input("Enter full name: ")
        solde = payment * solde_percentage
        client = Client(id=client_id, full_name=full_name, service=service, payment=payment, paid=paid, code=code, solde=solde)
        append_to_google_sheet(sheet_name, vars(client))
    print(f"{sheet_name.capitalize()} clients added successfully!")


def calculate_total(sheet_names, calculation_type):
    total = 0
    for sheet in sheet_names:
        df = fetch_google_sheet(sheet)
        if df.empty:
            print(f"Skipping {sheet}, no data found.")
            continue
        if calculation_type == "revenue":
            df["payment"] = pd.to_numeric(df["payment"], errors="coerce")
            total += df["payment"].sum()
        elif calculation_type == "marketing":
            total += sum(Client(**row).marketing_revenue() for _, row in df.iterrows() if row.get("code"))
    print(f"Total {calculation_type.capitalize()} Revenue: {total}")


def calculate_payment_for_user():
    full_name = input("Enter full name: ")
    for sheet in ["soloclient", "clientteams", "clientgrps"]:
        df = fetch_google_sheet(sheet)
        user_row = df[df["full_name"] == full_name]
        if not user_row.empty:
            client = Client(**user_row.iloc[0].to_dict())
            print(f"Payment for {full_name}: {client.calculate_payment()}")
            return
    print("User not found!")


# Main menu
while True:
    try:
        choice = int(input(
            "1: Add Solo Client\n2: Add Team\n3: Add Group\n4: Calculate Marketing Revenue\n5: Calculate Total Revenue\n6: Calculate Payment for Specific User\n7: Exit\n"))
        if choice == 1:
            add_client("soloclient", 1, 0)
        elif choice == 2:
            add_client("clientteams", 3, 0.10)
        elif choice == 3:
            add_client("clientgrps", 4, 0.15)
        elif choice == 4:
            calculate_total(["soloclient", "clientteams", "clientgrps"], "marketing")
        elif choice == 5:
            calculate_total(["soloclient", "clientteams", "clientgrps"], "revenue")
        elif choice == 6:
            calculate_payment_for_user()
        elif choice == 7:
            break
        else:
            print("Invalid choice, try again!")
    except ValueError:
        print("Please enter a valid number.")
