from typing import Dict, Tuple

from dm_control.rl import control
from dm_control.suite.common import ASSETS
from dm_control.suite.hopper import Hopper, Physics
from dm_control.utils import containers

from .utils import encode_parametrized_model

_DEFAULT_TIME_LIMIT = 20  # s
_DEFAULT_UPPER_HEIGHT = 0.2  # m, doesn't include lower part
_CONTROL_TIMESTEP = 0.02  # s
SUITE = containers.TaggedTasks()


def prepare_params(env_kwargs: Dict = None) -> Dict:
    # (Param name, default value)
    env_kwargs = env_kwargs.pop("params", {})
    return {"height": env_kwargs.get("value1", 1.0) * _DEFAULT_UPPER_HEIGHT}


def get_model_and_assets(parsed_params: Dict) -> Tuple[str, Dict]:
    """Returns a tuple containing the model XML string and a dict of assets."""
    model = encode_parametrized_model(
        params=parsed_params,
        filename="hopper.xml",
        file_var="$HEIGHT",
        param_var="height",
    )
    return model, ASSETS


@SUITE.add("benchmarking_param")
def stand_param(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns a Hopper that strives to stand upright, balancing its pose."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Hopper(hopping=False, random=random)
    return control.Environment(
        physics,
        task,
        time_limit=time_limit,
        control_timestep=_CONTROL_TIMESTEP,
        **environment_kwargs
    )


@SUITE.add("benchmarking_param")
def hop_param(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns a Hopper that strives to hop forward."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Hopper(hopping=True, random=random)
    return control.Environment(
        physics,
        task,
        time_limit=time_limit,
        control_timestep=_CONTROL_TIMESTEP,
        **environment_kwargs
    )
