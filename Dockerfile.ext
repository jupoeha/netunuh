FROM python:3.11-slim AS build
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libc6-dev \
 && rm -rf /var/lib/apt/lists/* \
 && pip install --no-cache-dir Cython
COPY web.py /srvbuild/site/web.py
RUN cd /srvbuild/site && cp web.py _speedups.py \
 && python3 -m cython --3str _speedups.py -o _speedups.c \
 && cc -O2 -shared -fPIC $(python3-config --includes) _speedups.c \
      -o _speedups.cpython-311-x86_64-linux-gnu.so

FROM python:3.11-slim
WORKDIR /srv
COPY --from=build /srvbuild/site/_speedups*.so ./
COPY run.py .
COPY www ./www
EXPOSE 11622
CMD ["python3", "run.py"]
