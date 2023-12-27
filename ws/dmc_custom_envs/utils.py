import os
from typing import Dict

_SUITE_DIR = os.path.dirname(os.path.dirname(__file__))


def get_parametrized_model(
    params: Dict, filename: str, file_var: str, param_var: str
) -> str:
    m = get_resource(filename)
    return m.replace(file_var, str(params[param_var]))


def encode_parametrized_model(
    params: Dict, filename: str, file_var: str, param_var: str
) -> bytes:
    print(
        f"[dmc_custom_envs][DEBUG] File: {filename} | Replacing '{file_var}' with '{params[param_var]}'."
    )
    m = get_parametrized_model(params, filename, file_var, param_var)
    return m.encode("utf-8")


def get_resource(filename: str, mode="r") -> str:
    path = os.path.join(_SUITE_DIR, "dmc_custom_envs", filename)
    with open(path, mode=mode) as f:
        return f.read()


def load(
    domains,
    domain_name,
    task_name,
    task_kwargs=None,
    environment_kwargs=None,
    visualize_reward=False,
):
    return build_environment(
        domains,
        domain_name,
        task_name,
        task_kwargs,
        environment_kwargs,
        visualize_reward,
    )


def build_environment(
    domains,
    domain_name,
    task_name,
    task_kwargs=None,
    environment_kwargs=None,
    visualize_reward=False,
):
    if domain_name not in domains:
        raise ValueError(f"Domain {domain_name} does not exist!!! Domains: {domains}")

    domain = domains[domain_name]

    if task_name not in domain.SUITE:
        raise ValueError(
            f"Level {task_name} does not exist in domain {domain_name}! Tasks avaiable: {domain.SUITE}"
        )

    task_kwargs = task_kwargs or {}
    if environment_kwargs is not None:
        task_kwargs = dict(task_kwargs, environment_kwargs=environment_kwargs)
    env = domain.SUITE[task_name](**task_kwargs)
    env.task.visualize_reward = visualize_reward
    return env
