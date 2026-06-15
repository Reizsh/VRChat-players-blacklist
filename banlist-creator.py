#!/usr/bin/env python3
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2026 Reizsh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os
from datetime import datetime

FILENAME = "banlist.json"

def load_banlist():
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Warning: 'banlist.json' is corrupted or contains invalid data.")
            print("Starting with an empty list.")
            return []
    return []

def save_banlist(data):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\nData successfully saved to '{FILENAME}'.")

def main():
    banlist = load_banlist()
    print("Script initialized.")
    print("Please enter the required information for each new entry.")
    print("-" * 56)

    while True:
        try:
            print("\n--- Add a New Player ---")

            # 1. ID
            while True:
                player_id = input("Player ID: ").strip()
                if player_id:
                    if not player_id.startswith("usr_"):
                        player_id = f"usr_{player_id}"
                    break
                print("Player ID cannot be empty. Please try again.")

            # 2. Name
            while True:
                name = input("Player Name: ").strip()
                if name:
                    break
                print("Player name cannot be empty. Please try again.")

            # 3. Punishment type
            punishment_types = ["kick", "ban", "mute", "none"]
            while True:
                ban_type = input(f"Punishment type ({', '.join(punishment_types)}) [default: none]: ").strip().lower() or "none"
                if ban_type in punishment_types:
                    break
                print(f"Invalid input. Please enter exactly one of: {', '.join(punishment_types)}")

            # 4. Reason
            while True:
                reason = input("Reason: ").strip()
                if reason:
                    break
                print("Reason cannot be empty. Please try again.")

            # 5. Date
            today = datetime.now().strftime("%Y-%m-%d")
            date = input(f"Date (press Enter for current date: {today}): ").strip() or today

            # 6. Expiration
            expires = input("Expiration date (press Enter for permanent punishment): ").strip() or "null"

            # 7. Appeal
            while True:
                allowed_appeal = input("Is appeal allowed? (y/n): ").strip().lower()
                if allowed_appeal in ["y", "n"]:
                    appeal = allowed_appeal
                    break
                print("Invalid input. Please enter exactly 'y' or 'n'.")

            # Form the entry
            new_entry = {
                "id": player_id,
                "name": name,
                "type": ban_type,
                "reason": reason,
                "date": date,
                "expires": expires,
                "appeal": appeal
            }

            # Add to the list
            banlist.append(new_entry)
            print(f"Player '{name}' has been successfully added to the list (total entries: {len(banlist)}).")

        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            save_banlist(banlist)
            print("Exiting. Goodbye!")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
