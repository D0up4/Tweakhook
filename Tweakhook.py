#by D0up4
import requests
import base64
import os
import sys
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

ASCII_ART = r"""
___________                      __   .__                   __    
\__    ___/_  _  __ ____ _____  |  | _|  |__   ____   ____ |  | __
  |    |  \ \/ \/ // __ \\__  \ |  |/ /  |  \ /  _ \ /  _ \|  |/ /
  |    |   \     /\  ___/ / __ \|    <|   Y  (  <_> |  <_> )    < 
  |____|    \/\_/  \___  >____  /__|_ \___|  /\____/ \____/|__|_ \
                       \/     \/     \/    \/                   \/"""

def print_menu():
    print(Fore.CYAN + ASCII_ART)
    print(Fore.CYAN + "=" * 66)
    print(Fore.GREEN + Style.BRIGHT + "                💬 Discord Webhook Tool by D0up4")
    print(Fore.CYAN + "=" * 66)
    print(Fore.YELLOW + Style.BRIGHT + """
[1] Change Webhook Name & Avatar
[2] Send Message (with or without file)
[3] Delete Webhook
[4] Exit
""")

def update_webhook(webhook_url):
    new_name = input("Insert new webhook name: ").strip()
    avatar_path = input("Insert avatar image path (or leave blank): ").strip() or None

    webhook_id, webhook_token = webhook_url.split("/")[-2:]
    url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"

    data = {"name": new_name}
    if avatar_path:
        try:
            with open(avatar_path, "rb") as f:
                b64_avatar = base64.b64encode(f.read()).decode("utf-8")
            data["avatar"] = f"data:image/png;base64,{b64_avatar}"
        except Exception as e:
            print(Fore.RED + f"❌ Error reading avatar file: {e}")
            return

    response = requests.patch(url, json=data)
    if response.ok:
        print(Fore.GREEN + "✅ Webhook updated successfully!")
    else:
        print(Fore.RED + "❌ Failed to update webhook:", response.text)

def send_message(webhook_url):
    message = input("Insert Text Message: ").strip()
    if not message:
        print(Fore.RED + "❌ Message text is required.")
        return

    try:
        amount = int(input("How many times do you want to send the message? (amount): ").strip())
        if amount < 1:
            raise ValueError
    except ValueError:
        print(Fore.RED + "❌ Invalid amount. Please enter a positive number.")
        return

    attach = input("Do you want to attach a file? (y/n): ").strip().lower()
    file_path = None
    if attach == "y":
        file_path = input("Enter path to the file/image: ").strip()
        if not os.path.isfile(file_path):
            print(Fore.RED + "❌ File does not exist.")
            return

    for i in range(1, amount + 1):
        if file_path:
            with open(file_path, "rb") as f:
                files = {'file1': (os.path.basename(file_path), f)}
                payload = {'payload_json': f'{{"content":"{message}"}}'}
                response = requests.post(webhook_url, data=payload, files=files)
        else:
            headers = {'Content-Type': 'application/json'}
            data = {"content": message}
            response = requests.post(webhook_url, headers=headers, json=data)

        if response.ok:
            print(Fore.GREEN + f"✅ ({i}/{amount}) Message sent.")
        else:
            print(Fore.RED + f"❌ ({i}/{amount}) Failed to send message:", response.text)

def delete_webhook(webhook_url):
    confirm = input(Fore.RED + "⚠️  Are you sure you want to delete the webhook? (y/n): ").strip().lower()
    if confirm != "y":
        print(Fore.YELLOW + "❌ Deletion cancelled.")
        return

    webhook_id, webhook_token = webhook_url.split("/")[-2:]
    url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"
    response = requests.delete(url)

    if response.status_code == 204:
        print(Fore.GREEN + "✅ Webhook deleted successfully.")
    else:
        print(Fore.RED + "❌ Failed to delete webhook:", response.text)

def main():
    webhook_url = input(Fore.CYAN + "Insert Webhook URL: ").strip()
    if not webhook_url:
        print(Fore.RED + "❌ Webhook URL is required.")
        return

    while True:
        print_menu()
        choice = input(Fore.CYAN + "Select an option (1-4): ").strip()

        if choice == "1":
            update_webhook(webhook_url)
        elif choice == "2":
            send_message(webhook_url)
        elif choice == "3":
            delete_webhook(webhook_url)
        elif choice == "4":
            print(Fore.MAGENTA + "👋 Exiting. Goodbye!")
            sys.exit()
        else:
            print(Fore.RED + "❌ Invalid choice. Please select 1-4.")

if __name__ == "__main__":
    main()
#by D0up4
