from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = Flask(__name__)
metrics = PrometheusMetrics(app)

trace_exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
provider = TracerProvider()
processor = BatchSpanProcessor(trace_exporter)
provider.add_span_processor(processor)

FlaskInstrumentor().instrument_app(app)

@app.route("/")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)
