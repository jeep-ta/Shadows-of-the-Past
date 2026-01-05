import pygame
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen Resolution
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
fake_screen = pygame.Surface((screen_width, screen_height))
pygame.display.set_caption("Shadows of the Past")
icon = pygame.image.load(r"pick-of-destiny.png")
pygame.display.set_icon(icon)

# Load background music
try:
    pygame.mixer.music.load(r"Ender Lilies OST - Cliffside Hamlet Extended.mp3")
    pygame.mixer.music.play(-1)  # Loop the music indefinitely
except pygame.error as e:
    print(f"Error loading music: {e}")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Font
font = pygame.font.Font(None, 22)
menu_font = pygame.font.SysFont("chiller", 40)
ending_font = pygame.font.Font(None, 72)
# Background Images
bg_images = []
bg_image_paths = [
    r"Background\Vague image of a towering creation and a lab.jpg",
    r"Background\Cryptic Symbol.jpg",
    r"Background\Triumphant battle from the past.jpg",
    r"Background\Vision of you creating the creatures.jpg",
    r"Background\Final Confrontation.jpg",
    r"Background\Cryptic Symbol.jpg",
    r"Background\Cryptic Symbol.jpg",
    r"Background\Cryptic Symbol.jpg",
    r"Background\Cryptic Symbol.jpg",
    r"Background\Cryptic Symbol.jpg",
    r"Background\Cryptic Symbol.jpg",
]

for path in bg_image_paths:
    try:
        bg_images.append(pygame.image.load(path))
    except pygame.error as e:
        print(f"Error loading background image {path}: {e}")

