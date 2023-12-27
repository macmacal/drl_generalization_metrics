from typing import Dict, Tuple

from dm_control.rl import control
from dm_control.suite.common import ASSETS
from dm_control.suite.reacher import Physics, Reacher
from dm_control.utils import containers

from .utils import encode_parametrized_model

_DEFAULT_TIME_LIMIT = 20  # s
_DEFAULT_GEAR_RATIO = 0.05  # ratio
_BIG_TARGET = 0.05  # m, tolerance size
_SMALL_TARGET = 0.015  # m, tolerance size
SUITE = containers.TaggedTasks()


def prepare_params(env_kwargs: Dict = None) -> Dict:
    # (Param name, default value)
    env_kwargs = env_kwargs.pop("params", {})
    return {"gears_ratio": env_kwargs.get("value1", 1.0) * _DEFAULT_GEAR_RATIO}


def get_model_and_assets(parsed_params: Dict) -> Tuple[str, Dict]:
    """Returns a tuple containing the model XML string and a dict of assets."""
    model = encode_parametrized_model(
        params=parsed_params,
        filename="reacher.xml",
        file_var="$GEAR",
        param_var="gears_ratio",
    )
    return model, ASSETS


@SUITE.add("benchmarking_param")
def easy_param(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns reacher with sparse reward with 5e-2 tol and randomized target."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Reacher(target_size=_BIG_TARGET, random=random)
    return control.Environment(
        physics, task, time_limit=time_limit, **environment_kwargs
    )


@SUITE.add("benchmarking_param")
def hard_param(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns reacher with sparse reward with 1e-2 tol and randomized target."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Reacher(target_size=_SMALL_TARGET, random=random)
    return control.Environment(
        physics, task, time_limit=time_limit, **environment_kwargs
    )
