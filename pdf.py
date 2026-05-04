from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, 
                                 Table, TableStyle, HRFlowable, PageBreak, KeepTogether)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

# ── colour palette ──────────────────────────────────────────────
C_HEAD   = colors.HexColor('#003366')   # deep navy – chapter headers
C_SUB    = colors.HexColor('#005a9c')   # medium blue – section heads
C_BOX    = colors.HexColor('#e8f0fb')   # pale blue – highlighted boxes
C_RULE   = colors.HexColor('#c0392b')   # red accent line
C_KEY    = colors.HexColor('#1a5276')   # key-term colour
C_LIGHT  = colors.HexColor('#f5f5f5')   # light grey for tables
C_DARK   = colors.HexColor('#2c3e50')   # near-black text

W, H = A4

doc = SimpleDocTemplate(
    'Finance_Banking_BD_Bank_Exam_MasterNotes ',
    pagesize=A4,
    leftMargin=1.8*cm, rightMargin=1.8*cm,
    topMargin=2*cm,    bottomMargin=2*cm,
)

styles = getSampleStyleSheet()

# ── custom styles ────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

COVER_TITLE = S('CoverTitle', fontName='Helvetica-Bold', fontSize=28,
                textColor=C_HEAD, alignment=TA_CENTER, spaceAfter=10, leading=34)
COVER_SUB   = S('CoverSub',   fontName='Helvetica-Bold', fontSize=14,
                textColor=C_RULE, alignment=TA_CENTER, spaceAfter=6)
COVER_BODY  = S('CoverBody',  fontName='Helvetica', fontSize=11,
                textColor=C_DARK, alignment=TA_CENTER, spaceAfter=4)

CHAP  = S('Chap',  fontName='Helvetica-Bold', fontSize=15, textColor=colors.white,
          alignment=TA_LEFT, spaceAfter=4, spaceBefore=8, leading=18)
SEC   = S('Sec',   fontName='Helvetica-Bold', fontSize=11, textColor=C_SUB,
          spaceAfter=3, spaceBefore=6, leading=14)
SSEC  = S('SSec',  fontName='Helvetica-Bold', fontSize=10, textColor=C_KEY,
          spaceAfter=2, spaceBefore=4, leading=13)
BODY  = S('Body',  fontName='Helvetica', fontSize=8.5, textColor=C_DARK,
          spaceAfter=3, leading=12, alignment=TA_JUSTIFY)
BULL  = S('Bull',  fontName='Helvetica', fontSize=8.5, textColor=C_DARK,
          spaceAfter=2, leading=11, leftIndent=12, bulletIndent=0,
          bulletFontName='Helvetica-Bold')
KEY   = S('Key',   fontName='Helvetica-Bold', fontSize=8.5, textColor=C_KEY,
          spaceAfter=2, leading=11)
FORM  = S('Form',  fontName='Helvetica-Oblique', fontSize=8.5, textColor=C_DARK,
          backColor=C_BOX, spaceAfter=3, leading=12, leftIndent=6, rightIndent=6)
NOTE  = S('Note',  fontName='Helvetica-Oblique', fontSize=8, textColor=colors.HexColor('#7f8c8d'),
          spaceAfter=2, leading=11)
TH    = S('TH',    fontName='Helvetica-Bold', fontSize=8, textColor=colors.white, alignment=TA_CENTER)
TD    = S('TD',    fontName='Helvetica', fontSize=8, textColor=C_DARK, alignment=TA_CENTER, leading=10)
TDL   = S('TDL',   fontName='Helvetica', fontSize=8, textColor=C_DARK, leading=10)

story = []

# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════
def chapter_header(num, title):
    t = Table([[Paragraph(f'CHAPTER {num}  ·  {title.upper()}', CHAP)]],
              colWidths=[W - 3.6*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_HEAD),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',   (0,0), (-1,-1), 6),
        ('BOTTOMPADDING',(0,0), (-1,-1), 6),
        ('ROUNDEDCORNERS', [4]),
    ]))
    story.append(t)
    story.append(Spacer(1, 4))

def section(text):
    story.append(Paragraph(text, SEC))

def sub(text):
    story.append(Paragraph(text, SSEC))

def body(text):
    story.append(Paragraph(text, BODY))

def bullet(text):
    story.append(Paragraph(f'• {text}', BULL))

def key(label, text):
    story.append(Paragraph(f'<b>{label}:</b> {text}', BODY))

def formula(text):
    story.append(Paragraph(text, FORM))

def note(text):
    story.append(Paragraph(f'★ {text}', NOTE))

def rule():
    story.append(HRFlowable(width='100%', thickness=0.5, color=C_RULE, spaceAfter=4, spaceBefore=2))

def box_table(rows, col_widths=None, header_row=True):
    """Generic coloured table."""
    tbl_data = []
    for i, row in enumerate(rows):
        tbl_data.append([Paragraph(str(c), TH if (i==0 and header_row) else TD) for c in row])
    cw = col_widths or [(W-3.6*cm)/len(rows[0])]*len(rows[0])
    t = Table(tbl_data, colWidths=cw)
    style = [
        ('GRID',        (0,0), (-1,-1), 0.4, colors.grey),
        ('TOPPADDING',  (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
    ]
    if header_row:
        style += [('BACKGROUND', (0,0), (-1,0), C_HEAD),
                  ('TEXTCOLOR',  (0,0), (-1,0), colors.white)]
    for i in range(1, len(rows)):
        bg = C_BOX if i%2==0 else colors.white
        style.append(('BACKGROUND', (0,i), (-1,i), bg))
    t.setStyle(TableStyle(style))
    story.append(t)
    story.append(Spacer(1, 4))

def sp(n=4):
    story.append(Spacer(1, n))

# ═══════════════════════════════════════════════════════════════
#  COVER PAGE
# ═══════════════════════════════════════════════════════════════
story.append(Spacer(1, 2.5*cm))
# Red banner
t = Table([[Paragraph('BANGLADESH BANK · ADDITIONAL DIRECTOR EXAM', COVER_SUB)]],
          colWidths=[W-3.6*cm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1), C_RULE),
                        ('TOPPADDING',(0,0),(-1,-1),8),
                        ('BOTTOMPADDING',(0,0),(-1,-1),8)]))
story.append(t)
sp(10)
story.append(Paragraph('Finance & Banking', COVER_TITLE))
sp(4)
story.append(Paragraph('Comprehensive Master Notes', COVER_SUB))
sp(6)
story.append(HRFlowable(width='60%', thickness=2, color=C_HEAD, spaceAfter=8))
sp(6)
story.append(Paragraph('Based on NCTB Class 9-10 Textbook · All 13 Chapters Covered', COVER_BODY))
story.append(Paragraph('Definitions · Principles · Formulas · Classifications · BD-Specific Facts', COVER_BODY))
sp(4)
# TOC box
toc_data = [
    ['Ch.', 'Topic', 'Ch.', 'Topic'],
    ['1', 'Finance & Business Finance', '8', 'Currency, Bank & Banking'],
    ['2', 'Sources of Finance', '9', 'Banking Business & Types'],
    ['3', 'Time Value of Money', '10', 'Introduction to Commercial Banks'],
    ['4', 'Risk and Uncertainty', '11', 'Bank Deposit'],
    ['5', 'Capital Budgeting', '12', 'Bank and Client'],
    ['6', 'Cost of Capital', '13', 'Central Bank'],
    ['7', 'Share, Bond & Debenture', '', ''],
]
cw2 = [0.8*cm, 6.5*cm, 0.8*cm, 6.5*cm]
t2 = Table([[Paragraph(str(c), TH if i==0 else TDL) for c in r] for i,r in enumerate(toc_data)],
           colWidths=cw2)
t2.setStyle(TableStyle([
    ('GRID',(0,0),(-1,-1),0.4,colors.grey),
    ('BACKGROUND',(0,0),(-1,0),C_HEAD),
    ('BACKGROUND',(0,1),(-1,-1),C_BOX),
    ('TOPPADDING',(0,0),(-1,-1),3),
    ('BOTTOMPADDING',(0,0),(-1,-1),3),
    ('LEFTPADDING',(0,0),(-1,-1),5),
]))
story.append(t2)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 1 — FINANCE AND BUSINESS FINANCE
# ═══════════════════════════════════════════════════════════════
chapter_header(1, 'Finance and Business Finance')

