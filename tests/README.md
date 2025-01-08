# Esecuzione dei Test

Questo documento spiega come eseguire la suite di test per il progetto Delta Personal Timeline.

## Prerequisiti

Prima di poter eseguire i test, assicurati di avere installato le seguenti dipendenze:

- Python 3.11 
- PyQt5
- psutil 
- pytest

Puoi installare le dipendenze eseguendo il seguente comando:

```bash
pip install PyQt5 psutil pytest
```

## Esecuzione dei Test

Per eseguire l'intera suite di test, naviga nella directory principale del progetto ed esegui il seguente comando:

```bash
python3.11 -m pytest tests/
```

Questo eseguirà tutti i file di test nella directory "tests" e nelle sue sottodirectory.
Se vuoi eseguire un singolo file di test, puoi specificare il percorso del file:

```bash
python3.11 -m pytest tests/timeline/test_timeline.py
```

## Struttura dei Test

I test sono organizzati in sottodirectory basate sulla funzionalità che stanno testando. Ad esempio:

- tests/timeline/: test relativi alla timeline e agli item musicali
- tests/dialogs/: test per le finestre di dialogo
- tests/commands/: test per il sistema di undo/redo
- tests/integration/: test che coprono interazioni tra componenti multipli

Ogni file di test contiene una o più classi di test che ereditano da BaseTest. Questa classe fornisce un setup comune e delle utility condivise.

## Segnalazione di Bug

Se i test rilevano un bug o un problema, per favore apri una nuova issue sul repository GitHub del progetto, descrivendo il problema e includendo qualsiasi output rilevante dei test.