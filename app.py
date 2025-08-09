import os
import uuid
import threading
from flask import Flask, render_template, request, jsonify, send_file, abort
from scraper import scrape_data

app = Flask(__name__, static_folder="static", template_folder="templates")
os.makedirs("outputs", exist_ok=True)

# simple in-memory job store: { job_id: {"status":"pending/running/done/error", "result": {...}} }
JOBS = {}


def run_job(job_id, params):
    JOBS[job_id]["status"] = "running"
    success, payload = scrape_data(**params)
    if success:
        JOBS[job_id]["status"] = "done"
        JOBS[job_id]["result"] = payload
    else:
        JOBS[job_id]["status"] = "error"
        JOBS[job_id]["error"] = payload


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/scrape", methods=["POST"])
def api_scrape():
    body = request.json or {}
    url = body.get("url", "").strip()
    selector_type = body.get("selector_type", "class")
    selector_value = body.get("selector_value", "").strip()
    attr = body.get("attr") or None
    pagination = body.get("pagination") or None
    timeout = body.get("timeout", 10)

    if not url or not selector_value:
        return (
            jsonify({"ok": False, "error": "url and selector_value are required"}),
            400,
        )

    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "pending", "params": body}
    thread = threading.Thread(
        target=run_job,
        args=(
            job_id,
            {
                "url": url,
                "selector_type": selector_type,
                "selector_value": selector_value,
                "attr": attr,
                "pagination": pagination,
                "timeout": timeout,
            },
        ),
        daemon=True,
    )
    thread.start()
    return jsonify({"ok": True, "job_id": job_id})


@app.route("/api/status/<job_id>")
def api_status(job_id):
    job = JOBS.get(job_id)
    if not job:
        return jsonify({"ok": False, "error": "job not found"}), 404
    return jsonify(
        {
            "ok": True,
            "job": {
                "status": job["status"],
                **({"result": job.get("result")} if "result" in job else {}),
                **({"error": job.get("error")} if "error" in job else {}),
            },
        }
    )


@app.route("/api/download")
def api_download():
    path = request.args.get("path")
    if not path:
        return abort(400)
    if not os.path.exists(path):
        return abort(404)
    return send_file(path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
