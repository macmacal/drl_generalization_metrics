from typing import Dict, Tuple

from dm_control.rl import control
from dm_control.suite.common import ASSETS
from dm_control.suite.manipulator import _ALL_PROPS, Bring, Physics
from dm_control.utils import containers, xml_tools
from lxml import etree

from .utils import get_parametrized_model

_DEFAULT_TIME_LIMIT = 10  # s
_DEFAULT_HIPS_GEAR = 120  # gear ratio
_CONTROL_TIMESTEP = 0.01  # s

SUITE = containers.TaggedTasks()


def prepare_params(env_kwargs: Dict = None) -> Dict:
    # (Param name, default value)
    env_kwargs = env_kwargs.pop("params", {})
    return {"hips_gear": env_kwargs.get("value1", 1.0) * _DEFAULT_HIPS_GEAR}


def get_model_and_assets(
    parsed_params: Dict, use_peg: bool, insert: bool
) -> Tuple[str, Dict]:
    """Returns a tuple containing the model XML string and a dict of assets."""
    xml_string = get_parametrized_model(
        params=parsed_params,
        filename="manipulator.xml",
        file_var="$GEAR",
        param_var="hips_gear",
    )

    parser = etree.XMLParser(remove_blank_text=True)
    mjcf = etree.XML(xml_string, parser)

    # Select the desired prop.
    if use_peg:
        required_props = ["peg", "target_peg"]
    if insert:
        required_props += ["slot"]
    else:
        required_props = ["ball", "target_ball"]
    if insert:
        required_props += ["cup"]

    # Remove unused props
    for unused_prop in _ALL_PROPS.difference(required_props):
        prop = xml_tools.find_element(mjcf, "body", unused_prop)
        prop.getparent().remove(prop)

    return etree.tostring(mjcf, pretty_print=True), ASSETS


@SUITE.add("benchmarking_param")
def bring_ball_param(
    fully_observable=True,
    time_limit=_DEFAULT_TIME_LIMIT,
    random=None,
    environment_kwargs=None,
):
    """Returns manipulator bring task with the ball prop."""
    use_peg = False
    insert = False
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)

    physics = Physics.from_xml_string(*get_model_and_assets(params, use_peg, insert))
    task = Bring(
        use_peg=use_peg, insert=insert, fully_observable=fully_observable, random=random
    )
    return control.Environment(
        physics,
        task,
        control_timestep=_CONTROL_TIMESTEP,
        time_limit=time_limit,
        **environment_kwargs
    )
