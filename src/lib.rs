const HELP_TEXT: &'static str = r#"
Python library to convert/optimize images.
Uses Rust glue to communicate with the mozjpeg, pngquant, webp and svgcleaner. 
"#;

use imgopt_native::Format;
use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;

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
        _ => Err("invalid format"),
    }
}

#[pyfunction]
#[pyo3(text_signature = "(input, output, /)")]
/// Convert the input image to the output image. The type is based on the file extension.
/// >>> # re-encode jpg image using mozjpeg
/// >>> convert("input_image.jpg", "output_image.jpg")
/// >>> # converts the input jpg image to png
/// >>> convert("input_image.jpg", "output_image.png")
fn convert(input: &str, output: &str) -> PyResult<()> {
    match imgopt_native::convert(input, output) {
        Ok(_) => Ok(()),
        Err(e) => Err(PyRuntimeError::new_err(e.to_string())),
    }
}

#[pyfunction]
#[pyo3(text_signature = "(input, output, /)")]
/// Convert the input image to the output image. The image type is given as an argument and the file extension is ignored.
/// This can be handy if you are handling temporary files for instance (that dont have file extensions).
/// >>> convert_explicit(("input_image.jpg", imgopt.JPG), ("output_image", imgopt.WEBP))
fn convert_explicit(input: (&str, &str), output: (&str, &str)) -> PyResult<()> {
    let input_format = string_to_format(input.1).map_err(PyValueError::new_err)?;
    let output_format = string_to_format(output.1).map_err(PyValueError::new_err)?;
    match imgopt_native::convert_explicit((input.0, input_format), (output.0, output_format)) {
        Ok(_) => Ok(()),
        Err(e) => Err(PyRuntimeError::new_err(e.to_string())),
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
    m.add("__doc__", HELP_TEXT)?;

    Ok(())
}