# Scenes and Choices
scenes = [
    (
        "I awaken in a desolate world.",
        "The air is thick with decay. Ruins surround me.",
        "A distant growl breaks the silence. What do I do?",
        "I look around, confusion clouding my thoughts.",
        "Where... am I? What happened here?",
        "I stumble forward, my boots crunching against brittle debris.",
        "The growl echoes again, low and menacing.",
        "I murmur to myself, ",
        "That does not sound good...",
        "I need to figure out where I am before something finds me."
    ),
    (
        "A mysterious figure approaches, their face hidden.",
        "They seem to know me, but won't explain more.",
        "The figure speaks, their tone calm but cold.",
        "Impressive… for someone who does not belong here.",
        "Panting, I snap, Who are you? What do you mean, I don't belong here?",
        "They don't answer my question, their gaze distant.",
        "This place is fractured, broken beyond repair… but maybe not entirely.",
        "Angrily, I demand, Answer me! What is this place? Why am I here?",
        "The figure offers a faint smile. You should not be here…",
        "but maybe you can fix what is broken."
    ),
    (
        "I come across a village under attack by monstrous creations.",
        "The villagers beg for help. What will I do?",
        "A villager grabs my arm, panic in their eyes.",
        "Please! You have to help us! Those creatures are destroying everything!",
        "I hesitate, looking around at the chaos.",
        "I am not sure I can… but I will do what I can to stop them.",
        "The villager pleads, “Thank you! The others are still inside—please, hurry!”",
        "I nod grimly. I will do what I can. Stay back and keep safe.",
        "I steel myself and step into the chaos, monstrous figures looming before me."
    ),
    (
        "I enter a lab or ruined fortress, remnants of my past.",
        "A vivid memory of creating monsters",
        "to 'save the world through domination' floods my mind.",
        "he steps forward, revealing the truth about my past."
    ),
    (
        "I stand in silence, the weight of the revelation sinking into my bones.",
        "My vision blurs as the memories I tried so hard to bury come flooding back.",
        "I see the lab, the experiments, the creatures I created in the name of progress,"
        "in the name of control.",
        "he steps closer, their expression somber,",
        "as if waiting for something from me.",
        "They don't speak; they don't need to.",
        "The truth hangs between us like a heavy fog.",
        "Real Protagonist: 'You know what must be done now. The world is on the edge, ",
        "everything you have done… has led to this moment.",
        "Redemption or destruction. It's your choice.'",
        "I look into their eyes, searching for a hint of hope,",
        "but all I see is the same sorrow I feel within myself.",
        "Is there even a way to redeem what I've done?",
        "Or am I doomed to continue the cycle of destruction I started?",
        "The choice weighs heavily on my mind as I look at the broken world around me.",
        "There is no going back now.",
        "There is only one path forward."
    ),
    (
        "I shake my head violently, as if trying to rid myself of the haunting words that he spoke.",
        "'This is not me,' I mutter to myself.",
        "'It is a lie. I didn't do that. I won't let it define me.'",
        "But deep down, I know.",
        "The shadows of my past are too close, and I can't run from them anymore.",
        "I have been lying to myself for so long that it is hard to distinguish the truth from my own delusions.",
        "he watches me, their gaze filled with pity and understanding, and yet… disappointment.",
        "Real Protagonist: 'You can't deny what you have done forever.",
        "The world will pay for it if you don't make the right choice now.",
        "Your actions have consequences, whether you face them or not.",
        "I feel the anger rising within me.",
        "No. I won't let them control me.",
        "I will fight for what I want.",
        "I can undo it.",
        "I can fix everything… can't I?"
    ),
    (
        "The final confrontation approaches. he stands before me,",
        "their eyes full of sorrow.",
        "The fate of the world depends on this moment. What will I choose?"
    ),
    (
        "I raise my weapon, but my hands don't shake with rage. They're steady, resolute.",
        "The fight is not born of hatred, but of the belief that things can still change,",
        "that there is a chance for redemption even after everything that has been lost.",
        "As the battle rages on, I aim to neutralize my opponent without unnecessary harm.",
        "I don't want to destroy what's left of us. I want to save what can still be saved.",
        "he meets my eyes as they fall, a faint look of surprise in their gaze,",
        "but there is something else there too—hope.",
        "They understood.",
        "With a final breath, they speak, their voice weak: 'You chose... hope. I always believed in you.'",
        "And then, they are gone.",
        "I stand alone, but not in despair.",
        "The weight of the world is heavy, but there is a flicker of light.",
        "Maybe, just maybe, this is the start of something better."
    ),
    # Ending 2: Choosing to Fight with Negative Karma
    (
        "The battle is fierce. Every strike I land is fueled by bitterness, anger, and a thirst for power.",
        "I don't care who I hurt. I need to prove that I am in control, that I can take what I want.",
        "he tries to fight back, but they're no match for the rage that has consumed me.",
        "I strike without hesitation, without remorse.",
        "Their eyes are filled with sorrow as they fall, and something inside me twists.",
        "They speak one last time, their voice trembling: 'You have become everything you once fought against.'",
        "But I don't care.",
        "I stand over their broken body, my chest heaving, and for the first time, I feel like I have won.",
        "But the victory is hollow.",
        "In the end, it is just me, alone with the consequences of my own actions."
    ),
    # Ending 3: Choosing Not to Fight with Positive Karma
    (
        "I lower my weapon, my heart heavy but clear.",
        "I won't fight this battle. There has been enough destruction, enough pain. I won't add to it.",
        "he stares at me, disbelief crossing their face at first.",
        "But as the moments stretch on, their expression softens,",
        "the tension in the air slowly dissipating.",
        "They see it—see the change in me.",
        "'You... you have made the right choice,' they say, their voice almost a whisper.",
        "'There is still hope for you, for all of us.'",
        "I nod, and together we walk away from the battlefield, leaving the war behind.",
        "The world is broken, but maybe, just maybe, we can start healing."
    ),
    # Ending 4: Choosing Not to Fight with Negative Karma (Bad Ending)
    (
        "I stand there, weapon in hand, but I can't bring myself to strike.",
        "Despite the rage coursing through me, despite everything I have been through,",
        "I don't want to kill.",
        "he eyes me carefully, as if trying to gauge whether this is some kind of trick.",
        "'You think you can just walk away from all this?' they ask, voice tinged with frustration.",
        "I hesitate, feeling the weight of my past mistakes, but something in me refuses to act.",
        "'I won't fight you. Not anymore.'",
        "he's expression darkens.",
        "They let out a bitter laugh, the disappointment in their eyes cutting deeper than any wound.",
        "'You think this will end? You think you can just walk away from the consequences of what you have done?'",
        "Before I can respond, they raise their weapon, and the final strike comes not from me, but from them.",
        "'You have failed,' they whisper as I fall.",
        "'All you have done is leave a broken world for others to suffer.'",
        "I close my eyes, the weight of my inaction crashing down on me.",
        "I thought I could avoid the consequences, but in the end, I couldn't escape them.",
        "The world moves on, broken and unforgiven, and there is nothing left for me but regret."
    )
]

scene_choices = [
    ["Explore the landscape", "Fight the hostile creature"],
    ["Who am I?", "Fix what?"],
    ["Save them", "Sacrifice them"],
    ["Accept the truth", "Deny the truth"],
    ["Continue", ""],
    ["Continue", ""],
    ["Fight", "Refuse to fight"],
    ["End", ""],
    ["End", ""],
    ["End", ""],
    ["End", ""]
]

# Menu
menu_items = ["Start Game", "    Quit"]
menu_positions = []

# Karma Tracking
positive_karma = 0
negative_karma = 0

