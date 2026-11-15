def evaluate_loan_application(
    age: int,
    annual_income: float,
    credit_score: int,
    existing_debt: float,
    employment_years: float,
    has_cosigner: bool,
    loan_amount: float,
) -> tuple[str, float, str]:
    """
    Evaluates a loan application using deterministic rule-based if/elif/else logic.
    Returns: (Decision, Interest Rate %, Reason)
    """
    # 1. Basic Eligibility Checks
    if age < 18:
        return ("REJECTED", 0.0, "Applicant must be at least 18 years old.")
    elif age > 75:
        if loan_amount > 20000:
            return ("REJECTED", 0.0, "High loan amount not permitted for applicants over 75.")
        elif not has_cosigner:
            return ("REJECTED", 0.0, "Applicants over 75 require a co-signer.")

    # 2. Income & Debt-to-Income (DTI) Ratio Checks
    if annual_income <= 0:
        return ("REJECTED", 0.0, "Applicant must have a verifiable positive income.")

    dti_ratio = existing_debt / annual_income

    if dti_ratio > 0.50:
        if has_cosigner and credit_score >= 720:
            pass  # Exception granted for high credit + co-signer
        else:
            return ("REJECTED", 0.0, f"Debt-to-income ratio too high ({dti_ratio:.0%}).")
    elif dti_ratio > 0.40:
        if loan_amount > annual_income * 0.5:
            return ("REJECTED", 0.0, "Requested loan is too large given existing debt.")

    # 3. Credit Score & Employment Tiering
    if credit_score >= 760:
        if employment_years >= 2.0:
            return ("APPROVED", 5.5, "Prime Tier: Excellent credit and stable employment.")
        elif employment_years >= 0.5:
            return ("APPROVED", 6.2, "Prime Tier: Excellent credit, short employment history.")
        else:
            if has_cosigner:
                return ("APPROVED", 6.5, "Approved with co-signer due to new employment.")
            else:
                return ("MANUAL REVIEW", 0.0, "Excellent credit, but requires 6+ months on the job.")

    elif 680 <= credit_score < 760:
        if employment_years >= 3.0 and dti_ratio < 0.30:
            return ("APPROVED", 7.8, "Standard Tier: Good credit and low debt.")
        elif employment_years >= 1.0:
            if loan_amount <= 25000:
                return ("APPROVED", 8.9, "Standard Tier: Capped loan approval.")
            else:
                return ("MANUAL REVIEW", 0.0, "Loan amount exceeds automated limit for this tier.")
        else:
            return ("REJECTED", 0.0, "Insufficient employment history for credit tier.")

    elif 600 <= credit_score < 680:
        if has_cosigner:
            if dti_ratio < 0.35 and employment_years >= 2.0:
                return ("APPROVED", 11.5, "Subprime Tier: Approved with qualified co-signer.")
            else:
                return ("MANUAL REVIEW", 0.0, "Co-signer present, but debt/employment needs review.")
        else:
            if loan_amount <= 5000 and employment_years >= 4.0:
                return ("APPROVED", 13.9, "Micro-loan approved based on long job stability.")
            else:
                return ("REJECTED", 0.0, "Credit score too low without a co-signer.")

    else:
        # Credit score below 600
        if has_cosigner and loan_amount <= 3000 and employment_years >= 5.0:
            return ("MANUAL REVIEW", 0.0, "High-risk exception routed to senior underwriter.")
        else:
            return ("REJECTED", 0.0, f"Credit score ({credit_score}) below minimum threshold.")


# --- Test Cases ---
applicants = [
    {"name": "Alice", "age": 32, "annual_income": 95000, "credit_score": 785, "existing_debt": 15000, "employment_years": 4.0, "has_cosigner": False, "loan_amount": 30000},
    {"name": "Bob",   "age": 24, "annual_income": 48000, "credit_score": 640, "existing_debt": 12000, "employment_years": 2.5, "has_cosigner": True,  "loan_amount": 10000},
    {"name": "Charlie", "age": 17, "annual_income": 20000, "credit_score": 700, "existing_debt": 0, "employment_years": 1.0, "has_cosigner": True, "loan_amount": 2000},
    {"name": "Diana", "age": 45, "annual_income": 60000, "credit_score": 620, "existing_debt": 10000, "employment_years": 5.0, "has_cosigner": False, "loan_amount": 4000},
    {"name": "Evan",  "age": 29, "annual_income": 55000, "credit_score": 570, "existing_debt": 20000, "employment_years": 1.0, "has_cosigner": False, "loan_amount": 15000},
]

for person in applicants:
    name = person.pop("name")
    decision, rate, reason = evaluate_loan_application(**person)
    rate_str = f" @ {rate}%" if rate > 0 else ""
    print(f"{name:8} -> {decision:13}{rate_str:8} | {reason}")