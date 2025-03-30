import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as ticker

# plt.style.use('dark_background') # for title image

def run_puzzle_storm_simulation(accuracy, time_spent, num_puzzles=137):
    time_left = 180
    score = 0
    streak = 0

    for puzzle in range(1, num_puzzles + 1):

        if random.random() < accuracy:
            streak += 1
            score += 1

            # Apply time bonuses based on streak
            match streak:
                case 5:
                    time_left += 3
                case 12:
                    time_left += 5
                case 20:
                    time_left += 7
                case _ if streak >= 30 and streak % 10 == 0:
                    time_left += 10
        else:
            # Penalty for incorrect answer
            streak = 0
            time_left -= 10

        time_left -= time_spent

        if time_left <= 0:
            break

    return score

def run_multiple_simulations(accuracies, times_spent, num_simulations=1000):
    results_avg_data = {}
    results_std_data = {} 

    print("Running simulations...")
    total_combinations = len(accuracies) * len(times_spent)
    count = 0

    for accuracy in accuracies:
        accuracy_avg_scores = []
        accuracy_std_devs = []
        for time_spent in times_spent:
            run_scores = []
            for i in range(num_simulations):
                score = run_puzzle_storm_simulation(accuracy, time_spent)
                run_scores.append(score)

            avg_score = np.mean(run_scores)
            std_dev_score = np.std(run_scores)

            accuracy_avg_scores.append(avg_score)
            accuracy_std_devs.append(std_dev_score)

            count += 1
            if count % max(1, (total_combinations // 50)) == 0 or count == total_combinations:
                 print(f"Progress: {count}/{total_combinations} combinations simulated ({count/total_combinations:.1%}).")

        results_avg_data[accuracy] = accuracy_avg_scores
        results_std_data[accuracy] = accuracy_std_devs

    results_avg_df = pd.DataFrame(results_avg_data, index=times_spent)
    results_avg_df.index.name = 'Time Spent (s)'

    results_std_df = pd.DataFrame(results_std_data, index=times_spent)
    results_std_df.index.name = 'Time Spent (s)'

    print("Simulations complete.")
    return results_avg_df, results_std_df


def plot_accuracy_lines(results_avg_df, results_std_df):

    plt.figure(figsize=(12, 7))
    times_spent_values = results_avg_df.index.values

    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    for n, accuracy_col in enumerate(results_avg_df.columns):
        avg_scores = results_avg_df[accuracy_col].values
        std_devs = results_std_df[accuracy_col].values

        lower_bound = avg_scores - std_devs
        upper_bound = avg_scores + std_devs

        color = colors[n % len(colors)]

        plt.plot(times_spent_values, avg_scores,
                 label=f'{accuracy_col*100:.0f}%',
                 marker='o',
                 linestyle='-',
                 color=color,
                 markersize=4)

        plt.fill_between(times_spent_values, lower_bound, upper_bound,
                         color=color,
                         alpha=0.2)

    plt.xlabel('Time Spent per Puzzle (s)')
    plt.ylabel('Average Score')
    plt.title('Puzzle Storm: Average Score vs. Time Per Puzzle (Shaded Area = +/- 1 Std Dev)')
    plt.legend(title='Accuracy')
    plt.grid(True, linestyle='--', alpha=0.6)

    plt.xticks(times_spent_values[1:], rotation=45)
    plt.xlim(times_spent_values.min(), times_spent_values.max()) # Set limits based on data
    plt.minorticks_on()
    plt.locator_params(axis='x', nbins=5)
    plt.show()

def plot_score_contours(results_avg_df, accuracies, times_spent):
    fig, ax = plt.subplots(figsize=(10, 7))
    X, Y = np.meshgrid(times_spent, accuracies)
    Z = results_avg_df.values.T
    levels = np.arange(20, 150, 10)

    CS = ax.contour(X, Y, Z, levels=levels, cmap='viridis')
    ax.clabel(CS, inline=True, fontsize=9, fmt='%d')
    ax.set_xlabel('Time Spent per Puzzle (s)')
    ax.set_ylabel('Accuracy')
    ax.set_title('Puzzle Storm: Equivalent Score Contours')
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in ax.get_yticks()])
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    # plt.grid(visible=None) # for title image
    plt.show()

accuracies = [i / 100 for i in reversed(range(50, 101, 10))] #50, 101, 10 for first graphs, 70, 101, 10 for contour
times_spent = [x / 2.0 for x in range(1, 20)] #20 for first graphs, 14 for contour
num_simulations_per_point = 1000


simulation_avg_results, simulation_std_results = run_multiple_simulations(
    accuracies, times_spent, num_simulations=num_simulations_per_point
)


plot_accuracy_lines(simulation_avg_results, simulation_std_results)
plot_score_contours(simulation_avg_results, accuracies, times_spent)