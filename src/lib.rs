use pyo3::prelude::*;
use pyo3::exceptions::{PyRuntimeError, PyValueError};
use imgopt_native::Format;

const JPEG: &'static str = "JPEG";
const PNG: &'static str = "PNG";
const SVG: &'static str = "SVG";
const WEBP: &'static str = "WEBP";

fn string_to_format(input: &str) -> Result<Format, &'static str> {
    match input {
        JPEG => Ok(Format::Jpeg),
        PNG => Ok(Format::Png),
        SVG => Ok(Format::Svg),
        WEBP => Ok(Format::Webp),
        _ => Err("invalid format")
    }
}

#[pyfunction]
fn convert(a: &str, b: &str) -> PyResult<()> {
    match imgopt_native::convert(a, b) {
        Ok(_) => Ok(()),
        Err(e) => Err(PyRuntimeError::new_err(e.to_string()))
    }
}

#[pyfunction]
fn convert_explicit(a: (&str, &str), b: (&str, &str)) -> PyResult<()> {
    let input_format = string_to_format(a.1).map_err(PyValueError::new_err)?;
    let output_format = string_to_format(b.1).map_err(PyValueError::new_err)?;
    match imgopt_native::convert_explicit((a.0, input_format), (b.0, output_format)) {
        Ok(_) => Ok(()),
        Err(e) => Err(PyRuntimeError::new_err(e.to_string()))
    }
}

#[pymodule]
fn imgopt(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert_explicit, m)?)?;
    m.add_function(wrap_pyfunction!(convert, m)?)?;
    m.add("JPG", JPEG)?;
    m.add("JPEG", JPEG)?;
    m.add("PNG", PNG)?;
    m.add("SVG", SVG)?;
    m.add("WEBP", WEBP)?;

    Ok(())
}