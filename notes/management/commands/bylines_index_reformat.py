import re
import sys
from openpyxl import load_workbook, Workbook

""" Reformats Railway Bylines Excel file to a more standardised format reading an Excel file and writing a new Excel file with the reformatted data. 

To excute, run the following command in the terminal:

python bylines_index_reformat.py Railway_Bylines_Index.xlsx  output.xlsx

"""


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

SMALL_WORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from",
    "in", "into", "of", "on", "or", "over", "the",
    "to", "under", "with", "without", "via"
}

KEEP_UPPER = {
    "BR", "LNER", "LMS", "GWR", "SR", "LSWR", "SECR", "SE&CR",
    "LBSC", "LCDR", "MR", "GER", "GNR", "NBR", "CR",
    "HR", "GSWR", "LYR", "NER", "S&DJR",
    "DMU", "EMU", "HST", "APT", "TOPS", "TPWS",
    "AWS", "ETCS", "ECS"
}

ROMAN_NUMERAL = re.compile(
    r'^(M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))$',
    re.IGNORECASE
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def clean_spaces(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def normalise_dashes(text):
    return (str(text)
            .replace("–", "-")
            .replace("—", "-")
            .replace("−", "-"))


def strip_leading_separators(text):
    return re.sub(r'^[\s\-,:;]+', '', text)


# ------------------------------------------------------------
# Reference number extraction
# ------------------------------------------------------------

def extract_reference_number(row, text):
    m = re.match(r'^\s*(\d+)(.*)$', text)
    if m:
        row[2] = m.group(1)
        return m.group(2)
    return text


# ------------------------------------------------------------
# Author extraction (fixed for ", by" and "- by")
# ------------------------------------------------------------

def is_title_exception(text):
    return "by the by" in text.lower()


def extract_author(text):

    if is_title_exception(text):
        return text, ""

    # normalise spacing before searching
    text = re.sub(r'\s*([,-])\s*\bby\b', r' \1 by', text, flags=re.IGNORECASE)

    matches = list(re.finditer(r'\bby\b', text, re.IGNORECASE))

    if matches:
        last = matches[-1]
        author = text[last.end():]
        main = text[:last.start()]
        return main, clean_spaces(author)

    return text, ""


# ------------------------------------------------------------
# Initials formatting
# ------------------------------------------------------------

def fix_initials(text):
    return re.sub(
        r'\b(?:[A-Z]\.){2,}[A-Z]?\b',
        lambda m: m.group(0).replace(".", ". ").strip(),
        text
    )


# ------------------------------------------------------------
# Fix apostrophe casing (important new rule)
# ------------------------------------------------------------

def fix_apostrophes(text):
    def repl(match):
        word = match.group(0)

        # Lowercase everything after apostrophe except first char
        parts = word.split("'")
        if len(parts) == 2:
            return parts[0] + "'" + parts[1].lower()
        return word

    # only apply to words with apostrophes
    return re.sub(r"\b[A-Za-z]+'[A-Za-z]+\b", repl, text)


# ------------------------------------------------------------
# Smart title case (railway-aware)
# ------------------------------------------------------------

def smart_title(text):

    def convert(word, first):

        if not word:
            return word

        if re.search(r'\d', word):
            return word

        if not (word.isupper() or word.islower()):
            return word

        upper = word.upper()

        if upper in KEEP_UPPER:
            return upper

        if ROMAN_NUMERAL.fullmatch(word):
            return word.upper()

        lower = word.lower()

        if not first and lower in SMALL_WORDS:
            return lower

        return lower.capitalize()

    tokens = re.split(r'(\W+)', text)

    result = []
    first = True

    for t in tokens:
        if re.fullmatch(r'[A-Za-z&()./\'-]+', t):
            result.append(convert(t, first))
            first = False
        else:
            result.append(t)

    return ''.join(result)


# ------------------------------------------------------------
# Final cleanup (NEW: remove ", by" / "- by")
# ------------------------------------------------------------

def final_cleanup(text):

    text = clean_spaces(text)

    # remove trailing punctuation before author patterns already handled
    text = re.sub(r'\s+,?\s*$', '', text)

    return text


# ------------------------------------------------------------
# Row processing pipeline
# ------------------------------------------------------------

def process_row(row):

    while len(row) < 5:
        row.append("")

    text = row[3]

    # normalise dash variants early
    text = normalise_dashes(text)

    # extract number
    text = extract_reference_number(row, text)

    # remove leading punctuation
    text = strip_leading_separators(text)

    # extract author (fixed handling of ", by" and "- by")
    text, author = extract_author(text)

    # formatting pipeline
    text = fix_initials(clean_spaces(text))
    text = smart_title(text)
    text = fix_apostrophes(text)
    text = final_cleanup(text)

    author = smart_title(clean_spaces(author)) if author else ""

    row[3] = text
    row[4] = author

    return row


# ------------------------------------------------------------
# Excel processing
# ------------------------------------------------------------

def process_excel(input_file, output_file, sheet_index=0):

    wb = load_workbook(input_file)
    ws = wb.worksheets[sheet_index]

    out_wb = Workbook()
    out_ws = out_wb.active

    for row in ws.iter_rows(values_only=True):
        row = list(row) if row else []
        out_ws.append(process_row(row))

    out_wb.save(output_file)


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python railway_cleaner_excel.py input.xlsx output.xlsx")
        sys.exit(1)

    process_excel(sys.argv[1], sys.argv[2])
    print("Done.")