### First step
```bash
git clone https://github.com/sahil7879/distributed-tracing.git
cd distributed-tracing
docker login
```

### To create images and push them to docker image 

```bash
docker build -t sahiljangra/service-a:latest ./service-a
docker build -t sahiljangra/service-b:latest ./service-b
docker build -t sahiljangra/service-c:latest ./service-c
docker push sahiljangra/service-a:latest
docker push sahiljangra/service-b:latest
docker push sahiljangra/service-c:latest
```

### to deploy all the deployment and services
```bash
kubectl apply -f deployment-jaeger.yaml
kubectl apply -f deployment-rabbitmq.yaml
kubectl apply -f deployment-service-a.yaml
kubectl apply -f deployment-service-b.yaml
kubectl apply -f deployment-service-c.yaml
kubectl apply -f extsvc-jaeger.yaml
kubectl apply -f extsvc-service-a.yaml
```
### check logs for rabbitmq if face any problem like internal server error and add the permissions and check if the problem resolves

```bash
kubectl exec -it rabbitmq-7fc95cd7b9-bp2tc -n tracing -- rabbitmqctl set_permissions -p / sahil ".*" ".*" ".*"
```
### if you want to delete all the deployment 
```bash
kubectl delete deploy jaeger -n tracing
kubectl delete deploy rabbitmq -n tracing
kubectl delete deploy service-a -n tracing
kubectl delete deploy service-b -n tracing
kubectl delete deploy service-c -n tracing
kubectl delete svc jaeger -n tracing
kubectl delete svc jaeger-ui -n tracing
kubectl delete svc rabbitmq -n tracing
kubectl delete svc service-a -n tracing
kubectl delete svc service-b -n tracing
kubectl delete svc service-c -n tracing
kubectl delete svc expose-service-a -n tracing
```
### docker command to start a container jaeger
```bash
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
```


How Each Port Works


```txt
Port		  Service		     Protocol Purpose

5775/udp	Jaeger Agent	     UDP	    Receives data from instrumented services (legacy format).
6831/udp	Jaeger Agent	     UDP	    Receives spans (Jaeger Thrift compact format).
6832/udp	Jaeger Agent	     UDP	    Receives spans (Jaeger Thrift binary format).
5778		 Jaeger Agent	     HTTP	    Provides a configuration endpoint for sampling.
16686		 Jaeger Query	     HTTP	    Web UI for querying and visualizing traces.
14268	   Jaeger Collector  HTTP	    Receives spans via HTTP (Jaeger Thrift over HTTP).
14250		 Jaeger Collector  gRPC	    Receives spans via gRPC.
9411		 Zipkin 		       HTTP	    Exposes a Zipkin-compatible API.
```

