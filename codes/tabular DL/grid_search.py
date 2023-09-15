
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


def extract_accuracy_or_rmse(target_dir, inv, bins):
    # # Construct the full path of the statistics file
    stats_file_path = f"{target_dir}/{'inv-' + str(inv) + '-bins-' + str(bins)}/stats.json"

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

def run_command_once(model_used, target_dir, inv, bins):
    cmd = f"python bin/{model_used}.py {target_dir}/inv-{inv}-bins-{bins}.toml -f"
    try:
        output = subprocess.check_output(cmd, shell=True)
        print('bins, inv::', [inv, bins])
        return [inv, bins]
    except subprocess.CalledProcessError:
        print(f"Command failed: {cmd}")
        return None

def fetch_original_toml_file(target_dir, original_dir):
    """Fetch the contents of the original .toml file."""
    with open(original_dir, 'r') as infile:
        return infile.read()


def create_cloned_toml_inv_bins_json(target_dir, inv, bins, original_content):
    """Create a cloned .toml file with a modified filename."""
    seed_file_path = os.path.join(target_dir, f'inv-{inv}-bins-{bins}.toml')
    with open(seed_file_path, 'w') as outfile:
        outfile.write(original_content)

    # Create a cloned JSON file with the same naming convention
    json_file_path = os.path.join(target_dir, f'inv-{inv}-bins-{bins}.json')
    with open(json_file_path, 'w') as outfile:
        outfile.write(f'{{"inv": {inv}, "bins": {bins}}}')

    # Update the JSON_FILE_PATH environment variable
    os.environ['JSON_FILE_PATH'] = json_file_path

    return json_file_path

def create_log_txt(full_log_path, target_list):
    if not os.path.exists(full_log_path):
        open(full_log_path, 'x').close()
    with open(full_log_path, 'a') as f:
        for item in target_list:
            f.write(f"{item}\n")
        f.close()

def create_directory(routes, dir_name):
    # Create directories and empty file
    for route in routes:
        os.makedirs(route, exist_ok=True)
        with open(os.path.join(route, dir_name), 'w') as f:
            pass
        print(f"Created directory: {route}")

def remove_all_txt_logs(log_dir):
    pattern = '{}.txt'.format(os.path.basename(log_dir))
    files = [f for f in os.listdir(log_dir) if f.endswith('.txt') and f != pattern]
    for f in files:
        os.remove(os.path.join(log_dir, f))


def remove_all_json_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith('.json'):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error removing file {filename}: {e}")
    return None

def remove_all_toml_files(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if filename.endswith('.toml'):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error removing file {filename}: {e}")
    return None


def remove_directories(routes):
    for route in routes:
        if os.path.exists(route):
            shutil.rmtree(route)
            print(f"Removed directory: {route}")
        else:
            print(f"Directory {route} does not exist.")



if __name__ == "__main__":
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

    models_path_name = [
        "mlp",
        "resnet",
    ]

    models_origin_or_MHE = [
        "mlp",
        "mlp_MHE",
        "resnet",
        "resnet_MHE",
        "resnet_MHE_splitNum1",
    ]

    # Define hyperparameters in the given format
    inv_range = [int, 5, 20, 125]
    bins_range = [int, 50, 200, 1050]

    # inv_range = [int, 0, 10, 50]
    # bins_range = [int, 0, 0, 0]
    # Generate lists of values for each hyperparameter
    inv_values = generate_values(inv_range)
    bins_values = generate_values(bins_range)
    search_space_size = len(inv_values) * len(bins_values)
    print('inv_values, bins_values, search_space_size:::', inv_values, bins_values, search_space_size)

    # directory setup
    test_dir_name = "tuned_emb_3"
    # test_dir_name = "tuned_1"
    # test_dir_name = "tuned_test_1"
    # test_dir_name = "tuned_test_cat_1"
    original_dir_name = "tuning/0/best.toml"

    target_dir =   f"output/{datasets[7]}/{models_path_name[0]}/{test_dir_name}"
    original_dir = f"output/{datasets[7]}/{models_path_name[0]}/{original_dir_name}"
    # training model selection
    models_used = models_origin_or_MHE[1]


    # # txt file name definition for create_log_txt()
    Hyperparameters_score_log = f"Hyperparameters_score_log.txt"
    max_min_rmse_accuracy = f"max_min_rmse_accuracy.txt"


    """Fetch the contents of the original .toml file."""
    original_toml_content = fetch_original_toml_file(target_dir, original_dir)


    hyperparameter_all = []
    accuracy_or_rmse_all = []
    for inv in inv_values:
        for bins in bins_values:

            os.environ['INV'] = str(inv)
            os.environ['BINS'] = str(bins)

            json_file_path = create_cloned_toml_inv_bins_json(target_dir, inv, bins, original_toml_content)
            print('environment variable json_file_path is ::', json_file_path)

            run_command_once(models_used ,target_dir, inv, bins)

            accuracy_or_rmse = extract_accuracy_or_rmse(target_dir, inv, bins)

            # Add the hyperparameters and accuracy/RMSE value to their respective lists
            hyperparameter_all.append([inv, bins])
            accuracy_or_rmse_all.append(accuracy_or_rmse)


    # # remove all the generated .toml .json file, txt log in target_dir
    remove_all_json_files(target_dir)
    remove_all_toml_files(target_dir)
    remove_all_txt_logs(target_dir)

    print('******************json, toml and txt has been cleanup******************')
    print("Hyperparameters:", hyperparameter_all)
    print("Accuracy or RMSE:", accuracy_or_rmse_all)


    combined_list = list(zip(accuracy_or_rmse_all, hyperparameter_all))
    print('combined_list::', combined_list)


    full_log_path = os.path.join(target_dir, Hyperparameters_score_log)
    max_min_path = os.path.join(target_dir, max_min_rmse_accuracy)


    create_log_txt(full_log_path, combined_list)

    sorted_list = sorted(combined_list, key=lambda x: x[0], reverse=True)
    print('sorted_list::', sorted_list)
    max_combined_list = sorted_list[0]
    min_combined_list = sorted_list[-1]
    max_min_combined = [max_combined_list, min_combined_list]
    print('max, min, max_min::', max_combined_list, min_combined_list, max_min_combined)

    create_log_txt(max_min_path, max_min_combined)
















