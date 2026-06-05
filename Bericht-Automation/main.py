import whisper
import subprocess
from docx import Document
from datetime import datetime
import os
import re

# Modell nur einmal laden, nicht bei jedem Aufruf
_WHISPER_MODEL = whisper.load_model("medium")


def find_audio_file(audio_dir="audio"):
    files=[
        os.path.join(audio_dir, filename)
        for filename in os.listdir(audio_dir)
        if filename.lower().endswith((".ogg", ".wav", ".mp3"))
    ] 
    files.sort()
    return files

def transcribe_audio(path):
    """Whisper‑Transkription; gibt reinen Text zurück."""
    print("🔹 Lade Whisper‑Modell (bereits im Modul); transkribiere …")
    result = _WHISPER_MODEL.transcribe(path, language="de")
    return result["text"]


def write_report_with_ollama(text):
    """Aufruf der `ollama`‑CLI; gibt bearbeitetes Protokoll zurück."""
    prompt = (
        "Landwirtschaftliches Protokoll. Regeln:\n"
        "- Stichpunkte mit •\n"
        "- Füllwörter entfernen (also, äh, irgendwie)\n"
        "- Fachbegriffe beibehalten\n"
        "- Keine Sätze umformulieren\n"
        "- Kurz und sachlich\n\n"
        f"Text: {text}\n\nProtokoll:"
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.1:8b", prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            check=True,
        )
    except FileNotFoundError:
        raise RuntimeError("Die 'ollama'-CLI wurde nicht gefunden – ist sie installiert?")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Ollama ist mit Fehlercode {e.returncode} beendet worden:\n{e.stderr}")

    output = result.stdout.strip()
    fixes = {
        "Fersen": "Färsen",
        "Milchbubestand": "Milchviehbestand",
        "Zuversetzung": "Aufzucht",
        "Milchbube": "Milchvieh",
        "Buko": "Büko",
    }
    for wrong, right in fixes.items():
        output = output.replace(wrong, right)
    return output


def einfache_stilisierung(text):
    saetze = re.split(
        r'(?<=[.!?])\s+|(?:und dann|außerdem|weiterhin)\s+',
        text,
        flags=re.IGNORECASE,
    )
    fuellwoerter = r'\b(also|äh|ähm|irgendwie|sozusagen|quasi|naja|moment|eigentlich)\b[,.]?'

    aufgeraeumt = []
    for satz in saetze:
        satz = re.sub(fuellwoerter, "", satz, flags=re.IGNORECASE).strip()
        if len(satz) > 10:
            satz = satz[0].upper() + satz[1:]
            aufgeraeumt.append(f"• {satz}")
    return "\n".join(aufgeraeumt)


def save_docx(content, idx):
    os.makedirs("berichte", exist_ok=True)
    filename = f"berichte/bericht_{idx}_{datetime.now():%Y%m%d}.docx"
    doc = Document()
    doc.add_paragraph(content)
    doc.save(filename)
    return filename


FACH_ERSETZUNGEN = {
    r'\b[Gg]rinder\b': 'Rinder',
    r'\b[Kk]ür\b': 'Kühe',
    r'\b[Üü]lbestand\b': 'Jungviehbestand',
    r'\b[Tt]rockn(?:masse|mas)\b': 'Trockensubstanz',
    r'\b[Tt]rockenmasse\b': 'Trockensubstanz',
    r'\b[Rr]evontier(?:ungsrate|ung)\b': 'Remontierungsrate',
    r'\b[Hh]ierde\b': 'Herde',
    r'\b[Hh]ierbestand\b': 'Herdenbestand',
    r'\b[Ll][Kk][Ss]\b': 'LKS',
    r'\b[Tt][Mm][Rr]\b': 'TMR',

    # typische Fehler
    r'\b[Mm]ilchbubestand\b': 'Milchviehbestand',
    r'\b[Mm]ilchbube\b': 'Milchvieh',
    r'\b[Ff]ersen\b': 'Färsen',
    r'\b[Zz]uversetzung\b': 'Aufzucht',
    r'\b[Jj]ungkind\b': 'Jungtier',
    r'\b[Bb]uko\b': 'Büko',
    r'\b[Ff]ersenleistung\b': 'Färsenleistung',
    r'\b[Aa]bgekäuft\b': 'abgekalbt',
    r'\b[Aa]bgekäuften\b': 'abgekalbten',
    r'\b[Pp]ettigries\b': 'Petit Gris',
    r'\b[Hh]ochleistende für mit\b': 'hochleistende mit',
    r'\b[Aa]ufzug(s)?kosten\b': r'Aufzucht\1kosten',
    r'\b[Hh]ochleistende\b': 'Hochleistende',
    r'\b[Hh]ochleistenden\b': 'Hochleistenden',
}


