import os
import subprocess
import toml


def generate_values(hyperparam):
    datatype, lowerlimit, stride, upperlimit = hyperparam
    if datatype == int:
        return list(range(lowerlimit, upperlimit + 1, stride))
    elif datatype == float:
        values = []
        current_value = lowerlimit
        while current_value <= upperlimit:
            values.append(current_value)
            current_value += stride
        return values
    else:
        raise ValueError(f"Unsupported datatype {datatype}")


# Define hyperparameters in the given format
inv = [int, 2, 1, 15]
bins = [int, 5, 1, 20]

# Generate lists of values for each hyperparameter
inv_values = generate_values(inv)
bins_values = generate_values(bins)

# Base path to the configuration file
base_config_path = "output/california_housing/mlp/tuned_reproduced/"

for inv_val in inv_values:
    for bin_val in bins_values:
        # Construct the configuration file path for the current seed
        seed_config_path = os.path.join(base_config_path, f"{inv_val}_{bin_val}.toml")

        # Here you would modify the `seed_config_path` file to set the `inv` and `bin` values
        # Read the TOML config file
        with open(seed_config_path, 'r') as f:
            config = toml.load(f)

        # Modify the values
        config["inv"] = inv_val
        config["bins"] = bin_val

        # Write back the modified TOML config
        with open(seed_config_path, 'w') as f:
            toml.dump(config, f)

        # Execute the training process
        cmd = f"python bin/mlp.py {seed_config_path}"
        subprocess.run(cmd, shell=True)

import json
import os


def extract_accuracy(stats_file_path):
    with open(stats_file_path, 'r') as f:
        stats = json.load(f)
    return stats.get('accuracy', None)


# Define a result file to store hyperparameter and accuracy combinations
results_file = "results.txt"

# ... [Previous code for grid search here] ...

for inv_val in inv_values:
    for bin_val in bins_values:
        # ... [Code for setting up TOML file and running training here] ...

        # Extract accuracy from stats.json
        stats_file_path = os.path.join(base_config_path, f"{inv_val}_{bin_val}", "stats.json")
        accuracy = extract_accuracy(stats_file_path)

        # Append results to the result file
        with open(results_file, 'a') as f:
            f.write(f"inv: {inv_val}, bins: {bin_val}, accuracy: {accuracy}\n")

        # Rename stats.json to include hyperparameters and accuracy
        new_file_name = f"stats_inv_{inv_val}_bins_{bin_val}_acc_{accuracy}.json"
        os.rename(stats_file_path, os.path.join(base_config_path, f"{inv_val}_{bin_val}", new_file_name))

