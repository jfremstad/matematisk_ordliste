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

Vi skiller på anbefalte og tillatte termer for en oversettelse. Hovedregelen er
at det kan være maksimalt én anbefalt term per skriftspråk, og at hver
oversettelse må ha minst én anbefalt _eller_ tillatt term per skriftspråk. En
oversettelse kan ha så mange tillatte termer som ønskelig. Det vil si at

- Dersom man har flere likestilte termer på et skriftspråk skal alle føres som
  tillatte termer.
- Dersom man kun har én term på et skriftspråk skal denne føres som anbefalt.
  Eksempel:

```yaml
- anbefalt:
    engelsk: restriction
  tillatt:
    bokmål:
    - begrensning
    - restriksjon
    nynorsk:
    - avgrensing
    - restriksjon
```

Siden det kun er én engelsk oversettelse føres denne som anbefalt, imens de
likestilte norske termene må føres som tillatt siden det er flere på hvert
skriftspråk.

Hver oppføring kan i alt ha følgende felter

- **anbefalt.** for den anbefalte termen for hvert skriftspråk
- **tillatt.** for tillatte termer for hvert av skriftspråkene. Kan inneholde en
  enkeltterm eller en liste av termer.
- **ordklasse.** Ordklasse for oversettelsen.
- **bruksområde.** Informasjon om bruksområde for oversettelsen. Denne
  informasjonen legges ikke automatisk til i merknadfeltet på nettsiden, så husk
  å legge til informasjonen i merknad-feltet også.
- **merknad.** Generell merknad med informasjon om oversettelsen, utenom
  ordklasse.

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
Eksempel med bruk av ordklasse-feltet:

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

Dersom en av oversettelsene er anbefalt fremfor de andre, skal dette presiseres
ved bruk av anbefalt-feltet for den foretrukne oversettelsen; det kan også
utdypes i merknadsfeltet. Anbefalt-feltet kan ha maksimum én term per
skriftspråk. Det vil si at hvis termene er likestilt skal tillatt-feltet brukes.
Dersom det kun er én oversettelse på et skriftspråk brukes anbefalt-feltet.
Eksempel:

```yaml
- anbefalt:
    bokmål: salpunkt
    nynorsk: salpunkt
    engelsk: saddle point
  tillatt:
    bokmål: sadelpunkt
  merknad: Begge skrivemåtene brukes på bokmål, men salpunkt anbefales.
```

De spesialiserte utdypningsfeltene _ordklasse_ og _bruksområde_ føres separat
for å gjøre denne informasjonen tilgjengelig til mekanisk uthenting. Denne
informasjonen brukes av [Termportalen](https://www.termportalen.no/).

## Detaljer om føring i YAML

Er du bekymret for å føre feil? Frykt ikke. YAML-filens struktur sjekkes av
[kvalitetskontrollskriptet vårt](../skript/kvalitetssjekk_termbase.py) som
[del av den kontinuerlige integreringen på GitHub](../.github/workflows/kvalitetskontroll.yml).
Det vil si at GitHub vil flagge eventuelle formateringsfeil i oppføringer før de
har sjanse til å nå nettsiden. Denne kontrollen består av flere deler:

1. Det sjekkes at oppføringene har korrekt YAML-formatering. Termbasen skal
   arrangeres som en lang liste av oppføringer, hvor hver nye oppføring er
   markert med et `-`-symbol. Videre er YAML-formatet _innrykkssensitivt_: hver
   oppføring er indentert med to mellomrom, og hvert ytterligere nøstet felt er
   indentert med to mellomrom ekstra. Dette gjelder da spesielt anbefalt- og
   tillatt-feltene som har nøstede felter for bokmål, nynorsk og engelsk, samt
   merknad-feltet dersom inneholdet spenner me enn én linje.
2. Det sjekkes at den strukturerte dataen følger
   [termbasespesifikasjonen](../termbase_skjema.json). Det vil si at det
   kontrolleres at oppføringene kun har feltene beskrevet innledningsvis i dette
   dokumentet, og at de inneholder informasjon på den forventede formen.
   <!-- Dersom flere felter skal legges til må det også implementeres støtte for det på nettsiden, og Termportalen bør få beskjed -->
3. Det sjekkes at feltene innad i hver oppføring følger den gitte rekkefølgen.
4. Det sjekkes at det er oppført minst én term for hvert skriftspråk, og at det
   maks er én anbefalt term per skriftspråk.

## Se også

- [Våre konvensjoner](konvensjoner_merknader.md) for føring av merknader.
- Se [termbasespesifikasjonen](../termbase_skjema.json) for en maskinleselig
  teknisk spesifikasjon av termbaseformatet.