def korrigiere_fachbegriffe(text):
    for pattern, ersatz in FACH_ERSETZUNGEN.items():
        text = re.sub(pattern, ersatz, text, flags=re.IGNORECASE)
    return text


def save_debug(content, step_name, idx=None):
    os.makedirs("debug", exist_ok=True)
    filename = f"debug/{step_name}_{idx}.txt" if idx is not None else f"debug/{step_name}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"💾 Saved: {filename}")


def repariere_saetze(text):
    broken_ends = ['ca.', 'z.B.', 'd.h.', 'u.a.']
    lines = text.splitlines()
    result = []
    buffer = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if buffer:
            line = buffer + " " + line
            buffer = ""
        if any(line.rstrip().endswith(end) for end in broken_ends):
            buffer = line
            continue
        result.append(line)

    if buffer:
        result.append(buffer)

    return "\n".join(result)


def fix_verbsatz(text):
    text = re.sub(r'•\s*Ist\s+der\s+(\w+)(\s+\w+)?\s+nicht', r'• Der \1\2 ist nicht', text)
    text = re.sub(r'•\s*Ist\s+die\s+(\w+)(\s+\w+)?\s+nicht', r'• Die \1\2 ist nicht', text)
    return text


def strukturiere_sicher(text):
    themen_keywords = {
        "Tierbestandsplanung": ["jungrinder", "färsen", "aufzucht",
                                "bestand", "remontierung", "milchviehbestand",
                                "büko", "überbelegung"],
        "Leistungsdepression": ["leistungsdepression", "erstlaktierend",
                                "abgekalbt", "leistungspiegel", "liter"],
        "Fütterung": ["futter", "ration", "trockensubstanz", "megajoule",
                      "rohprotein", "futteraufnahme"],
        "Genetik": ["genetik", "zuchtwert", "abstammung", "deckwohle",
                    "petit gris"],
        "Herdenmanagement": ["herdenmanagement", "veränderungen",
                             "leistungsbereitschaft"],
    }

    punkte = [p.strip() for p in text.split("•") if p.strip()]
    themen_dict = {name: [] for name in themen_keywords}
    ungekl = []           # hier sammeln wir alles ohne Treffer

    for punkt in punkte:
        punkt_lower = punkt.lower()
        getroffen = False
        for thema, keywords in themen_keywords.items():
            if any(kw in punkt_lower for kw in keywords):
                themen_dict[thema].append(punkt)
                getroffen = True
                break
        if not getroffen:
            ungekl.append(punkt)

    output = []
    for thema, satz_liste in themen_dict.items():
        if satz_liste:
            output.append(f"\n{thema}\n")
            block = " ".join(satz_liste)
            output.append(block[0].upper() + block[1:] + "\n")

    if ungekl:                       # alles, was keiner Kategorie zugeordnet war
        output.append("\nSonstiges\n")
        block = " ".join(ungekl)
        output.append(block[0].upper() + block[1:] + "\n")

    return "".join(output)


def main():

    audio_files = find_audio_file()
    if not audio_files:
        print("❌ Keine Audiodateien gefunden.")
        return
    print(f"{len(audio_files)} Audiodatei(en) gefunden:")

    for idx, audio_path in enumerate(audio_files, start=1):
        print(f"{idx}. {audio_path}")

        raw_text = transcribe_audio(audio_path)
        save_debug(raw_text, "01_raw")

        corrected = korrigiere_fachbegriffe(raw_text)
        save_debug(corrected, "02_fachkorrigiert")

        stilisiert = einfache_stilisierung(corrected)
        stilisiert = repariere_saetze(stilisiert)
        stilisiert = fix_verbsatz(stilisiert)
        save_debug(stilisiert, "03_stilisiert", idx)

        strukturiert = strukturiere_sicher(stilisiert)
        save_debug(strukturiert, "04_strukturiert")

        file_path = save_docx(strukturiert, idx)
        print("\n✅ Bericht gespeichert unter:", file_path)


if __name__ == "__main__":
    main()