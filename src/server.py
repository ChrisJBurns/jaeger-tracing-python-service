from flask import jsonify, make_response, Flask
import requests
import os
import logging

from opentelemetry import trace
from opentelemetry.exporter.jaeger import JaegerSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

# SpanExporter receives the spans and send them to the target location.
exporter = JaegerSpanExporter(
    service_name=os.getenv('OTEL_JAEGER_SERVICE_NAME', "python-service"),
    agent_host_name=os.getenv('OTEL_JAEGER_AGENT_HOST', "localhost"),
    agent_port=6831
)

span_processor = BatchExportSpanProcessor(exporter)
trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(span_processor)

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route("/get-salary-grade/<occupation>")
def getSalaryGrade(occupation):
    print("request recieved")
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("salary-grade-lookup"):
        if occupation == "Lead Software Engineer":
            return jsonify(paygrade="A1")
        if occupation == "Senior Software Engineer":
            return jsonify(paygrade="A2")
        if occupation == "Junior Software Engineer":
            return jsonify(paygrade="A3")
        if occupation == "Graduate Software Engineer":
            return jsonify(paygrade="A4") 
        return make_response(jsonify(message="grade not found"), 404)
        
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8092)
