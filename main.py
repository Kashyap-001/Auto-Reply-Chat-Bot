import pyautogui
import time
import pyperclip
import keyboard  # For detecting quit key
from google import genai
from google.genai import types

# ========================
# HARD-CODED API KEY FOR TESTING (⚠ Not safe for production)
# ========================
api_key = ""
client = genai.Client(api_key=api_key)

# ========================
# Helper function
# ========================
def message_is_from_kashyap(line: str) -> bool:
    """Detects if a given chat line is from Kashyap."""
    if "]" in line:
        after_timestamp = line.split("]", 1)[1].strip()
        return after_timestamp.lower().startswith("kashyap:")
    return False

# ========================
# Startup
# ========================
print("✅ Script started. Press 'q' to quit at any time.")
time.sleep(2)  # Give time to focus chat window before automation starts

# ========================
# Main Loop
# ========================
pyautogui.click(1212, 1049)
while True:
    # --- Check for quit key ---
    if keyboard.is_pressed('q'):
        print("🛑 Quit key pressed. Stopping script...")
        break

    # === Step 1: Select chat history text ===
    pyautogui.moveTo(738, 196)  # Start point for selection (your chat top)
    pyautogui.dragTo(1833, 946, duration=3.0, button='left')  # Drag to bottom
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'c')  # Copy
    time.sleep(0.5)
    pyautogui.click(794, 975)# Click away to deselect
    
    # === Step 2: Get copied chat text ===
    selected_text = pyperclip.paste()
    print("📜 Selected text:")
    print(selected_text)

    # === Step 3: Process last message ===
    lines = [line.strip() for line in selected_text.splitlines() if line.strip()]
    last_line = lines[-1] if lines else ""

    if message_is_from_kashyap(last_line):
       
        

        print("⏩ Last message is from Kashyap. Skipping reply.")
    else:
        # === Step 4: Send to Gemini API ===
        chat = client.chats.create(
            model="gemini-2.5-flash",
            history=[
                types.Content(
                    role="model",
                    parts=[types.Part(text=(
                        "You are Kashyap, a witty friend who speaks in a Gujarati-English casual mix "
                        "written in Gujarati Roman script (Gujarati words in English letters). "
                        "Always give short replies, just like talking to close friends. "
                        #"Example tone: 'Kaya theater ma gayo hato?'. "
                        "Do not add your name or any prefix. "
                        "Always keep replies short."
                    ))]
                )
            ]
        )

        # === Step 5: Get streaming AI response ===
        response_stream = chat.send_message_stream(message=selected_text)
        ai_reply = "".join(chunk.text or "" for chunk in response_stream)

        # Clean reply if it still starts with "Kashyap:"
        if ai_reply.lower().startswith("kashyap:"):
            ai_reply = ai_reply.split(":", 1)[1].strip()

        print("\n💬 AI Reply (cleaned):", ai_reply)

        # === Step 6: Paste reply in chat ===
        pyautogui.click(794, 975)  # Click chat input box
        time.sleep(0.2)
        pyperclip.copy(ai_reply)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.2)
        pyautogui.press('enter')

    # === Step 7: Wait before next scan ===
    time.sleep(2)

