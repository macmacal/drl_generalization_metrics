from typing import Dict, Tuple

from dm_control.rl import control
from dm_control.suite.cheetah import Cheetah, Physics
from dm_control.suite.common import ASSETS
from dm_control.utils import containers

from .utils import encode_parametrized_model

_DEFAULT_TIME_LIMIT = 10  # s
_DEFAULT_HALF_LENGTH = 0.5  # m
SUITE = containers.TaggedTasks()


def prepare_params(env_kwargs: Dict = None) -> Dict:
    # (Param name, default value)
    env_kwargs = env_kwargs.pop("params", {})
    return {"half_length": env_kwargs.get("value1", 1.0) * _DEFAULT_HALF_LENGTH}


def get_model_and_assets(parsed_params: Dict) -> Tuple[str, Dict]:
    """Returns a tuple containing the model XML string and a dict of assets."""
    model = encode_parametrized_model(
        params=parsed_params,
        filename="cheetah.xml",
        file_var="$LENGTH",
        param_var="half_length",
    )
    return model, ASSETS


@SUITE.add("benchmarking_param")
def run_param(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns the run task."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = Cheetah(random=random)
    return control.Environment(
        physics, task, time_limit=time_limit, **environment_kwargs
    )
