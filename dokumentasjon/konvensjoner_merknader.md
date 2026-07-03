# Konvensjoner for føring av merknader

### Generelle konvensjoner

- Alle merknader skal formuleres som helsetninger med unntak av informasjon om
  uttale, flertallsform og genus.

- Når en engelsk term opptrer i en merknad, markeres dette med kursiv. Man fører
  i kursiv ved å skrive `<i>kursivert tekst</i>`.

- Genus, altså grammatisk kjønn, føres opp i tilfeller der dette kan være
  nyttig. Spesielt føres dette alltid opp for forkortelser (av substantiv).
  Genus til en forkortelse settes til å være det samme som genus til det norske
  uttrykket som forkortes.

### Informasjon om ordklasse, bruksområde, synonym, uttale og genus

- Ordklasse føres kun i det strukturerte `ordklasse`-feltet, ikke i `merknad`.

- Bruksområde føres både i det strukturerte `bruksområde`-feltet og som
  helsetning i `merknad`. Feltet `bruksområde` gjør informasjonen maskinlesbar
  for Termportalen, mens merknaden sørger for at samme informasjon vises på
  nettsiden og kan formuleres med nødvendig presisering. Eksempel:

  ```yaml
  - anbefalt:
      bokmål: midtpunkt
      nynorsk: midtpunkt
      engelsk: midrange
    ordklasse: substantiv
    bruksområde: statistikk
    merknad: Oversettelsen gjelder bruk i statistikk og utelukker ikke at termen kan benyttes ulikt i andre sammenhenger.
  ```

- Synonymer føres opp under samme oppføring. Eksempel:

  ```yaml
  - tillatt:
      bokmål:
      - største felles divisor
      - største felles faktor
      nynorsk:
      - største felles divisor
      - største felles faktor
      engelsk:
      - greatest common divisor
      - greatest common factor
  ```

