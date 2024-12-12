# To run don docker

## Run on production
Command to build image

```
docker build --tag phen/api_fetch:24.06 .
```

To run the container

```
docker run --name api_fetch_phen -p 8082:8000 -d --network=net-phenotypic -e DATABASE_USERNAME=admin -e DATABASE_PASSWORD=Fantasy24 -e DATABASE=phenotypic_db -e DATABASE_HOST=mariadb_phenotypic -e DATABASE_SOCKET=3306 -e FTP_HOSTNAME=ftp_phenotypic -e FTP_PORT=21 -e FTP_USERNAME=user -e FTP_PASSWORD=ftp1221Wheat phen/api_fetch:24.05
```

## Run on dev

Create image to dev project

```
docker build --tag phen/api_fetch:dev -f Dockerfile.dev .
```

Run image in a container

```
docker run -it -d --name dev_api_fetch -p 8092:8000 --network=net-phenotypic -v ${PWD}:/develop  phen/api_fetch:00.dev
```

### About author


In collaboration with the [Universidad Autonoma del Estado de Mexico](https://www.uaemex.mx/)  and supported by [CONAHCYT](https://conahcyt.mx/) scholarships, this project was created. For new features, changes, or improvements, please reach out to:

Student, Ph.D.

Juan Carlos Moreno Sanchez

Please contact me at:

<carlos.moreno.phd@gmail.com>

<jcmorenos001@alumno.uaemex.mx>