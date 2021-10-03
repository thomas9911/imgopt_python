import os
import random
import tempfile
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

import imgopt

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "svg", "webp"}


def new_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1000 * 1000
    app.config["UPLOAD_FOLDER"] = tempfile.gettempdir()

    def allowed_file(filename):
        return (
            "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @app.route("/", methods=["GET", "POST"])
    def upload_file():
        if request.method == "POST":
            # check if the post request has the file part
            if "file" not in request.files:
                flash("No file part")
                return redirect(request.url)
            file = request.files["file"]
            out_type = request.form["type"]
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            print(out_type)
            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = to_out_filename(file.filename, out_type)
                in_tmp_file = random_filename(file.content_type)
                out_tmp_file = random_filename(out_type)
                in_path = os.path.join(app.config["UPLOAD_FOLDER"], in_tmp_file)
                out_path = os.path.join(app.config["UPLOAD_FOLDER"], out_tmp_file)
                file.save(in_path)
                imgopt.convert(in_path, out_path)
                return redirect(
                    url_for("download_file", tmp_file=out_tmp_file, name=filename)
                )
        return """
        <!doctype html>
        <title>Optimize/convert file</title>
        <h1>Optimize/convert file</h1>
        <form method=post enctype=multipart/form-data>
            <input type=file name=file accept="{}">
            <select name="type" id="type">
                <option value="png">png</option>
                <option value="jpeg">jpeg</option>
                <option value="webp">webp</option>
                <option value="svg">svg</option>
            </select>
            <input type=submit value=Upload>
        </form>
        """.format(
            ",".join([".{}".format(x) for x in ALLOWED_EXTENSIONS])
        )

    @app.route("/uploads/<tmp_file>/<name>")
    def download_file(tmp_file, name):
        return send_from_directory(
            app.config["UPLOAD_FOLDER"], tmp_file, download_name=name
        )

    def random_filename(content_type):
        ext = content_type_to_extension(content_type)
        return "{}{}".format(random.randbytes(16).hex(), ext)

    def to_out_filename(filename, ext):
        return os.path.splitext(secure_filename(filename))[0] + "." + ext

    def content_type_to_extension(content_type):
        if content_type == "image/jpeg" or content_type == "jpeg":
            return ".jpeg"
        if content_type == "image/png" or content_type == "png":
            return ".png"
        if content_type == "image/webp" or content_type == "webp":
            return ".webp"
        if content_type == "image/svg" or content_type == "svg":
            return ".svg"

    return app
