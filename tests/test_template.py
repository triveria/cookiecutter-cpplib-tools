import json
import pathlib
import shutil
import subprocess

import cookiecutter.main
import pytest


def count(iterable):
    """ Return a count of elements in `iterable`. """
    return sum(1 for _ in iterable)


def has_build_tools() -> bool:
    """ Return whether the system has cmake and make available in PATH. """
    return all(shutil.which(program) is not None for program in ['cmake', 'make'])


def template_directory() -> pathlib.Path:
    """ Return the root directory containing cookiecutter.json. """
    return pathlib.Path(__file__).parent.parent


def parameterize_by_template_parameter(parameter_name):
    """ Return a test decorator that parameterizes its arguments over
    all values of `parameter_name`. """
    choices = _template()[parameter_name]
    parameters = [pytest.param(value, id='{}={!r}'.format(parameter_name, value))
                  for value in choices]
    return pytest.mark.parametrize(parameter_name, parameters)


def _template() -> dict:
    """ Return the cookiecutter template as a dictionary. """
    with open(template_directory() / "cookiecutter.json") as f:
        return json.load(f)


@pytest.fixture()
def cookiecutter_renderer(tmp_path: pathlib.Path):
    """ Return a function that can perform cookiecutter rendering. """
    output_dir = (tmp_path / "output")
    output_dir.mkdir()

    def render_template(**extra_context) -> pathlib.Path:
        """ Return the result of running cookiecutter with the given context. """
        return pathlib.Path(
            cookiecutter.main.cookiecutter(template=template_directory().as_posix(),
                                           no_input=True,
                                           extra_context=extra_context,
                                           output_dir=output_dir)
        )

    return render_template


# Unit tests
def test_template(cookiecutter_renderer):
    cookiecutter_renderer()


@parameterize_by_template_parameter('license')
def test_license_choices(license, cookiecutter_renderer):
    project_path = cookiecutter_renderer(license=license, unit_test_framework="None", use_sanitizers_cmake="no")
    license_path = project_path / 'LICENSE'
    if license == "Not open source":
        assert pathlib.Path(license_path).exists() == False
    else:
        with open(license_path) as license_file:
            line_count = count(license_file)
        assert line_count >= 5, "Expected non-empty LICENSE file: {}".format(license_path)


@pytest.mark.skipif(not has_build_tools(), reason='Does not have cmake and make')
@parameterize_by_template_parameter('use_boost')
def test_build(cookiecutter_renderer, use_boost):
    project_path = cookiecutter_renderer(use_boost=use_boost, unit_test_framework="None", use_sanitizers_cmake="no")
    build_dir = (project_path / "build")
    for command in ['cmake ..', 'cmake --build .', 'ctest']:
        subprocess.run(command.split(), cwd=build_dir, check=True)

@pytest.mark.skipif(not has_build_tools(), reason='Does not have cmake and make')
@parameterize_by_template_parameter('use_boost')
def test_build_with_makefile(cookiecutter_renderer, use_boost):
    project_path = cookiecutter_renderer(use_boost=use_boost, unit_test_framework="Catch2", use_sanitizers_cmake="no")
    subprocess.run(['make', 'test'], check=True, cwd=project_path)
