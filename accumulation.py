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

def new_genes_found(incidence_matrix):
    num_samples, num_genes = incidence_matrix.shape

    # Initialize a set to keep track of unique genes
    unique_genes_seen = set()

    # Initialize an array to store the number of new genes found at each step
    genes_found = np.zeros(num_samples)

    # Iterate through each sample row and record the number of unique genes found
    for i in range(num_samples):
        current_sample = incidence_matrix[i, :]
        
        # Count the number of new genes found in the current sample
        num_new_genes = len(set(np.where(current_sample > 0)[0]) - unique_genes_seen)
        
        # Update the set of unique genes seen
        unique_genes_seen.update(set(np.where(current_sample > 0)[0]))
        
        # Record the number of new genes found for this sample
        genes_found[i] = genes_found[i-1] + num_new_genes

    # Plot the rarefaction curve
    plt.plot(np.arange(1, num_samples + 1), genes_found, marker='o')
    plt.xlabel('Number of sequences sampled')
    plt.ylabel('Number of genes found')
    plt.title('Gene accumulation curve')
    plt.grid(True)

    # Save the plot as a PDF file with the input file name
    plt.savefig(f"./{input_file}_plot.pdf")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    gene_names, incidence_matrix = read_incidence_matrix(input_file)
    new_genes_found(incidence_matrix)