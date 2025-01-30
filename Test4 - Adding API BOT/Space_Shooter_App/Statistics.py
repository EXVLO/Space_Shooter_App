import numpy as np
import matplotlib.pyplot as plt
import json
from datetime import datetime

def plot_data(curr_client, account_age, scores):
    # Scale the account age by dividing by 50
    scaled_account_age = [age / 50 for age in account_age]

    # Scale the scores by dividing the max score by the size of the list
    max_score = max(scores)
    list_size = len(scores)
    scaled_scores = [score / list_size for score in scores]

    # Create the scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Scatter plot for scaled account age vs scaled scores
    scatter = ax.scatter(scaled_account_age, scaled_scores, color='blue', label="Scores", alpha=0.7, edgecolors='black', s=100)

    # Calculate the centroid (mean of scaled account_age and scaled scores)
    centroid_x = np.mean(scaled_account_age)
    centroid_y = np.mean(scaled_scores)

    # Plot the centroid as a red point
    centroid = ax.scatter(centroid_x, centroid_y, color='red', marker='X', s=200, label="Centroid", edgecolors='black')

    # Convert curr_client.account_created to account age in days
    account_created = datetime.strptime(curr_client.account_created, "%m/%d/%Y %H:%M:%S")
    current_date = datetime.now()
    account_age_client = (current_date - account_created).days

    # Scale the account age for curr_client
    scaled_account_age_client = account_age_client / 50

    # Get curr_client's score and scale it
    score_client = curr_client.max_Score / list_size

    # Plot the client's dot as a green dot and label it as "You"
    client_point = ax.scatter(scaled_account_age_client, score_client, color='green', s=250, label="You", marker='*', edgecolors='black')

    # Annotate the centroid and client's point
    ax.annotate('Centroid', xy=(centroid_x, centroid_y), xytext=(centroid_x + 0.5, centroid_y + 0.5),
                arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12, color='red')
    ax.annotate('You', xy=(scaled_account_age_client, score_client), xytext=(scaled_account_age_client + 0.5, score_client + 0.5),
                arrowprops=dict(facecolor='black', shrink=0.05), fontsize=12, color='green')

    # Labels and title
    ax.set_xlabel("Account Age (Days in 50s)", fontsize=14, fontweight='bold')
    ax.set_ylabel("Score (Scaled)", fontsize=14, fontweight='bold')
    ax.set_title("Scaled Score vs Scaled Account Age", fontsize=16, fontweight='bold')

    # Add a legend
    ax.legend(loc='upper right', fontsize=12)

    # Add grid lines
    ax.grid(True, linestyle='--', alpha=0.6)

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show the graph
    plt.show()

def show_graph(curr_client, server):
    message = f"%%%GETSTATS"
    server.serv.send(message.encode("utf-8"))
    while True:
        message = server.serv.recv(1024).decode("utf-8")
        try:
            # Parse the JSON response
            response = json.loads(message)
        
            # Get both max_score and acc_created data
            max_score_data = response["%%%max_score_list"]
            acc_created_data = response["%%%acc_created_list"]
        
            # Calculate account age in days
            account_age_in_days = []
            for created_date_str in acc_created_data:
                created_date = datetime.strptime(created_date_str, "%m/%d/%Y %H:%M:%S")
                current_date = datetime.now()
                age_in_days = (current_date - created_date).days
                account_age_in_days.append(age_in_days)
        
            break

        except json.JSONDecodeError as e:
            print(f"Error decoding server response: {e}")
        except KeyError as e:
            print(f"Missing key in server response: {e}")

    # Call plot_data with the scaled data
    plot_data(curr_client, account_age_in_days, max_score_data)