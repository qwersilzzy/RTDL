


import os




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


dir_name = 'tuned_reproduced_MHE_tune_test'




models = [
            "mlp",
            "mlp_MHE",
            "resnet",
            "resnet_MHE",
            "ft_transformer",
            "ft_transformer_MHE",
            ]

#
# for seed in range(15):
#     cmd = f"python bin/{models[3]}.py output/{datasets[2]}/{models[2]}/{dir_name}/{seed}.toml -f"
#     # cmd = f"python bin/resnet_MHE.py output/{datasets[0]}/resnet/{dir_name}/{seed}.toml -f"
#     os.system(cmd)


cmd = f"python bin/{models[3]}.py output/{datasets[2]}/{models[2]}/{dir_name}/{seed}.toml -f"





