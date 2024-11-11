# Turtle Rush
# Team 6 Monday Batch
# The project uses tkinter to set up a menu screen, pandas as a database,
# pygame and random for the main game and matplotlib to plot the leaderboards


# Login and Menu interface
# Chirag M Nayak 5/5

# The Game
# Neet Lahoti 5/5
# Omkar Dharavath 4/5
# Tanmay Sarvaiya 2/5

# The Leaderboards
# Amisha Kohli 5/5
# Cyrus Saiyed 4/5


#importing libraries
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
import random
import pandas as pd
import pygame
import matplotlib.pyplot as plt
import threading

user_data_path = 'First Team Project/Resources/userinfo.csv'
user_data = pd.read_csv(user_data_path, index_col="Username")

font_location = 'First Team Project/Resources/Retro Gaming.ttf'

# memory
username = ''
remembering = False
run = True

# checks if anybody wanted to stay signed in
if True in user_data['Signed In'].values:
    remembering = True
    username = user_data[user_data['Signed In'] == True].index[0]

# function to save updated dataframe
def update_user_data():
    # updates the changes made to user_data
    user_data.to_csv(user_data_path)

# function containing the game
def run_game():
    global run
    max_score = user_data.at[username,'High Score']
    # initialising the pygame
    pygame.init()

    # dimensions of main screen
    WIDTH = 600
    HEIGHT = 600

    # setting up the main screen
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    # setting game name as caption
    pygame.display.set_caption("Turtle Rush")

    # setting up the game icon
    icon = pygame.image.load("First Team Project/Resources/t.png")
    pygame.display.set_icon(icon)

    # getting the player ready as "turtle"
    character_image = pygame.image.load("First Team Project/Resources/image.png")
    char_size = pygame.transform.scale(character_image, (90, 90))

    # assigning the six lanes' coordinates
    lanes = [[10, 0], [110, 0], [210, 0], [310, 0], [410, 0], [510, 0]]

    # initial player position
    i = 3  
    p_x = lanes[i][0]
    p_y = 450

    # speed with which the obstacles move
    obstacle_speed = 5.0 

    # setting the time interval in which the obstacles generate 
    timer = 0
    spawn_interval = 20

    # getting player visible on screen
    def player(x, y):
        screen.blit(char_size, (x, y))

    

    # collection of random obstaclesd
    obstacles = []

    # assigning obstacles a random lane 
    def create_obstacle():
        x = random.choice(lanes)[0]
        y = -90
        return [x, y]

    # initial score
    score = 0

    # setting up health of player
    health = 3
    max_health = 3

    # setting the font for "Score" and "Game Over"
    font = pygame.font.Font(font_location, 30)
    font1 = pygame.font.Font(font_location,50)

    # function to stop the game after the collision
    def game_over(): 
        screen.fill((240,240,240))
        pygame.display.flip() 
        gameover_text = font1.render('Game Over !!', True, (0, 0, 0)) 
        screen.blit(gameover_text, (130,250)) 
        pygame.display.flip() 
        pygame.time.delay(1000)
        global run
        run = False

    while run:
        
        screen.fill((240,240,240))

        pygame.draw.line(screen,(0,0,0),(100,0),(100,550),4)
        pygame.draw.line(screen,(0,0,0),(200,0),(200,550),4)
        pygame.draw.line(screen,(0,0,0),(300,0),(300,550),4)
        pygame.draw.line(screen,(0,0,0),(400,0),(400,550),4)
        pygame.draw.line(screen,(0,0,0),(500,0),(500,550),4)
        pygame.draw.line(screen,(0,0,0),(0,550),(600,550),4)

        health_bar_width = 130
        health_bar_height = 10
        current_health_width = int(health_bar_width * (health / max_health))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(235, 575, current_health_width, health_bar_height))  # Remaining health

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(230, 570, health_bar_width + 10, health_bar_height + 10), 5)
        pygame.draw.line(screen,(0,0,0),(276.6,570),(276.6,585),5)
        pygame.draw.line(screen,(0,0,0),(323.3,570),(323.3,585),5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if p_x >= 0 and p_x <= 600:
                        i -= 1
                        i %= 6
                        p_x = lanes[i][0]
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if p_x >= 0 and p_x <= 600:
                        i += 1
                        i %= 6
                        p_x = lanes[i][0]

        if timer % spawn_interval == 0:
            obstacles.append(create_obstacle())

        timer += 1

        player_collison_rect = pygame.Rect(p_x,p_y,80,80)

        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            rect = pygame.Rect(obstacle[0], obstacle[1], 80, 80)
            pygame.draw.rect(screen, (83, 83, 83), rect)

            if player_collison_rect.colliderect(rect):
                health -= 1  
                obstacles.remove(obstacle)  
                if health == 0:
                    game_over()
                    
            if obstacle[1]>=470:
                score+=5
                #print(score)

        if score>=100 and score<200:
            obstacle_speed = 7
        if score>=200 and score<300:
            obstacle_speed =10
        if score>=300 and score<400:    
            obstacle_speed = 20

        obstacles = [obstacle for obstacle in obstacles if obstacle[1] < 470]

        score_text = font.render(f"Score: {score}", True, (0, 0, 0)) 
        screen.blit(score_text, (10, 15))
        
        player(p_x, p_y)

        pygame.display.update()
        pygame.time.delay(20)
    
    # Stores High Score
    if score > max_score:
        user_data.at[username, 'High Score'] = score
        update_user_data()

    pygame.quit()


# contains the GUI linking the different aspects of the application
# includes login system
class GUI:
    def __init__(self):
        global remembering


        #initializing a screen and title
        self.screen = tk.Tk()
        self.screen.geometry('800x600')
        self.screen.title('Turtle Rush')

        #
        icon = PhotoImage(file='First Team Project/Resources/t.png')
        self.screen.iconphoto(False, icon)
        

        # Login Screen
        self.log_in_frame = tk.Frame(self.screen)

        self.username_label = tk.Label(self.log_in_frame, text='Username : ', font=('Retro Gaming', 12))
        self.username_label.grid(row=0,column=0)

        self.username_textbox = tk.Entry(self.log_in_frame,width=20, font=('Retro Gaming', 12))
        self.username_textbox.grid(row=0, column=1)
        self.username_textbox.bind('<Return>', lambda e: self.password_textbox.focus_set())

        self.password_label = tk.Label(self.log_in_frame, text='Password : ', font=('Retro Gaming', 12))
        self.password_label.grid(row=1,column=0)

        self.password_textbox = tk.Entry(self.log_in_frame, width=20, font=('Retro Gaming', 12),show='*')
        self.password_textbox.grid(row=1, column=1)

        self.sign_up_in_button = tk.Button(self.log_in_frame, text='Sign Up/Sign In',font=('Retro Gaming', 10), command=self.sign_up_in)
        self.sign_up_in_button.grid(row=3,columnspan=2)

        self.remember_me_var = tk.BooleanVar(value = remembering)
        self.remember_me_checkbox = tk.Checkbutton(self.log_in_frame, text='Remember Me :)', font=('Retro Gaming', 12), variable=self.remember_me_var, command=self.toggle_remember)
        self.remember_me_checkbox.grid(row=2,columnspan=2)

        if remembering:
            self.main_menu()
        else:
            self.log_in_frame.pack(fill='none', expand=True)

        self.screen.mainloop()
    
    # allows user to stay signed in even after the application closes
    def toggle_remember(self):
        global remembering
        remembering = self.remember_me_var.get()
    
    # adds / checks the data provided by the user
    def sign_up_in(self):
        global username
        username = self.username_textbox.get().strip()
        password = self.password_textbox.get().strip()
        usernames = user_data.index

        #makes sure the username or password is not empty
        if not username or not password:
            messagebox.showwarning("Warning", "Username or Password cannot be empty")
        
        elif username in usernames:
            #Sign In
            if user_data.at[username, 'Password'] == password:

                #Update the Signed_In state
                user_data['Signed In'] = False #Resets all the states to False
                user_data.at[username, 'Signed In'] = self.remember_me_var.get()
                update_user_data()

                self.main_menu()
            else:
                messagebox.showerror('Error', 'Incorrect Password / Username already taken')

        else:
            #Sign Up
            user_data.loc[username] = [password, 0, 0, self.remember_me_var.get()]
            if self.remember_me_var.get():
                user_data['Signed In'] = False
                user_data.at[username,'Signed In'] = True
            update_user_data()
            self.main_menu()

    # Menu screen        
    def main_menu(self):
        self.log_in_frame.pack_forget()

        self.main_menu_frame = tk.Frame(self.screen)

        self.welcome_message_label = tk.Label(self.main_menu_frame, text = f'Hello {username}', font=('Retro Gaming', 8))
        self.welcome_message_label.grid(row=0,column=0)

        self.start_game_button = tk.Button(self.main_menu_frame, text='START GAME', font=('Retro Gaming', 12), command=self.game)
        self.start_game_button.grid(row=1,column=0)

        self.leaderboard_button = tk.Button(self.main_menu_frame, text='LEADERBOARDS', font=('Retro Gaming', 12), command=self.leaderboard)
        self.leaderboard_button.grid(row=2,column=0)

        
        self.main_menu_frame.pack(fill='none',expand=True)
        self.sign_out_button = tk.Button(self.screen, text='Sign Out', font=('Retro Gaming', 12), command=self.sign_out)
        self.sign_out_button.pack(side='bottom', anchor='se',padx=10, pady=10)

    # allows user to sign out
    def sign_out(self):
        global username, remembering
        self.username_textbox.delete(0, tk.END)
        self.password_textbox.delete(0,tk.END)
        user_data.at[username, 'Signed In'] = False
        update_user_data()

        username = ''
        remembering = False
        self.remember_me_var.set(False)

        self.main_menu_frame.pack_forget()
        self.sign_out_button.pack_forget()
        self.log_in_frame.pack(fill='none', expand=True)

    # plots graphs of the high scores
    def leaderboard(self):
        # plt.clf()
        # scores = pd.read_csv(user_data_path)
        # x = scores['Username']
        # y = scores['High Score']
        # z = scores['Time Played']
        # plt.plot(x, y, label='Scores')
        # plt.title("Leaderboard")
        # plt.xlabel("Username")
        # plt.ylabel("High Score")

        # plt.legend()

        # plt.show()
        try:
            scores = pd.read_csv("First Team Project/Resources/userinfo.csv")
        except FileNotFoundError:
            print("The file 'userinfo.csv' was not found.")
        except pd.errors.EmptyDataError:
            print("The file 'userinfo.csv' is empty.")
        except pd.errors.ParserError:
            print("Error parsing the file.")
        else:
            # Check if required columns are in the DataFrame
            if {'Username', 'High Score', 'Time Played'}.issubset(scores.columns):
                
                # Ask the user for their username
                user_name = username

                # Sort by 'High Score' in descending order
                scores_sorted = scores.sort_values(by='High Score', ascending=False)
                
                # Check if the user is in the top 10
                top_10_scores = scores_sorted.head(10)
                if user_name in top_10_scores['Username'].values:
                    # User is in the top 10, so plot the top 10
                    plot_data = top_10_scores
                    print("Displaying top 10 players including you.")
                else:
                    # User is not in the top 10, so find their position and select nearby players
                    user_row = scores_sorted[scores_sorted['Username'] == user_name]
                    
                    if user_row.empty:
                        print(f"{user_name} not found in the leaderboard.")
                        plot_data = top_10_scores  # Default to top 10 if user is not found
                    else:
                        # Get the index of the user in the sorted DataFrame
                        user_index = user_row.index[0]
                        
                        # Select one player above and one below the user, if they exist
                        nearby_indices = [user_index]
                        if user_index > 0:
                            nearby_indices.insert(0, user_index - 1)  # Add player above
                        if user_index < len(scores_sorted) - 1:
                            nearby_indices.append(user_index + 1)  # Add player below

                        plot_data = scores_sorted.loc[nearby_indices]
                        print("Displaying one player above, you, and one player below.")

                # Display the names and scores of selected players
                print("Selected Players and their High Scores:")
                for index, row in plot_data.iterrows():
                    print(f"{row['Username']}: {row['High Score']}")
                
                # Set figure size and background color to white
                plt.figure(figsize=(10, 6))
                
                # Extract data for plotting
                x = plot_data['Username']
                y = plot_data['High Score']
                
                # Plot High Scores as vertical bars
                plt.bar(x, y, label='High Score', color='red')  # Set bar color to red
                
                # Titles and labels
                plt.title("Leaderboard", color='black')  # Title in black for visibility
                plt.xlabel("Username", color='black')  # X label in black
                plt.ylabel("High Score", color='black')  # Y label in black
                
                # Customize tick colors
                plt.xticks(color='black')
                plt.yticks(color='black')
                
                # Add grid
                plt.grid(axis='y', linestyle='--', alpha=0.5, color='gray')  # Grid in gray for y-axis
                
                # Add legend with custom text color
                plt.legend(facecolor='white', edgecolor='black', labelcolor='black')
                
                # Show the plot
                plt.tight_layout()  # Adjust layout to fit labels
                plt.show()
            else:
                print("Required columns are missing in the CSV file.")
    
    # starts a new thread of game so that the event loops of pygame and tkinter dont affect each other
    def game(self):
        global run
        run = True
        game_thread = threading.Thread(target=run_game)
        game_thread.start()

GUI() #runs the program