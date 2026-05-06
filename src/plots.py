import matplotlib.pyplot as plt

def plot_listening_trend(series):
    series.plot()
    plt.title("Listening Over Time")
    plt.ylabel("Minutes Played")
    plt.xlabel("Year")
    plt.show()