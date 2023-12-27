from typing import Dict, Tuple

from dm_control.rl import control
from dm_control.suite.common import ASSETS
from dm_control.suite.swimmer import Physics, Swimmer, _make_body
from dm_control.utils import containers
from lxml import etree

from .utils import get_parametrized_model

_DEFAULT_TIME_LIMIT = 30  # s
_CONTROL_TIMESTEP = 0.03  # s
_DEFAULT_GEAR_RATIO = 5e-4  # ratio
SUITE = containers.TaggedTasks()


def prepare_params(env_kwargs: Dict = None) -> Dict:
    # (Param name, default value)
    env_kwargs = env_kwargs.pop("params", {})
    return {"gears_ratio": env_kwargs.get("value1", 1.0) * _DEFAULT_GEAR_RATIO}


def get_model_and_assets(n_joints: int, parsed_params: Dict) -> Tuple[str, Dict]:
    """Returns a tuple containing the model XML string and a dict of assets."""
    model = _make_model(n_joints, parsed_params)
    return model, ASSETS


def _make_model(n_bodies: int, parsed_params: Dict):
    """Generates an xml string defining a swimmer with `n_bodies` bodies."""
    if n_bodies < 3:
        raise ValueError("At least 3 bodies required. Received {}".format(n_bodies))
    xml_string = get_parametrized_model(
        params=parsed_params,
        filename="swimmer.xml",
        file_var="$GEAR",
        param_var="gears_ratio",
    )
    mjcf = etree.fromstring(xml_string)
    head_body = mjcf.find("./worldbody/body")
    actuator = etree.SubElement(mjcf, "actuator")
    sensor = etree.SubElement(mjcf, "sensor")

    parent = head_body
    for body_index in range(n_bodies - 1):
        site_name = "site_{}".format(body_index)
        child = _make_body(body_index=body_index)
        child.append(etree.Element("site", name=site_name))
        joint_name = "joint_{}".format(body_index)
        joint_limit = 360.0 / n_bodies
        joint_range = "{} {}".format(-joint_limit, joint_limit)
        child.append(etree.Element("joint", {"name": joint_name, "range": joint_range}))
        motor_name = "motor_{}".format(body_index)
        actuator.append(etree.Element("motor", name=motor_name, joint=joint_name))
        velocimeter_name = "velocimeter_{}".format(body_index)
        sensor.append(
            etree.Element("velocimeter", name=velocimeter_name, site=site_name)
        )
        gyro_name = "gyro_{}".format(body_index)
        sensor.append(etree.Element("gyro", name=gyro_name, site=site_name))
        parent.append(child)
        parent = child

    # Move tracking cameras further away from the swimmer according to its length.
    cameras = mjcf.findall("./worldbody/body/camera")
    scale = n_bodies / 6.0
    for cam in cameras:
        if cam.get("mode") == "trackcom":
            old_pos = cam.get("pos").split(" ")
            new_pos = " ".join([str(float(dim) * scale) for dim in old_pos])
            cam.set("pos", new_pos)

    return etree.tostring(mjcf, pretty_print=True)


def _make_swimmer(
    n_joints: int, time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None
) -> control.Environment:
    """Returns a swimmer control environment."""
    environment_kwargs = environment_kwargs or {}
    params = prepare_params(environment_kwargs)
    model_string, assets = get_model_and_assets(n_joints, params)

    physics = Physics.from_xml_string(model_string, assets=assets)
    task = Swimmer(random=random)
    return control.Environment(
        physics,
        task,
        time_limit=time_limit,
        control_timestep=_CONTROL_TIMESTEP,
        **environment_kwargs
    )


@SUITE.add("benchmarking_param")
def swimmer6_param(
    time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None
):
    """Returns a 6-link swimmer."""
    return _make_swimmer(
        6, time_limit, random=random, environment_kwargs=environment_kwargs
    )


@SUITE.add("benchmarking_param")
def swimmer15_param(
    time_limit=_DEFAULT_TIME_LIMIT, random=None, environment_kwargs=None
):
    """Returns a 15-link swimmer."""
    return _make_swimmer(
        15, time_limit, random=random, environment_kwargs=environment_kwargs
    )
