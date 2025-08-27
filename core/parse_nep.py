# core/parse_nep.py
import re
from typing import Dict

# ---------------- Digit helpers ----------------
NEP2ASCII = str.maketrans("०१२३४५६७८९", "0123456789")
ASCII2NEP = str.maketrans("0123456789", "०१२३४५६७८९")

def nep_to_ascii(s: str) -> str:
    """Convert Nepali digits to ASCII digits."""
    return s.translate(NEP2ASCII) if s else s

def ascii_to_nep(s: str) -> str:
    """Convert ASCII digits to Nepali digits."""
    return s.translate(ASCII2NEP) if s else s

# ---------------- Small helpers ----------------
def _g(rx: str, t: str, flags: int = re.I | re.S | re.M) -> str:
    m = re.search(rx, t, flags)
    return m.group(1).strip() if m else ""

def _clean(text: str) -> str:
    """
    Normalize OCR text for regex:
    - Nepali→ASCII digits
    - collapse big spaces (keep newlines)
    - trim trailing spaces
    """
    t = nep_to_ascii(text or "")
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r"[ \t]+\n", "\n", t)
    return t

# ---------------- Main parser ----------------
def parse_ocr(text: str) -> Dict[str, str]:
    """
    Parse Nepali pre-approval/ads. Returns ASCII digits for numbers.
    Keys (when found):
      lt_no, chalani_no, date, employer, country,
      position, male, female, salary_currency, salary_amount,
      salary_kd, salary_npr, overtime, hours_per_day, days_per_week,
      yearly_leave, min_qualification, eating, sleeping, tenure, total_expense,
      application_deadline, medical_cost_local, medical_cost_foreign, insurance_local,
      insurance_employment, air_ticket, visa_fee, visa_stamp_fee, recruitment_fee,
      welfare_fund, labor_fee, service_fee, company_address, company_phone, company_email
    """
    asc = _clean(text)
    d: Dict[str, str] = {}

    # ---- IDs & date ----
    d["lt_no"]      = _g(r"(?:L\.?\s*T\.?\s*No\.?|LOT\s*No\.?)\s*[:：\-]?\s*([0-9]+)", asc)
    d["chalani_no"] = _g(r"(?:चलानी\s*नं\.?|Chalani\s*No\.?|फोन\s*नं\.?|Phone)\s*[:：\-]?\s*([0-9]+)", asc)
    d["date"]       = _g(r"(?:Date|मिति)\s*[:：\-]?\s*([0-9]{4}/[0-9]{2}/[0-9]{2})", asc)

    # ---- employer / country ----
    d["employer"] = _g(r"([A-Z0-9 .,&'/\-]+(?:L\.?\s*L\.?\s*C|W\.?\s*L\.?\s*L|CO\.|COMPANY))", asc)
    d["country"]  = _g(r"\b(UAE|Qatar|Saudi|Kuwait|Bahrain|Oman)\b", asc)

    # ---- main row variants ----
    # Full row: 1 <position> <male> <female> <CUR> <amount>
    m = re.search(
        r"""(?mx)
        ^\s*1\s+                             # line starts with 1
        ([A-Za-z][A-Za-z /-]+?)\s+           # position
        ([0-9]{1,4})\s+                      # male
        ([0-9]{1,4})\s+                      # female
        (AED|KD|USD|NPR|Nrs\.?|Dollar)\s*    # currency
        ([0-9][0-9,\.]*)\s*$                 # amount
        """,
        asc,
    )
    if m:
        d["position"]        = m.group(1).strip()
        d["male"]            = m.group(2)
        d["female"]          = m.group(3)
        d["salary_currency"] = m.group(4).replace("Nrs.", "NPR").replace("Dollar", "USD")
        d["salary_amount"]   = m.group(5).replace(",", "")

    # Alt row: 1 <position> <CUR> <amount>  (no counts on this line)
    if "position" not in d or "salary_amount" not in d:
        m2 = re.search(
            r"""(?mx)
            ^\s*1\s+                           # line starts with 1
            ([A-Za-z][A-Za-z /-]+?)\s+         # position
            (AED|KD|USD|NPR|Nrs\.?|Dollar)\s*  # currency
            ([0-9][0-9,\.]*)\s*$               # amount
            """,
            asc,
        )
        if m2:
            d["position"]        = d.get("position") or m2.group(1).strip()
            d["salary_currency"] = m2.group(2).replace("Nrs.", "NPR").replace("Dollar", "USD")
            d["salary_amount"]   = m2.group(3).replace(",", "")

    # ---- counts lines ----
    # "पूर्व स्वीकृतिको संख्या 150 50"
    if "male" not in d or "female" not in d:
        m3 = re.search(r"पूर्व\s*स्वीकृतिको\s*संख्या\s*([0-9]{1,4})\s+([0-9]{1,4})", asc, re.I)
        if m3:
            d["male"]   = m3.group(1)
            d["female"] = m3.group(2)

    # "पूर्व स्वीकृतिको संख्या 150" (only one number present)
    if "male" not in d:
        m4 = re.search(r"पूर्व\s*स्वीकृतिको\s*संख्या\s*([0-9]{1,4})(?!\s*[0-9])", asc, re.I)
        if m4:
            d["male"] = m4.group(1)

    # Fallback explicit labels
    if "male" not in d:
        d["male"] = _g(r"\bMale\s*[:：]?\s*([0-9]{1,4})\b", asc)
    if "female" not in d:
        d["female"] = _g(r"\bFemale\s*[:：]?\s*([0-9]{1,4})\b", asc)

    # ---- KD / NPR amounts if present anywhere ----
    d["salary_kd"]  = _g(r"\bKD\s*([0-9][0-9,\.]*)", asc).replace(",", "") or ""
    d["salary_npr"] = _g(r"(?:ने\.?\s*\.?रु\.?|NPR|Nrs\.?)\s*([0-9][0-9,\.]*)", asc).replace(",", "") or ""

    # ---- Extras: overtime / hours / days / leave / qualification / facilities / tenure ----
    d["overtime"] = (
        _g(r"(?:ओभर\s*टाइम\s*सुविधा|Overtime\s*Facility)\s*[:：\-]?\s*([^\n]+)", asc)
        or _g(r"\b(?:company'?s|कम्पनीको)\s*नियम\s*अनुसार\b", asc)
    )
    d["hours_per_day"] = (
        _g(r"(?:प्रतिदिन\s*काम\s*गर्ने\s*घण्टा|Working\s*Hours\s*/?\s*Day)\D{0,12}([0-9]{1,2})", asc)
        or _g(r"\b([0-9]{1,2})\s*(?:घण्टा|hours?)\b", asc)
    )
    d["days_per_week"] = (
        _g(r"(?:हप्तामा\s*काम\s*गर्ने\s*दिन|Working\s*days\s*/\s*week)\D{0,12}([0-9]{1,2})", asc)
        or _g(r"\b([0-9]{1,2})\s*(?:दिन|days?)\b", asc)
    )
    d["yearly_leave"] = (
        _g(r"(?:वार्षिक\s*विदा|Yearly\s*Holiday)\D{0,12}([0-9]{1,3})", asc)
        or _g(r"(?:वार्षिक\s*विदा|Yearly\s*Holiday)\s*[:：\-]?\s*(कम्पनीको\s*नियम\s*अनुसार)", asc)
    )
    d["min_qualification"] = _g(
        r"(?:न्यूनतम\s*शैक्षिक\s*योग्यता|Minimum\s*Qualif(?:ication)?)\s*[:：\-]?\s*([^\n]+)", asc
    )
    d["eating"]  = _g(r"(?:खाने\s*सुविधा|Eating\s*Facility)\s*[:：\-]?\s*([^\n]+)", asc)
    d["sleeping"] = _g(r"(?:बस्ने\s*सुविधा|Sleeping\s*Facility)\s*[:：\-]?\s*([^\n]+)", asc)
    d["tenure"] = (
        _g(r"(?:करार\s*अवधि|Tenure)\s*[:：\-]?\s*([^\n]+)", asc)
        or _g(r"([0-9]{1,2})\s*(?:वर्ष|years?)", asc)
    )

    # ---- Application Deadline ----
    d["application_deadline"] = (
        _g(r"(?:अन्तिम\s*आवेदन\s*मिति|Application\s*Deadline|Last\s*Date)\s*[:：\-]?\s*([^\n]+)", asc)
        or _g(r"(?:आवेदन\s*मिति|Deadline)\s*[:：\-]?\s*([^\n]+)", asc)
    )

    # ---- Extra Information Fields ----
    # Medical costs
    d["medical_cost_local"] = _g(r"(?:स्वदेशमा\s*मेडिकल|Local\s*Medical)\s*[:：\-]?\s*([^\n]+)", asc)
    d["medical_cost_foreign"] = _g(r"(?:विदेशमा\s*मेडिकल|Foreign\s*Medical)\s*[:：\-]?\s*([^\n]+)", asc)
    
    # Insurance
    d["insurance_local"] = _g(r"(?:स्वदेशमा\s*बीमा|Local\s*Insurance)\s*[:：\-]?\s*([^\n]+)", asc)
    d["insurance_employment"] = _g(r"(?:रोजगारमा\s*बीमा|Employment\s*Insurance)\s*[:：\-]?\s*([^\n]+)", asc)
    
    # Travel and visa
    d["air_ticket"] = _g(r"(?:हवाई\s*टिकट|Air\s*Ticket)\s*[:：\-]?\s*([^\n]+)", asc)
    d["visa_fee"] = _g(r"(?:भिसा\s*शुल्क|Visa\s*Fee)\s*[:：\-]?\s*([^\n]+)", asc)
    d["visa_stamp_fee"] = _g(r"(?:भिसा\s*स्ट्याम्प\s*शुल्क|Visa\s*Stamp\s*Fee)\s*[:：\-]?\s*([^\n]+)", asc)
    
    # Fees
    d["recruitment_fee"] = _g(r"(?:अभिकृतिकरण\s*शुल्क|Recruitment\s*Fee)\s*[:：\-]?\s*([^\n]+)", asc)
    d["welfare_fund"] = _g(r"(?:कल्याणकारी\s*कोष|Welfare\s*Fund)\s*[:：\-]?\s*([^\n]+)", asc)
    d["labor_fee"] = _g(r"(?:श्रमशुल्क|Labor\s*Fee)\s*[:：\-]?\s*([^\n]+)", asc)
    d["service_fee"] = _g(r"(?:सेवा\s*शुल्क|Service\s*Fee)\s*[:：\-]?\s*([^\n]+)", asc)

    # ---- Company Information ----
    d["company_address"] = _g(r"(?:ठेगाना|Address)\s*[:：\-]?\s*([^\n]+)", asc)
    d["company_phone"] = _g(r"(?:फोन|Phone)\s*[:：\-]?\s*([^\n]+)", asc)
    d["company_email"] = _g(r"(?:इमेल|Email)\s*[:：\-]?\s*([^\n]+)", asc)
    d["company_website"] = _g(r"(?:वेब|Website|Web)\s*[:：\-]?\s*([^\n]+)", asc)
    d["license_number"] = _g(r"(?:लाइसेन्स\s*नं\.?|License\s*No\.?|Gov\.?\s*Lic\.?)\s*[:：\-]?\s*([^\n]+)", asc)

    # ---- Total expense (optional) ----
    tot = _g(r"जम्मा\s*खर्च\s*([0-9][0-9,\.]*)", asc)
    if tot:
        d["total_expense"] = tot.replace(",", "")

    # prune empties
    return {k: v for k, v in d.items() if v}
