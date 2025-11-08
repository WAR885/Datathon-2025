import matplotlib.pyplot as plt

def graph_earnings(data:list[float]):
        # Create the plot
    plt.figure(figsize=(8, 5))  # Set a nice size for the plot
    plt.plot(range(len(data)), data, marker='o', linestyle='-')
    
    # Add titles and labels for clarity
    plt.title("Total Yearly Earnings")
    plt.xlabel("Year")
    plt.ylabel("Earnings")
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Display the plot
    plt.tight_layout()
    plt.show()
def get_total_earnings(data:list[float]):
    return sum(data)