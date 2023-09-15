import os
import subprocess
import toml
import json
import shutil

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

def extract_accuracy_or_rmse(stats_file_path):
    with open(stats_file_path, 'r') as f:
        stats = json.load(f)
        if stats["metrics"]["test"]["rmse"] is None:
            return stats["metrics"]["test"]["accuracy"]
        else:
            return stats["metrics"]["test"]["rmse"]



def remove_directories(routes):
    for route in routes:
        if os.path.exists(route):
            shutil.rmtree(route)
            print(f"Removed directory: {route}")
        else:
            print(f"Directory {route} does not exist.")

def clone_toml_file(target_dir, dir_name,original_dir, inv_length, bins_length, inv, bins):
    # Create directories and empty file
    for route in target_dir:
        os.makedirs(route, exist_ok=True)
        with open(os.path.join(route, dir_name), 'w') as f:
            pass

    # Populate .toml files for each seed
    for route in target_dir:
        # Modify route to point to the directory containing the original .toml file
        base_route = os.path.dirname(os.path.dirname(route))
        original_toml_path = os.path.join(base_route, f'{original_dir}/best.toml')

        # Get the content of the original .toml file
        with open(original_toml_path, 'r') as infile:
            original_content = infile.read()

        # Populate the seed .toml files with the modified content
        for seed in range(inv_length*bins_length):
            seed_file_path = os.path.join(route, f'inv-{inv}-bins-{bins}.toml')
            with open(seed_file_path, 'w') as outfile:
                content = original_content.replicate()
                outfile.write(content)

# def grid_search(inv_values, bins_values, base_config_path):
#     results = {}
#     for inv_val in inv_values:
#         for bin_val in bins_values:
#             cmd = f"python bin/resnet_MHE.py {base_config_path}california_housing.toml"
#             stats_file_path = os.path.join(base_config_path, f"{inv_val}_{bin_val}", "stats.json")
#             accuracy_or_rmse = extract_accuracy_or_rmse(stats_file_path)
#             results[(inv_val, bin_val)] = accuracy_or_rmse
#     return results


def save_results_to_file(results, results_file):
    with open(results_file, 'a') as f:
        for (inv_val, bin_val), accuracy in results.items():
            f.write(f"inv: {inv_val}, bins: {bin_val}, accuracy: {accuracy}\n")

def rename_stats_file(results, base_config_path):
    for (inv_val, bin_val), accuracy in results.items():
        stats_file_path = os.path.join(base_config_path, f"{inv_val}_{bin_val}", "stats.json")
        new_file_name = f"stats_inv_{inv_val}_bins_{bin_val}_acc_{accuracy}.json"
        os.rename(stats_file_path, os.path.join(base_config_path, f"{inv_val}_{bin_val}", new_file_name))


def main():
    # Define hyperparameters in the given format
    inv_range = [int, 2, 1, 3]
    bins_range = [int, 5, 5, 10]

    # Generate lists of values for each hyperparameter
    inv_values = generate_values(inv_range)
    bins_values = generate_values(bins_range)

    # Base path to the configuration file
    base_config_path = "output/california_housing/resnet/tuned_test_0/"
    #
    # # Define a result file to store hyperparameter and accuracy combinations
    # results_file = "results.txt"
    #
    # # Perform grid search
    # results = grid_search(inv_values, bins_values, base_config_path)
    #
    # # Save results to a file
    # save_results_to_file(results, results_file)
    #
    # # Rename stats.json files
    # rename_stats_file(results, base_config_path)
    #
    # # Save overall results to a JSON file
    # with open("grid_search_results.json", "w") as f:
    #     json.dump(results, f)


    for inv_val in inv_values:
        for bin_val in bins_values:
            cmd = f"python bin/resnet_MHE.py {base_config_path}california_housing.toml"



    # dir_name = 'tuned_test_0'
    # base_config_path = f"output/{datasets[2]}/{models[2]}/{dir_name}"
    # cmd = f"python bin/{models[3]}.py {base_config_path}/california_housing.toml"
    # cmd = f"python bin/resnet_MHE.py output/california_housing/resnet/tuned_test_0/california_housing.toml"
    # os.system(cmd)


# shared_inv_bins = {{}, {}}


# shared_inv_bins = {"inv": {}, "bins": {}}
shared_inv_bins = [{}, {}]

shared_inv_bins = {"bins": [], "inv": []}