
# H1

```shell script
docker build -t test-bot:0.1 .
```

```shell script
docker run \
--name yandex-bot-test \
-e TZ=Europe/Moscow \
--shm-size="1g" -d \
--restart=always \
-v /home/www/logs:/root/logs/ \
--network host \
test-bot:0.1
```

```shell script
docker logs --tail 50 --follow --timestamps yandex-bot-test
```

```shell script
docker exec -it yandex-bot-test /bin/bash
```

```shell script
docker rm $(docker ps -aq)
```

```shell script
docker rmi $(docker images -aq)
```