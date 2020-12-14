# in case we ever do any installs
# lets make them non-interactive
ARG DEBIAN_FRONTEND=noninteractive

###### stage 1 - build image with dependencies
#python image as base
FROM python:3 as base-compile-image


WORKDIR /opt/github-get


##### stage 2 - compile the code

FROM base-compile-image as compile-image

COPY . /opt/github-get
## Stage 3

FROM ubuntu:18.04 as runtime-image

ARG DEBIAN_FRONTEND=noninteractive
RUN echo "building runtime-image" && \
    apt-get update && \
    apt-get install -y libssl1.0.0 && \
    apt-get install -y netbase && \
    apt-get install -y ca-certificates

RUN mkdir -p /opt/github-get
WORKDIR /opt/github-get
ENTRYPOINT ["/opt/github-get/github-get-exe"]
COPY --from=compile-image /opt/github-get/.stack-work/dist/x86_64-linux/Cabal-3.0.1.0/build/github-get-exe/github-get-exe .
CMD [""]