section('1.1 Concept of Finance')
body('Finance deals with <b>fund management</b> — planning how much fund to collect from which sources and where/how to invest it for maximum profit. It regulates inflows and outflows of fund in business. Finance is now the <b>main driving force</b> of business, not merely a supporting system.')

section('1.2 Classification of Finance')
box_table([
    ['Type','Definition / Key Points'],
    ['Family Finance','Source identification & utilization for family welfare; regular vs. occasional expenditures; bank loans for fixed assets (TV, fridge, car).'],
    ['Public Finance','Government income-expenditure management. Sources: income tax, VAT, gift tax, import/export custom, savings certificates, prize bond, treasury bill. Objective: social welfare. Can use PPP (Public-Private Partnership). International loans from ADB, World Bank, IDB.'],
    ['International Finance','Covers export-import analysis; Bangladesh is mainly import-oriented; trade deficiency compensated by remittance. Jute & garments exported; foodstuff/raw materials/petroleum imported.'],
    ['Non-Profit Organisation Finance','Identification of fund sources (grants, donations) and efficient utilization for service objectives.'],
    ['Business Finance','Most important type. Fund collection & investment for profit. Three forms: Sole Proprietorship, Partnership, Joint Stock Company.'],
    ['Bank & Financial Institution Finance','Collect small deposits → pay lower interest → lend at higher rate → difference = profit. Examples: Sonali Bank, Janata Bank, Prime Bank, Shahjalal Islami Bank. NBFI examples: ICB, Bangladesh House Building Finance Corp., Bangladesh Agricultural Bank.'],
], col_widths=[3.5*cm, 12*cm])

section('1.3 Importance of Business Finance (BD Context)')
body('<b>Four key reasons:</b>')
bullet('<b>Capital Crisis:</b> BD is developing; financial crisis is regular; finance helps collect fund at right time.')
bullet('<b>Backward Banking System:</b> Loans cannot always be arranged in time; financial planning helps predict and overcome such problems.')
bullet('<b>Less Educated Entrepreneur:</b> Many BD entrepreneurs lack financial literacy; financial knowledge prevents loss through improper planning.')
bullet('<b>Production-Oriented Investment & National Income:</b> Profitable investment directly increases national income through cost-benefit analysis.')

section('1.4 Principles of Business Finance')
box_table([
    ['Principle','Explanation'],
    ['Liquidity vs. Profitability','Inverse relationship: excess cash ↓ profitability; excess investment ↑ cash crisis. Balance must be maintained.'],
    ['Competence (Maturity Matching)','Current assets financed by short-term funds; fixed assets by long-term funds.'],
    ['Diversification & Risk Distribution','Diversify products/services to distribute risk. Principle also applies to fund-collection sources.'],
], col_widths=[4.5*cm, 11*cm])

section('1.5 Functions of Financial Manager')
bullet('<b>Income/Financing Decision:</b> Selection of fund sources (short-term for current expenses; long-term for fixed). Balances owner equity vs. liabilities.')
bullet('<b>Expenditure/Investment Decision:</b> Evaluate if future cash inflows from an investment > purchase price (e.g., machine for 10 years).')
bullet('<b>Other:</b> Current investment decision (raw material quantity); cash reserve management; dues payment (interest on loans, dividends on shares).')

section('1.6 Evolution of Finance (Key Decades)')
box_table([
    ['Period','Milestone'],
    ['Pre-1930','Company unification; financial statements framework.'],
    ['1930s','High depression in USA; company reorganization to avoid bankruptcy; share selling started.'],
    ['1940s','Liquidity focus; cash budget management.'],
    ['1950s','Mathematical analysis for investment; long-term profit maximisation (Traditional trend).'],
    ['1960s','Modern finance begins; capital market priority; shareholder wealth maximisation.'],
    ['1970s','Computer-based finance; complex mathematics (Markowitz, Miller, Modigliani — Nobel 1990s).'],
    ['1980s','Efficient capital distribution among alternative projects; income calculation & analysis.'],
    ['1990s+','WTO era; internationality of finance; global capital market sourcing; fusion of accountancy, economics & finance.'],
], col_widths=[2.5*cm, 13*cm])

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 2 — SOURCES OF FINANCE
# ═══════════════════════════════════════════════════════════════
chapter_header(2, 'Sources of Finance')