- Informasjon om uttale føres slik (oppsett for føring av uttale er hentet fra
  [NAOB](https://naob.no/uttale-veiledning)):

  ```yaml
  - anbefalt:
      bokmål: syzygi
      nynorsk: syzygi
      engelsk: syzygy
    merknad: 'Uttale: [sytsygi:´]'
  ```

  > **Obs!** Merknader som inneholder et kolontegn (`:`) må skrives i gåse-
  > eller hermetegn (`'...'` eller `"..."`), eller i flerlinjemodus (startes med
  > `|`).

  Uttale for deltermer kan føres i helsetningsform:

  ```yaml
  - anbefalt:
      bokmål: chiffertekst
      nynorsk: chiffertekst
      engelsk: ciphertext
    merknad: Chiffer uttales [ʃi´f:ər].
  ```

  Eller på formen:

  ```yaml
  - anbefalt:
      engelsk: rigour
    tillatt:
      bokmål:
      - rigor
      - rigorøsitet
      - stringens
      nynorsk:
      - rigor
      - rigorøsitet
      - stringens
    ordklasse: substantiv
    merknad: 'Uttale for rigor: [ri:´går]'
  ```

- Informasjon om genus føres slik:

  ```yaml
  - anbefalt:
      bokmål: topos
      nynorsk: topos
      engelsk: topos
    merknad: 'Genus: hankjønn'
  ```

  I noen tilfeller blir genus forskjellig på bokmål og nynorsk. I slike
  tilfeller gjøres det tydelig forskjell, for eksempel med
  helsetningsforklaring:

  ```yaml
  - tillatt:
      bokmål:
      - endelig tilstandsautomat
      - endelig tilstandsmaskin
      - FSM
      - FSA
      nynorsk:
      - endeleg tilstandsautomat
      - endeleg tilstandsmaskin
      - FSM
      - FSA
      engelsk:
      - finite-state automaton
      - finite-state machine
      - FSM
      - FSA
    merknad: FSM er en forkortelse for endelig tilstandsmaskin (bokmål) og endeleg tilstandsmaskin
      (nynorsk) og stammer fra <i>finite-state machine</i>. FSA er en forkortelse for endelig
      tilstandsautomat (bokmål) og endeleg tilstandsautomat (nynorsk) og stammer fra <i>finite-state
      automaton</i>. Forkortelsen FSM har hankjønn på bokmål og både hankjønn og hunkjønn på nynorsk.
      Forkortelsen FSA har hankjønn på bokmål og nynorsk.
  ```

- Dersom en term inneholder informasjon om flere av følgende: uttale, genus,
  flertallsform, og bruksområde, så føres det i denne rekkefølgen. Det skilles
  mellom de ulike typene informasjon ved linjeskift. Man får linjeskift ved å
  starte merknadsfeltet med et `|`-symbol, og deretter føre merknaden med
  vanlige linjeskift startende på neste linje med ett ekstra nivå av innrykk.
  Oppsettet ser altså slik ut:

  ```yaml
  - anbefalt:
      bokmål: entydig faktoriseringsområde
      nynorsk: eintydig faktoriseringsområde
      engelsk: unique factorization domain
    tillatt:
      bokmål: UFD
      nynorsk: UFD
      engelsk: UFD
    ordklasse: substantiv
    merknad: |
      Genus: intetkjønn

      UFD er en forkortelse for entydig faktoriseringsområde (bokmål) og eintydig faktoriseringsområde (nynorsk) og stammer fra <i>unique factorization domain</i>.
  ```

  Symbolet `|` forteller YAML at linjeskift innad i tekstfeltet skal bevares.

### Informasjon om forkortelser

Informasjon om forkortelse føres slik:

```yaml
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

Merk at begge termer føres opp under samme oppføring. Ettersom begge termene er
likestilte i dette tilfellet, føres de som likestilte under `tillatt`.

### Andre eksempler

- Informasjon om alternativ oversettelse der alternativet ikke anses som fullt
  likeverdig føres slik:

  ```yaml
  - anbefalt:
      bokmål: komplementvinkel
      nynorsk: komplementvinkel
      engelsk: complementary angle
    tillatt:
      bokmål: komplementær vinkel
      nynorsk: komplementær vinkel
    merknad: Komplementvinkler kan også omtales som komplementære vinkler (bokmål) og komplementære vinklar (nynorsk).
  ```

- Informasjon om alternativ oversettelse der alternativet anses som klart
  dårligere føres slik:

  ```yaml
  - anbefalt:
      bokmål: rotasjon
      nynorsk: rotasjon
      engelsk: curl
    tillatt:
      bokmål: curl
      nynorsk: curl
    merknad: Curl brukes også på norsk, men rotasjon anbefales.
  ```

- Anbefaling av oversettelse/skrivemåte der begge termene er oppført i lista
  føres slik:

  ```yaml
  - anbefalt:
      bokmål: kolineær
      nynorsk: kolineær
    tillatt:
      bokmål: kollineær
      nynorsk: kollineær
      engelsk:
      - colinear
      - collinear
    merknad: Begge skrivemåtene brukes på norsk, men kolineær anbefales.
  ```

- Informasjon om kontekst kan for eksempel gis slik:

  ```yaml
  - anbefalt:
      bokmål: forsøksplan
      nynorsk: forsøksplan
      engelsk: design
    bruksområde: statistikk
    merknad: Oversettelsen gjelder bruk i statistikk og utelukker ikke at termen kan
      benyttes ulikt i andre sammenhenger.
  - anbefalt:
      bokmål: felt
      nynorsk: felt
      engelsk: field
    merknad: Merk at oversettelsen av <i>field</i> er avhengig av kontekst. Oversettelsen
      felt brukes for eksempel i forbindelse med vektorfelt.
  - anbefalt:
      bokmål: kropp
      nynorsk: kropp
      engelsk: field
    merknad: Merk at oversettelsen av <i>field</i> er avhengig av kontekst. En kropp
      er en kommutativ ring der ethvert ikke-nullelement har en multiplikativ invers.
      For eksempel utgjør de reelle tall en kropp.
  ```

- I denne [oversikten](termer_med_merknad_eksempler.yaml) finner man flere
  eksempler på termer med merknad. Nye oppslagsord med merknad kan gjerne legges
  til blant disse eksemplene.
