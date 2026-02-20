# Delopgave 3: Multi-container Setup

Dette er en Flask webserver der gemmer besøgsdata i en PostgreSQL database.

## Hvad er anderledes fra delopgave 2?

- Besøgsdata gemmes i en database i stedet for i hukommelsen
- Kræver PostgreSQL database for at køre
- Data overlever genstart af containere (hvis volumes bruges korrekt)

## Din opgave

Du skal oprette en multi-container setup med Docker Compose:

1. Skriv en Dockerfile for webserveren (lignende delopgave 2)
2. Skriv en docker-compose.yml der definerer to services: web og database
3. Konfigurer networking mellem services
4. Tilføj volumes så database-data bevares
5. Start begge containere med `docker-compose up`

## Hvad er docker-compose.yml?

Docker Compose lader dig definere og køre flere containere sammen. I stedet for at starte hver container individuelt, beskriver du hele setuppet i én fil.

## Hjælpespørgsmål

**For webserver service:**
- Hvordan bygger du fra din Dockerfile?
- Hvilken port skal mappes?
- Hvilke environment variables skal webserveren bruge til at forbinde til databasen?
- Skal webserveren vente på at databasen er klar?

**For database service:**
- Hvilket PostgreSQL image skal du bruge?
- Hvilke environment variables kræver PostgreSQL?
- Hvor gemmer PostgreSQL sin data i containeren?
- Hvordan sikrer du at data bevares mellem genstarts?

**Networking:**
- Hvordan kommunikerer webserver med database?
- Hvad skal DB_HOST være sat til?

## Eksempel struktur

Din docker-compose.yml skal have denne grundstruktur:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=???
      - DB_NAME=???
      - DB_USER=???
      - DB_PASSWORD=???
    depends_on:
      - db

  db:
    image: postgres:16
    environment:
      - POSTGRES_DB=???
      - POSTGRES_USER=???
      - POSTGRES_PASSWORD=???
    volumes:
      - ???:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## Tips til Docker Compose kommandoer

```bash
# Start alle services
docker-compose up

# Start i baggrunden
docker-compose up -d

# Se logs
docker-compose logs
docker-compose logs web
docker-compose logs db

# Se kørende services
docker-compose ps

# Stop alle services
docker-compose down

# Stop og fjern volumes (sletter data!)
docker-compose down -v
```

## Test af persistence

Sådan tester du at data bevares:

1. Start services: `docker-compose up`
2. Besøg http://localhost:5000 flere gange
3. Stop services: `docker-compose down`
4. Start igen: `docker-compose up`
5. Besøgstælleren burde huske tidligere besøg!

## Forventet resultat

Når du besøger http://localhost:5000 skal du se:
- Webside med besøgstæller
- "Seneste 5 besøg" liste med timestamps
- Badge der viser "Persistent"
- Data som overlever container genstart

## Troubleshooting

**"could not connect to server: Connection refused"**
- Database er ikke startet endnu
- Vent 5-10 sekunder og prøv at reload siden
- Check at db containeren kører: `docker-compose ps`

**"database does not exist"**
- Environment variables matcher ikke mellem web og db
- Check at POSTGRES_DB matcher DB_NAME
- Check at passwords matcher

**"password authentication failed"**
- POSTGRES_USER/PASSWORD matcher ikke DB_USER/PASSWORD
- Slet volumes og start forfra: `docker-compose down -v && docker-compose up`

**Web container crasher ved opstart**
- Check logs: `docker-compose logs web`
- Mangler psycopg2-binary i requirements.txt?
- Er environment variables sat korrekt?

**Data forsvinder ved genstart**
- Har du defineret volumes korrekt?
- Bruger du `docker-compose down -v`? (det sletter volumes)
- Check volumes med: `docker volume ls`

## Vigtigt at forstå

**Environment variables:**
Webserveren og databasen skal bruge samme credentials. Hvis du sætter:
- `POSTGRES_PASSWORD=hemmelig` på db
- Så skal `DB_PASSWORD=hemmelig` på web

**Networking:**
Docker Compose opretter automatisk et netværk hvor services kan tale sammen ved navn. Derfor kan webserveren forbinde til `DB_HOST=db` (navnet på database servicen).

**Volumes:**
Uden volumes forsvinder database-data når containeren slettes. Med volumes gemmes data på host-maskinen og overlever genstart.
