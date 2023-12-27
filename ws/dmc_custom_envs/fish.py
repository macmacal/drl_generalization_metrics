from typing import Dict, Tuple

from dm_control.rl import control
from dm_control.suite.common import ASSETS
from dm_control.suite.fish import Physics, Swim, Upright
from dm_control.utils import containers

from .utils import encode_parametrized_model

_DEFAULT_TIME_LIMIT = 40  # s
_CONTROL_TIMESTEP = 0.04  # s
_DEFAULT_SERVO_GAIN = 3e-4  # tendon's servo proportional gain
SUITE = containers.TaggedTasks()


def prepare_params(env_kwargs: Dict = None) -> Dict:
    # (Param name, default value)
    env_kwargs = env_kwargs.pop("params", {})
    return {"servo_kp": env_kwargs.get("value1", 1.0) * _DEFAULT_SERVO_GAIN}


def get_model_and_assets(parsed_params: Dict) -> Tuple[str, Dict]:
    """Returns a tuple containing the model XML string and a dict of assets."""
    model = encode_parametrized_model(
        params=parsed_params,
        filename="fish.xml",
        file_var="$SERVO_KP",
        param_var="servo_kp",
    )
    return model, ASSETS


@SUITE.add("benchmarking_param")
def upright_param(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns the Fish Upright task."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Upright(random=random)
    return control.Environment(
        physics,
        task,
        control_timestep=_CONTROL_TIMESTEP,
        time_limit=time_limit,
        **environment_kwargs
    )


@SUITE.add("benchmarking_param")
def swim_param(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns the Fish Swim task."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Swim(random=random)
    return control.Environment(
        physics,
        task,
        control_timestep=_CONTROL_TIMESTEP,
        time_limit=time_limit,
        **environment_kwargs
    )
