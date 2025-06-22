# -*- coding: utf-8 -*-
"""
Created on Sat Jun 21 00:26:01 2025

@author: 派渡明
"""

import os
import uuid
from flask import Flask, request, render_template, send_file, redirect, url_for
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = request.form.get("api_key")
        num_slides = request.form.get("num_slides")
        file = request.files["pdf_file"]

        if not (api_key and num_slides and file):
            return "Missing required input."

        # Save PDF
        pdf_filename = f"{uuid.uuid4().hex}.pdf"
        pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
        file.save(pdf_path)

        # Generate PowerPoint
        try:
            result = subprocess.run(
                [
                    "python", "pdf2ppt.py",
                    api_key, pdf_path, num_slides
                ],
                capture_output=True,
                text=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            return f"<pre>Error:\n{e.stderr}</pre>"

        pptx_filename = os.path.splitext(os.path.basename(pdf_filename))[0] + "_summary.pptx"
        pptx_path = os.path.join(".", pptx_filename)
        if not os.path.exists(pptx_path):
            pptx_path = os.path.join("output", pptx_filename)  # if your script saves there

        return send_file(pptx_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run()

