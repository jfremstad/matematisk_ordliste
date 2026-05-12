# Oppsett for oppføring av termer

Oppslagstermer føres i [termbasen](../termbase.yaml) på et strukturert
dataformat ved hjelp av språket [YAML](https://yaml.org/). En enkel oppføring
kan se slik ut:

```yaml
- anbefalt:
    bokmål: basiselement
    nynorsk: basiselement
    engelsk: basis element
  merknad: De engelske termene <i>base</i> og <i>basis</i> brukes ikke helt synonymt. For eksempel vil <i>base</i> foretrekkes i topologi, mens <i>basis</i> brukes i lineær algebra. Merk at begge oversettes til basis på norsk.
```

Her er det ført opp én anbefalt term for hvert skriftspråk, samt en merknad med
utdypende informasjon om begrepet.

Hver oppføring kan ha feltene

- **anbefalt:** for den anbefalte termen for hvert skriftspråk
- **tillatt:** for tillatte termer for hvert av skriftspråkene. Dersom det er
  flere termer som alle skal likestilles, føres de alle som tillatte termer for
  det gitte skriftspråket
- **ordklasse**
- **bruksområde**
- **merknad** Generell merknad med all ytterligere informasjon.

Feltene skal forekomme i denne rekkefølgen dersom de er til stede. Alle feltene
er valgfrie, men det skal forekomme minst én anbefalt eller tillatt term per
skriftspråk. For eksempel føres synonyme og likestilte oversettelser slik (i
alfabetisk rekkefølge):

```yaml
- tillatt:
    bokmål:
    - på
    - surjektiv
    nynorsk:
    - på
    - surjektiv
    engelsk:
    - onto
    - surjective
- tillatt:
    bokmål:
    - variansanalyse
    - ANOVA
    nynorsk:
    - variansanalyse
    - ANOVA
    engelsk:
    - analysis of variance
    - variance analysis
    - ANOVA
  merknad: Variansanalyse forkortes ofte til ANOVA, som stammer fra <i>analysis of variance</i>.
```

Termer med mer enn én gyldig oversettelse med _ulik betydning_ føres opp som to
ulike oppslag. Informasjon om forskjellen mellom oversettelsene bør som
hovedregel legges inn som merknad eller i et av de andre spesialiserte feltene.
Eksempel med bruk av "ordklasse"-feltet:

```yaml
- anbefalt:
    bokmål: algebraisk
    nynorsk: algebraisk
    engelsk: algebraic
  ordklasse: adjektiv
- anbefalt:
    bokmål: algebraisk
    nynorsk: algebraisk
    engelsk: algebraically
  ordklasse: adverb
```

Dersom én av oversettelsene er anbefalt fremfor de andre, skal dette presiseres
ved bruk av "anbefalt"-feltet for den foretrukne oversettelsen. Det kan også
utdypes i merknadsfeltet. "Anbefalt"-feltet kan ha maksimum én term per
skriftspråk. Det vil si at hvis termene er likestilt skal feltet "tillatt"
brukes. Dersom det kun er én oversettelse på et skriftspråk brukes
"anbefalt"-feltet som en hovedregel. Eksempel:

```yaml
- anbefalt:
    bokmål: salpunkt
    nynorsk: salpunkt
    engelsk: saddle point
  tillatt:
    bokmål: sadelpunkt
  merknad: Begge skrivemåtene brukes på bokmål, men salpunkt anbefales.
```

De spesialiserte utdypningsfeltene "ordklasse" og "bruksområde" føres separat
for å gjøre denne informasjonen tilgjengelig til mekanisk uthenting. Denne
informasjonen brukes av [Termportalen](https://www.termportalen.no/).

## Detaljer om føring i YAML

YAML-filens struktur sjekkes av
[kvalitetskontrollskriptet vårt](../skript/kvalitetssjekk_termbase.py) som
[del av den kontinuerlige integreringen på GitHub](../.github/workflows/kvalitetskontroll.yml).
Det vil si at GitHub vil flagge eventuelle formateringsfeil i oppføringer før de
har sjanse til å nå nettsiden. Denne kontrollen består av flere deler:

1. Det sjekkes at oppføringene har korrekt YAML-formatering. Merk at hele
   termbasen er arrangert som en lang liste av oppføringer, som hver skal starte
   med et `-`-symbol. I tillegg er YAML-formatet _indenteringssensitivt_. Hver
   oppføring er indentert med to mellomrom, og hvert ytterligere nøstet felt er
   indentert med to mellomrom ekstra. Dette gjelder "anbefalt"- og
   "tillatt"-feltene, samt om "merknad"-feltet består av mer enn én linje.
2. Det sjekkes at den strukturerte dataen følger
   [termbasespesifikasjonen](../termbase_skjema.json). Det vil si at det
   kontrolleres at oppføringene kun har feltene som var beskrevet
   innledningsvis.
   <!-- Dersom flere felter skal legges til må det også implementeres støtte for det på nettsiden, og Termportalen bør få beskjed -->
3. Det sjekkes at feltene innad i hver oppføring følger rekkefølgen gitt innledningsvis.

## Se også

- [Våre konvensjoner](konvensjoner_merknader.md) for føring av merknader.
- Se [termbasespesifikasjonen](../termbase_skjema.json) for en maskinleselig
  teknisk spesifikasjon av termbaseformatet.
