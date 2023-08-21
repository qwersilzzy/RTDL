#
# import os
# import shutil
# dir_name = 'tuned_reproduced_MHE_tune_test'
# models = [
#             "mlp",
#             "mlp_MHE",
#             "resnet",
#             "resnet_MHE",
#             "ft_transformer",
#             "ft_transformer_MHE",
#             ]
#
# routes = [
#     f'output/adult/{models[0]}/{dir_name}/',
#     f'output/aloi/{models[0]}/{dir_name}/',
#     f'output/california_housing/{models[0]}/{dir_name}/',
#     f'output/covtype/{models[0]}/{dir_name}/',
#     f'output/epsilon/{models[0]}/{dir_name}/',
#     f'output/helena/{models[0]}/{dir_name}/',
#     f'output/higgs_small/{models[0]}/{dir_name}/',
#     f'output/jannis/{models[0]}/{dir_name}/',
#     f'output/microsoft/{models[0]}/{dir_name}/',
#     f'output/yahoo/{models[0]}/{dir_name}/',
#     f'output/year/{models[0]}/{dir_name}/',
#     # ... add other routes as needed
# ]
import os
import shutil

# Directory name variable
dir_name = 'tuned_reproduced_MHE_tune_test'

# Models array
models = [
    "mlp",
    "mlp_MHE",
    "resnet",
    "resnet_MHE",
    "ft_transformer",
    "ft_transformer_MHE",
]

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

# Generate routes using nested list comprehensions
routes = [f'output/{datasets[1]}/{models[2]}/{dir_name}/']

#
# ###############################
# # Remove directories
# for route in routes:
#     if os.path.exists(route):
#         shutil.rmtree(route)
#         print(f"Removed directory: {route}")
#     else:
#         print(f"Directory {route} does not exist.")
# ###############################

# Create directories and empty file
for route in routes:
    os.makedirs(route, exist_ok=True)
    with open(os.path.join(route, dir_name), 'w') as f:
        pass


# Populate .toml files for each seed
for route in routes:
    # Modify route to point to the directory containing the original .toml file
    base_route = os.path.dirname(os.path.dirname(route))
    original_toml_path = os.path.join(base_route, 'tuning/0/best.toml')

    # Get the content of the original .toml file
    with open(original_toml_path, 'r') as infile:
        original_content = infile.read()

    # Populate the seed .toml files with the modified content
    for seed in range(15):
        seed_file_path = os.path.join(route, f'{seed}.toml')
        with open(seed_file_path, 'w') as outfile:
            content = original_content.replace('seed = 0', f'seed = {seed}')
            outfile.write(content)






