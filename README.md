# 🚀 Playwright Enterprise Automation Framework

A scalable and maintainable **Playwright + Python** automation framework designed for end-to-end UI and API testing. The framework follows industry best practices such as the **Page Object Model (POM)**, reusable utilities, detailed reporting, logging, and continuous integration using **GitHub Actions**.

This project demonstrates how to build a production-ready automation framework suitable for enterprise applications while maintaining clean architecture, readability, and scalability.

---

# 📌 Project Highlights

* ✅ UI Automation using Playwright
* ✅ API Automation using Playwright APIRequestContext
* ✅ Page Object Model (POM)
* ✅ Pytest Framework
* ✅ Cross-browser execution
* ✅ HTML Reports
* ✅ Allure Reports
* ✅ Screenshot capture on failures
* ✅ Logging for debugging
* ✅ GitHub Actions CI/CD Integration
* ✅ Configurable execution using fixtures and configuration files
* ✅ Reusable utilities and helper methods
* ✅ Clean folder structure for easy maintenance

---

# 🛠 Tech Stack

| Technology     | Purpose                |
| -------------- | ---------------------- |
| Python         | Programming Language   |
| Playwright     | UI & API Automation    |
| Pytest         | Test Framework         |
| Allure         | Advanced Reporting     |
| HTML Report    | Test Execution Report  |
| GitHub Actions | Continuous Integration |
| Git            | Version Control        |
| GitHub         | Source Code Management |

---

# 📂 Project Structure

```text
Playwright_Enterprise_Framework/
│
├── config/
├── pages/
├── tests/
│   ├── ui/
│   └── api/
├── utilities/
├── reports/
├── screenshots/
├── logs/
├── allure-results/
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md
```

---

# ⚙️ Features Implemented

### UI Automation

* Login Validation
* Logout Validation
* Note Creation
* Note Update
* Note Deletion
* Navigation Validation
* Form Validation
* Error Message Validation
* End-to-End User Flow

---

### API Automation

* User Authentication
* Create Note
* Get Notes
* Get Note by ID
* Update Note
* Delete Note
* Response Validation
* Status Code Validation
* Authentication Validation
* Negative Test Scenarios

---

# 📊 Reporting

The framework generates:

* HTML Report
* Allure Report
* Execution Logs
* Screenshots for Failed Tests

These reports help identify failures quickly and provide detailed execution insights.

---

# 🔄 Continuous Integration

GitHub Actions is configured to automatically:

* Install project dependencies
* Execute the complete automation suite
* Generate test reports
* Upload Allure artifacts
* Provide execution status for every commit and pull request

---

# ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/sapellysaivivek/Playwright_Enterprise_Framework.git
```

Navigate to the project:

```bash
cd Playwright_Enterprise_Framework
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

---

# ▶️ Execute Tests

Run all tests:

```bash
pytest
```

Run only UI tests:

```bash
pytest -m ui
```

Run only API tests:

```bash
pytest -m api
```

Run tests with HTML report:

```bash
pytest --html=reports/report.html
```

Generate Allure report:

```bash
allure serve allure-results
```

---

# 📈 Skills Demonstrated

This project demonstrates practical experience in:

* Test Automation Framework Design
* Playwright Automation
* API Testing
* UI Testing
* Page Object Model
* Pytest Fixtures
* Assertions
* Logging
* Reporting
* CI/CD Pipeline
* Git & GitHub
* Automation Best Practices

---

# 📸 Screenshots

Add screenshots in this section after uploading them to your repository.

Suggested screenshots:

* ✅ GitHub Actions Successful Workflow
* ✅ Allure Dashboard
* ✅ HTML Report
* ✅ Project Folder Structure

---

# 🚀 Future Enhancements

* Parallel Execution
* Data-Driven Testing
* Environment-based Configuration
* Docker Integration
* Performance Testing
* Advanced API Assertions
* Test Data Management
* Code Coverage Metrics

---

# 👨‍💻 About Me

I am a Quality Assurance Automation Engineer passionate about building scalable and maintainable automation frameworks using modern testing tools and best practices.

I enjoy working on:

* UI Automation
* API Automation
* Test Framework Development
* CI/CD Pipelines
* Software Quality Engineering

---

## ⭐ Support

If you found this project helpful, consider giving the repository a ⭐ on GitHub.

Thank you for visiting this repository!
