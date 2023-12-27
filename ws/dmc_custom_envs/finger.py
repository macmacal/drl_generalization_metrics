from typing import Dict, Tuple

from dm_control.rl import control
from dm_control.suite.common import ASSETS
from dm_control.suite.finger import Physics, Spin, Turn
from dm_control.utils import containers

from .utils import encode_parametrized_model

_DEFAULT_TIME_LIMIT = 20  # s
_CONTROL_TIMESTEP = 0.02  # s
_DEFAULT_DAMPING = 2.5  # damping ratio
# For TURN tasks, the 'tip' geom needs to enter a spherical target of sizes:
_EASY_TARGET_SIZE = 0.07
_HARD_TARGET_SIZE = 0.03

SUITE = containers.TaggedTasks()


def prepare_params(env_kwargs: Dict = None) -> Dict:
    # (Param name, default value)
    env_kwargs = env_kwargs.pop("params", {})
    return {"damping": env_kwargs.get("value1", 1.0) * _DEFAULT_DAMPING}


def get_model_and_assets(parsed_params: Dict) -> Tuple[str, Dict]:
    """Returns a tuple containing the model XML string and a dict of assets."""
    model = encode_parametrized_model(
        params=parsed_params,
        filename="finger.xml",
        file_var="$DAMPING",
        param_var="damping",
    )
    return model, ASSETS


@SUITE.add("benchmarking_param")
def spin_param(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns the Spin task."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Spin(random=random)
    return control.Environment(
        physics,
        task,
        time_limit=time_limit,
        control_timestep=_CONTROL_TIMESTEP,
        **environment_kwargs
    )


@SUITE.add("benchmarking_param")
def turn_easy_param(
    time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None
):
    """Returns the easy Turn task."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Turn(target_radius=_EASY_TARGET_SIZE, random=random)
    return control.Environment(
        physics,
        task,
        time_limit=time_limit,
        control_timestep=_CONTROL_TIMESTEP,
        **environment_kwargs
    )


@SUITE.add("benchmarking_param")
def turn_hard_param(
    time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None
):
    """Returns the hard Turn task."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Turn(target_radius=_HARD_TARGET_SIZE, random=random)
    return control.Environment(
        physics,
        task,
        time_limit=time_limit,
        control_timestep=_CONTROL_TIMESTEP,
        **environment_kwargs
    )
