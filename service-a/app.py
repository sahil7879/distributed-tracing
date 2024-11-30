from flask import Flask, request
import requests
import pika
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.pika import PikaInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# Tracing setup
trace_provider = TracerProvider()
jaeger_exporter = JaegerExporter(agent_host_name="jaeger-agent", agent_port=6831)
trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

app.config["OPENTELEMETRY_PROVIDER"] = trace_provider

# Instrument RabbitMQ
PikaInstrumentor().instrument(tracer_provider=trace_provider)

@app.route("/service-a")
def service_a():
    # Call to service-b
    try:
        response_b = requests.get("http://service-b:5001/service-b")
        status_b = response_b.text
    except Exception as e:
        status_b = f"Failed to call service-b: {e}"

    # Send message to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials=pika.PlainCredentials('sahil', 'jangra')))
    channel = connection.channel()
    channel.queue_declare(queue='service-c-queue')
    channel.basic_publish(exchange='', routing_key='service-c-queue', body='Task for service-c')
    connection.close()

    return {
        "message": "Service A processed the request",
        "service_b_status": status_b,
        "service_c_status": "Task submitted to service-c queue"
    }, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
