import matplotlib.pyplot as plt
import os

def create_test_chart():
    # Sample data
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [60, 25, 15]

    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the figure
    image_path = os.path.join('sentiment_chart.png')  # Save in the current directory
    plt.savefig(image_path)
    plt.close()

    print(f"Chart saved at: {image_path}")

if __name__ == "__main__":
    create_test_chart()
