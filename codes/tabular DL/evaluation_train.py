
import os
import shutil
import json
import subprocess


def extract_accuracy_or_rmse(stats_file_path):

    # Open the statistics file and extract the accuracy or RMSE
    with open(stats_file_path, 'r') as f:
        stats = json.load(f)
        # Check if accuracy or RMSE was detected
        if stats["metrics"]["test"].get("accuracy") or stats["metrics"]["test"].get("rmse"):
            if stats["metrics"]["test"].get("accuracy"):
                accuracy_or_rmse = stats["metrics"]["test"]["accuracy"]
                print('current accuracy::', accuracy_or_rmse)
            else:
                accuracy_or_rmse = stats["metrics"]["test"]["rmse"]
                print('current rmse::', accuracy_or_rmse)

            return accuracy_or_rmse
        else:
            accuracy_or_rmse = None
            print("neither accuracy nor rmse found in:::", stats_file_path)
            return None

if __name__ == "__main__":

# Datasets array
    datasets = [
    "adult",
    "aloi",
    "california_housing",
    "covtype",
    "epsilon",
    "helena",
    "higgs_small",
    "jannis",
    "microsoft",
    "yahoo",
    "year"
]


# Models array
    models = [
    "mlp",
    "mlp_MHE",
    "resnet",
    "resnet_MHE",
    "ft_transformer",
    "ft_transformer_MHE",
]

# Directory name variable
    dir_name = 'seed_test'
#     dir_name = 'tuned'
# Generate routes using nested list comprehensions
    routes = f'output/{datasets[5]}/{models[2]}/{dir_name}'
    accuracy_or_rmse_all = []

# Loop through the seed values 0 to 14
    for seed in range(15):
        config_file = f"{routes}/{seed}.toml"
        # "resnet_MHE_splitNum1",
        subprocess.run(["python", "bin/resnet_MHE_splitNum1.py", config_file])
        # "resnet_MHE_splitNum1",
        config_file_folder =f"{routes}/{seed}/stats.json"
        accuracy_or_rmse = extract_accuracy_or_rmse(config_file_folder)
        print('current accuracy_or_rmse::',accuracy_or_rmse)
        accuracy_or_rmse_all.append(accuracy_or_rmse)
    # print('current accuracy_or_rmse_all list::', accuracy_or_rmse_all)

    sorted_accuracy_or_rmse_all = sorted(accuracy_or_rmse_all, reverse=True)
    max_combined_list = sorted_accuracy_or_rmse_all[0]
    min_combined_list = sorted_accuracy_or_rmse_all[-1]
    max_min_combined = [max_combined_list, min_combined_list]
    print('max, min, max_min::', max_combined_list, min_combined_list, max_min_combined)









