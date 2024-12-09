import sys
import numpy as np
import matplotlib.pyplot as plt

def read_incidence_matrix(file_path):
    # Read the TSV file and skip the first row (header)
    data = np.loadtxt(file_path, dtype=str, delimiter='\t', skiprows=1)

    # Extract the gene names and incidence matrix
    gene_names = data[:, 0]
    incidence_matrix = data[:, 1:].T.astype(int)

    return gene_names, incidence_matrix

def new_genes_found(incidence_matrix, num_iterations=1000):
    num_samples, num_genes = incidence_matrix.shape

    # Initialize an array to store the results of gene accumulation for each iteration
    accumulated_genes_all_iterations = np.zeros((num_iterations, num_samples))

    # Perform multiple iterations of random sampling and accumulation
    for iteration in range(num_iterations):
        # Shuffle the sample order for each iteration
        shuffled_samples = np.random.permutation(incidence_matrix)

        # Initialize a set to keep track of unique genes
        unique_genes_seen = set()

        # Initialize an array to store the number of new genes found at each step
        genes_found = np.zeros(num_samples)

        # Iterate through each sample and accumulate the genes
        for i in range(num_samples):
            current_sample = shuffled_samples[i, :]

            # Count the number of new genes found in the current sample
            num_new_genes = len(set(np.where(current_sample > 0)[0]) - unique_genes_seen)

            # Update the set of unique genes seen
            unique_genes_seen.update(set(np.where(current_sample > 0)[0]))

            # Record the number of new genes found for this sample
            genes_found[i] = genes_found[i-1] + num_new_genes if i > 0 else num_new_genes

        # Store the accumulated genes for this iteration
        accumulated_genes_all_iterations[iteration, :] = genes_found

        # Plot the individual accumulation curves (in translucent black)
        plt.plot(np.arange(1, num_samples + 1), genes_found, color='black', alpha=0.02)  # Translucent black line

    # Calculate the average accumulated genes across all iterations
    avg_accumulated_genes = np.mean(accumulated_genes_all_iterations, axis=0)

    # Plot the averaged rarefaction curve (in blue with points)
    plt.plot(np.arange(1, num_samples + 1), avg_accumulated_genes, marker='o', color='blue')
    plt.xlabel('Number of sequences sampled')
    plt.ylabel('Average number of unique genes found')
    plt.title('Gene Rarefaction Curve (1000 samples)')
    plt.grid(True)

    # Save the plot as a PNG file with the input file name
    plt.savefig(f"./{input_file}_rarefaction.png")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    gene_names, incidence_matrix = read_incidence_matrix(input_file)
    new_genes_found(incidence_matrix)
