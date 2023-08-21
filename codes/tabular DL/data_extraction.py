import os
import json

def extract_rmse_from_json(file_path):
    """Extracts the RMSE value from a given JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data["metrics"]["test"]["rmse"]

# # accuracy
# # rmse

def compute_average_rmse(rmse_values):
    """Computes the average of the given RMSE values."""
    return sum(rmse_values) / len(rmse_values)

def main():

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
    ]  # Add any other directory names here



    models = [
        "mlp",
        "mlp_MHE",
        "resnet",
        "resnet_MHE",
        "ft_transformer",
        "ft_transformer_MHE",
    ]



    last_dir = [
            "tuned_reproduced",
            "tuned_reproduced_ensemble",
            "tuned_reproduced_MHE",
            "tuned_reproduced_MHE_ensemble",
            "tuned_reproduced_MHE_2",
            "tuned_reproduced_MHE_tune_test",
            "tuned_reproduced_MHE_0",
            ]# Add any other last_dir names here


    base_path = r"E:\Personnel\Jiayi Feng\tabular-dl-revisiting-models-main\tabular-dl-revisiting-models-main\output" \
                r"\{}\{}\{}".format(datasets[10], models[0], last_dir[6])

    directories = [f"{base_path}/{i}" for i in range(15)]

    # directories = [f"{base_path}/0_4",
    #                f"{base_path}/5_9",
    #                f"{base_path}/10_14"]

    rmse_values = []

    # Iterate over directories and extract RMSE values
    for directory in directories:
        json_path = os.path.join(directory, "stats.json")
        if os.path.exists(json_path):
            rmse_values.append(extract_rmse_from_json(json_path))
        else:
            print(f"'stats.json' not found in {directory}")

    # Calculate average RMSE value
    average_rmse = compute_average_rmse(rmse_values)

    # Store RMSE values in a separate file within base_path with the averaged value in its name
    rmse_output_path = os.path.join(base_path.format(""), f"test_values_averaged_{average_rmse}.txt")
    with open(rmse_output_path, "w") as file:
        for rmse in rmse_values:
            file.write(f"{rmse}\n")
        # file.write(f"\nAverage RMSE: {average_rmse}\n")
        file.write(f"{average_rmse}\n")

    print(f"Average RMSE: {average_rmse}")
    print(f"Extracted {len(rmse_values)} RMSE values. Stored in {rmse_output_path}")


if __name__ == "__main__":
    main()

