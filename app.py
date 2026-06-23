from functools import wraps

from flask import Flask, redirect, render_template, request, session, url_for
import json

try:
    with open("users.json", "r") as file:
        users = json.load(file)
except FileNotFoundError:
    users = {}

app = Flask(__name__)
app.secret_key = "hello"

users = {
    "chloe123": {
        "password": "1234",
        "accounts": {
            "checking": 1000,
            "savings": 500
        },
        "first_name": "Chloe",
        "last_name": "Gates",
        "email_address": "cgates123@gmail.com",
        "phone_number": "470-582-8286",
        "date_of_birth": "11/19/2002",
    },
    "mike22": {
        "password": "abcd",
        "accounts": {
            "checking": 3000,
            "savings": 1200
        },
        "first_name": "Mike",
        "last_name": "Jacobs",
        "email_address": "mjacobs456@gmail.com",
        "phone_number": "404-252-88745",
        "date_of_birth": "09/10/2000"
    }
}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("sign_in"))
        return view(*args, **kwargs)
    return wrapped


def logged_in_context(active_page=None):
    return {"logged_in": True, "active_page": active_page}


def public_context(active_page=None):
    return {"logged_in": False, "active_page": active_page}


BANKING_PAGES = {
    "personal": {
        "title": "Personal Banking",
        "headline": "Personal Banking",
        "subtitle": "Checking, savings, and everyday tools built for your life.",
        "sections": [
            {
                "title": "Everyday Checking",
                "body": "No monthly maintenance fees with direct deposit. Free debit card, mobile deposit, and bill pay included.",
                "cta_url": None,
                "cta_label": None,
            },
            {
                "title": "High-Yield Savings",
                "body": "Earn competitive interest on your balance with no minimum deposit to open.",
                "cta_url": None,
                "cta_label": None,
            },
        ],
        "features": [
            {"icon": "💳", "title": "Free Debit Card", "body": "Tap to pay and ATM access nationwide."},
            {"icon": "📱", "title": "Mobile Deposit", "body": "Snap a photo to deposit checks from anywhere."},
            {"icon": "🔔", "title": "Account Alerts", "body": "Get notified about balances and transactions."},
        ],
    },
    "business": {
        "title": "Business Banking",
        "headline": "Business Banking",
        "subtitle": "Accounts and tools to help your business grow.",
        "sections": [
            {
                "title": "Business Checking",
                "body": "Manage cash flow with unlimited transactions and integrated payroll support.",
                "cta_url": None,
                "cta_label": None,
            },
            {
                "title": "Merchant Services",
                "body": "Accept card payments in-store and online with competitive processing rates.",
                "cta_url": None,
                "cta_label": None,
            },
        ],
        "features": [
            {"icon": "🏢", "title": "Multi-User Access", "body": "Assign roles for owners, managers, and bookkeepers."},
            {"icon": "📊", "title": "Reporting", "body": "Export transactions for QuickBooks and tax prep."},
            {"icon": "💼", "title": "Business Loans", "body": "Lines of credit and term loans for expansion."},
        ],
    },
    "commercial": {
        "title": "Commercial Banking",
        "headline": "Commercial Banking",
        "subtitle": "Treasury, lending, and advisory services for larger organizations.",
        "sections": [
            {
                "title": "Treasury Management",
                "body": "Optimize liquidity with wire transfers, ACH origination, and fraud prevention tools.",
                "cta_url": None,
                "cta_label": None,
            },
            {
                "title": "Commercial Lending",
                "body": "Real estate, equipment, and working capital financing tailored to your industry.",
                "cta_url": None,
                "cta_label": None,
            },
        ],
        "features": [
            {"icon": "🌐", "title": "Global Payments", "body": "International wire and foreign exchange services."},
            {"icon": "🛡️", "title": "Fraud Protection", "body": "Positive pay and dual-control approvals."},
            {"icon": "🤝", "title": "Dedicated Advisor", "body": "A relationship manager who knows your business."},
        ],
    },
    "community": {
        "title": "Community",
        "headline": "Community Commitment",
        "subtitle": "Banking that invests in the neighborhoods we serve.",
        "sections": [
            {
                "title": "Financial Literacy",
                "body": "Free workshops on budgeting, credit, and homeownership across Atlanta.",
                "cta_url": None,
                "cta_label": None,
            },
            {
                "title": "Local Sponsorships",
                "body": "We partner with schools, nonprofits, and small businesses to strengthen our community.",
                "cta_url": None,
                "cta_label": None,
            },
        ],
        "features": [
            {"icon": "🎓", "title": "Youth Programs", "body": "Student savings accounts and scholarship funds."},
            {"icon": "🌱", "title": "Small Business Grants", "body": "Annual grants for local entrepreneurs."},
            {"icon": "❤️", "title": "Volunteer Days", "body": "Employees donate 1,000+ hours each year."},
        ],
    },
    "how_it_works": {
        "title": "How It Works",
        "headline": "How BANKAHEAD Works",
        "subtitle": "Open an account in minutes and bank from anywhere.",
        "sections": [
            {"title": "1. Sign Up", "body": "Create your profile with basic personal information.", "cta_url": None, "cta_label": None},
            {"title": "2. Choose Accounts", "body": "Select checking, savings, or both — no minimum balance required.", "cta_url": None, "cta_label": None},
            {"title": "3. Start Banking", "body": "Transfer money, pay bills, and track spending online or in our app.", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "testimonials": {
        "title": "Testimonials",
        "headline": "What Our Customers Say",
        "subtitle": "Trusted by families and businesses across Georgia.",
        "sections": [
            {"title": "Chloe G.", "body": "“Switching to BANKAHEAD was the easiest financial decision I’ve made. Transfers are instant and support is always helpful.”", "cta_url": None, "cta_label": None},
            {"title": "Mike J.", "body": "“I run a small business and their business checking saved me hours every month on bookkeeping.”", "cta_url": None, "cta_label": None},
            {"title": "Sarah T.", "body": "“The mobile app is clean and simple. I deposit checks from my couch.”", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "careers": {
        "title": "Careers",
        "headline": "Careers at BANKAHEAD",
        "subtitle": "Build a career with purpose at a community-focused bank.",
        "sections": [
            {"title": "Branch Associate", "body": "Full-time · Atlanta, GA · Help customers with everyday banking needs.", "cta_url": None, "cta_label": None},
            {"title": "Commercial Loan Officer", "body": "Full-time · Atlanta, GA · Structure lending solutions for business clients.", "cta_url": None, "cta_label": None},
            {"title": "Software Engineer", "body": "Full-time · Remote · Build secure digital banking experiences.", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "investments": {
        "title": "Investments",
        "headline": "Investments & Wealth",
        "subtitle": "Plan for tomorrow with guidance from licensed advisors.",
        "sections": [
            {"title": "Retirement Planning", "body": "IRAs, 401(k) rollovers, and long-term portfolio strategies.", "cta_url": None, "cta_label": None},
            {"title": "Managed Portfolios", "body": "Diversified investments aligned to your risk tolerance and timeline.", "cta_url": None, "cta_label": None},
        ],
        "features": [
            {"icon": "📈", "title": "Market Insights", "body": "Quarterly reports and advisor check-ins."},
            {"icon": "🎯", "title": "Goal Tracking", "body": "Monitor progress toward retirement and major purchases."},
            {"icon": "🔒", "title": "Secure Accounts", "body": "SIPC-insured brokerage through partner institutions."},
        ],
    },
    "terms": {
        "title": "Terms of Service",
        "headline": "Terms of Service",
        "subtitle": "Important information about using BANKAHEAD products.",
        "sections": [
            {"title": "Account Agreement", "body": "By opening an account you agree to our deposit account terms, fee schedule, and electronic communications policy.", "cta_url": None, "cta_label": None},
            {"title": "Online Banking", "body": "You are responsible for safeguarding your login credentials and reporting unauthorized activity within 60 days.", "cta_url": None, "cta_label": None},
            {"title": "Privacy", "body": "We do not sell your personal information. See our privacy notice for details on data collection and sharing.", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "contact": {
        "title": "Contact",
        "headline": "Contact Us",
        "subtitle": "We’re here to help — reach out anytime.",
        "sections": [
            {"title": "Phone", "body": "1-800-BANK-HEAD (1-800-226-5432) · Mon–Fri 8am–8pm, Sat 9am–5pm ET", "cta_url": None, "cta_label": None},
            {"title": "Email", "body": "support@bankahead.com — we respond within one business day.", "cta_url": None, "cta_label": None},
            {"title": "Mail", "body": "BANKAHEAD · 100 Peachtree St NW · Atlanta, GA 30303", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "support": {
        "title": "Support",
        "headline": "Customer Support",
        "subtitle": "Get answers and resolve issues quickly.",
        "sections": [
            {"title": "Account Help", "body": "Locked out, forgot password, or need to update your profile? Call or chat with us.", "cta_url": None, "cta_label": None},
            {"title": "Disputes", "body": "Report unauthorized transactions within 60 days for full fraud protection.", "cta_url": None, "cta_label": None},
            {"title": "Technical Support", "body": "Mobile app or online banking not working? Our tech team is available 24/7.", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "branches": {
        "title": "Branch Locations",
        "headline": "Branch & ATM Locations",
        "subtitle": "Visit us in person across the Atlanta metro area.",
        "sections": [
            {"title": "Downtown Atlanta", "body": "100 Peachtree St NW · Open Mon–Fri 9am–5pm", "cta_url": None, "cta_label": None},
            {"title": "Midtown", "body": "950 West Peachtree St NW · Open Mon–Fri 9am–5pm, Sat 10am–2pm", "cta_url": None, "cta_label": None},
            {"title": "Decatur", "body": "125 Clairemont Ave · Open Mon–Fri 9am–5pm", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "loans": {
        "title": "Loans",
        "headline": "Loans & Lending",
        "subtitle": "Competitive rates for auto, home, and personal needs.",
        "sections": [
            {"title": "Auto Loans", "body": "Rates from 5.49% APR with terms up to 72 months. Pre-approval in minutes.", "cta_url": None, "cta_label": None},
            {"title": "Home Mortgages", "body": "Fixed and adjustable rates, first-time buyer programs, and refinancing options.", "cta_url": None, "cta_label": None},
            {"title": "Personal Loans", "body": "Borrow $1,000–$50,000 with no prepayment penalties.", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "credit_cards": {
        "title": "Credit Cards",
        "headline": "Credit Cards",
        "subtitle": "Rewards and low rates for every spending style.",
        "sections": [
            {"title": "Cash Back Card", "body": "2% cash back on all purchases. No annual fee.", "cta_url": None, "cta_label": None},
            {"title": "Travel Rewards", "body": "3x points on travel and dining. No foreign transaction fees.", "cta_url": None, "cta_label": None},
            {"title": "Student Card", "body": "Build credit with a low limit and free credit score monitoring.", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "mobile_banking": {
        "title": "Mobile Banking",
        "headline": "Mobile Banking",
        "subtitle": "Your bank in your pocket — secure and easy to use.",
        "sections": [
            {"title": "Download the App", "body": "Available on iOS and Android. Biometric login and instant balance alerts.", "cta_url": None, "cta_label": None},
            {"title": "Mobile Deposit", "body": "Deposit checks by taking a photo — funds available next business day.", "cta_url": None, "cta_label": None},
        ],
        "features": [
            {"icon": "📲", "title": "Bill Pay", "body": "Schedule and manage payments from your phone."},
            {"icon": "🔐", "title": "Face ID / Touch ID", "body": "Quick, secure access without typing passwords."},
            {"icon": "💬", "title": "In-App Chat", "body": "Message support without leaving the app."},
        ],
    },
    "security": {
        "title": "Security",
        "headline": "Security Center",
        "subtitle": "How we protect your money and personal information.",
        "sections": [
            {"title": "Encryption", "body": "256-bit SSL encryption on all online and mobile sessions.", "cta_url": None, "cta_label": None},
            {"title": "Fraud Monitoring", "body": "24/7 transaction monitoring with automatic card lock on suspicious activity.", "cta_url": None, "cta_label": None},
            {"title": "Your Role", "body": "Never share your password, use unique credentials, and enable two-factor authentication.", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "rates": {
        "title": "Rates",
        "headline": "Current Rates",
        "subtitle": "Transparent pricing updated weekly.",
        "sections": [
            {"title": "Savings APY", "body": "4.25% APY on balances up to $250,000.", "cta_url": None, "cta_label": None},
            {"title": "Checking", "body": "No monthly fee with $500 direct deposit or $1,500 average balance.", "cta_url": None, "cta_label": None},
            {"title": "Auto Loan APR", "body": "Starting at 5.49% APR for qualified borrowers.", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
    "faq": {
        "title": "FAQ",
        "headline": "Frequently Asked Questions",
        "subtitle": "Quick answers to common banking questions.",
        "sections": [
            {"title": "How do I open an account?", "body": "Click Sign Up, enter your personal information, create a username and password, and you’re ready to go.", "cta_url": None, "cta_label": None},
            {"title": "Is my money insured?", "body": "Yes — deposits are FDIC insured up to $250,000 per depositor.", "cta_url": None, "cta_label": None},
            {"title": "How do I transfer money?", "body": "Log in and go to Pay and Transfer to move funds between your checking and savings accounts.", "cta_url": None, "cta_label": None},
        ],
        "features": [],
    },
}


def render_banking_page(page_key, active_page=None):
    page = BANKING_PAGES[page_key].copy()
    if "user" in session:
        ctx = logged_in_context(active_page or page_key)
    else:
        ctx = public_context(active_page or page_key)
    return render_template("info_page.html", page=page, **ctx)


# Sign in
@app.route("/", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and users[username]["password"] == password:
            session["user"] = username
            return redirect(url_for("my_accounts"))
        return render_template(
            "Sign_In.html",
            error="Invalid username or password",
            **public_context("sign_in"),
        )

    return render_template("Sign_In.html", **public_context("sign_in"))


# Homepage (logged in)
@app.route("/home")
@login_required
def home():
    user = session["user"]
    user_data = users[user]
    return render_template(
        "index.html",
        username=user,
        first_name=user_data["first_name"],
        **logged_in_context("home"),
    )


@app.route("/users")
@login_required
def show_users():
    user = session["user"]
    return f"<h1>Logged in as: {user}</h1>"


@app.route("/my_accounts")
@login_required
def my_accounts():
    user = session["user"]
    user_accounts = users[user]["accounts"]
    total = user_accounts["checking"] + user_accounts["savings"]
    return render_template(
        "my_accounts.html",
        accounts=user_accounts,
        total=total,
        **logged_in_context("accounts"),
    )


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("sign_in"))


@app.route("/add_account")
@login_required
def add_account():
    return render_template("add_account.html", **logged_in_context("accounts"))


@app.route("/add_checking_account")
@login_required
def add_checking_account():
    return render_template("add_checking_account.html", **logged_in_context("accounts"))


@app.route("/pay_and_transfer")
@login_required
def pay_and_transfer():
    user = session["user"]
    return render_template(
        "pay_and_transfer.html",
        accounts=users[user]["accounts"],
        message=None,
        **logged_in_context("transfer"),
    )


@app.route("/transfer", methods=["POST"])
@login_required
def transfer():
    user = session["user"]

    from_account = request.form["from_account"]
    to_account = request.form["to_account"]
    amount = float(request.form["amount"])

    if from_account == to_account:
        return render_template(
            "pay_and_transfer.html",
            accounts=users[user]["accounts"],
            error="Choose two different accounts",
            **logged_in_context("transfer"),
        )

    if users[user]["accounts"][from_account] < amount:
        return render_template(
            "pay_and_transfer.html",
            accounts=users[user]["accounts"],
            error="Insufficient funds",
            **logged_in_context("transfer"),
        )

    users[user]["accounts"][from_account] -= amount
    users[user]["accounts"][to_account] += amount

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    return render_template(
        "pay_and_transfer.html",
        accounts=users[user]["accounts"],
        message=f"Successfully transferred ${amount:.2f}",
        **logged_in_context("transfer"),
    )


@app.route("/services")
@login_required
def services():
    return render_template("services.html", **logged_in_context("services"))


@app.route("/profile")
@login_required
def profile():
    user = session["user"]
    return render_template(
        "profile.html",
        username=user,
        user_info=users[user],
        **logged_in_context("profile"),
    )


# Sign up flow
@app.route("/personal_info")
def personal_info():
    return render_template("personal_info.html", **public_context("signup"))


@app.route("/create_user_password", methods=["POST"])
def create_user_password():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    dob = request.form.get("date_of_birth")
    phone = request.form.get("phone_number")
    email = request.form.get("email_address")

    session["signup"] = {
        "first_name": first_name,
        "last_name": last_name,
        "date_of_birth": dob,
        "phone_number": phone,
        "email_address": email,
    }

    if not all([first_name, last_name, dob, phone, email]):
        return "No information added or information incomplete"

    return render_template("create_user_password.html", **public_context("signup"))


@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form.get("usrnme")
    password = request.form.get("psswrd")
    confirm_password = request.form.get("cnfrm_psswrd")

    if not all([username, password, confirm_password]):
        return "Please fill in all fields"

    if password != confirm_password:
        return "Passwords do not match"

    if username in users:
        return "Username already exists"

    signup = session.get("signup")
    if not signup:
        return redirect(url_for("personal_info"))

    users[username] = {
        "password": password,
        "accounts": {"checking": 0, "savings": 0},
        "first_name": signup["first_name"],
        "last_name": signup["last_name"],
        "email_address": signup["email_address"],
        "phone_number": signup["phone_number"],
        "date_of_birth": signup["date_of_birth"],
    }

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    session.pop("signup", None)
    return redirect(url_for("sign_in"))


# Public banking info pages
@app.route("/personal")
def personal_banking():
    return render_banking_page("personal", "personal")


@app.route("/business")
def business_banking():
    return render_banking_page("business", "business")


@app.route("/commercial")
def commercial_banking():
    return render_banking_page("commercial", "commercial")


@app.route("/community")
def community():
    return render_banking_page("community", "community")


@app.route("/how-it-works")
def how_it_works():
    page = BANKING_PAGES["how_it_works"].copy()
    page["sections"][0]["cta_url"] = url_for("personal_info")
    page["sections"][0]["cta_label"] = "Sign Up Now"
    ctx = logged_in_context("how_it_works") if "user" in session else public_context("how_it_works")
    return render_template("info_page.html", page=page, **ctx)


@app.route("/testimonials")
def testimonials():
    return render_banking_page("testimonials")


@app.route("/careers")
def careers():
    return render_banking_page("careers")


@app.route("/investments")
def investments():
    return render_banking_page("investments")


@app.route("/terms")
def terms():
    return render_banking_page("terms")


@app.route("/contact")
def contact():
    return render_banking_page("contact")


@app.route("/support")
def support():
    return render_banking_page("support")


@app.route("/branches")
def branches():
    return render_banking_page("branches")


@app.route("/loans")
def loans():
    return render_banking_page("loans")


@app.route("/credit-cards")
def credit_cards():
    return render_banking_page("credit_cards")


@app.route("/mobile-banking")
def mobile_banking():
    return render_banking_page("mobile_banking")


@app.route("/security")
def security():
    return render_banking_page("security")


@app.route("/rates")
def rates():
    return render_banking_page("rates")


@app.route("/faq")
def faq():
    return render_banking_page("faq")


@app.route("/all_users")
def all_users():
    return str(users)


if __name__ == "__main__":
    app.run(debug=True)
