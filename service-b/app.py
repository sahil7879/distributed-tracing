from flask import Flask
import sqlite3
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

# Initialize database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, name TEXT)')
cursor.execute('INSERT INTO data (name) VALUES ("Sample Data")')
conn.commit()
conn.close()

@app.route("/service-b")
def service_b():
    # Query the database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data')
    result = cursor.fetchall()
    conn.close()
    return {"data": result}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
