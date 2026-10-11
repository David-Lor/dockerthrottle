# dockerthrottle

throttle docker containers cpu usage, based on the temperature.

- this may run in the host or as a docker container, mounting the docker.sock.
- everything is configured in the [settings file](settings.template.yaml).
- when the `temperature.limit` is surpassed, the cpu-limit of the `containers` is set with the command `docker update --cpus="$LIMIT" "$CONTAINER"`.
- each one of `containers` is evaluated against the currently running containers, using [fnmatch](https://docs.python.org/es/3.9/library/fnmatch.html).
- the temperature evaluation and cpu-limit applying is done in a loop, with an interval of `temperature.delay` seconds.
- the cpu-limit is reduced by the `cpu_limit.step` for each loop, until reaching the `cpu_limit.min_cores`.
- when the `temperature.limit` is not surpassed, the cpu-limit is increased by the `cpu_limit.step` for each loop, until reaching the `cpu_limit.max_cores`.
- when the app starts or exits, the cpu-limit of the `containers` is set to `cpu_limit.max_cores`.
- if `cpu_limit.max_cores` is not set or 0, the value is auto-detected as the number of cores in the host.

## Usage

```bash
# build the image
docker build . -t local/cputhrottle:latest

# create & edit your settings
cp settings.template.yaml settings.yaml

# run container
docker run -d --name=cputhrottle \
  -v $(pwd)/settings.yaml:/app/settings.yaml \
  -v /var/run/docker.sock:/var/run/docker.sock \
  local/cputhrottle:latest
```