section('2.1 Classification of Sources')
body('<b>Two broad categories:</b> (A) Internal Sources — provided by owner; (B) External Sources — provided by creditors.')
body('<b>Owner's share of capital = equity. Loan = liability.</b> Most organisations use both.')

section('2.2 Internal Sources')
sub('Ownership-Based (by type of business)')
bullet('<b>Sole Proprietorship:</b> Owner\'s own savings; personal liability is unlimited.')
bullet('<b>Partnership:</b> Combined capital of partners; partners share profit/loss; personal assets at risk.')
bullet('<b>Joint Stock Company:</b> Capital collected through selling shares to public.')
sub('Profit-Based')
bullet('<b>Retained Earnings / Undistributed Profit:</b> Reinvesting profit instead of distributing as dividend. Avoids interest cost.')

section('2.3 Short-Term Sources (up to 1 year)')
box_table([
    ['Source','Key Points'],
    ['Credit Purchase (Trade Credit)','Buy raw materials now, pay later. No interest usually. Oldest and most common.'],
    ['Bank Overdraft','Withdraw more than deposited. Interest on overdrawn amount only.'],
    ['Short-term Bank Loan','Loan for short period; usually for working capital needs.'],
    ['Advances from Purchasers','Pre-payment by buyers against future delivery.'],
    ['Discounting Bills Receivable','Bank pays discounted value of bill immediately; collects full amount on maturity.'],
    ['Micro-credit (NGO)','Grameen Bank, BRAC, ASA — small collateral-free loans for rural poor. BD-specific.'],
], col_widths=[4*cm, 11.5*cm])

section('2.4 Medium-Term Sources (1–5 years)')
box_table([
    ['Source','Key Points'],
    ['Specialised Financial Institutions','Bangladesh Agricultural Bank, BSB (Shilpa Bank), BSRS — term loans 1–5 years.'],
    ['Medium-term Bank Loan','Commercial banks; 1–5 year term; security often required.'],
    ['Deferred Payment Purchase','Buy equipment on instalment; supplier is creditor.'],
], col_widths=[4.5*cm, 11*cm])

section('2.5 Long-Term Sources (5 years+)')
box_table([
    ['Source','Key Points'],
    ['Long-term Loan','Bank/NBFI loan against fixed asset as security. Analysed: income, goodwill, fixed assets, prior repayment history.'],
    ['Debenture','Fixed-rate loan capital divided into small units. Interest must be paid regardless of profit. Term ≥ 5 years. Alternative to share.'],
    ['Leasing','Use expensive machine/equipment without buying. Pay rent to leasing company. Ownership stays with lessor. Good for new firms lacking capital.'],
    ['Share Issue (Equity)','Sole Proprietorship & Partnership → savings; Company → IPO in share market. Dividend is taxable (higher cost).'],
    ['Bond','Loan with mortgage/security. Fixed interest. Maturity date specified.'],
], col_widths=[4*cm, 11.5*cm])

section('2.6 IMF (International Monetary Fund)')
body('<b>Founded:</b> 1945 (Bretton Woods Conference, USA). HQ: Washington DC. Members: 189. Helps reconstruct economies. Provides conditional loans to countries.')

section('2.7 Factors for Selecting Source of Finance')
bullet('<b>Type of Business:</b> Sole Prop./Partnership → savings, profit, loans from relatives. Company → shares, debentures, long-term loans.')
bullet('<b>Insufficiency of Security:</b> New business → no fixed asset → use leasing.')
bullet('<b>Type of Need:</b> Current expenses → short-term; Fixed assets → long-term.')
bullet('<b>Cost:</b> Dividend (taxable) = higher cost than interest on loan (non-taxable = tax shield). Choose minimum-cost mix.')
bullet('<b>Risk:</b> Mortgaged property seized if loan unpaid; assess risk per source.')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 3 — TIME VALUE OF MONEY
# ═══════════════════════════════════════════════════════════════
chapter_header(3, 'Time Value of Money')

section('3.1 Concept')
body('Money has <b>time value</b> because: (a) money available today can be invested to earn interest; (b) purchasing power changes with inflation. Tk.1,000 today > Tk.1,000 next year.')
body('<b>Two processes:</b>')
bullet('<b>Compounding:</b> Present → Future Value (FV). Interest added on principal + previous interest.')
bullet('<b>Discounting:</b> Future → Present Value (PV). Reverse of compounding.')

section('3.2 Key Formulas')
formula('<b>Simple Interest:</b>  I = P × r × n   →   FV = P(1 + r×n)')
formula('<b>Compound Interest (Annual):</b>  FV = PV × (1 + i)<super>n</super>')
formula('<b>Present Value (Annual Compounding):</b>  PV = FV ÷ (1 + i)<super>n</super>')
formula('<b>Compound Interest (Periodic/Monthly):</b>  FV = PV × (1 + i/m)<super>m×n</super>')
formula('<b>Present Value (Periodic):</b>  PV = FV ÷ (1 + i/m)<super>m×n</super>')
formula('<b>Effective Annual Rate (EAR):</b>  EAR = (1 + i/m)<super>m</super> – 1')
body('<i>Where: PV = Present Value, FV = Future Value, i = annual interest rate, n = years, m = compounding frequency per year</i>')

section('3.3 Worked Examples')
body('<b>Example 1 – FV (Annual Compounding):</b> PV = Tk.10,000; i = 10%; n = 5 yrs')
formula('FV = 10,000 × (1.10)<super>5</super> = 10,000 × 1.6105 = Tk.16,105')
body('<b>Example 2 – PV (Discounting):</b> FV = Tk.50,000 in 5 yrs; i = 10% p.a.')
formula('PV = 50,000 ÷ (1.1)<super>5</super> = 50,000 ÷ 1.6105 = Tk.31,046.07')
body('<b>Example 3 – EAR:</b> Weekly rate = 1%; Nominal = 52%; Compounding = 52 times/yr')
formula('EAR = (1.01)<super>52</super> – 1 = 1.6777 – 1 = 67.77% (actual annual effective rate)')
note('BD exam favourite: money lenders charging 1%/week appears to be 52% per year BUT effective rate is 67.77%.')

section('3.4 Decision Rule')
body('Higher interest rate → prefer Bank that offers higher rate for deposit (same time); prefer Bank with lower rate for loan. Always compare using PV or FV on same basis.')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 4 — RISK AND UNCERTAINTY
# ═══════════════════════════════════════════════════════════════
chapter_header(4, 'Risk and Uncertainty')

section('4.1 Definitions')
key('Risk', 'Probability that actual results differ from expected results. Risk = measurable deviation. The higher the volatility of returns, the higher the risk.')
key('Uncertainty', 'Events that cannot be measured or predicted. E.g., death of CEO. NOT all uncertainties are risks.')
body('<b>Key distinction:</b> Risk can be measured and controlled; Uncertainty cannot.')

section('4.2 Types of Risk')
sub('From Business Firm Perspective')
bullet('<b>Business Risk:</b> Inability to meet operating costs (rent, wages, insurance) due to volatile sales revenue or high fixed costs. Risk when financed only internally.')
bullet('<b>Financial Risk:</b> Inability to repay debt obligations. Arises from external (debt) financing. Creditors may sue → bankruptcy. Interest must be paid regardless of profit.')
sub('From Investor Perspective')
bullet('<b>Interest Rate Risk:</b> Bond/debenture values move inversely with market interest rates. If rates ↑ → bond value ↓.')
bullet('<b>Liquidity Risk:</b> Inability to sell investments quickly at a reasonable price. Higher for Sole Prop./Partnership. Lower for listed company shares (secondary market). Higher for bonds/debentures (fewer buyers).')

section('4.3 Implications of Risk')
bullet('Unanticipated events (flood, river erosion) cause huge loss if not considered beforehand.')
bullet('Lower actual sales than expected → insufficient profit. Diversification mitigates this.')

section('4.4 Risk-Free vs. Risky Return')
bullet('<b>Risk-free return:</b> Government treasury bills/bonds, bank fixed deposits — actual = expected return.')
bullet('<b>Risky return:</b> Common stock dividends — most risky because income is not fixed.')

section('4.5 Measurement of Risk — Standard Deviation')
formula('<b>Standard Deviation (σ) = √[ Σ(Return – Average Return)<super>2</super> ÷ (n–1) ]</b>')
body('<b>Decision Rule:</b> Higher σ = higher risk. For same return → prefer lower σ. For same σ → prefer higher return.')

body('<b>Worked Example:</b>')
box_table([
    ['Year','Return (%)','Deviation (R–Avg)','Squared Deviation'],
    ['2007','20','7','49'],
    ['2008','5','-8','64'],
    ['2009','-5','-18','324'],
    ['2010','15','2','4'],
    ['2011','30','17','289'],
    ['Total','65%','—','730'],
    ['Average','13%','Variance = 730/4 = 182.5','σ = √182.5 = 13.5%'],
], col_widths=[2*cm,3*cm,4*cm,5.5*cm])
note('If alternate project offers same 13% return but 15% σ → original project (σ=13.5%) is preferred.')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 5 — CAPITAL BUDGETING
# ═══════════════════════════════════════════════════════════════
chapter_header(5, 'Capital Budgeting')

section('5.1 Definition & Scope')
key('Capital Budgeting', 'Evaluation process for long-term investment decisions involving fixed assets (purchase, replacement, modernisation, expansion, new product development).')
body('<b>Net Cash Inflow = Net Profit + Depreciation</b>  |  Cash Inflow > Outflow → Accept project.')
body('<b>Decision responsibility:</b> Financial manager bears responsibility for capital budgeting failures.')

section('5.2 Importance of Capital Budgeting')
bullet('<b>Profit-Oriented:</b> Directly affects profitability (e.g., fridge purchase → more sales → more profit).')
bullet('<b>Large Investment:</b> Mistakes are costly and hard/impossible to reverse. Errors can bankrupt the company.')
bullet('<b>Risk-Oriented:</b> Future is uncertain (market demand, sales volume, prices). CB techniques include risk management.')

section('5.3 Process of Capital Budgeting')
bullet('<b>(a) Expected Cash Flow:</b> Estimate selling price, sales volume, current expenses, capital cost.')
bullet('<b>(b) Discount Rate:</b> Usually = Cost of Capital. Converts future cash flows to present value.')
bullet('<b>(c) Apply Technique:</b> Select appropriate method based on project nature and risk.')

section('5.4 Techniques of Capital Budgeting')
rule()
sub('1. ARR – Accounting Rate of Return')
formula('ARR = (Average Net Profit ÷ Average Investment) × 100')
body('<i>Average Net Profit = Total Net Profit ÷ Years  |  Average Investment = Initial Investment ÷ 2</i>')
body('<b>Decision Rule:</b> Higher ARR → Accept. If ARR > minimum required rate → Accept.')
body('<b>Limitation:</b> Ignores time value of money; uses profit not cash flow.')
rule()
sub('2. Pay Back Period (PBP)')
formula('PBP = Investment ÷ Annual Cash Inflow  (if uniform cash inflows)')
body('<i>If non-uniform: PBP = Full years before recovery + (Remaining amount ÷ Next year cash inflow)</i>')
body('<b>Decision Rule:</b> Lower PBP → more attractive. Management sets benchmark PBP based on project type & risk.')
body('<b>Limitations:</b> (1) Not a rate of profit. (2) Not applicable for single project comparison. (3) Ignores cash flows after PBP. (4) Ignores time value of money.')
body('<b>Example:</b> Investment = Tk.100; Year 1 CF = Tk.69.99; Year 2 CF = Tk.49.90.')
formula('PBP = 1 + (30.01 ÷ 49.90) = 1.6 years')
rule()
sub('3. NPV – Net Present Value  &  4. IRR – Internal Rate of Return')
body('NPV and IRR are <b>most acceptable</b> methods because they consider time value of money. Details covered in higher classes.')
body('<b>NPV Rule:</b> If NPV > 0 → Accept.   <b>IRR Rule:</b> If IRR > Cost of Capital → Accept.')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 6 — COST OF CAPITAL
# ═══════════════════════════════════════════════════════════════
chapter_header(6, 'Cost of Capital')

section('6.1 Definition')
key('Cost of Capital', 'The minimum rate of return a business must earn on its investments to satisfy its financiers (investors/creditors). Equals expected income of the financer.')
body('<b>Precondition:</b> Investment returns must exceed cost of capital; otherwise the business cannot meet obligations.')

section('6.2 Significance of Cost of Capital')
bullet('<b>Investment Decision:</b> Must earn more than cost of capital (e.g., if loan rate = 18% but business earns 10% → failure).')
bullet('<b>Capital Structure Decision:</b> Choose mix of equity & debt that minimises average cost of capital.')

section('6.3 Cost of Different Sources')
rule()
sub('a) Cost of Loan Capital (Kd)')
formula('Pre-tax cost = Interest Rate (e.g., 15%)')
formula('Tax-adjusted cost = Pre-tax rate × (1 – Tax rate)   →   e.g., 15% × (1–0.30) = 10.5%')
note('Interest on loan is tax-deductible → creates tax shield → reduces effective cost. This is the advantage of debt financing.')
rule()
sub('b) Cost of Priority (Preference) Share Capital (Kp)')
formula('Kp = Expected Dividend per Share ÷ Net Proceeds from Sale × 100')
body('<b>Example:</b> 10% priority share, face value Tk.1,000, sold at Tk.820.')
formula('Kp = 100 ÷ 820 × 100 = 12.20%')
note('Company not always bound to pay priority dividend, but usually does when profitable.')
rule()
sub('c) Cost of General (Equity) Share Capital (Ke)')
body('<b>Method 1 — Zero Dividend Growth:</b>')
formula('Ke = Dividend<sub>1</sub> ÷ Share Price<sub>0</sub>  [× 100]')
body('<b>Example:</b> Share price = Tk.110; Dividend = Tk.10. → Ke = 10/110 = 9.09%')
sp(3)
body('<b>Method 2 — Constant Dividend Growth (Gordon Growth Model):</b>')
formula('Ke = [Dividend<sub>0</sub> × (1 + g)] ÷ Share Price<sub>0</sub> + g')
body('<b>Example:</b> Price = Tk.150; Dividend = Tk.15; Growth = 5%.')
formula('Ke = [15 × 1.05 ÷ 150] + 0.05 = 0.105 + 0.05 = 15.5%')
rule()
sub('d) Cost of Retained Earnings (Reserved Income)')
body('Has <b>opportunity cost</b> — shareholders forgo income they could earn elsewhere. Cost = same rate as equity shareholders\' expected return.')
body('If company retained profit instead of distributing, and shareholders could earn 15% elsewhere → 15% is the opportunity cost of retained earnings.')
rule()

section('6.4 Average (Weighted) Cost of Capital (WACC)')
formula('WACC = Σ (Cost of each source × Weight of that source in total capital)')
body('<b>Example:</b> General share: Tk.2,000M (40%); Loan: Tk.2,000M (40%); Priority share: Tk.1,000M (20%).')
body('Loan i=10%, Tax=40% → Kd=6%. Priority share 8%, price=Tk.110 → Kp=7.27%. General share: Div=Tk.13, price=Tk.255, g=4% → Ke=9.30%.')
formula('WACC = (9.30 × 0.40) + (6 × 0.40) + (7.27 × 0.20) = 3.72 + 2.40 + 1.454 = 7.57%')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 7 — SHARE, BOND AND DEBENTURE
# ═══════════════════════════════════════════════════════════════
chapter_header(7, 'Share, Bond and Debenture')

section('7.1 Concept of Share')
key('Share', 'Small unit of total capital of a public limited company. Shareholders = co-owners. Earn dividend. Capital is NOT refundable unless sold in secondary market.')

section('7.2 Types of Share')
box_table([
    ['Type','Features','Adv.','Disadv.'],
    ['General (Ordinary) Share','Ownership + voting rights. Variable dividend — not fixed. Residual claim (paid last). Easily transferable (Dhaka/Chittagong Stock Exchange).','Potentially higher income; limited liability; liquidity.','Risky; last claim on profit and assets.'],
    ['Priority (Preference) Share','Fixed dividend rate. No voting right. Paid before general shareholders. Can be convertible.','Fixed income; priority over general shareholders.','No control; limited/fixed income.'],
    ['Deferred Share','Paid after all other shareholders. Usually held by founders/promoters. Also called promoter share.','Founders maintain control.','Last to receive dividend/assets.'],
    ['Right Share','Offered to existing shareholders first when new shares issued.','Existing owners protected from dilution.','—'],
    ['Bonus Share','Undistributed earnings converted to free shares (stock dividend). Proportionate to existing holdings.','Increases number of shares. Tax-efficient.','No cash received.'],
], col_widths=[3*cm,5.5*cm,3*cm,3*cm])

section('7.3 Bond')
body('Bond = <b>loan capital with mortgage/security</b>. Investors are creditors, not owners. No voting right.')
box_table([
    ['Feature','Detail'],
    ['Mortgage','Property/documents kept as security. If company defaults → investors sell assets.'],
    ['Date of Maturity','Specific date when face value is repaid.'],
    ['Interest','Fixed rate; paid before all others from company income.'],
    ['Claims on Closure','Bond holders paid FIRST before preference and general shareholders.'],
    ['Transformability','Some bonds convertible to general shares.'],
], col_widths=[4*cm,11.5*cm])

section('7.4 Debenture')
body('<b>Debenture = Bond WITHOUT mortgage/security.</b> Otherwise same as bond. Issued mainly by large, reputed companies. Not common in Bangladesh yet.')
box_table([
    ['','Bond','Debenture','Priority Share','General Share'],
    ['Security/Mortgage','Yes','No','No','No'],
    ['Fixed Rate','Yes','Yes','Yes','No'],
    ['Voting Right','No','No','No','Yes'],
    ['Claim Order','1st','2nd','3rd','Last'],
    ['Ownership','Creditor','Creditor','Partial Owner','Full Owner'],
], col_widths=[3.5*cm,3*cm,3*cm,3.5*cm,2.5*cm])

section('7.5 Share Market of Bangladesh')
bullet('<b>Two Stock Exchanges:</b> Dhaka Stock Exchange (DSE) and Chittagong Stock Exchange (CSE).')
bullet('<b>DSE Indices:</b> DSE Broad Index (DSEX), DSE Shariah Index, DSE 30 Index.')
bullet('<b>CSE Indices:</b> CSE All Shares Price Index, CSE Selective Categories Index, CSE 30 Index.')
bullet('<b>Share Categories:</b> A, B, G, N, Z (based on dividend payment history, etc.).')
bullet('<b>Important analysis before investing:</b> EPS (Earnings Per Share), NAV (Net Asset Value), management quality, industry sector, economic condition. Never invest on rumour.')

section('7.6 Primary vs. Secondary Market')
bullet('<b>Primary Market:</b> Company sells shares for the first time → IPO (Initial Public Offering). Investors buy directly from company.')
bullet('<b>Secondary Market:</b> Investors trade shares among themselves. DSE and CSE are secondary markets.')

section('7.7 Dividend and Dividend Policy')
body('<b>Dividend</b> = portion of company profit distributed to shareholders. Two types:')
bullet('<b>Cash Dividend:</b> Paid in cash. E.g., 10% on Tk.5,000 investment = Tk.500.')
bullet('<b>Stock/Bonus Dividend:</b> Free shares given instead of cash. Increases total shares outstanding.')
body('<b>Three Dividend Policies:</b>')
bullet('<b>Fixed Money Dividend Policy:</b> Same amount every year regardless of profit.')
bullet('<b>Dividend Payment Ratio Policy:</b> Fixed % of profit distributed every year.')
bullet('<b>Fixed + Additional Dividend Policy:</b> Minimum fixed dividend + extra when profits allow. Ideal for companies with irregular income.')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 8 — CURRENCY, BANK & BANKING
# ═══════════════════════════════════════════════════════════════
chapter_header(8, 'Currency, Bank and Banking')

section('8.1 History of Currency')
body('Earliest: <b>Barter System</b> — direct exchange of goods. Problem: double coincidence of wants. Evolution: kowri → ivory/stone/pearl → metal coins (bronze, silver, gold) → paper money (19th century). Paper money advantages: abundant, light, easy to carry, security features.')

section('8.2 Functions of Currency (Money)')
bullet('<b>Medium of Exchange:</b> Facilitates all transactions (primary function).')
bullet('<b>Measure of Value:</b> Determines price of goods and services.')
bullet('<b>Means of Savings:</b> Store value for future use.')
bullet('<b>Standard of Deferred Payment:</b> Enables lending and borrowing.')

section('8.3 Currency & Bank Relationship')
body('"<b>Currency is the mother of banking system.</b>" Without currency, banking cannot exist. Bank collects surplus savings → pays interest → lends to borrowers at higher rate → earns profit.')

section('8.4 Bank, Banking, Banker')
key('Bank','A financial institution that collects deposits from people against interest, makes investments for profit, and is bound to return money on demand or after a fixed time.')
key('Banking','All legal activities of a bank — deposit collection, loan sanction, bill discounting, foreign trade finance, money transfer, locker services, asset management.')
key('Banker','People directly involved in banking business. Requires education and training in banking.')
body('<b>Etymology of "Bank":</b> From Latin words <i>Banco / Banak / Banque / Bancus</i> = bench/long table. Lombardy Street merchants in Italy used benches to conduct money business in the Middle Ages.')

section('8.5 History & Evolution of Banking in Bangladesh')
box_table([
    ['Period','Key Event'],
    ['5000 BC','First banking activities (Babylonian Civilization)'],
    ['400 BC','Greek/Roman/Chinese/Babylonian civilizations contributed'],
    ['1700 AD','Hindustan Bank established in India'],
    ['1935','Reserve Bank of India established'],
    ['1948','State Bank of Pakistan established (controlled East & West Pakistan banking)'],
    ['26 March 1972 (eff. 16 Dec 1971)','Bangladesh Bank established by President\'s Order No.127'],
    ['Post-liberation','1090 branches of 12 banks. 6 nationalised banks created: Sonali, Agrani, Janata, Rupali, Pubali, Uttara Bank'],
    ['1980s','Denationalisation began. Private banks permitted.'],
    ['Present','4 Govt., 4 Specialised, 30+ Private banks operating in Bangladesh'],
], col_widths=[4*cm,11.5*cm])

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 9 — BANKING BUSINESS AND TYPES
# ═══════════════════════════════════════════════════════════════
chapter_header(9, 'Banking Business and Types')

section('9.1 Objectives of Bank')
sub('From Owner/Management Perspective')
bullet('Investment of fund → earn profit; protect owner image through goodwill; social contribution (portion of profit in social activities); participate in national development.')
sub('From Government/State Perspective')
bullet('Currency circulation; capital formation; investment & industrialisation (priority sectors); controlling money market; employment generation.')
sub('From Client Perspective')
bullet('Deposit security; savings habit; advisor/consultant services (professional business evaluation); representative & trustee; money transfer; improving standard of living (ATM, credit card, internet banking, mobile banking).')

section('9.2 Structure of a Bank (BD Regulations)')
body('<b>Private bank (as per Bangladesh Bank):</b> Minimum 2, Maximum 13 directors.')
body('<b>Public Limited Company bank:</b> Minimum 7 members, maximum unlimited.')
body('No bank can operate in Bangladesh without <b>approval of Bangladesh Bank</b>. Unauthorised banks (even cooperative) = illegal.')

section('9.3 Principles of Banking')
box_table([
    ['Principle','Explanation'],
    ['Security','Ensure security of both client deposits and loans. Evaluate financial solvency and honesty before lending.'],
    ['Profitability','Charge higher interest on loans than paid on deposits. Difference = main profit.'],
    ['Liquidity','Maintain sufficient liquid assets to meet withdrawal demands at any time.'],
    ['Social Welfare','Participate in national development; not purely profit-driven.'],
    ['Efficiency','Skilled management; efficient service delivery.'],
], col_widths=[4*cm,11.5*cm])

section('9.4 Classification of Banks')
box_table([
    ['Classification Basis','Types'],
    ['By Function','Central Bank, Commercial Bank, Investment Bank, Agricultural Bank, Industrial Bank, Cooperative Bank, Exchange Bank, Consumer Credit Bank'],
    ['By Ownership','Government (Nationalized): Sonali, Agrani, Janata, Rupali; Specialised: BSB, BKB, RAKUB, BSRS; Private: Prime Bank, BRAC Bank, Dutch-Bangla, etc.; Foreign: Citibank, HSBC, Standard Chartered'],
    ['By Activity Area','Local Bank, Regional Bank, National Bank, International Bank'],
    ['By Banking System','Conventional Bank, Islamic Bank (Islami Bank Bangladesh, SIBL, EXIM Bank, etc.)'],
    ['By Formation','Chain Banking, Group Banking'],
], col_widths=[4.5*cm,11*cm])

section('Key Bank Types — Definitions')
box_table([
    ['Bank Type','Key Role'],
    ['Central Bank','Banker of banks; issues currency; controls money market; lender of last resort. Bangladesh: Bangladesh Bank.'],
    ['Commercial Bank','Accepts deposits; provides short & medium-term loans; main banking institution. BD: Sonali, Janata, Prime Bank.'],
    ['Investment Bank','Finances long-term industrial projects; capital market operations.'],
    ['Agricultural Bank','Credit for agriculture sector. BD: Bangladesh Krishi Bank (BKB), RAKUB.'],
    ['Industrial Bank','Long-term industrial loans. BD: Bangladesh Shilpa Bank (BSB).'],
    ['Cooperative Bank','Formed by cooperative societies; rural credit.'],
    ['Exchange Bank','Facilitates foreign exchange transactions.'],
    ['Islamic Bank','Interest-free banking based on Sharia law. BD: Islami Bank Bangladesh Ltd.'],
    ['Chain Banking','Several banks managed under single ownership/management.'],
    ['Group Banking','Holding company controls group of banks.'],
    ['Grameen Bank','Microcredit to rural poor (esp. women); collateral-free. Founded by Dr. Muhammad Yunus (Nobel 2006).'],
], col_widths=[3.5*cm,12*cm])

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 10 — INTRODUCTION TO COMMERCIAL BANKS
# ═══════════════════════════════════════════════════════════════
chapter_header(10, 'An Introduction to Commercial Banks')

section('10.1 Definition & Concept')
key('Commercial Bank', 'Profit-oriented financial institution that collects deposits, provides loans, and creates mediums of exchange (cheques, bills, draft). Handles short, medium and long-term credit.')

section('10.2 Objectives of Commercial Banks')
bullet('Making profit (fundamental goal).')
bullet('Introducing mediums of exchange (cheques, bills of exchange, debit/credit cards).')
bullet('Capital formation from scattered public savings.')
bullet('Welfare of people (indirect goal).')
bullet('Assisting central bank in loan regulation and monetary policy.')
bullet('Proper distribution of wealth; employment generation; mitigating rich-poor gap.')
bullet('Savings tendency formation; money security; economic stability.')
bullet('Development of trade and industries; improving standard of living.')

section('10.3 Functions of Commercial Banks')
sub('A) Main Functions')
bullet('<b>Receiving Deposits & Paying Interest:</b> Current (no interest, many services), Savings (interest ~5-7%), Fixed Deposit (interest 12-13%, cannot withdraw early without penalty).')
bullet('<b>Capital Creation:</b> Accumulates separate savings into capital pool.')
bullet('<b>Granting Loans & Charging Interest:</b> Main income source. Charges higher rate than it pays on deposits.')
bullet('<b>Creating Loan Deposits:</b> When loan sanctioned → account opened in borrower\'s name → amount credited. This creates "credit money."')
bullet('<b>Creating Medium of Exchange:</b> Cheque, bill of exchange, certificate, bank draft, pay order, debit card, credit card.')
bullet('<b>Issue Notes (Indirect):</b> Not directly (only central bank issues notes). Indirectly: bank cheques serve as currency alternative.')
bullet('<b>Trustee Service:</b> Safeguard client property; issue solvency certificates.')
bullet('<b>Import-Export Assistance:</b> Currency conversion; Letter of Credit (LC); representative services.')
bullet('<b>Government Treasury Service:</b> Selected banks serve as government treasury.')
bullet('<b>Discounting Bills of Exchange:</b> Pays discounted value in advance; collects full amount at maturity.')
sub('B) Special Functions')
bullet('Investment of capital in industrial/commercial organisations.')
bullet('Money transfer (domestic and international).')
bullet('Security of money and valuables (locker service).')
bullet('Guidance on business decisions; property management.')
bullet('Employment generation (direct and indirect through lending).')
bullet('Loan regulation assistance (expands/contracts credit supply).')
bullet('Agricultural and industrial development loans.')

section('10.4 Sources of Income of Commercial Banks')
box_table([
    ['Source of Income','Detail'],
    ['Interest on Loans','Primary income — difference between lending & deposit rates.'],
    ['Investment Income','Profit from shares, government securities, letters of credit.'],
    ['Bill Discount','Discounted payment of bills of exchange in advance.'],
    ['Commissions','Bank drafts, traveller\'s cheques, agency services.'],
    ['Correspondence Fees','Charges for correspondence services.'],
    ['Locker Rent','Fee for safekeeping valuables.'],
    ['Brokerage','Commission on share purchase/trading.'],
    ['Foreign Exchange','Profit from buying/selling foreign currency.'],
    ['Import/Export','Commission/service charges for international trade facilitation.'],
    ['Letter of Credit','Commission for issuing LC on behalf of importers.'],
    ['Trustee Fee','Charges for trustee services.'],
], col_widths=[4.5*cm,11*cm])

section('10.5 Expenditures of Commercial Banks')
body('Interest paid to depositors; interest to central bank/other banks; salaries & allowances; director/manager allowances; auditor charges; legal costs for loan recovery; office rent; taxes; insurance premium; communication costs (SWIFT, fax, telex); advertisement; staff training.')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 11 — BANK DEPOSIT
# ═══════════════════════════════════════════════════════════════
chapter_header(11, 'Bank Deposit')

section('11.1 Purposes and Importance of Bank Deposit')
box_table([
    ['For Clients','For the Bank','National Economy'],
    ['Security of money','Collecting deposit','Creating saving habit'],
    ['Business transaction','Investment','Capital formation'],
    ['Loan facility','Foreign exchange','Investment & production'],
    ['Risk-free investment','—','Employment generation'],
    ['Availing services','—','International trade'],
    ['Meeting excess fund demand','—','—'],
], col_widths=[5.2*cm,3.8*cm,6.5*cm])

section('11.2 Types of Bank Accounts')
box_table([
    ['Account Type','Who Opens It','Interest','Withdrawal Flexibility','Special Features'],
    ['Current Account','Businesspersons, companies','None','Unlimited (any time)','Overdraft facility; no interest but many services.'],
    ['Savings Account','Salaried/fixed income persons','Low (~5-7%)','Limited (2×/week or regulated)','Most common; balance earns interest.'],
    ['Fixed Deposit (FDR)','Anyone wanting time-bound savings','High (12-13%)','NOT allowed before maturity','Terms: 1 month to 5+ years; early withdrawal = no interest.'],
    ['School Savings Account','School students','Low','Regulated','Builds savings habit among youth.'],
    ['Insurance Savings Account','Account holders wanting insurance','Yes','Regulated','Combines life insurance + current account.'],
    ['Foreign Exchange Savings Account','Exporters/importers, frequent travellers','Yes','Restricted to foreign currency','Only foreign exchange transacted.'],
    ['Deposit Pension Scheme (DPS)','Regular savers','High','Monthly deposit; lump sum at maturity','Popular for long-term savings.'],
    ['Loan Deposit Account','Borrowers','N/A','Within sanctioned limit','Created when bank sanctions loan.'],
    ['RFCD (Resident Foreign Currency Deposit)','Citizens travelling abroad regularly','Yes','Foreign currency only','For those needing extra forex quota.'],
], col_widths=[3.8*cm,2.8*cm,1.5*cm,2*cm,5.4*cm])

section('11.3 Opening a Bank Account — Key Considerations')
body('Location, efficiency, multifarious services, foreign exchange facility, bank goodwill, number of branches, scheduled bank status, loan facility, interest rates, service tariffs, electronic banking (ATM, online, any-branch).')
body('<b>Scheduled Bank:</b> Bangladesh Bank recognises good banks as "Scheduled Banks" — considered more secure.')

section('11.4 Documents Required to Open an Account')
body('Name, NID/passport copy, occupation, photograph of client & nominee, sources of income, amount of deposit, present/permanent/office address, contact number. For company: trade license + board resolution.')
body('<b>To Close Account:</b> Written request + return of unused cheque-book, passbook, debit/credit card. No outstanding loan required.')

section('11.5 Electronic Banking Products')
box_table([
    ['Product','Function'],
    ['Debit Card','Withdraw money from ATM or purchase using existing account balance. Account required.'],
    ['Credit Card','Purchase on credit even without account balance. Personal loan facility; interest charged after period. No bank account required.'],
    ['ATM (Automated Teller Machine)','Withdraw cash, check balance, deposit cheques 24 hours/day without staff.'],
    ['Phone/Call Banking','Banking services via phone after identity verification.'],
    ['SMS Banking','Account balance info, cheque book requests via SMS.'],
    ['Internet Banking','Account management, bill payment, statement viewing via bank website + password.'],
    ['Any Branch Banking (Online)','Transact from any branch of same bank anywhere in country.'],
    ['Mobile Banking','Banking via mobile phone (e.g., bKash, Nagad, Rocket in BD context).'],
], col_widths=[4*cm,11.5*cm])
note('BD context: E-banking providing money transfer, remittance delivery, and 24-hour service to rural areas. Large initial investment; serviced by fewer skilled employees earning commission.')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 12 — BANK AND CLIENT
# ═══════════════════════════════════════════════════════════════
chapter_header(12, 'Bank and Client')

section('12.1 Nature of Bank-Client Relationship')
box_table([
    ['Relationship Type','Description'],
    ['Debtor-Creditor','When client deposits → bank = debtor, client = creditor. Reversed when bank lends.'],
    ['Contractual','Opens with account opening. Creates rights/obligations for both parties.'],
    ['Trustee','Bank protects client valuables/documents via locker service.'],
    ['Mortgage Provider-Receiver','Bank provides loan against client\'s property as collateral.'],
    ['Agency','Bank collects receivables and pays dues on behalf of clients.'],
], col_widths=[4.5*cm,11*cm])

section('12.2 Bank\'s Responsibilities towards Clients')
bullet('<b>Pay back money:</b> Must return client money when demanded (current/savings: via cheque; fixed: on maturity).')
bullet('<b>Account secrecy:</b> Never disclose client information EXCEPT when ordered by Court, Bangladesh Bank, or the client themselves.')
bullet('<b>Carry out depositor\'s orders:</b> Pay specified parties, collect receivables as instructed.')
bullet('<b>Interest and service fee exchange:</b> Collect and credit receivable interest to client\'s account.')
bullet('<b>Easy loan repayment opportunity:</b> Fair dealing with borrower; give adequate time and opportunity.')

section('12.3 Client\'s Responsibilities towards the Bank')
bullet('<b>Honesty:</b> Disclose all required information accurately when opening an account.')
bullet('<b>Loan repayment:</b> Pay instalments on schedule. Default → bank may seize and sell mortgaged property by law.')
bullet('<b>Interest payment:</b> Pay interest on overdraft and loan as per contract.')
bullet('<b>Cautiousness with cheques:</b> Correct signature, correct date, sufficient balance, correct payee name.')

section('12.4 Types of Cheque')
box_table([
    ['Type','Description'],
    ['Bearer Cheque','Paid to whoever presents it. Bank pays to bearer on demand within specified time.'],
    ['Order Cheque','Paid ONLY to named person. Cannot be encashed without that named payee.'],
    ['Crossed Cheque','Two parallel lines drawn in top-left corner. "A/C Payee" or "& Co." written between lines. Money credited to account only — NOT paid in cash. More secure.'],
], col_widths=[4*cm,11.5*cm])

section('12.5 Termination of Bank-Client Relationship')
body('<b>Reasons the relationship dissolves:</b>')
bullet('Client declared <b>bankrupt</b> by court.')
bullet('Client suffers <b>mental disorder</b> (incapable of transaction).')
bullet('<b>Garnishee order</b> by court forces account closure.')
bullet('<b>Bank\'s own decision:</b> if client violates bank rules.')
bullet('<b>Client\'s decision:</b> client no longer wants account.')
bullet('<b>War:</b> parties separated by enemy territory.')
bullet('<b>Complete balance transfer:</b> all funds moved to another bank.')
bullet('<b>Death</b> of client.')
bullet('<b>Long-term inactivity:</b> no transaction for prolonged period → dormant/auto-closed.')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  CH 13 — CENTRAL BANK
# ═══════════════════════════════════════════════════════════════
chapter_header(13, 'Central Bank')

section('13.1 Definition & Concept')
key('Central Bank (Prof. R.S. Sayers)', '"The organ of government that undertakes major financial operations of the government and influences the behaviour of financial institutions to support economic policy."')
key('Central Bank (Kisch & Elkin)', '"A bank whose essential duty is to maintain stability of the monetary standard."')
key('Central Bank (Dr. S.N. Sen)', '"Central Bank is as the leader of banking society, the King and the Sun — rules banking sector like a leader."')
body('Established in 17th century when controlling the money market became crucial. <b>Non-profitable, public welfare-based national institution.</b>')

section('13.2 Objectives of Central Bank')
body('<b>16 Key Objectives:</b>')
bullet('Strong money market formation and control.')
bullet('Economic development through planning and implementation.')
bullet('Notes and currency circulation (according to market demand).')
bullet('Controlling foreign currency and exchange rate.')
bullet('Maintain home currency value (positive balance of trade).')
bullet('Banker of other banks — builds scheduled and non-scheduled bank efficiency.')
bullet('Acts as clearing house — resolves inter-bank transactions.')
bullet('Credit control — provides credit; prevents excess credit.')
bullet('Advises government on economic policy.')
bullet('Maintains price stability by controlling money supply.')
bullet('Bank of the government — preserves government funds; reconciles transactions.')
bullet('Public welfare — social/national activities.')
bullet('Equal distribution of wealth — invest in all regions and sectors.')
bullet('Capital formation facilitation — credit to commercial banks.')
bullet('Organised banking system development.')
bullet('Guide of banking system — guides all other banks.')

section('13.3 Functions of Central Bank')
sub('A) General Functions')
box_table([
    ['Function','Details'],
    ['Notes & Currency Circulation','Sole authority to circulate currency (legal monopoly).'],
    ['Guardian of Money Market','Controls and monitors entire money market.'],
    ['Easy Medium of Exchange','Creates currency, bills, hundi etc.'],
    ['Credit Control','Mechanisms: Bank Rate Policy, Open Market Operations (OMO), Deposit Rate changes.'],
    ['Controls Purchasing Power','Increases/decreases money supply to maintain currency value.'],
    ['Controls Foreign Exchange','Manages exchange rate; preserves home currency prestige.'],
    ['Price Level Stability','Controls money supply to stabilise prices.'],
    ['Foreign Currency Reserve','Maintains adequate forex reserve; exchange rate depends on it.'],
    ['Banking Development','Develops infrastructure of entire banking sector.'],
    ['Employment Creation','Approves new branches → creates jobs.'],
    ['Monitors Govt. Loans','Monitors use and repayment of government loans.'],
], col_widths=[5*cm,10.5*cm])

sub('B) Functions as Government Bank')
bullet('Source of credit for government in financial crisis.')
bullet('Maintains government fund, assets and documents.')
bullet('Maintains different government accounts.')
bullet('Handles government transactions and documents.')
bullet('Purchases and sells foreign currency on behalf of government.')
bullet('Acts as advisor in planning, policy making and implementation.')
bullet('Collects and maintains information and statistics.')
bullet('Builds international relationships (IMF, World Bank, foreign banks).')
bullet('Acts as government representative domestically and internationally.')

sub('C) Banker of Other Banks')
bullet('<b>Approving & Scheduling:</b> Approves establishment of new banks; schedules them.')
bullet('<b>Branch Opening:</b> Provides approval for new branches.')
bullet('<b>Clearing House:</b> Resolves inter-bank transactions through clearing houses.')
bullet('<b>Lender of Last Resort:</b> Provides emergency financial support when no other source available.')
bullet('<b>Controls Commercial Banks:</b> Enforces rules, regulations and policies.')
bullet('<b>Examines Accounts:</b> Audits commercial bank accounts.')
bullet('<b>Advisor/Consultant:</b> Provides banking advice and consultancy.')
bullet('<b>Statutory Reserve (CRR/SLR):</b> All scheduled banks must deposit specified % of total deposits with central bank.')
bullet('<b>Representative of All Banks:</b> Represents scheduled banks collectively.')
bullet('<b>Loan Recovery Support:</b> Assists in recovering bad loans.')
bullet('<b>International Trade Development:</b> Supports commercial banks in expanding international trade.')

sub('D) Other (Development) Functions')
bullet('Agricultural development — establishes agricultural banks; low-interest agricultural loans.')
bullet('Industrial development — motivational plans for industry.')
bullet('Cooperative bank development.')
bullet('Research-based activities for trade/commerce development.')
bullet('Ensures proper utilisation of floated loan.')

section('13.4 Bangladesh Bank — Formation and Management')
body('<b>Bangladesh Bank founded:</b> 31 October 1972 (effective from 16 December 1971) by <b>President\'s Order No. 127.</b>')
body('Established at the Dhaka office of the local Deputy Governor of the then <b>State Bank of Pakistan.</b>')
body('<b>Management Hierarchy:</b>')
box_table([
    ['Position','Number'],
    ['Governor (Chief Executive)','1'],
    ['Deputy Governor','4'],
    ['Executive Director','12'],
    ['Financial Advisor','1'],
    ['General Manager → System Manager → Other Officers & Staff','Hierarchical'],
], col_widths=[6*cm,9.5*cm])

section('13.5 Divisions of Bangladesh Bank')
body('<b>9 Divisions:</b> (1) Note Issuing, (2) Banking, (3) Accounts, (4) Administrative, (5) Banking Control, (6) Bank Auditing, (7) Exchange Control, (8) Statistics, (9) Secretariat.')

section('13.6 Relationship — Central Bank & Commercial Banks')
box_table([
    ['Relationship','Description'],
    ['Statutory Reserve','Commercial banks must maintain fixed % of deposits with central bank as statutory reserve (CRR).'],
    ['Clearing House','Central bank provides clearing house facility — fosters good relationship.'],
    ['Working Paper','Commercial banks send weekly/monthly working papers; central bank analyses and guides.'],
    ['Information Provider','Central bank collects worldwide money market & economic information.'],
    ['Liquidity Monitoring','Central bank monitors commercial banks\' liquidity position to protect clients.'],
    ['Guardian Role','Central bank = guardian of commercial banks.'],
    ['Lender of Last Resort','Central bank lends to commercial banks when they face crisis.'],
    ['Scheduling Benefit','Advice, guidance, financial support to scheduled banks.'],
    ['Bank-Client Relationship','Commercial banks lend to clients; clients deposit savings in banks.'],
    ['Assistance','Central bank implements plans through commercial banks.'],
    ['Banker of all Banks','Most fundamental relationship.'],
], col_widths=[4*cm,11.5*cm])

section('13.7 Role of Bangladesh Bank in Economic Development')
body('<b>Key contributions of Bangladesh Bank:</b>')
bullet('Issues notes and coins (sole authority).')
bullet('Maintains foreign currency reserve.')
bullet('Conducts government accounts.')
bullet('Distributes industrial and agricultural loans through commercial banks as per government policy.')
bullet('Controls scheduled and non-scheduled banks; Monitoring Cell ties all commercial banks by rules.')
bullet('Publishes economic and statistical information.')
bullet('Handles foreign currency transfer and management.')
bullet('Research Division provides guidance through research activities.')
bullet('Monitors Rural Micro Credit and special credit projects — supports economic freedom of distressed class.')
bullet('Creates employment to eliminate poverty.')
bullet('Stabilises price level by controlling foreign exchange rate.')
bullet('Assists government in developmental activities.')
bullet('Contributes to maintaining law and order (economic impact).')

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════
#  QUICK REFERENCE — KEY TERMS & FORMULAS
# ═══════════════════════════════════════════════════════════════
chapter_header('★', 'Quick Reference — Key Terms, Formulas & BD-Specific Facts')

section('Essential Formulas — One Page')
box_table([
    ['Formula','Expression','Used In'],
    ['Simple Interest','I = P × r × n','Ch. 3'],
    ['Compound FV (Annual)','FV = PV × (1+i)^n','Ch. 3'],
    ['Compound FV (Periodic)','FV = PV × (1+i/m)^(m×n)','Ch. 3'],
    ['Present Value (Annual)','PV = FV ÷ (1+i)^n','Ch. 3'],
    ['Present Value (Periodic)','PV = FV ÷ (1+i/m)^(m×n)','Ch. 3'],
    ['EAR','EAR = (1+i/m)^m – 1','Ch. 3'],
    ['Standard Deviation','σ = √[Σ(R–R̄)² ÷ (n–1)]','Ch. 4'],
    ['ARR','(Avg. Net Profit ÷ Avg. Investment) × 100','Ch. 5'],
    ['Pay Back Period','Investment ÷ Annual CF  OR  Full years + (Remaining ÷ Next yr CF)','Ch. 5'],
    ['Cost of Loan (Tax-adjusted)','Kd = Pre-tax rate × (1–Tax rate)','Ch. 6'],
    ['Cost of Priority Share','Kp = (Dividend ÷ Net Proceeds) × 100','Ch. 6'],
    ['Cost of Equity (Zero Growth)','Ke = Dividend₁ ÷ Share Price₀','Ch. 6'],
    ['Cost of Equity (Gordon Model)','Ke = [Div₀(1+g) ÷ P₀] + g','Ch. 6'],
    ['WACC','Σ(Cost × Weight) for each source','Ch. 6'],
], col_widths=[5*cm,6*cm,2.5*cm])

section('Critical Bangladesh-Specific Facts')
box_table([
    ['Fact','Detail'],
    ['Bangladesh Bank Founded','31 October 1972 (effective 16 Dec 1971). President\'s Order No. 127.'],
    ['Bangladesh Bank Governor','Head of management (Chief Executive)'],
    ['Bangladesh Bank HQ','Motijheel, Dhaka'],
    ['Deputy Governors','4 (assist Governor)'],
    ['Executive Directors','12'],
    ['BB Divisions','9: Note Issuing, Banking, Accounts, Admin, Banking Control, Bank Auditing, Exchange Control, Statistics, Secretariat'],
    ['Nationalised Banks after Liberation','Sonali, Agrani, Janata, Rupali, Pubali, Uttara Bank (6 banks)'],
    ['Currently Govt. Banks','4 (Sonali, Agrani, Janata, Rupali)'],
    ['Stock Exchanges','DSE (Dhaka) and CSE (Chittagong)'],
    ['DSE Indices','DSEX (Broad), Shariah Index, DSE 30'],
    ['CSE Indices','CSE All Shares Price Index, CSE Selective, CSE 30'],
    ['IMF HQ','Washington DC. Founded 1945 (Bretton Woods). Members: 189.'],
    ['Grameen Bank','Microcredit; collateral-free; rural poor (esp. women). Nobel 2006 — Dr. Muhammad Yunus.'],
    ['Specialised Banks','BKB (Agriculture), RAKUB (Agriculture, NW), BSB (Industrial), BSRS (Investment)'],
    ['Islamic Banking (BD)','Islami Bank Bangladesh Ltd., SIBL, EXIM Bank, Al-Arafah Islami Bank'],
    ['First Modern Bank in India','Hindustan Bank (1700 AD)'],
    ['Barter System','Exchange of goods without money. Still exists in small scale.'],
    ['PPP','Public Private Partnership — for large govt. projects (e.g., Bangabandhu Bridge).'],
    ['NCTB Finance & Banking','Class 9-10 textbook, first published December 2012, revised September 2014.'],
], col_widths=[5.5*cm,10*cm])

section('Compare & Contrast — Key Pairs')
box_table([
    ['','Bond','Debenture'],
    ['Security','With mortgage','Without mortgage'],
    ['Risk to investor','Lower','Higher'],
    ['Popularity in BD','Low','Very low'],
    ['Interest rate','Fixed','Fixed'],
    ['Voting right','No','No'],
    ['Claim order','1st (before debenture)','2nd (after bond)'],
], col_widths=[3.5*cm,6.5*cm,5.5*cm])
sp(4)
box_table([
    ['','General Share','Priority Share'],
    ['Dividend rate','Variable (not fixed)','Fixed rate'],
    ['Voting right','Yes (control)','No'],
    ['Risk','Higher','Lower'],
    ['Dividend priority','Last among shareholders','Before general shareholders'],
    ['Claims on closure','Last','Before general; after bond/debenture'],
    ['Transferability','High (listed on exchange)','Moderate'],
    ['Convertibility','Source of all conversion','Can convert to general share'],
], col_widths=[3.5*cm,6.5*cm,5.5*cm])
sp(4)
box_table([
    ['','Primary Market','Secondary Market'],
    ['Definition','First-time sale by company','Investors trade among themselves'],
    ['Mechanism','IPO (Initial Public Offering)','Stock Exchange (DSE, CSE)'],
    ['Price','Determined by company (face/issue price)','Determined by market forces'],
    ['Participants','Company + Public investors','Investors only'],
], col_widths=[3.5*cm,6.5*cm,5.5*cm])

section('Types of Cheque — Summary')
box_table([
    ['Cheque Type','Payable To','Cash/Account','Security Level'],
    ['Bearer Cheque','Whoever presents it (bearer)','Cash directly','Low'],
    ['Order Cheque','Specifically named person only','Cash directly','Medium'],
    ['Crossed Cheque','Named account only (A/C payee)','Account credit only — NOT cash','High'],
], col_widths=[4*cm,4.5*cm,4*cm,3*cm])

section('Types of Bank Accounts — Quick Summary')
box_table([
    ['Account','Interest','Withdrawal','Best For'],
    ['Current','None','Unlimited','Businesses'],
    ['Savings','Low 5-7%','Limited (~2×/wk)','Salaried persons'],
    ['Fixed Deposit','High 12-13%','Only at maturity','Long-term savings'],
    ['DPS','High','Monthly deposit; lump sum end','Pension planning'],
    ['RFCD','Yes','Foreign currency only','Regular overseas travellers'],
], col_widths=[3.5*cm,2.5*cm,3*cm,6.5*cm])

section('Risk Types — Summary')
box_table([
    ['Risk Type','Who Faces It','Cause'],
    ['Business Risk','Firms','Volatile sales + high fixed costs. Internal finance only.'],
    ['Financial Risk','Firms with debt','Unable to repay interest/principal. External debt financing.'],
    ['Interest Rate Risk','Bond/Debenture investors','Market interest ↑ → bond value ↓'],
    ['Liquidity Risk','All investors','Cannot sell investment quickly at fair price.'],
], col_widths=[3.5*cm,3.5*cm,8.5*cm])

section('Capital Budgeting Methods — At a Glance')
box_table([
    ['Method','Formula','Considers TVM?','Decision Rule'],
    ['ARR','Avg Net Profit ÷ Avg Investment × 100','No','Higher ARR = Accept'],
    ['Pay Back Period','Investment ÷ Annual CF','No','Lower PBP = Accept'],
    ['NPV','PV of Inflows – PV of Outflows','Yes','NPV > 0 = Accept'],
    ['IRR','Rate where NPV = 0','Yes','IRR > Cost of Capital = Accept'],
], col_widths=[3*cm,4.5*cm,3*cm,5*cm])

section('Finance Evolution Decades — Memory Aid')
body('<b>1920s:</b> Unification | <b>1930s:</b> Depression & Reorganisation | <b>1940s:</b> Liquidity | <b>1950s:</b> Profit Maximisation (Traditional) | <b>1960s:</b> Shareholder Wealth (Modern Finance) | <b>1970s:</b> Computers & Mathematics | <b>1980s:</b> Capital Efficiency | <b>1990s+:</b> Globalisation & WTO')

sp(6)
rule()
body('<i>This document covers all 13 chapters of the NCTB Finance & Banking textbook (Classes 9-10) comprehensively prepared for the Bangladesh Bank Additional Director Examination. All definitions, principles, formulas, classifications, and Bangladesh-specific contextual facts are preserved.</i>')

doc.build(story)
print("PDF created successfully.")
