docker run -d --name jaeger `
-e COLLECTOR_ZIPKIN_HTTP_PORT=9411 `
-p 5775:5775/udp `
-p 6831:6831/udp `
-p 6832:6832/udp `
-p 5778:5778 `
-p 16686:16686 `
-p 14268:14268 `
-p 14250:14250 `
-p 9411:9411 `
rancher/jaegertracing-all-in-one:1.20.0



How Each Port Works
Port		Service		   Protocol Purpose
5775/udp	Jaeger Agent	   UDP	    Receives data from instrumented services (legacy format).
6831/udp	Jaeger Agent	   UDP	    Receives spans (Jaeger Thrift compact format).
6832/udp	Jaeger Agent	   UDP	    Receives spans (Jaeger Thrift binary format).
5778		Jaeger Agent	   HTTP	    Provides a configuration endpoint for sampling.
16686		Jaeger Query	   HTTP	    Web UI for querying and visualizing traces.
14268		Jaeger Collector   HTTP	    Receives spans via HTTP (Jaeger Thrift over HTTP).
14250		Jaeger Collector   gRPC	    Receives spans via gRPC.
9411		Zipkin 		   HTTP	    Exposes a Zipkin-compatible API.


http://localhost:16686/

kubectl port-forward svc/service-a 5000:5000 -n tracing
kubectl port-forward svc/jaeger 16686:16686 -n tracing
