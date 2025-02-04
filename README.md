# 🛠️ GitHub to Gitea Migration Script  

> **Forked from** [GitHub Repository Migration to Gitea Script](https://www.wyr.me/post/612)  

This script provides an automated way to **migrate GitHub repositories to a self-hosted Gitea instance** using **Token authentication**.  

---

## 🚀 Why I Created This Script  

I developed this script out of necessity—**to regain control over my own code**. My experience with GitHub's restrictive handling of my access to GitHub Copilot left me not only **frustrated** but also **deeply concerned** about the security and reliability of the platform.  

### 📌 What Happened?  

One day, I suddenly lost access to GitHub Copilot, and some pages on GitHub started loading unusually slowly. I reached out to GitHub support, only to be told that I had allegedly engaged in **"abusive behavior"** with GitHub Copilot.  

This claim made no sense. The only time I had ever used Copilot was **briefly under the GitHub Student Plan in VS Code**, and after that, I never used it again. When I pointed this out, their response was **dismissive and inflexible**. Instead of investigating further, they kept repeating **threats of account termination** for violating their Terms of Service (TOS).  

In the end, they **abruptly closed my support ticket** without providing any detailed records or evidence of my supposed violation.  

### 🔍 The Realization  

This incident made me realize something important:  
> **GitHub.com is not truly a trustworthy platform for hosting my code.**  

If a platform can **restrict access, enforce opaque policies, and refuse to offer transparency**, then it's not a place where I want to store my work.  

Thus, I decided to migrate my repositories to my **own self-hosted Gitea server**—where I have full control over my code, my tools, and my future.  

---

## 🔧 Usage  

### 1. Configure `main.py`  

Edit `main.py` and update the following settings:  

```python
# Gitea Configuration (Token authentication only)
GITEA_URL = 'https://gitea.example.com'  # Your Gitea server URL
GITEA_USERNAME = 'fakeUser'  # Gitea username
GITEA_PASSWORD = 'f4bb667932306c04c7b1eec7466be4a053f5a03e'  # Gitea access token (see below)

# GitHub Configuration (Token authentication only)
GITHUB_USERNAME = 'fakeGitHubUser'  # GitHub username
GITHUB_TOKEN = 'ghp_abcdefghijklmnopqrstuvwxyz1234567890FAKE'  # GitHub access token
```

### 2. Gitea Access Token  

- If **2FA (Two-Factor Authentication)** or **WebAuthn** is enabled on your Gitea account, `GITEA_PASSWORD` should be set to your **Gitea Token**.  
- **Do not change the variable name**, simply replace `f4bb667932306c04c7b1eec7466be4a053f5a03e` with your actual Gitea token.  

---

## 🌍 Network Settings  

### 📌 If you are in China or have a slow network  

Since GitHub API access may be restricted, ensure that your **Gitea server can connect to GitHub without issues**. We recommend:  

- **Enabling a proxy** (such as a TUN proxy) for smooth API communication.  
- **Using a GitHub API accelerator** (such as `ghproxy.com`) to speed up requests.  

---

## ⚠️ Disclaimer  

This script is intended **only for personal or organizational migration of repositories from GitHub to Gitea**. Please comply with GitHub and Gitea terms of use.  

---

### 🌟 Why Self-Hosting Matters  

This project is not just about **migrating repositories**—it’s about **digital independence**. By self-hosting on Gitea, you **own your data, control your tools, and avoid arbitrary restrictions** imposed by centralized platforms.  

If you're considering moving away from GitHub, this script is here to help. 🚀  
