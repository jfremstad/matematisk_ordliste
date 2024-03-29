# Konvensjoner for føring av merknader

### Generelle konvensjoner

- Av tekniske grunner skrives alltid anførselstegn rundt hele merknaden.

- Alle merknader skal formuleres som helsetninger, med unntak av informasjon om
  ordklasse, synynom, uttale og genus.

- Når en engelsk term opptrer i merknad, markeres dette med kursiv. Man får
  kursiv ved å skrive

  `<i>kursivert tekst</i>`.

- Genus, altså grammatisk kjønn, føres opp i tilfeller der dette kan være
  nyttig. Spesielt føres dette alltid opp for forkortelser (av substantiv).
  Genus til en forkortelse settes til å være det samme som genus til det norske
  uttrykket som forkortes.

### Informasjon om ordklasse, synonym, uttale og genus

- Informasjon om ordklasse føres slik:

  ```
  metrikk,metrikk,metric,"Ordklasse: substantiv"
  metrisk,metrisk,metric,"Ordklasse: adjektiv"
  ```

- Synonymer oppgis kun på bokmål. Informasjon om synonym føres slik:

  ```
  største felles divisor,største felles divisor,greatest common divisor,"Synonym: største felles faktor"
  ```

  Dersom en term har flere synonymer, føres merknaden slik:

  ```
  bijeksjon,bijeksjon,bijection,"Synonym: én-entydig korrespondanse / én-til-én-korrespondanse"
  ```

- Informasjon om uttale føres slik (oppsett for føring av uttale er hentet fra
  [NAOB](https://www.naob.no/)):

  ```
  syzygi,syzygi,syzygy,"Uttale: [sytsygi:´]"
  ```

- Informasjon om genus føres slik:

  ```
  chiffer,chiffer,cipher,"Genus: intetkjønn"
  ```

  I noen tilfeller blir genus forskjellig på bokmål og nynorsk. I slike
  tilfeller skriver man:

  ```
  FSM,FSM,FSM,"Genus bokmål: hankjønn<br>Genus nynorsk: hankjønn/hunkjønn"
  ```

  Se informasjon om linjeskift nedenfor.

- Dersom en term skal ha informasjon om både ordklasse, uttale, synonym og/eller
  genus, skrives ordklasse øverst, deretter uttale, så synonym og til slutt
  genus. Det skilles mellom de ulike typene informasjon ved linjeskift. Man får
  linjeskift ved å skrive `<br>`. Eventuell ytterligere merknad føres etter en
  tom linje. Oppsettet ser altså slik ut:

  ```
  Ordklasse: adjektiv
  Synonym: et synonym til termen
  Uttale: [hvordan uttale termen]
  Genus: hankjønn

  Her kommer en uttypende forklaring (i hele setninger).
  ```

### Informasjon om forkortelser

- Informasjon om forkortelse føres slik for den forkortede termen:

  ```
  ANOVA,ANOVA,ANOVA,"ANOVA er en forkortelse for variansanalyse og stammer fra <i>analysis of variance</i>."
  ```

- Informasjon om forkortelse føres slik for den ikke-forkortede termen:
  ```
  variansanalyse,variansanalyse,analysis of variance<br>variance analysis,"Variansanalyse forkortes ofte til ANOVA."
  ```

### Andre eksempler

- Informasjon om alternativ oversettelse der alternativet ikke anses som fullt
  likeverdig føres slik:

  ```
  komplementvinkel,komplementvinkel,complementary angle,"Komplementvinkler kan også omtales som komplementære vinkler (bokmål) og komplementære vinklar (nynorsk)."
  ```

- Informasjon om alternativ oversettelse der alternativet anses som klart
  dårligere føres slik:

  ```
  rotasjon,rotasjon,curl,"Curl brukes også på norsk, men rotasjon anbefales."
  ```

- Anbefaling av oversettelse/skrivemåte der begge termene er oppført i lista
  føres slik:

  ```
  kolineær<br>kollineær,kolineær<br>kollineær,colinear<br>collinear,"Begge skrivemåtene brukes på norsk, men kolineær anbefales."
  heltallsområde<br>integritetsområde,heiltalsområde<br>integritetsområde,integral domain,"Begge oversettelsene brukes på norsk, men heltallsområde anbefales."
  prosentil,prosentil,percentile,"Både persentil og percentil forekommer i bruk på norsk, men prosentil anbefales."
  ```

- Informasjon om kontekst kan f.eks. gis slik:

  ```
  forsøksplan,forsøksplan,design,"Oversettelsen gjelder bruk i statistikk og utelukker ikke at termen kan benyttes ulikt i andre sammenhenger."
  felt,felt,field,"Merk at oversettelsen av <i>field</i> er avhengig av kontekst. Oversettelsen felt brukes for eksempel i forbindelse med vektorfelt."
  kropp,kropp,field,"Merk at oversettelsen av </i>field</i> er avhengig av kontekst. En kropp er en kommutativ ring der ethvert ikke-nullelement har en multiplikativ invers. For eksempel utgjør de reelle tall en kropp."
  ```

- I denne [oversikten](termer_med_merknad_eksempler.csv) finner man flere
  eksempler på termer med merknad. Nye oppslagsord med merknad kan gjerne legges
  til blant disse eksemplene.
