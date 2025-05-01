IMAGE_NAME=minhvh/anti
TAG=latest

push:
	docker build --platform=linux/amd64 -t $(IMAGE_NAME):$(TAG) . && \
	docker push $(IMAGE_NAME):$(TAG)