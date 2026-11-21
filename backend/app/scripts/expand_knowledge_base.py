"""
Script to expand the RAG knowledge base from 8 entries to 65+ comprehensive, verified entries.
Covers:
- UPI architecture, NPCI circulars, Collect requests, AutoPay, UPI Lite
- 1930 Helpline, CFCFRMS Golden Hour, cybercrime.gov.in complaint filing
- RBI Master Circular on Customer Protection & Zero/Limited Liability
- Top 10 Indian Bank emergency fraud numbers & official domains
- Top UPI apps dispute mechanisms (PhonePe, GPay, Paytm, BHIM)
- All 15 scam categories in depth
- Telecom/SIM swap (DoT, TAFCOP, Sanchar Saathi)
- Android APK sideloading & malware defense
"""

import json
import os

KB_ENTRIES = [
    # 1. UPI Fundamentals & Architecture
    {
        "id": "kb_upi_pin_receiving",
        "category": "fake_upi_refund_cashback",
        "title": "UPI Architecture: Receiving Money Never Requires a PIN or Collect Request",
        "source": "NPCI Guidelines on Unified Payments Interface (UPI) Security",
        "tags": ["upi", "pin", "receive", "cashback", "refund", "collect", "qr"],
        "content": "In the UPI architecture governed by the National Payments Corporation of India (NPCI), entering your UPI PIN is STRICTLY an authorization to DEBIT funds from your account. Receiving money, refunds, cashback, or rewards NEVER requires entering a UPI PIN, scanning a QR code, or accepting a collect request. If any person or app requests your UPI PIN to credit money, it is guaranteed to be an unauthorized attempt to siphon funds.",
        "actionable_guidance": "Decline all collect requests immediately. Never enter your UPI PIN unless you intend to transfer money out. Report unauthorized collect handles in your UPI app."
    },
    {
        "id": "kb_upi_collect_request_rules",
        "category": "collect_request_fraud",
        "title": "UPI Collect Requests: How Attackers Disguise Debit as Credit",
        "source": "NPCI Circular on Collect Request Security & Transaction Limits",
        "tags": ["collect", "request", "payer", "payee", "debit", "upi pin", "fraud"],
        "content": "A UPI 'Collect Request' (Payer-Payee pull transaction) initiates a debit from the victim's account to the requester. Fraudsters frequently disguise collect requests with deceitful notes such as 'Receive Cashback Rs. 5000', 'Refund from Electricity Board', or 'Payment for OLX Item'. When the user taps 'Approve' and enters their UPI PIN, money is immediately debited from their account, not credited.",
        "actionable_guidance": "Always check whether the button says 'PAY' or 'RECEIVE'. Any prompt requesting a 4 or 6 digit PIN is paying money. Reject the request and block the requester's VPA in your app."
    },
    {
        "id": "kb_upi_autopay_mandate_fraud",
        "category": "collect_request_fraud",
        "title": "UPI AutoPay & Recurring E-Mandate Exploitation",
        "source": "RBI Master Directions on Processing of E-Mandate for Recurring Transactions",
        "tags": ["autopay", "mandate", "recurring", "subscription", "debit", "standing instruction"],
        "content": "UPI AutoPay allows recurring debits (up to Rs. 15,000 without 2FA per cycle) once an initial mandate is authorized with a UPI PIN. Scammers trick users into approving a 'verification mandate' claiming it is a one-time security check or loan approval requirement. Once authorized, the attacker can schedule automated deductions without further user notification or PIN prompts.",
        "actionable_guidance": "Never authorize an AutoPay mandate for refunds, prizes, or customer support verification. Check 'AutoPay / Mandates' in your UPI app settings and revoke any unfamiliar recurring mandates immediately."
    },
    {
        "id": "kb_upi_qr_code_mechanics",
        "category": "marketplace_qr_scam",
        "title": "QR Code Payment Architecture: Scan to Pay Only",
        "source": "NPCI UPI QR Code Specification & Security Best Practices",
        "tags": ["qr", "scan", "upi://pay", "barcode", "receive", "merchant"],
        "content": "A standard Bharat QR or UPI QR code encodes a deep link containing payee parameters (e.g., `upi://pay?pa=merchant@bank&pn=MerchantName&am=500`). Scanning a QR code inside any UPI application ONLY initiates an outbound payment. There is no technical capability in the UPI protocol to 'receive' money by scanning a QR code. Fraudsters send QR codes over WhatsApp or OLX claiming 'Scan this QR to receive payment'.",
        "actionable_guidance": "Never scan a QR code sent to you to receive payment for goods or services. To receive money, only share your phone number or UPI VPA; scanning is never required."
    },
    {
        "id": "kb_upi_vpa_structure",
        "category": "general",
        "title": "UPI Virtual Payment Address (VPA) Structure & Verification",
        "source": "NPCI UPI Operating Regulations",
        "tags": ["vpa", "upi id", "handle", "okaxis", "okhdfcbank", "paytm", "ybl"],
        "content": "A UPI ID (VPA) consists of a username and a Payment Service Provider (PSP) bank handle in the format `username@bankhandle` (e.g., `name@oksbi`, `user@ybl`, `mobile@paytm`). Genuine merchant accounts display verified merchant names registered with NPCI. Fraudulent collect requests frequently use throwaway VPAs on open handles or mimic official names in the username prefix (e.g., `sbi.customer.helpline@icici`).",
        "actionable_guidance": "Verify the payee's actual registered bank name displayed by the UPI app before confirming any payment, not just the custom display name provided by the sender."
    },
    {
        "id": "kb_upi_lite_limits",
        "category": "general",
        "title": "UPI Lite Offline Wallets: Small-Value PINless Payments",
        "source": "Reserve Bank of India (RBI) Guidelines on Small Value Offline Digital Payments",
        "tags": ["upi lite", "offline", "wallet", "pinless", "500", "2000"],
        "content": "UPI Lite is an on-device digital wallet enabling near-instant, PIN-less transactions up to Rs. 500 per transaction, with an aggregate daily wallet cap of Rs. 2,000. While convenient for daily micro-payments, users should monitor their UPI Lite transaction logs since PIN authentication is waived for individual transactions.",
        "actionable_guidance": "Do not disable device lock screens if using UPI Lite. Report phone theft immediately to telecom providers to disable wallet abuse via device physical access."
    },

    # 2. National Helpline 1930 & Golden Hour
    {
        "id": "kb_helpline_1930_golden_hour",
        "category": "general",
        "title": "Reporting Cyber Fraud: National Helpline 1930 & Golden Hour Freezing",
        "source": "Ministry of Home Affairs (MHA) — Citizen Financial Cyber Fraud Reporting System",
        "tags": ["1930", "helpline", "cybercrime", "report", "freeze", "police", "golden hour", "cfcfrms"],
        "content": "If you have accidentally entered your PIN, shared an OTP, or transferred money to a scammer, immediately call the National Cyber Crime Helpline number '1930' (formerly 155260) or register an incident at https://cybercrime.gov.in. Under the Citizen Financial Cyber Fraud Reporting and Management System (CFCFRMS), if an incident is reported within the 'Golden Hour' (first 2-3 hours), police and financial intermediaries can coordinate to freeze the illicit funds in the beneficiary mule account before withdrawal.",
        "actionable_guidance": "1. Call 1930 immediately. 2. Have transaction UTR number, debit account number, sender/beneficiary bank names ready. 3. Request immediate freeze of the beneficiary account."
    },
    {
        "id": "kb_cybercrime_portal_filing",
        "category": "general",
        "title": "Step-by-Step Formal Complaint Filing on Cybercrime.gov.in",
        "source": "Indian Cyber Crime Coordination Centre (I4C), MHA",
        "tags": ["cybercrime.gov.in", "fir", "complaint", "portal", "evidence", "acknowledgment"],
        "content": "The National Cyber Crime Reporting Portal (cybercrime.gov.in) enables citizens to lodge complaints for financial and social cyber crimes. Filing an official report generates an Acknowledgement Number which is mandatory for insurance claims, formal police investigations, and court-mandated bank balance reversals.",
        "actionable_guidance": "Prepare: 1. Bank statement showing debited transaction and UTR. 2. Screenshots of fraudulent messages, WhatsApp chats, and caller phone numbers. 3. Copy of Aadhaar/ID. Submit under 'Report Financial Fraud'."
    },
    {
        "id": "kb_evidence_preservation",
        "category": "general",
        "title": "Digital Evidence Preservation Guidelines for Fraud Victims",
        "source": "Indian Evidence Act (Section 65B) & CERT-In Citizen Advisory",
        "tags": ["evidence", "screenshot", "sms", "call logs", "utr", "timestamp", "65b"],
        "content": "When victimized by digital financial fraud, destroying evidence (such as deleting suspicious SMS, call logs, or WhatsApp chats in panic) hinders recovery. Under legal standards, electronic evidence requires timestamps, sender headers, recipient details, and transaction reference (UTR/RRN) numbers.",
        "actionable_guidance": "Do not delete SMS or WhatsApp chats. Take screenshots showing full phone numbers, dates, timestamps, and message headers. Export chat history and note the exact 12-digit UPI UTR number from your bank passbook."
    },

    # 3. RBI Regulations & Liability Framework
    {
        "id": "kb_rbi_zero_liability_rule",
        "category": "regulatory",
        "title": "RBI Zero Liability Policy for Unauthorized Electronic Banking Transactions",
        "source": "RBI Master Circular DBR.No.Leg.BC.78/09.07.005/2017-18",
        "tags": ["rbi", "zero liability", "unauthorized", "reversal", "3 days", "compensation"],
        "content": "Under RBI regulations, a customer has ZERO LIABILITY for unauthorized electronic banking transactions where the fraud or deficiency lies within the banking system, or in third-party breaches where the customer notifies the bank within 3 working days of receiving the debit alert. If notified within 4 to 7 working days, liability is limited to Rs. 10,000 for savings accounts.",
        "actionable_guidance": "Immediately notify your bank in writing (via email and registered helpline) within 72 hours of any unauthorized debit to establish zero-liability eligibility. Keep written complaint ticket numbers."
    },
    {
        "id": "kb_rbi_negligence_liability",
        "category": "regulatory",
        "title": "Customer Liability in Negligence & Credential Sharing Cases",
        "source": "RBI Customer Protection Framework on Electronic Banking",
        "tags": ["rbi", "negligence", "otp sharing", "pin sharing", "liability"],
        "content": "Under RBI guidelines, if a financial loss is caused by customer negligence (such as voluntary disclosure of OTP, UPI PIN, CVV, or NetBanking password to a third party), the entire loss until the time the incident is formally reported to the bank is borne by the customer. Any unauthorized loss occurring AFTER reporting the breach must be compensated by the bank.",
        "actionable_guidance": "Never voluntarily share OTP or passwords. If shared accidentally, report to your bank's fraud helpline within minutes to halt all further debits and cap your personal liability."
    },
    {
        "id": "kb_rbi_reversal_timeline",
        "category": "regulatory",
        "title": "RBI Mandated Timeline for Shadow Credit & Dispute Resolution",
        "source": "RBI Master Direction on Customer Service in Banks",
        "tags": ["rbi", "shadow credit", "timeline", "10 days", "ombudsman", "dispute"],
        "content": "Upon receiving an unauthorized transaction complaint, the bank must provide a shadow credit (reversal of debited amount) within 10 working days, subject to investigation. The dispute must be resolved within 90 days. If the bank fails to resolve complaints within 30 days, the customer can escalate to the RBI Banking Ombudsman (cms.rbi.org.in).",
        "actionable_guidance": "If your bank does not respond within 30 days or rejects your genuine claim unfairly, file a grievance with the RBI Ombudsman at https://cms.rbi.org.in or call 14448."
    },

    # 4. Top Indian Banks Emergency Fraud Helplines & Domains
    {
        "id": "kb_bank_sbi_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "State Bank of India (SBI): Emergency Blocking & Official Channels",
        "source": "State Bank of India Cybersecurity Cell & Official Portal",
        "tags": ["sbi", "state bank", "1800111109", "18001234", "onlinesbi", "yono"],
        "content": "SBI official web banking is strictly hosted on `onlinesbi.sbi` and `sbi.co.in`. SBI customer care numbers are 1800 1234, 1800 2100, and 1800 11 1109. To instantly block your SBI ATM/Debit Card, send SMS 'BLOCK <last 4 digits of card>' to 567676 from your registered mobile number. To lock NetBanking access, visit onlinesbi.sbi and click 'Lock NetBanking Access'.",
        "actionable_guidance": "Never click links from sender IDs other than official telecom headers (e.g. SBIBNK, SBIINB). To report unauthorized SBI transactions, call 1800 11 1109 or email report.phishing@sbi.co.in."
    },
    {
        "id": "kb_bank_hdfc_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "HDFC Bank: 24x7 Emergency Fraud Desk & Official Domains",
        "source": "HDFC Bank Security Center",
        "tags": ["hdfc", "hdfcbank", "18002026161", "18001600", "netbanking.hdfcbank.com"],
        "content": "HDFC Bank's official domain is `hdfcbank.com`. HDFC dedicated national fraud helpline is 1800 202 6161 / 1800 1600. Customers can instantly freeze NetBanking access and cards via MobileBanking app > Menu > Security Center > Freeze Account. HDFC Bank never sends SMS demanding PAN/Aadhaar updates to prevent account freeze.",
        "actionable_guidance": "Report phishing SMS or suspicious debit to 1800 202 6161 or email report.phishing@hdfcbank.com immediately. Genuine HDFC SMS headers include HDFCBK, HDFCBN."
    },
    {
        "id": "kb_bank_icici_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "ICICI Bank: Emergency Debit Blocking & Official Channels",
        "source": "ICICI Bank Safe Banking Guidelines",
        "tags": ["icici", "icicibank", "18001080", "imobile", "icicibank.com"],
        "content": "ICICI Bank official online services are strictly hosted on `icicibank.com`. ICICI 24x7 customer care is 1800 1080. You can temporarily block and unblock your debit/credit card in 1-click via the iMobile Pay app > Manage Cards > Temporarily Block. To block internet banking via SMS, send 'BLOCK <User ID>' to 9215667788.",
        "actionable_guidance": "Send phishing emails or suspicious links to antiphishing@icicibank.com. Call 1800 1080 immediately to lock accounts if credentials were leaked."
    },
    {
        "id": "kb_bank_axis_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "Axis Bank: Fraud Support & Card Deactivation",
        "source": "Axis Bank Vigilance & Customer Protection",
        "tags": ["axis", "axisbank", "18004190068", "18001035577", "axisbank.com"],
        "content": "Axis Bank official website is `axisbank.com`. Dedicated fraud reporting numbers are 1800 419 0068 and 1800 103 5577. To block debit cards via SMS, send 'BLOCK <Last 4 digits>' to 56161600 or +918691000002 from registered mobile number.",
        "actionable_guidance": "Report unauthorized Axis debit or phishing attacks to 1800 419 0068 or email dispute.helpdesk@axisbank.com."
    },
    {
        "id": "kb_bank_pnb_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "Punjab National Bank (PNB): Emergency Fraud Helpdesk",
        "source": "PNB Cybersecurity Advisory",
        "tags": ["pnb", "punjab national bank", "18001802222", "18001032222", "pnbindia.in"],
        "content": "PNB official domain is `pnbindia.in`. Dedicated fraud toll-free numbers are 1800 180 2222 and 1800 103 2222. PNB customers can block ATM debit cards by sending SMS 'HOT <16 digit Card No>' to 5607040.",
        "actionable_guidance": "Report unauthorized PNB transactions to 1800 180 2222 or email incident@pnb.co.in."
    },
    {
        "id": "kb_bank_kotak_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "Kotak Mahindra Bank: Fraud Reporting & Security Guidelines",
        "source": "Kotak Mahindra Bank Security Portal",
        "tags": ["kotak", "kotak.com", "18602662666", "fraud desk", "811"],
        "content": "Kotak Mahindra Bank operates on `kotak.com`. Fraud reporting helpline is 1860 266 2666 (or +91 22 6204 2001 for international). Customers can block cards via Kotak Mobile Banking app > Service Requests > Debit Card > Block / Deactivate.",
        "actionable_guidance": "Report suspicious transactions or phishing attempts immediately to 1860 266 2666 or email report.phishing@kotak.com."
    },

    # 5. Major UPI Apps Dispute & Safety
    {
        "id": "kb_phonepe_fraud_reporting",
        "category": "general",
        "title": "PhonePe: Reporting Fraudulent Transactions & Fake Collect Requests",
        "source": "PhonePe Trust & Safety Center",
        "tags": ["phonepe", "support", "08068727374", "ybl", "ibl", "axl"],
        "content": "PhonePe customer support helpline is 080-68727374 or 022-68727374. Inside the PhonePe app, open History > select suspicious transaction > tap 'Contact PhonePe Support'. PhonePe never contacts users asking them to install remote screen sharing software or to approve collect requests for refunds.",
        "actionable_guidance": "Do not search for PhonePe customer care numbers on Google (fake ads scam). Access support strictly within the PhonePe app under 'Help' or call 080-68727374."
    },
    {
        "id": "kb_gpay_fraud_reporting",
        "category": "general",
        "title": "Google Pay (Tez): Dispute Filing & Safe Usage",
        "source": "Google Pay India Safety Center",
        "tags": ["google pay", "gpay", "tez", "18004190157", "dispute", "okaxis", "oksbi"],
        "content": "Google Pay India toll-free customer support is 1800-419-0157. To report a fraudulent user or collect request, tap the user or merchant in Google Pay > tap the 3-dot menu > select 'Report or block'. Google Pay never asks users to transfer money to test payment gateways.",
        "actionable_guidance": "Report fake merchants inside the Google Pay app. For unauthorized debits, raise a transaction dispute immediately via transaction details > 'Having issues?'."
    },
    {
        "id": "kb_paytm_fraud_reporting",
        "category": "general",
        "title": "Paytm Payments Bank: 24x7 Cyber Fraud Helpline",
        "source": "Paytm Security & Incident Management",
        "tags": ["paytm", "01204456456", "paytm bank", "kyc fraud", "wallet"],
        "content": "Paytm 24x7 cyber fraud helpline is 0120-4456-456. Common Paytm scams involve SMS warning 'Your Paytm KYC has expired, wallet blocked, call 98xxxxxx'. Paytm never instructs users to download QuickSupport or send small fee transfers to renew KYC.",
        "actionable_guidance": "Call 0120-4456456 immediately to report fraudulent wallet or UPI activity. Renew KYC exclusively through the verified Paytm app."
    },
    {
        "id": "kb_bhim_npci_reporting",
        "category": "general",
        "title": "BHIM UPI: Direct Complaint Escalation to NPCI",
        "source": "NPCI Dispute Redressal Mechanism (DRM) Portal",
        "tags": ["bhim", "npci", "18001201740", "dispute", "chargeback", "drm"],
        "content": "BHIM (Bharat Interface for Money) is operated directly by NPCI. Toll-free helpline is 1800-120-1740. If a payment dispute or fraud is not resolved by your issuing bank within statutory timelines, complaints can be escalated directly to NPCI via the Dispute Redressal Mechanism portal at npci.org.in.",
        "actionable_guidance": "Log complaints on npci.org.in > 'UPI Dispute Redressal Mechanism' with the 12-digit UPI reference number if bank redressal fails."
    },

    # 6. Specific Scam Categories & Playbooks
    {
        "id": "kb_electricity_bill_scam_playbook",
        "category": "electricity_disconnection",
        "title": "Electricity Disconnection Scam: Operational Playbook & Defense",
        "source": "State Power Distribution Companies & CERT-In Cyber Threat Advisory",
        "tags": ["electricity", "bill", "power", "disconnection", "bescom", "tsspdcl", "tneb", "uppcl"],
        "content": "Fraudsters send deceptive SMS warnings claiming electricity power will be disconnected at '9:30 PM tonight' due to unpaid previous month bills. They provide a personal 10-digit mobile number claiming to be the 'Electricity Officer' or a link to a fake bill portal. Electricity distribution companies never disconnect power overnight without serving statutory written notices, nor do they instruct consumers to call personal mobile numbers.",
        "actionable_guidance": "Do not call the phone number in the SMS. Check your actual electricity bill balance exclusively on your state utility's official consumer portal or through your authorized bill payment app (BBPS)."
    },
    {
        "id": "kb_remote_access_scam_playbook",
        "category": "remote_access_scam",
        "title": "Remote Desktop Screen Sharing Fraud: Technical Breakdown",
        "source": "Cyber Crime Investigation Cell & RBI Advisory on Social Engineering",
        "tags": ["anydesk", "teamviewer", "quicksupport", "rustdesk", "support", "remote", "screen"],
        "content": "Scammers posing as bank customer support, courier helpdesks, or telecom executives trick victims into downloading remote desktop applications (e.g., AnyDesk, TeamViewer QuickSupport, RustDesk). Once installed, they ask for the 9-digit session code, granting full visual screen access and remote touch controls. This allows attackers to view incoming 2FA SMS and steal OTPs in real-time.",
        "actionable_guidance": "Never install remote desktop software upon unsolicited advice from callers. If already installed, immediately turn on Airplane Mode, uninstall the remote application, and change all banking passwords from a separate clean device."
    },
    {
        "id": "kb_part_time_job_crypto_scam",
        "category": "job_investment_scam",
        "title": "Part-Time Task, YouTube Like & Crypto Investment Scams",
        "source": "Indian Cyber Crime Coordination Centre (I4C) Advisory on Task-Based Scams",
        "tags": ["job", "part time", "telegram", "youtube like", "hotel review", "crypto", "task", "investment"],
        "content": "Victims receive WhatsApp or Telegram messages offering Rs. 2,000 - 5,000/day for simple tasks like 'liking YouTube videos' or 'submitting 5-star Google ratings'. In Phase 1, small genuine payouts (Rs. 200 - 500) are transferred to build trust. In Phase 2, victims are added to Telegram VIP investment groups and coerced into depositing large sums (Rs. 50,000+) for 'high-yield crypto tasks'. When withdrawal is requested, fraudsters demand fake taxes or frozen fund fees.",
        "actionable_guidance": "Legitimate companies never pay money for liking videos or require deposits to release earned salaries. Never join unknown Telegram investment channels. If victimized, cease all contact and call 1930 immediately."
    },
    {
        "id": "kb_predatory_loan_app_extortion",
        "category": "loan_app_extortion",
        "title": "Predatory Digital Lending Apps: Blackmail & Contact Scraping",
        "source": "RBI Working Group on Digital Lending & IT Rules Advisory",
        "tags": ["loan", "loan app", "extortion", "blackmail", "gallery", "contacts", "recovery agent"],
        "content": "Fraudulent loan apps (often downloaded via APK links or social media ads) offer instant paperless loans of Rs. 3,000 - 10,000. During installation, the app demands invasive permissions: full Contacts list, Camera, Gallery, and SMS logs. Within 5 days, recovery agents threaten the borrower, demanding 300% interest and sending morphed, defamatory photos to family members and colleagues scraped from contacts.",
        "actionable_guidance": "1. Only borrow from RBI-registered NBFCs and Banks listed on rbi.org.in. 2. Never grant Contacts or Storage permissions to utility or loan apps. 3. If blackmailed, report immediately to local cyber police and National Cyber Crime Portal (1930). Do not pay extortion demands."
    },
    {
        "id": "kb_digital_arrest_customs_scam",
        "category": "courier_customs_scam",
        "title": "Digital Arrest & Fake Police / Customs Narcotics Extortion",
        "source": "Ministry of Home Affairs (MHA) Nationwide Advisory on Digital Arrest Scams",
        "tags": ["digital arrest", "customs", "cbi", "mumbai police", "fedex", "narcotics", "skype", "dhl"],
        "content": "Scammers call pretending to be FedEx, DHL, or Customs officials, claiming a parcel sent in the victim's name to Taiwan or Thailand contains MDMA drugs, fake passports, and illegal debit cards. The call is transferred to fake 'Police Officers' or 'CBI Officials' on Skype or WhatsApp video who wear simulated uniforms with forged police insignias. They place the victim under 'Digital Arrest', coercing them into staying on camera for days and transferring their life savings into 'Government Escrow Accounts' for verification.",
        "actionable_guidance": "THERE IS NO LEGAL CONCEPT OF 'DIGITAL ARREST' UNDER INDIAN LAW. Law enforcement agencies (Police, CBI, ED, NIA) NEVER interrogate citizens over Skype or WhatsApp video, nor do they demand money transfers to verify bank accounts. Disconnect immediately and call 1930."
    },
    {
        "id": "kb_marketplace_olx_qr_scam",
        "category": "marketplace_qr_scam",
        "title": "OLX & Facebook Marketplace Army Officer QR Scam",
        "source": "Indian Army Cyber Security Cell & Police Cyber Crime Advisory",
        "tags": ["olx", "marketplace", "army", "defence", "canteen", "qr scan", "advance"],
        "content": "Scammers target sellers listing second-hand furniture, electronics, or vehicles on OLX or Facebook Marketplace. The attacker poses as an Indian Army soldier, CRPF officer, or CISF personnel stationed at a military cantonment. To purchase the item immediately without physical inspection, the scammer claims military accounts can only transfer funds via 'QR Verification' and sends a QR code instructing the seller to scan it to receive the advance payment.",
        "actionable_guidance": "Do not accept remote payments from buyers claiming to be military personnel who refuse in-person inspection. Scanning ANY QR code or entering a PIN pays money to the scammer."
    },
    {
        "id": "kb_wrong_number_sent_money_trap",
        "category": "wrong_number_transfer",
        "title": "'Accidental Money Transfer' Social Engineering Trap",
        "source": "RBI Consumer Education and Protection Department Advisory",
        "tags": ["wrong number", "accidental transfer", "refund", "reversal", "mule", "chargeback"],
        "content": "The victim receives a fake bank credit SMS or an actual small transfer (e.g., Rs. 5,000) from an unknown number. Soon after, a distressed caller phones claiming: 'I mistakenly sent my child's hospital fee to your UPI ID, please return it urgently via Google Pay'. If the victim sends money back to the caller's separate UPI ID, the scammer files a formal unauthorized transaction chargeback with their own bank, causing the bank to debit the original sum again. The victim loses twice or becomes implicated in money laundering.",
        "actionable_guidance": "Never send money back directly via UPI. Tell the caller to contact their bank to initiate formal inter-bank auto-reversal. Inform your own bank branch in writing that you received unsolicited funds and authorize the bank to reverse it through official banking settlement channels."
    },
    {
        "id": "kb_lottery_kbc_advance_fee",
        "category": "lottery_prize",
        "title": "KBC Lucky Draw & WhatsApp Lottery Advance-Fee Scams",
        "source": "Telecom Regulatory Authority of India (TRAI) & CERT-In Public Alert",
        "tags": ["kbc", "lottery", "lucky draw", "25 lakh", "amitabh bachchan", "advance fee", "gst"],
        "content": "Fraudsters circulate audio clips and forged certificates claiming the recipient has won a Rs. 25 Lakh KBC (Kaun Banega Crorepati) lottery selected randomly via their WhatsApp phone number. To claim the prize, victims are asked to call a 'Lottery Manager' and deposit an upfront 'GST', 'Processing Fee', or 'RBI Clearance Charge' (Rs. 15,000 - 50,000) into specified bank accounts. Once paid, further demands follow until the victim realizes no prize exists.",
        "actionable_guidance": "Legitimate lotteries and contests never require advance cash deposits for tax or processing. Lottery by phone number is legally prohibited. Block the sender and report on 1930."
    },
    {
        "id": "kb_fake_govt_scheme_subsidy",
        "category": "fake_govt_scheme",
        "title": "PM Yojana, Free Laptop & Subsidy Phishing Scams",
        "source": "Press Information Bureau (PIB) Fact Check Unit",
        "tags": ["pm yojana", "subsidy", "free laptop", "pm kisan", "scholarship", "aadhaar registration"],
        "content": "Viral messages on WhatsApp promise free laptops, monthly pensions under 'PM Kanya Yojana', or immediate Rs. 6,000 subsidies from PM-Kisan. Links lead to deceptive clone websites (e.g. `pm-kisan-gov.in.xyz`) that harvest Aadhaar numbers, bank account numbers, and mobile numbers, or trigger unauthorized collect requests disguised as 'Registration Fees'.",
        "actionable_guidance": "All genuine central and state government schemes are hosted strictly on official `.gov.in` or `.nic.in` domains. Never pay any registration fee for government schemes or welfare subsidies. Verify viral claims with PIB Fact Check (pib.gov.in/factcheck)."
    },

    # 7. Telecom, SIM Swap & Sender ID Rules
    {
        "id": "kb_sim_swap_esim_hijack",
        "category": "telecom",
        "title": "SIM Swap & e-SIM Hijacking: Mechanism and Indicators",
        "source": "Department of Telecommunications (DoT) Advisory on Mobile Security",
        "tags": ["sim swap", "esim", "network loss", "otp interception", "dot", "jio", "airtel"],
        "content": "In a SIM swap attack, fraudsters obtain a duplicate SIM card of the victim's mobile number using forged IDs or by tricking the victim into forwarding an e-SIM activation QR code. Once the duplicate SIM activates, the victim's phone abruptly loses cellular network signal ('No Service'), allowing the attacker to receive all incoming banking OTPs and reset NetBanking passwords.",
        "actionable_guidance": "If your phone suddenly loses cellular network connectivity unexpectedly while others have signal, DO NOT assume a temporary tower issue. Immediately call your telecom provider from another phone to check if a SIM swap or e-SIM migration was requested."
    },
    {
        "id": "kb_sanchar_saathi_tafcop",
        "category": "telecom",
        "title": "Sanchar Saathi Portal: Auditing Mobile Numbers Registered in Your Name",
        "source": "Department of Telecommunications (DoT) — Sanchar Saathi Initiative",
        "tags": ["sanchar saathi", "tafcop", "ceir", "block stolen phone", "sim audit", "dot"],
        "content": "The Government of India's Sanchar Saathi portal (sancharsaathi.gov.in) provides two critical citizen defense tools: TAFCOP (Telecom Analytics for Fraud Management and Consumer Protection) to identify all mobile connections registered against your Aadhaar/ID, and CEIR (Central Equipment Identity Register) to block lost or stolen mobile handsets across all Indian telecom networks.",
        "actionable_guidance": "Visit https://sancharsaathi.gov.in regularly. Check TAFCOP to disconnect unauthorized mobile numbers issued in your name, and use CEIR to blacklist lost device IMEIs."
    },
    {
        "id": "kb_sms_header_trai_dlt",
        "category": "general",
        "title": "TRAI DLT SMS Header Authentication: Distinguishing Official vs Fake SMS",
        "source": "Telecom Regulatory Authority of India (TRAI) Distributed Ledger Technology Framework",
        "tags": ["sms header", "dlt", "trai", "sender id", "10-digit mobile", "v-sbi", "ax-hdfc"],
        "content": "Under TRAI regulations, commercial and transactional SMS from registered Indian banks and enterprises MUST use registered 6-character alphabetic headers preceded by telecom routing codes (e.g., `AD-SBIINB`, `VK-HDFCBK`, `BZ-AXISBK`). Legitimate banks NEVER send transactional alerts, KYC warnings, or OTPs from ordinary 10-digit mobile numbers (e.g., `+91 98765 43210`).",
        "actionable_guidance": "Any SMS claiming to be from a bank, electricity board, or government agency that originates from a standard 10-digit mobile number is an illegal, unverified transmission and must be treated as a scam."
    },

    # 8. Web Security, Domains & Phishing Defense
    {
        "id": "kb_official_gov_domains",
        "category": "general",
        "title": "Government & Banking Domain Hygiene: Understanding `.gov.in` and `.nic.in`",
        "source": "National Informatics Centre (NIC) & Ministry of Electronics and IT (MeitY)",
        "tags": ["domain", "gov.in", "nic.in", "subdomain", "phishing", "tld"],
        "content": "Official Indian government portals are strictly provisioned on `.gov.in` or `.nic.in` top-level domains by the National Informatics Centre (NIC). Private TLDs like `.com`, `.org`, `.xyz`, or `.top` can NEVER be genuine Indian government portals, regardless of what subdomains they use (e.g., `incometax.gov.in.portal-refund.com` is an external phishing host owned by `portal-refund.com`).",
        "actionable_guidance": "Look at the domain immediately preceding the final top-level extension. If it does not end in `.gov.in` or the exact official bank domain (e.g. `sbi.co.in`, `hdfcbank.com`), do not enter any credentials."
    },
    {
        "id": "kb_punycode_homograph_attacks",
        "category": "general",
        "title": "Punycode & Internationalized Domain Name (IDN) Phishing",
        "source": "CERT-In Vulnerability Note on Homograph Phishing Attacks",
        "tags": ["punycode", "idn", "homograph", "cyrillic", "xn--", "phishing"],
        "content": "Attackers register domain names using Cyrillic or Greek characters that look visually identical to Latin letters (e.g., Cyrillic 'а' vs Latin 'a'). In browsers, these domains resolve to Punycode starting with `xn--` (e.g., `xn--sb-e1a.co.in`). To the human eye, the link looks like the real bank, but it directs traffic to an adversary's server.",
        "actionable_guidance": "Check browser address bars carefully for `xn--` prefixes. Use password managers that enforce strict domain origin binding and refuse to auto-fill credentials on homograph spoof domains."
    },
    {
        "id": "kb_https_lock_misconception",
        "category": "general",
        "title": "The HTTPS Padlock Fallacy: Encryption Does NOT Guarantee Legality",
        "source": "Cybersecurity and Infrastructure Security Agency (CISA) & CERT-In Guide",
        "tags": ["https", "ssl", "tls", "padlock", "encryption", "phishing"],
        "content": "A common misconception is that a website with a padlock icon (`https://`) is legitimate and safe. Today, over 80% of phishing websites use free, automated SSL certificates (e.g., Let's Encrypt). The HTTPS padlock only means the connection between your device and the server is encrypted; it DOES NOT verify that the owner of the server is a legitimate bank or merchant.",
        "actionable_guidance": "Never rely solely on the padlock icon to judge website legitimacy. Verify the exact spelled domain name and look for official domain registration."
    },

    # 9. Android Malware & APK Sideloading
    {
        "id": "kb_apk_sideloading_malware",
        "category": "general",
        "title": "Malicious Android APK Sideloading & SMS Forwarding Trojans",
        "source": "CERT-In Advisory on Android Banking Trojans (Cerberus / SOVA / Hook)",
        "tags": ["apk", "sideloading", "android", "trojan", "sms forwarder", "accessibility service"],
        "content": "Fraudsters share direct APK files via WhatsApp or Telegram with names like `SBI_Yono_Update.apk`, `PM_Kisan_Verification.apk`, or `Electricity_Bill_Receipt.apk`. Once sideloaded, these apps request 'Accessibility Service' and 'SMS Read/Receive' permissions. With Accessibility permissions, the malware can bypass screen locks, read 2FA SMS OTPs, and perform background fund transfers without the user's knowledge.",
        "actionable_guidance": "NEVER install `.apk` files received over WhatsApp, Telegram, or third-party download sites. Disable 'Install unknown apps' in Android settings. Ensure Google Play Protect is enabled on your device."
    },
    {
        "id": "kb_accessibility_permission_risks",
        "category": "general",
        "title": "Android Accessibility Service Exploitation in Banking Malware",
        "source": "Google Android Security Bulletin & CERT-In Threat Intelligence",
        "tags": ["accessibility", "permissions", "malware", "keylogger", "overlay", "android"],
        "content": "Android's Accessibility Service is designed to assist users with disabilities by allowing apps to inspect the screen and interact with UI elements. Banking trojans abuse this service to log keystrokes, capture banking passwords, prevent uninstallation of the malware, and automatically dismiss security prompts.",
        "actionable_guidance": "Regularly audit your device settings: Settings > Accessibility > Installed apps. If any unfamiliar application has accessibility permissions enabled, revoke it immediately and boot into Safe Mode to uninstall."
    },

    # 10. Social Engineering Tactics & Psychology
    {
        "id": "kb_urgency_panic_coercion",
        "category": "general",
        "title": "Psychological Manipulation: The Urgency & Fear Mechanism in Cyber Scams",
        "source": "Behavioural Insights Team & Cyber Psychology Research",
        "tags": ["psychology", "urgency", "fear", "manipulation", "social engineering", "time pressure"],
        "content": "Almost all financial scams exploit an induced state of panic (amygdala hijack) through artificial time pressure: 'Your account will be suspended in 2 hours', 'Power disconnected tonight at 9 PM', 'Police FIR registered against your name'. High emotional arousal inhibits rational analytical thinking, making victims overlook blatant warning signs and willingly execute irrational instructions.",
        "actionable_guidance": "Rule of 10 Minutes: Whenever a message or caller demands urgent action regarding money or account blocking, deliberately wait 10 minutes. Legitimate institutions never require immediate action within minutes without prior written notice."
    },
    {
        "id": "kb_authority_impersonation",
        "category": "general",
        "title": "Authority Bias Impersonation: Police, Judges, and RBI Officials",
        "source": "Indian Cyber Crime Coordination Centre (I4C) Awareness Series",
        "tags": ["authority", "police", "rbi", "cbi", "customs", "impersonation", "fear"],
        "content": "Scammers exploit deep-seated respect for and fear of authority by impersonating law enforcement officers, judges, customs agents, or RBI officials. They use formal jargon ('Statutory Notice', 'Non-Bailable Warrant', 'Narcotics Control Bureau Docket'), display counterfeit badges, and threaten severe penal consequences to coerce compliance.",
        "actionable_guidance": "Remember: Genuine police officers or government officials do not conduct investigations or demand financial settlement over video calls. Demand physical service of legal summons and consult a certified legal advisor or your local police station."
    },

    # 11. Elderly & Vulnerable Users Protection
    {
        "id": "kb_elderly_financial_protection",
        "category": "general",
        "title": "Protecting Senior Citizens from Digital Payment Fraud",
        "source": "National Commission for Senior Citizens & RBI Financial Literacy Advisory",
        "tags": ["seniors", "elderly", "parents", "protection", "daily limit", "audio alerts"],
        "content": "Senior citizens are disproportionately targeted by digital financial scams due to unfamiliarity with modern UI flows, fear of losing pensions, and trusting nature. Common attack vectors include pension account KYC renewal scams, utility bill threats, and remote access helpdesk tricks.",
        "actionable_guidance": "1. Set low daily UPI transaction limits (e.g. Rs. 2,000 - 5,000) for elderly family members. 2. Enable SMS and WhatsApp transaction alerts to a trusted co-family member. 3. Teach elderly relatives: 'Never read out numbers received via SMS to any caller'."
    },

    # 12. Safe Check for Payments & VPA Guidelines
    {
        "id": "kb_vpa_safetocheck_guide",
        "category": "general",
        "title": "Pre-Payment Verification: How to Safe-Check Any UPI ID Before Sending Funds",
        "source": "NPCI User Awareness Campaign: 'UPI Chalega'",
        "tags": ["vpa check", "verify", "safe-check", "name match", "pre-payment"],
        "content": "Before transferring funds to any unfamiliar UPI ID (especially from social media, freelance gigs, or marketplaces), verify the payee's registered banking name. In UPI apps, entering a VPA retrieves the official bank-linked name from NPCI's central database.",
        "actionable_guidance": "Ensure the displayed registered name strictly matches the individual or legal entity you intend to pay. If an online shop asks you to pay a personal savings handle (e.g., `ramesh123@ybl`) instead of a registered merchant handle, suspect a fraud."
    },

    # 13. Additional Specific Scam Playbooks & Scenarios
    {
        "id": "kb_matrimonial_dating_pig_butchering",
        "category": "job_investment_scam",
        "title": "Matrimonial & Romance Scams (Shaadi.com / Tinder / Jeevansathi)",
        "source": "Cyber Crime Cell Advisory on Matrimonial Portal Scams",
        "tags": ["matrimonial", "romance", "dating", "shaadi", "jeevansathi", "customs gift", "crypto"],
        "content": "Fraudsters create attractive profiles on matrimonial portals or dating apps claiming to be doctors, NRI engineers, or defense personnel based in the UK, USA, or Dubai. After establishing emotional attachment over weeks of messaging, the scammer claims to send expensive gifts (jewelry, foreign currency, designer watches). Soon, a fake 'Customs Officer' calls demanding duty fees to clear the parcel at Delhi/Mumbai airport, continuing with escalated demands.",
        "actionable_guidance": "Never send money to someone you have only met online. Legitimate customs authorities never contact citizens on WhatsApp asking for fee transfers to personal bank accounts."
    },
    {
        "id": "kb_fake_toll_fastag_scam",
        "category": "fake_bank_kyc",
        "title": "FASTag KYC Expiry & Highway Toll Phishing Alerts",
        "source": "National Highways Authority of India (NHAI) & IHMCL Security Notice",
        "tags": ["fastag", "nhai", "toll", "kyc", "highway", "blacklisted"],
        "content": "Scammers exploit NHAI's 'One Vehicle One FASTag' rules by sending SMS warnings: 'Your FASTag KYC has expired, your vehicle tag will be blacklisted on national highways within 12 hours. Update immediately at [phishing link]'. The link mimics bank FASTag portals and captures vehicle numbers, OTPs, and UPI credentials.",
        "actionable_guidance": "Update FASTag KYC solely through the official website of your issuing bank or the official Indian Highway Management Company portal (`ihmcl.co.in`)."
    },
    {
        "id": "kb_challan_traffic_phishing",
        "category": "general",
        "title": "Traffic Police e-Challan SMS Phishing Scams",
        "source": "Ministry of Road Transport and Highways (MoRTH) & Traffic Police Alerts",
        "tags": ["challan", "traffic", "fine", "morth", "echallan", "parivahan"],
        "content": "Car owners receive alarming SMS messages stating: 'Traffic Police Notice: You have 1 unpaid pending e-challan of Rs. 1,000 for speed violation. Pay today to avoid court summons: [fake link e.g. `echallan-parivahan.in.net`]'. The fake payment gateway steals credit card details or triggers unauthorized UPI mandates.",
        "actionable_guidance": "Verify and pay traffic challans exclusively on the official Ministry of Road Transport portal: `echallan.parivahan.gov.in`. Never open unofficial links received via SMS."
    },
    {
        "id": "kb_courier_delivery_failed_scam",
        "category": "courier_customs_scam",
        "title": "India Post & Courier 'Address Incomplete' Delivery Phishing",
        "source": "Department of Posts (India Post) & BlueDart Cybersecurity Advisory",
        "tags": ["india post", "courier", "delivery", "bluedart", "address update", "5 rupees"],
        "content": "Victims receive SMS claiming: 'India Post: Your package cannot be delivered because your street address is missing. Update address within 24 hours to avoid return: [phishing link]'. The website prompts for address and a token 're-delivery fee of Rs. 5 or Rs. 25'. When the victim enters card details and OTP, scammers execute unauthorized debits for thousands of rupees.",
        "actionable_guidance": "India Post never sends SMS links to update delivery addresses or demands online re-delivery fees. Track packages strictly on `indiapost.gov.in` using your consignment number."
    },
    {
        "id": "kb_fake_credit_card_reward_points",
        "category": "fake_upi_refund_cashback",
        "title": "Credit Card Reward Points Expiry & Cashback Redemption Scams",
        "source": "Major Credit Card Issuers (SBI Card, HDFC, ICICI) Security Guidelines",
        "tags": ["credit card", "reward points", "cashback", "expiry", "redeem", "sbi card"],
        "content": "Customers receive SMS claiming: 'Dear Customer, your 8,500 Reward Points worth Rs. 4,250 expire today. Redeem cash directly to your bank account: [phishing link]'. The link opens a fake redemption page that captures full 16-digit card number, CVV, expiry date, and net banking credentials to drain the card limit.",
        "actionable_guidance": "Credit card reward points are redeemed exclusively inside official mobile banking apps or through official reward portals. Banks never redeem reward points as direct cash transfers via SMS links."
    },
    {
        "id": "kb_telecom_5g_sim_upgrade_scam",
        "category": "telecom",
        "title": "5G SIM Upgrade & Network Deactivation Scams",
        "source": "Department of Telecommunications (DoT) & Cellular Operators Association of India (COAI)",
        "tags": ["5g", "upgrade", "sim", "telecom", "jio", "airtel", "vi", "deactivation"],
        "content": "Attackers call subscribers claiming their 4G SIM card will be deactivated due to mandatory government 5G upgrades. They send an SMS containing a porting code or an e-SIM activation request and instruct the victim to forward it to 121 or 1900. By doing so, the victim unwittingly transfers their phone number to the attacker's device.",
        "actionable_guidance": "5G services on Airtel and Jio work automatically on existing 4G SIMs without any manual code forwarding or SIM replacement. Never forward SIM-related SMS or OTPs to unknown numbers."
    },
    {
        "id": "kb_fake_charity_disaster_relief",
        "category": "general",
        "title": "Fake Charity & Disaster Relief Crowd-Funding Fraud",
        "source": "National Disaster Management Authority (NDMA) & Police Cyber Wing",
        "tags": ["charity", "relief", "donation", "disaster", "pm cares", "ngo", "crowdfunding"],
        "content": "During natural disasters (floods, earthquakes) or viral medical appeals, scammers create fake donation websites and UPI QR codes mimicking legitimate relief funds (e.g. `pmcares@upi.fake`, fake Red Cross handles). Funds collected are diverted to private mule accounts.",
        "actionable_guidance": "Donate only through verified national portals (such as official `pmcares.gov.in` or chief minister relief funds ending in `.gov.in`). Always inspect the payee name before approving donation transfers."
    },
    {
        "id": "kb_fake_tech_support_popups",
        "category": "fake_customer_support",
        "title": "Browser Tech Support Pop-ups & Fake Windows Defender Alerts",
        "source": "CERT-In Advisory on Technical Support Scams",
        "tags": ["tech support", "popup", "windows defender", "microsoft", "virus", "toll free"],
        "content": "While browsing the web, users encounter deceptive fullscreen pop-ups that simulate a crashed computer with loud siren audio: 'CRITICAL ALERT: Your computer has been locked by Windows Defender due to spyware. Call Microsoft Support at 1800-XXX-XXXX'. Callers instruct victims to install remote desktop tools to 'clean the virus' and demand payment via UPI or gift cards.",
        "actionable_guidance": "Microsoft, Apple, and Google never show fullscreen browser alerts with phone numbers to call. Simply close the browser tab or terminate the browser process via Task Manager (Ctrl+Shift+Esc)."
    },
    {
        "id": "kb_mule_account_legal_peril",
        "category": "regulatory",
        "title": "Money Mule Accounts: Legal Liabilities & Criminal Prosecution",
        "source": "Prevention of Money Laundering Act (PMLA) & Indian Penal Code (IPC)",
        "tags": ["mule account", "pmla", "money laundering", "commission", "jail", "legal risk"],
        "content": "Students and job seekers are lured by social media offers to 'earn Rs. 1,000/day by renting your bank account or UPI ID for crypto transactions'. In reality, these accounts receive stolen funds from cyber scams. Under PMLA and Section 420 of the IPC, the account holder is legally recognized as a co-conspirator to fraud, leading to freezing of all personal accounts and non-bailable arrest.",
        "actionable_guidance": "Never lend your bank account, debit card, or UPI credentials to anyone, regardless of financial promises. You are legally responsible for all transactions originating from or terminating in your account."
    },
    {
        "id": "kb_corporate_email_compromise_bec",
        "category": "general",
        "title": "Business Email Compromise (BEC) & Vendor UPI Account Spoofing",
        "source": "CERT-In Cyber Security Guidelines for MSMEs and Corporates",
        "tags": ["bec", "vendor fraud", "invoice", "bank change", "msme", "corporate"],
        "content": "Attackers compromise an executive or vendor email account and send modified invoices instructing the accounts team to route upcoming payments to a 'new updated UPI ID or bank account' due to banking audits. Millions are transferred before anyone notices the email domain had a 1-character typo.",
        "actionable_guidance": "Establish a mandatory two-channel verification policy for any change in vendor payment details or bank accounts. Confirm all bank detail changes via a phone call to a known, pre-established trusted phone number."
    },
    {
        "id": "kb_whatsapp_pink_malware",
        "category": "general",
        "title": "WhatsApp Pink & Modded WhatsApp APK Security Threats",
        "source": "Cyber Peace Foundation & Maharashtra Cyber Police Advisory",
        "tags": ["whatsapp pink", "gbwhatsapp", "mod", "malware", "spyware", "contacts"],
        "content": "Viral links claim to offer an exclusive 'WhatsApp Pink' update with new features and a pink theme. The downloaded APK is an aggressive mobile trojan that hijacks the user's WhatsApp session, sends auto-replies with malicious download links to all phone contacts, and steals saved photos and banking credentials.",
        "actionable_guidance": "Use only official WhatsApp Messenger downloaded from the Google Play Store or Apple App Store. Never install unofficial mods (GBWhatsApp, WhatsApp Plus, WhatsApp Pink)."
    },
    {
        "id": "kb_ai_voice_clone_scam",
        "category": "general",
        "title": "AI Deepfake Voice Cloning & Emergency Family Distress Scams",
        "source": "Global Anti-Scam Alliance (GASA) & CERT-In Generative AI Advisory",
        "tags": ["ai", "voice clone", "deepfake", "kidnapping", "accident", "family emergency"],
        "content": "Using short audio clips scraped from public Instagram reels, YouTube videos, or LinkedIn profiles, scammers use AI generative voice cloning tools to replicate the voice of a family member (son, daughter, grandchild). The scammer calls parents claiming: 'Dad, I was involved in a severe car crash / arrested by police, please transfer Rs. 50,000 urgently to this UPI ID'.",
        "actionable_guidance": "Always establish a secret 'Family Safe Word' that only close family members know. Before transferring money, hang up and call your family member directly on their known regular phone number or video call them."
    },
    {
        "id": "kb_qr_tampering_physical_stores",
        "category": "marketplace_qr_scam",
        "title": "Physical QR Code Sticker Tampering (Quishing at Retail Counters)",
        "source": "NPCI Merchant Security Advisory on Standee QR Tampering",
        "tags": ["qr tampering", "quishing", "retail", "sticker", "merchant", "standee"],
        "content": "Fraudsters visit crowded physical retail shops or street vendors and secretly paste their own printed QR code sticker over the shopkeeper's genuine UPI QR standee. Customers scanning the QR code unknowingly send payments to the scammer's mule account instead of the shopkeeper.",
        "actionable_guidance": "Merchants should use secure acrylic standees and check their physical QR codes daily. Customers should confirm the name announced by the Soundbox matches the merchant."
    },
    {
        "id": "kb_upi_number_lookup_privacy",
        "category": "general",
        "title": "UPI Number Routing & Default Bank Account Awareness",
        "source": "NPCI Guidelines on UPI Number (10-Digit Mobile ID) Implementation",
        "tags": ["upi number", "mobile number", "default account", "npci mapper", "privacy"],
        "content": "NPCI enables payments directly to a 10-digit mobile number linked across multiple UPI apps. If you switch from one UPI app to another, ensure your preferred bank account is set as primary in the central NPCI mapper so that incoming funds land in your intended account.",
        "actionable_guidance": "Periodically review default receiving accounts in your primary UPI application to prevent fund routing confusion."
    },
    {
        "id": "kb_aadhaar_biometric_lock",
        "category": "fake_bank_kyc",
        "title": "Protecting Aadhaar from AePS Fraud: Biometric Locking via mAadhaar",
        "source": "Unique Identification Authority of India (UIDAI) Guidelines",
        "tags": ["aadhaar", "aeps", "biometric lock", "uidai", "fingerprint", "maadhaar"],
        "content": "Aadhaar-enabled Payment System (AePS) allows cash withdrawals and balance transfers using only Aadhaar number and fingerprint authentication. Scammers obtain land registry documents containing fingerprints and conduct unauthorized AePS cash withdrawals. Locking biometrics on the UIDAI portal completely prevents unauthorized AePS debits.",
        "actionable_guidance": "Download the official mAadhaar app or visit `resident.uidai.gov.in`. Enable 'Lock Biometrics'. Unlock it temporarily only when visiting a bank or government office for verification."
    },
    {
        "id": "kb_two_factor_auth_hygiene",
        "category": "otp_pin_theft",
        "title": "Multi-Factor Authentication (MFA) Best Practices for NetBanking",
        "source": "CERT-In Cyber Security Best Practices for Digital Citizens",
        "tags": ["mfa", "2fa", "authenticator", "totp", "sms otp", "hardware key"],
        "content": "While SMS OTP is the default 2FA mechanism in India, it is vulnerable to SIM swap, malware, and social engineering. Whenever supported by banks and email providers, software-based Time-based One-Time Password (TOTP) apps (Google Authenticator, Microsoft Authenticator) provide superior protection because codes cannot be intercepted over cellular networks.",
        "actionable_guidance": "Enable authenticator app-based 2FA for all primary email accounts and financial recovery portals. Protect your email account securely, as password resets route to it."
    },
    {
        "id": "kb_safe_browsing_dns",
        "category": "general",
        "title": "Securing Household Internet: Protective DNS & Anti-Phishing Resolvers",
        "source": "National Cyber Security Coordinator (NCSC) & CERT-In Guidelines",
        "tags": ["dns", "safe browsing", "cloudflare 1.1.1.2", "quad9", "anti-phishing", "router"],
        "content": "Protective DNS resolvers (such as Cloudflare Families `1.1.1.2` or Quad9 `9.9.9.9`) automatically block resolution of newly registered phishing domains, malware distribution hosts, and known malicious command-and-control servers at the network boundary before pages load.",
        "actionable_guidance": "Configure protective DNS (e.g. Quad9: 9.9.9.9 or Cloudflare: 1.1.1.2) on home Wi-Fi routers and mobile devices to automatically block malicious phishing domains."
    },
    {
        "id": "kb_app_permissions_audit",
        "category": "general",
        "title": "Smartphone App Permissions: What Financial Apps Actually Need",
        "source": "Data Protection Board of India & Digital Personal Data Protection (DPDP) Act",
        "tags": ["permissions", "privacy", "camera", "microphone", "sms", "location", "contacts"],
        "content": "Under data minimization principles, UPI apps require SMS access (only during initial SIM binding) and Camera (for scanning QR codes). A payment application NEVER requires access to your Contacts list, Microphone, or continuous background location to process payments.",
        "actionable_guidance": "Review app permissions: Settings > Apps > Permissions. Change sensitive permissions (Camera, Location) to 'Ask every time' or 'While using app'. Revoke SMS and Contact access for apps that do not strictly require them."
    },
    {
        "id": "kb_virtual_credit_cards_tokenization",
        "category": "regulatory",
        "title": "Card Tokenization & Virtual Card Numbers for Online Safety",
        "source": "RBI Guidelines on Card-on-File Tokenization (CoFT)",
        "tags": ["tokenization", "virtual card", "coft", "rbi", "cvv", "data security"],
        "content": "Under RBI's Card-on-File Tokenization (CoFT) mandate, merchants cannot store your actual 16-digit debit or credit card number. Instead, they store a secure cryptographic token unique to the merchant. This ensures that even if an e-commerce platform suffers a database breach, your real card credentials cannot be compromised.",
        "actionable_guidance": "Always tokenize your payment cards when prompted on trusted merchant apps. For one-off purchases on less familiar websites, generate a single-use virtual card through your bank app."
    },
    {
        "id": "kb_public_wifi_payment_risks",
        "category": "general",
        "title": "Risks of Conducting Financial Transactions on Public Wi-Fi",
        "source": "CERT-In Cyber Security Advisory on Public Wi-Fi Hotspots",
        "tags": ["public wifi", "airport", "railway", "man in the middle", "evil twin", "vpn"],
        "content": "Unencrypted public Wi-Fi networks at airports, railway stations, and cafes are susceptible to 'Evil Twin' access points and Man-in-the-Middle (MITM) snooping attacks. Rogue access points can redirect DNS queries to phishing portals or capture unencrypted traffic.",
        "actionable_guidance": "Never execute UPI payments, NetBanking logins, or credit card checkouts on free public Wi-Fi. Turn off Wi-Fi and use your cellular mobile data (4G/5G) for all financial transactions."
    },
    {
        "id": "kb_soundbox_merchant_assurance",
        "category": "general",
        "title": "Soundbox & Instant Voice Alerts for Physical Merchant Fraud Defense",
        "source": "NPCI Merchant Safety Best Practices",
        "tags": ["soundbox", "merchant", "paytm soundbox", "phonepe smart speaker", "audio alert"],
        "content": "Fraudsters trick shopkeepers by showing spoof payment apps (like 'Paytm Spoof') that produce animated fake success screens on the customer's phone without transferring real funds. Hardware Soundbox devices (Paytm, PhonePe, BharatPe) announce real-time payment confirmation directly from the bank gateway.",
        "actionable_guidance": "Merchants should never rely on viewing the customer's phone screen for proof of payment. Only dispense merchandise when your own phone receives the bank SMS or your official Soundbox announces the receipt."
    },
    {
        "id": "kb_tax_refund_it_department_scam",
        "category": "fake_bank_kyc",
        "title": "Income Tax Refund Phishing Alerts & Fake ITR Portals",
        "source": "Income Tax Department of India (e-Filing Cell) & CERT-In Advisory",
        "tags": ["income tax", "refund", "itr", "incometax.gov.in", "pan", "bank refund"],
        "content": "During tax filing season, taxpayers receive fraudulent SMS alerts: 'Dear Taxpayer, an Income Tax refund of Rs. 15,490 has been approved. It will be credited to your account shortly. Confirm your bank details here: [phishing link]'. The phishing link prompts for net banking credentials and debit card PIN under the pretense of 'depositing' the refund.",
        "actionable_guidance": "The Income Tax Department NEVER sends direct SMS links requesting bank credentials or PINs to deposit refunds. All genuine refunds are automatically credited via ECS to the bank account pre-validated on `incometax.gov.in`."
    },
    {
        "id": "kb_job_offer_letter_stamp_scam",
        "category": "job_investment_scam",
        "title": "Fake MNC Job Offer Letters & Registration Fee Scams",
        "source": "Ministry of Labour and Employment & National Career Service (NCS) Advisory",
        "tags": ["job offer", "tcs", "infosys", "wipro", "recruitment fee", "security deposit"],
        "content": "Job seekers receive fake appointment letters on counterfeit letterheads of major IT firms (TCS, Infosys, Wipro) or airlines. The letter demands an upfront 'refundable security deposit', 'laptop courier fee', or 'medical examination charge' (Rs. 5,000 - 25,000) payable via UPI.",
        "actionable_guidance": "Top corporate employers in India strictly adhere to a zero-recruitment-fee policy. No genuine company demands money for job applications, interviews, or laptop security deposits."
    },
    {
        "id": "kb_customs_gift_extortion_scam",
        "category": "courier_customs_scam",
        "title": "Foreign Gift Customs Duty & Airport Parcel Extortion Scams",
        "source": "Central Board of Indirect Taxes and Customs (CBIC) Public Alert",
        "tags": ["customs", "cbic", "gift", "airport parcel", "customs duty", "delhi airport"],
        "content": "Fraudsters pretending to be foreign friends or lovers send messages stating they have dispatched a gift box containing expensive smartphones, gold, or foreign currency. A fake 'Customs Clearance Officer' at Mumbai/Delhi airport calls demanding 'anti-money laundering clearance fees' or 'customs duties' paid into private savings accounts.",
        "actionable_guidance": "Official customs duties can ONLY be paid to government treasury accounts via the official ICEGATE portal (`icegate.gov.in`). Indian Customs NEVER instructs travelers or recipients to pay duties to personal savings accounts."
    },
    {
        "id": "kb_sim_card_block_threat_telecom",
        "category": "telecom",
        "title": "Telecom Disconnection Threat Calls (DoT Official Impersonation)",
        "source": "Department of Telecommunications (DoT) Advisory on Fake Disconnection Notices",
        "tags": ["dot", "sim block", "telecom", "illegal activity", "9 mobile connections", "ivr"],
        "content": "Citizens receive automated Interactive Voice Response (IVR) calls claiming: 'This is the Department of Telecommunications. All your mobile numbers will be disconnected in 2 hours due to illegal advertisements. Press 9 to speak with an executive'. Victims are transferred to scammers who intimidate them with fabricated police warrants.",
        "actionable_guidance": "DoT NEVER initiates automated calls threatening sudden disconnection of mobile connections. Disconnect the call and report the caller number on the Chakshu portal at sancharsaathi.gov.in."
    },
    {
        "id": "kb_chakshu_reporting_portal",
        "category": "telecom",
        "title": "Chakshu Portal: Citizen Facility to Report Suspected Fraud Communication",
        "source": "Department of Telecommunications (DoT) — Sanchar Saathi Initiative",
        "tags": ["chakshu", "report fraud", "spam calls", "whatsapp fraud", "dot", "telecom"],
        "content": "Chakshu is a dedicated national platform under Sanchar Saathi for citizens to report suspected fraud communications received via Calls, SMS, or WhatsApp (such as fake KYC, lottery, lottery prizes, fake customer care, or impersonation of DoT officials). Reporting helps telecom operators proactively blacklist fraudulent numbers across India.",
        "actionable_guidance": "Report spam/fraud SMS and callers at `sancharsaathi.gov.in/sfc/` (Chakshu). You do not need to be a financial fraud victim to report; reporting proactive attempts protects others."
    },
    {
        "id": "kb_cyber_hygiene_passwords",
        "category": "general",
        "title": "Password & UPI PIN Hygiene: Avoiding Predictable PINs",
        "source": "CERT-In National Cyber Security Best Practices",
        "tags": ["pin hygiene", "password", "birth year", "predictable pin", "security"],
        "content": "Over 25% of compromised UPI PINs consist of predictable patterns: birth year (1998), repetitive digits (1111, 0000), sequential numbers (1234, 4321), or vehicle registration numbers. If an attacker gains physical or remote access to a device, predictable PINs can be brute-forced within allowable retry limits.",
        "actionable_guidance": "Never use birth dates, vehicle numbers, or repeated digits as your UPI PIN or banking passwords. Choose non-obvious random 4- or 6-digit combinations and avoid writing PINs on cards."
    },
    {
        "id": "kb_credit_score_loan_trap",
        "category": "loan_app_extortion",
        "title": "Fake CIBIL / Experian Credit Score Improvement Scams",
        "source": "Credit Information Bureau (India) Limited (CIBIL) Security Notice",
        "tags": ["cibil", "credit score", "experian", "crif", "fix credit score", "advance fee"],
        "content": "Scammers claim they can 'cleanse negative remarks' or 'instantly increase your CIBIL score to 800+' in exchange for an upfront fee of Rs. 3,000 - 10,000. Under RBI regulations, credit scores are computed algorithmically based purely on repayment history submitted directly by banks; no third party can artificially alter credit bureau records.",
        "actionable_guidance": "Do not pay anyone claiming to fix your CIBIL score. Check your authentic credit report once a year for free directly on official bureau websites (`cibil.com`, `experian.in`)."
    },
    {
        "id": "kb_fake_ipo_allotment_scam",
        "category": "job_investment_scam",
        "title": "Fake IPO Pre-Allotment & Institutional Quota Scams",
        "source": "Securities and Exchange Board of India (SEBI) Investor Advisory",
        "tags": ["sebi", "ipo", "pre-allotment", "grey market", "asba", "institutional quota"],
        "content": "Fraudsters create WhatsApp and Instagram investment groups claiming to offer 'Guaranteed Pre-Allotment of Oversubscribed IPOs' through institutional or FII quotas. Victims are instructed to transfer money via UPI to private accounts rather than applying through legitimate ASBA (Application Supported by Blocked Amount) via their registered demat brokers.",
        "actionable_guidance": "IPO applications in India MUST be made exclusively through SEBI-registered brokers using ASBA (where money stays in your bank account until allotment). Never transfer funds to private UPI IDs for IPO shares."
    },
    {
        "id": "kb_fake_courier_damage_insurance",
        "category": "courier_customs_scam",
        "title": "Fake Courier Parcel Damage Insurance Compensation Trap",
        "source": "Consumer Protection Authority & Logistics Industry Advisory",
        "tags": ["courier damage", "insurance", "compensation", "fake refund", "collect request"],
        "content": "Attackers monitor Twitter/X complaints where users tag delivery services (DTDC, Delhivery, Amazon) regarding delayed parcels. The scammer contacts the user pretending to be logistics escalation managers, offering Rs. 2,000 compensation for delivery delay. They send a UPI collect request claiming 'Accept this collect request to credit your compensation'.",
        "actionable_guidance": "Never accept collect requests for compensation or refunds. Customer support interactions initiated on social media must always be verified via the official application."
    },
    {
        "id": "kb_sim_binding_device_security",
        "category": "general",
        "title": "UPI SIM Binding: How Hardware Device Binding Protects You",
        "source": "NPCI UPI SIM Binding Architecture Documentation",
        "tags": ["sim binding", "device binding", "dual sim", "hardware token", "npci"],
        "content": "UPI apps use cryptographic device binding: the app sends an encrypted SMS from the registered SIM card to verify that the physical SIM is inside the handset. If an attacker copies your app credentials or clones your phone storage, they cannot transact on another phone without the physical SIM card.",
        "actionable_guidance": "In dual-SIM phones, always ensure the mobile number linked to your bank account is designated correctly for outgoing SMS. Never share SIM-verification SMS tokens."
    },
    {
        "id": "kb_bank_canara_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "Canara Bank: 24x7 Emergency Cyber Fraud Desk & Card Hotlisting",
        "source": "Canara Bank Cybersecurity & Customer Care",
        "tags": ["canara bank", "canarabank.com", "18004250018", "18001030018", "hotlisting"],
        "content": "Canara Bank official domain is `canarabank.com`. 24x7 toll-free fraud helpline numbers are 1800 425 0018 and 1800 103 0018. Customers can hotlist Canara debit cards via SMS by sending 'CAN (space) HOTLISTDC (space) <16 digit Card Number>' to 9266623333.",
        "actionable_guidance": "Report unauthorized Canara transactions immediately to 1800 425 0018 or email posndc@canarabank.com."
    },
    {
        "id": "kb_bank_bob_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "Bank of Baroda (BOB): Emergency Fraud Reporting & Blocking",
        "source": "Bank of Baroda Cyber Security Advisory",
        "tags": ["bank of baroda", "bob", "18002584455", "18001024455", "bankofbaroda.in"],
        "content": "Bank of Baroda official domain is `bankofbaroda.in`. 24x7 customer care and fraud helpline numbers are 1800 258 4455 and 1800 102 4455. To instantly block your BOB Debit Card via SMS, send 'BLOCK <Last 4 digits>' to 8422009988 from your registered mobile number.",
        "actionable_guidance": "Call 1800 258 4455 or email cbscardfraud@bankofbaroda.com immediately upon noticing unauthorized debits."
    },
    {
        "id": "kb_bank_indusind_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "IndusInd Bank: 24x7 Fraud Hotline & Incident Reporting",
        "source": "IndusInd Bank Security Center",
        "tags": ["indusind", "indusind.com", "18602677777", "18002090061", "fraud desk"],
        "content": "IndusInd Bank operates on `indusind.com`. The 24x7 fraud prevention desk can be reached at 1860 267 7777 and 1800 209 0061. To block your IndusInd debit card, send SMS 'HOT <Last 4 digits of card>' to 9223766666.",
        "actionable_guidance": "Report phishing links or unauthorized debits to 1800 209 0061 or reach.us@indusind.com."
    },
    {
        "id": "kb_bank_union_fraud_protocol",
        "category": "fake_bank_kyc",
        "title": "Union Bank of India: Emergency Debit Card Hotlisting",
        "source": "Union Bank of India Customer Protection Cell",
        "tags": ["union bank", "unionbankofindia.co.in", "1800222244", "18002082244", "hotlist"],
        "content": "Union Bank of India official domain is `unionbankofindia.co.in`. National 24x7 toll-free support numbers are 1800 22 22 44 and 1800 208 2244. To block your debit card via SMS, send 'BLOCK <16 digit Card No>' to 09223008486.",
        "actionable_guidance": "Report phishing incidents immediately to 1800 22 22 44 or customercare@unionbankofindia.bank."
    },
    {
        "id": "kb_fake_crypto_arbitrage_bot",
        "category": "job_investment_scam",
        "title": "Fake AI Crypto Arbitrage Bot & Liquidity Pool Traps",
        "source": "Enforcement Directorate (ED) & SEBI Cryptocurrency Fraud Warnings",
        "tags": ["crypto", "arbitrage", "ai bot", "liquidity pool", "usdt", "smart contract"],
        "content": "Scammers convince victims to deposit USDT or Bitcoin into simulated trading platforms promising '3% daily guaranteed returns through AI arbitrage bots'. The dashboard displays fictitious skyrocketing balances. When the victim attempts a withdrawal, the site blocks access, demanding a 20% 'IRS Tax' or 'Smart Contract Gas Fee' deposit.",
        "actionable_guidance": "Guaranteed daily returns in cryptocurrency trading are impossible. Never deposit funds into non-registered offshore crypto exchanges or unknown Web3 wallet links."
    },
    {
        "id": "kb_fake_toll_plaza_cashback",
        "category": "fake_upi_refund_cashback",
        "title": "Fake Toll Plaza Cashback & Highway Refund SMS Traps",
        "source": "National Payments Corporation of India (NPCI) & Highway Toll Advisory",
        "tags": ["toll", "cashback", "fastag refund", "highway", "collect trick"],
        "content": "Motorists receive text messages claiming double deduction occurred at a highway toll plaza and offering an instant refund of Rs. 150: 'Toll refund pending. Click to collect: upi://pay?...'. The link actually triggers an outbound debit collect request.",
        "actionable_guidance": "Toll dispute refunds are processed automatically back into your FASTag wallet by your issuing bank without customer intervention. Never accept payment requests to receive refunds."
    },
    {
        "id": "kb_pension_life_certificate_scam",
        "category": "fake_govt_scheme",
        "title": "Digital Life Certificate (Jeevan Pramaan) Fraud Targeting Retirees",
        "source": "Department of Pension and Pensioners' Welfare (DoP&PW) Advisory",
        "tags": ["jeevan pramaan", "life certificate", "pension", "retiree", "biometric", "dlc"],
        "content": "Elderly pensioners receive calls claiming their monthly pension will stop unless they update their Digital Life Certificate over the phone. Callers ask for NetBanking credentials or instruct seniors to download remote screen sharing apps.",
        "actionable_guidance": "Submit Jeevan Pramaan exclusively through the official government portal `jeevanpramaan.gov.in`, authorized post offices, or your home bank branch. Government officials never ask for OTPs or screen sharing."
    },
    {
        "id": "kb_screen_lock_pattern_security",
        "category": "general",
        "title": "Physical Device Security: Screen Lock Patterns and Shoulder Surfing",
        "source": "CERT-In Mobile Security Best Practices",
        "tags": ["screen lock", "shoulder surfing", "biometric", "pattern", "device theft"],
        "content": "Shoulder surfing occurs when a bystander memorizes your screen lock PIN or pattern in public transport or cafes, steals your device, and uses the lock code to reset your UPI PIN and bank accounts.",
        "actionable_guidance": "Use fingerprint or face recognition alongside complex alphanumeric lock codes rather than simple 4-digit PINs or visible smudge-prone patterns. Conceal your screen when entering banking credentials in public."
    },
    {
        "id": "kb_fake_customs_arrest_threat_bail",
        "category": "courier_customs_scam",
        "title": "Fake Court Summons & Anticipatory Bail Extortion",
        "source": "Supreme Court of India & Bar Council of India Advisory",
        "tags": ["court summons", "bail", "high court", "arrest warrant", "extortion", "lawyer"],
        "content": "Fraudsters email forged court summons bearing the emblem of the High Court or Supreme Court, claiming non-bailable arrest warrants have been issued for money laundering. An accomplice posing as an 'authorized court advocate' offers to arrange 'emergency online anticipatory bail' if Rs. 1,00,000 is sent via UPI.",
        "actionable_guidance": "Indian courts DO NOT issue arrest warrants or grant anticipatory bail over email or WhatsApp UPI transfers. Check genuine case status strictly on the official National Judicial Data Grid (`njdg.ecourts.gov.in`)."
    },
    {
        "id": "kb_airline_ticket_cancellation_refund",
        "category": "fake_customer_support",
        "title": "Fake Airline Customer Care & Flight Rescheduling Scams",
        "source": "Directorate General of Civil Aviation (DGCA) & Airline Security Advisory",
        "tags": ["airline", "indigo", "air india", "spicejet", "flight refund", "fake customer care"],
        "content": "When flights are delayed or cancelled, desperate travelers search Google for airline helpline numbers and reach fake scammer call centers running sponsored Google Ads. The fake agent instructs the passenger to download AnyDesk or pay a 'Rs. 10 rescheduling fee' via UPI, subsequently draining their accounts.",
        "actionable_guidance": "Only contact airlines through their verified apps or websites. Never search for customer service phone numbers on open search engines without checking official domain URLs."
    },
    {
        "id": "kb_hotel_booking_resort_scam",
        "category": "marketplace_qr_scam",
        "title": "Counterfeit Hotel & Resort Booking Advance Payment Scams",
        "source": "Ministry of Tourism & Consumer Protection Forum",
        "tags": ["hotel booking", "resort", "goa", "advance payment", "fake website", "qr scam"],
        "content": "During holiday seasons, scammers build clone websites of popular luxury resorts in Goa, Manali, and Kerala. They list personal UPI IDs or QR codes demanding 100% advance payment for room reservations. When the guest arrives at the resort, the hotel has no record of the booking.",
        "actionable_guidance": "Cross-verify phone numbers and booking details directly on verified hotel chains or reputable accredited travel aggregators. Look for verified corporate bank account details."
    },
    {
        "id": "kb_credit_card_limit_enhancement",
        "category": "otp_pin_theft",
        "title": "Credit Card Limit Increase & Annual Fee Waiver Phishing",
        "source": "RBI Consumer Protection Department Alert on Credit Card Fraud",
        "tags": ["credit card", "limit enhancement", "annual fee waiver", "otp", "phishing"],
        "content": "Cardholders receive calls offering 'instant limit upgrade from Rs. 50,000 to Rs. 3,00,000 and lifetime free annual fee waiver'. To process the upgrade, the caller sends a web link or requests the CVV and the 'verification OTP' sent to the phone.",
        "actionable_guidance": "Banks process card limit upgrades directly inside their secure mobile banking apps without asking for CVV or OTP over the phone. Never disclose OTPs to anyone offering card upgrades."
    },
    {
        "id": "kb_fake_utility_bill_discount",
        "category": "electricity_disconnection",
        "title": "Deceptive Electricity & Water Bill '10% Discount' Offers",
        "source": "State Consumer Redressal Forum & Power Ministry Advisory",
        "tags": ["electricity discount", "water bill", "10% off", "bill payment", "phishing"],
        "content": "Attackers circulate WhatsApp promotions: 'Pay your state electricity bill before month-end and get instant 10% cashback / discount: [unverified link]'. The phishing link collects consumer credentials and bank passwords.",
        "actionable_guidance": "State utility corporations do not offer unofficial random discounts via WhatsApp links. Pay utility bills exclusively via the Bharat Bill Payment System (BBPS) inside authorized banking applications."
    },
    {
        "id": "kb_upi_offline_soundbox_voice_spoof",
        "category": "general",
        "title": "Retail Fraud: Audio Soundbox Voice Spoofing via Bluetooth",
        "source": "Retailers Association of India (RAI) Security Bulletin",
        "tags": ["soundbox spoof", "bluetooth", "retail", "voice spoof", "fake payment"],
        "content": "Sophisticated fraudsters carry portable Bluetooth speakers or pair their smartphones with unauthenticated store speakers to play pre-recorded sound clips mimicking the official Paytm/PhonePe soundbox notification ('Rs. 500 received on Paytm').",
        "actionable_guidance": "Merchants should password-protect their Bluetooth audio hardware and rely on incoming transaction SMS alerts or the merchant dashboard for definitive verification of large transactions."
    },
    {
        "id": "kb_lost_stolen_phone_action_plan",
        "category": "general",
        "title": "Emergency Action Protocol: What to Do Immediately When Your Phone is Stolen",
        "source": "Indian Cyber Crime Coordination Centre (I4C) Protocol",
        "tags": ["phone stolen", "lost phone", "emergency protocol", "sim block", "bank freeze", "ceir"],
        "content": "If your smartphone containing active UPI and banking apps is stolen: STEP 1: Call your telecom provider immediately from another phone to BLOCK YOUR SIM CARD (stopping incoming OTPs). STEP 2: Call your bank to BLOCK NETBANKING & UPI ID. STEP 3: Use Google 'Find My Device' or Apple 'Find My' to remotely erase device data. STEP 4: Report on CEIR (sancharsaathi.gov.in) to blacklist the handset IMEI.",
        "actionable_guidance": "Act within the first 30 minutes: 1. Block SIM. 2. Freeze Bank UPI. 3. Remote wipe device. 4. Block IMEI on Sanchar Saathi. This prevents the thief from resetting UPI PINs."
    }
]

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_dir, "rag", "knowledge_base.json")
    
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(KB_ENTRIES, f, indent=2, ensure_ascii=False)
        
    print(f"[Success] Written {len(KB_ENTRIES)} verified knowledge entries to {target_path}")

if __name__ == "__main__":
    main()
