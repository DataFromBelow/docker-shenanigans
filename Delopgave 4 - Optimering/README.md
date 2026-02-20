# Delopgave 4: Optimering

Denne mappe indeholder en webserver med en uoptimeret Dockerfile.

## Opgave

Jeres opgave er at optimere Dockerfile'en. Den nuværende version virker, men har flere problemer:

- Stor image størrelse
- Unødvendige pakker installeret
- Ineffektiv layer caching
- Sikkerhedsproblemer
- Manglende monitoring

## Workflow

1. Byg den nuværende Dockerfile og noter image størrelsen
2. Identificer problemer og mulige forbedringer
3. Optimer Dockerfile'en
4. Sammenlign før og efter
5. Dokumentér dine ændringer

## Områder at undersøge

**Base image valg**
Overvej om `python:3.11` er den bedste løsning. Undersøg alternativer som slim eller alpine varianter.

**Dependencies**
Gennemgå hvilke pakker der reelt er nødvendige for at køre applikationen.

**Build optimization**
Tænk over rækkefølgen af instruktioner i Dockerfile. Hvilke ændringer trigger rebuild af hvilke lag?

**Sikkerhed**
Overvej hvilken bruger containeren kører som, og om det er nødvendigt.

**Monitoring**
Undersøg hvordan Docker kan verificere om containeren er sund.

**.dockerignore**
Undersøg om der er filer der ikke bør inkluderes i image.

## Ressourcer

- Docker dokumentation: https://docs.docker.com/
- Docker best practices: https://docs.docker.com/develop/dev-best-practices/
- Python Docker images: https://hub.docker.com/_/python

## Aflevering

Jeres optimerede løsning skal indeholde:

- Optimeret Dockerfile
- .dockerignore fil (hvis relevant)
- Dokumentation i README der beskriver:
  - Hvad I ændrede
  - Image størrelse før og efter
  - Begrundelse for jeres valg
