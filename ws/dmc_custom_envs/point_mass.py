from typing import Dict, Tuple

from dm_control.rl import control
from dm_control.suite.common import ASSETS
from dm_control.suite.point_mass import Physics, PointMass
from dm_control.utils import containers

from .utils import encode_parametrized_model

_DEFAULT_TIME_LIMIT = 20  # s
_DEFAULT_MASS = 0.3  # kg
SUITE = containers.TaggedTasks()


def prepare_params(env_kwargs: Dict = None) -> Dict:
    # (Param name, default value)
    env_kwargs = env_kwargs.pop("params", {})
    return {"mass": env_kwargs.get("value1", 1.0) * _DEFAULT_MASS}


def get_model_and_assets(parsed_params: Dict) -> Tuple[str, Dict]:
    """Returns a tuple containing the model XML string and a dict of assets."""
    model = encode_parametrized_model(
        params=parsed_params,
        filename="point_mass.xml",
        file_var="$MASS",
        param_var="mass",
    )
    return model, ASSETS


@SUITE.add("benchmarking_param")
def easy_param(time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None):
    """Returns the easy point_mass task."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    physics = Physics.from_xml_string(*get_model_and_assets(params))
    task = PointMass(randomize_gains=False, random=random)
    return control.Environment(
        physics, task, time_limit=time_limit, **environment_kwargs
    )
