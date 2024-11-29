from flask import Flask
import pika
import time
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Tracing setup
trace_provider = TracerProvider()
jaeger_exporter = JaegerExporter(agent_host_name="jaeger-agent", agent_port=6831)
trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
app.config["OPENTELEMETRY_PROVIDER"] = trace_provider

def callback(ch, method, properties, body):
    print(f"Received task: {body}")
    time.sleep(2)  # Simulate processing time

@app.route("/service-c")
def service_c():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq', 5672, '/', credentials=pika.PlainCredentials('sahil', 'jangra')))
    channel = connection.channel()
    channel.queue_declare(queue='service-c-queue')
    channel.basic_consume(queue='service-c-queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    return "Service C is processing tasks"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