def get_scaled_mouse_pos():
    mouse_pos = pygame.mouse.get_pos()
    scale_x = screen.get_width() / screen_width
    scale_y = screen.get_height() / screen_height
    return (mouse_pos[0] / scale_x, mouse_pos[1] / scale_y)

# Function to render text with an outline
def render_text_with_outline(text, font, color, outline_color, position):
    # Render the outline text
    outline_surface = font.render(text, True, outline_color)
    # Render the main text
    text_surface = font.render(text, True, color)
    
    # Get the rectangles for the outline and main text
    outline_rect = outline_surface.get_rect(topleft=position)
    text_rect = text_surface.get_rect(topleft=position)

    # Blit the outline first, then the main text
    fake_screen.blit(outline_surface, outline_rect.move(-1, -1))  # Top-left
    fake_screen.blit(outline_surface, outline_rect.move(1, -1))   # Top-right
    fake_screen.blit(outline_surface, outline_rect.move(-1, 1))   # Bottom-left
    fake_screen.blit(outline_surface, outline_rect.move(1, 1))    # Bottom-right
    fake_screen.blit(text_surface, text_rect)
    return text_rect

def draw_highlight_box(rect):
    s = pygame.Surface((rect.width + 10, rect.height + 10))  # Slightly larger than text
    s.set_alpha(150)                # Alpha level
    s.fill((0, 0, 100))            # Dark Blue
    fake_screen.blit(s, (rect.x - 5, rect.y - 5))

