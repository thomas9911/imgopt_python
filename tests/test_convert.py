import os

import pytest
import imgopt
from imgopt import convert, convert_explicit


def test_convert_works_jpg(tmp_path):
    path = tmp_path / "out.jpg"
    assert (
        convert(
            "tests/data/pexels-abet-llacer-919734.jpg",
            str(path),
        )
        is None
    )

    # image is written
    assert os.lstat(path).st_size > 100000


def test_convert_works_webp(tmp_path):
    path = tmp_path / "out.webp"
    assert (
        convert(
            "tests/data/pexels-abet-llacer-919734.jpg",
            str(path),
        )
        is None
    )

    # image is written
    assert os.lstat(path).st_size > 100000


def test_convert_works_png(tmp_path):
    path = tmp_path / "out.png"
    assert (
        convert(
            "tests/data/pexels-abet-llacer-919734.jpg",
            str(path),
        )
        is None
    )

    # image is written
    assert os.lstat(path).st_size > 100000


def test_convert_explicit_works_png(tmp_path):
    # set output name as jpg
    path = tmp_path / "out.jpg"
    assert (
        convert_explicit(
            ("tests/data/pexels-abet-llacer-919734.jpg", imgopt.JPEG),
            # but override it to png
            (str(path), imgopt.PNG),
        )
        is None
    )

    # image is written
    assert os.lstat(path).st_size > 100000
    with open(path, "rb") as f:
        f.read(1)
        png_header = f.read(3)

    assert b"PNG" == png_header


def test_convert_raises_on_invalid_output_format(tmp_path):
    path = tmp_path / "out.txt"
    with pytest.raises(RuntimeError, match="txt cannot be optimized"):
        convert(
            "tests/data/pexels-abet-llacer-919734.jpg",
            str(path),
        )
    with pytest.raises(FileNotFoundError):
        # file should not exist
        os.lstat(path).st_size


def test_convert_raises_on_file_not_found(tmp_path):
    path = tmp_path / "out.jpg"
    with pytest.raises(RuntimeError):
        convert(
            "tests/data/not-found.jpg",
            str(path),
        )

    with pytest.raises(FileNotFoundError):
        # file should not exist
        os.lstat(path).st_size


def test_convert_explicit_raises_on_invalid_output_format(tmp_path):
    path = tmp_path / "out.txt"
    with pytest.raises(ValueError, match="invalid format"):
        convert_explicit(
            ("tests/data/pexels-abet-llacer-919734.jpg", "txt"),
            (str(path), "png"),
        )
    with pytest.raises(FileNotFoundError):
        # file should not exist
        os.lstat(path).st_size


def test_convert_raises_on_invalid_input_type(tmp_path):
    path = tmp_path / "out.txt"
    with pytest.raises(TypeError):
        convert_explicit(123456789, str(path))


def test_convert_explicit_raises_on_invalid_input_type(tmp_path):
    path = tmp_path / "out.txt"
    with pytest.raises(TypeError):
        convert_explicit("tests/data/pexels-abet-llacer-919734.jpg", str(path))