#Draw Ending
def ending():
    end = True
    while end:
        fake_screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                end = False
        text_lines = [
        "Thank you for playing the game!",
        "",
        "Viper team <3"
        ]
            # Render each line of text
        for i, line in enumerate(text_lines):
                text_surface = font.render(line, True, white)
                fake_screen.blit(text_surface, (screen_width // 2, screen_height// 2 + i * 30))
        
        # Scale and blit
        scaled_surface = pygame.transform.scale(fake_screen, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()  # Update the display
    menu()
# Draw Game
def draw_game(scene_index):
    global menu_positions, positive_karma, negative_karma
    
    # Text Animation State
    active_lines_idx = 0       # The index of the line currently being animated/shown
    char_idx = 0               # Current character index for the active line
    last_type_time = pygame.time.get_ticks()
    type_speed = 30            # ms per character
    text_state = "typing"      # "typing" (animating), "waiting" (waiting for click to next line), "done" (all text shown)
    
    # Pre-calculate lines for the scene
    current_scene_lines = scenes[scene_index]
    
    waiting_for_choice = True
    while waiting_for_choice:
        # 1. Draw Background & Overlay
        fake_screen.blit(bg_images[scene_index], (0, 0))
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(170)
        fake_screen.blit(overlay, (0, 0))
        
        # 2. Logic: Update Typewriter
        # Only update if we are in "typing" state and haven't shown all lines yet
        if text_state == "typing" and active_lines_idx < len(current_scene_lines):
            current_time = pygame.time.get_ticks()
            if current_time - last_type_time > type_speed:
                char_idx += 1
                last_type_time = current_time
                # Check if we finished the current line
                if char_idx >= len(current_scene_lines[active_lines_idx]):
                    char_idx = len(current_scene_lines[active_lines_idx])
                    text_state = "waiting" # Line finished, wait for click
        
        # 3. Draw Text (up to active_lines_idx)
        y_offset = 50
        
        # Draw all fully revealed previous lines
        for i in range(active_lines_idx):
            render_text_with_outline(current_scene_lines[i], font, white, black, (50, y_offset))
            y_offset += 30
            
        # Draw the currently animating line (if we are still within bounds)
        if active_lines_idx < len(current_scene_lines):
            line_to_draw = current_scene_lines[active_lines_idx][:char_idx]
            render_text_with_outline(line_to_draw, font, white, black, (50, y_offset))
            y_offset += 30
        
        # 4. Draw Choices (Only if all text is fully shown)
        if active_lines_idx >= len(current_scene_lines): # All lines done
            choices = scene_choices[scene_index]
            menu_positions.clear()
            mouse_pos = get_scaled_mouse_pos()
            for i, choice in enumerate(choices):
                # Calculate rect first for hover check
                rect = font.render(choice, True, white).get_rect(topleft=(50, y_offset + 20))
                
                # Draw highlight if hovered
                if rect.collidepoint(mouse_pos):
                    draw_highlight_box(rect)
                    
                render_text_with_outline(choice, font, white, black, (50, y_offset + 20))
                menu_positions.append(rect)
                y_offset += 30

        # 5. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # If we are finished reading (showing choices)
                if active_lines_idx >= len(current_scene_lines):
                    mouse_pos = get_scaled_mouse_pos()
                    for i, rect in enumerate(menu_positions):
                        if rect.collidepoint(mouse_pos):
                            # Handle scene transitions (Logic remains same, just indented)
                            if scene_index == 0:  # First scene choices
                                if i == 0:  # Explore
                                    draw_game(1)  # Move to scene 2
                                elif i == 1:  # Fight
                                    positive_karma += 1
                                    draw_game(2)  # Move to scene 3
                            elif scene_index == 1:  # Second scene choices
                                if i == 0:  # Who am I?
                                    draw_game(3)  # Move to scene 4
                                elif i == 1:  # Fix what?
                                    draw_game(3)  # Move to scene 4
                            elif scene_index == 2:  # Third scene choices
                                if i == 0:  # Save them
                                    draw_game(3)  # Move to scene 4
                                elif i == 1:  # Sacrifice them
                                    negative_karma += 2
                                    draw_game(3)  # Move to scene 4
                            elif scene_index == 3:  # Fourth scene choices
                                if i == 0:  # Accept the truth
                                    positive_karma += 3
                                    draw_game(4)  # Move to scene 5
                                elif i == 1:  # Deny the truth
                                    negative_karma += 1
                                    draw_game(5)  # Move to scene 6
                            elif scene_index in [4, 5]:  # Fifth scene choices
                                if i == 0:  # Continue
                                    draw_game(6)  # Move to final confrontation
                                elif i == 1:  # Refuse to fight
                                    draw_game(6)  # Move to final confrontation
                            elif scene_index == 6:  # Final confrontation choices
                                if i == 0:  # Fight
                                    if positive_karma > negative_karma:
                                        draw_game(7)  # Positive ending
                                    else:
                                        draw_game(8)  # Negative ending
                                elif i == 1:  # Refuse to fight
                                    if positive_karma > negative_karma:
                                        draw_game(9)  # Positive ending
                                    else:
                                        draw_game(10)  # Negative ending
                            elif scene_index > 6:
                                if i == 0: #End
                                    ending()
                else:
                    # Text Interaction Logic
                    if text_state == "typing":
                        # Instant finish current line
                        char_idx = len(current_scene_lines[active_lines_idx])
                        text_state = "waiting"
                    elif text_state == "waiting":
                        # Advance to next line
                        active_lines_idx += 1
                        char_idx = 0
                        # If we still have lines, start typing next one
                        if active_lines_idx < len(current_scene_lines):
                            text_state = "typing"
                        else:
                            text_state = "done"

        # 6. Scale and Update Logic (Moved inside loop)
        scaled_surface = pygame.transform.scale(fake_screen, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()
# Draw Menu
def draw_menu():
    bg = pygame.image.load(os.path.join("Background", "Menuscreen.jpg"))
    title = pygame.image.load(os.path.join("Background", "title screen.png"))
    fake_screen.blit(bg, (0, 0))
    overlay = pygame.Surface((screen_width, screen_height))
    overlay.fill((0, 0, 0))
    overlay.set_alpha(170)
    fake_screen.blit(overlay, (0, 0))
    fake_screen.blit(title, (325, 50))
    fake_screen.blit(title, (325, 50))
    menu_positions.clear()
    
    mouse_pos = get_scaled_mouse_pos()
    
    for i, option in enumerate(menu_items):
        # Calculate rect
        text_rect = font.render(option, True, white).get_rect(center=((screen_width // 2)-10 , screen_height // 2 + i * 60))
        
        # Highlight if hovered (adjust rect for center alignment)
        # Note: render_text_with_outline draws at top-left, but we used center for rect calculation logic in original code
        # Let's keep logic consistent. The original code calculated rect using 'center' but rendered using topleft calc
        # We need to match the rendering position to be accurate.
        
        render_pos = (screen_width // 2 - 50, screen_height // 2 + i * 60)
        # Let's recalculate rect based on where it is actually drawn
        drawn_rect = menu_font.render(option, True, white).get_rect(topleft=render_pos)
        
        if drawn_rect.collidepoint(mouse_pos):
            draw_highlight_box(drawn_rect)

        render_text_with_outline(option, menu_font, white, black, render_pos)
        menu_positions.append(drawn_rect)

def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Transform mouse pos
                mouse_pos = get_scaled_mouse_pos()
                for i, rect in enumerate(menu_positions):
                    if rect.collidepoint(mouse_pos):
                        if i == 0:  # Start game
                            print("Game is starting...")
                            draw_game(0)  # Start with the first scene
                        elif i == 1:  # Quit
                            print("Game is quitting...")
                            pygame.quit()
                            sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        draw_menu()
        # Scale fake_screen to current screen size
        scaled_surface = pygame.transform.scale(fake_screen, screen.get_size())
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

# Game loop
running = True
while running:
    menu()  # Start with the menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
sys.exit()