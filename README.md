---

<h1 align="center">cspr fans bot</h1>

<p align="center">Automate tasks in CSPR Fans to boost your efficiency and maximize your rewards!</p>

---

## 🚀 **About the Bot**

The **cspr fans bot** is designed to automate various tasks in CSPR Fans, including:

- **Auto Solve Task 📝**: Automatically solve your tasks.
- **Auto Spin Daily 🎰**: Automatically perform your daily spin for rewards.
- **Proxy Support 🔌**: Manage multiple accounts securely using proxies.
- **Delay & Account Switching ⏱️**: Set custom delays for looping and switching between accounts.

With this bot, you can save time and focus on what really matters while the bot handles repetitive tasks automatically.

---

## 🌟 **Version v1.0.0**

### **Updates**

1. Enhanced automation for task solving and daily spins.
2. Improved proxy handling and dynamic account switching.

### **Upcoming Updates**

- Additional customization options for tasks.
- Extended logging and error reporting features.

Stay tuned for more updates!

---

### **Features in This Version**:

- **Auto Task**: Automatically solve tasks by leveraging the API.
- **Auto Spin**: Automatically perform your daily spin.
- **Proxy Support**: Use proxies to manage multiple accounts securely.
- **Delay Loop & Account Switching**: Customize the delay between each automation loop and account switching.

---

## 📥 **How to Register**

Start using **cspr fans bot** by registering through the following link:

<div align="center">
  <a href="https://t.me/csprfans_bot?start=535079996" target="_blank">
    <img src="https://img.shields.io/static/v1?message=cspr%20fans%20bot&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---

## ⚙️ **Configuration in `config.json`**

Below is the configuration file structure for **cspr fans bot**:

| **Function**           | **Description**                                                             | **Default** |
| ---------------------- | --------------------------------------------------------------------------- | ----------- |
| `spin`                 | **Auto Spin Daily 🎰** - Automatically perform your daily spin for rewards. | `true`      |
| `task`                 | **Auto Solve Task 📝** - Automatically solve your tasks.                    | `true`      |
| `proxy`                | Enable/Disable proxy usage.                                                 | `false`      |
| `delay_loop`           | Delay before the next loop (in milliseconds).                               | `3000`      |
| `delay_account_switch` | Delay between account switches (in seconds).                                | `10`        |

---

## 📖 **Installation Steps**

1. **Clone the Repository**  
   Copy the project to your local machine:

   ```bash
   git clone https://github.com/livexords-nw/cspr-fans-bot.git
   ```

2. **Navigate to the Project Folder**  
   Move to the project directory:

   ```bash
   cd cspr-fans-bot
   ```

3. **Install Dependencies**  
   Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Query**  
   To configure your API:

   - Locate the API on your platform.
   - Open the request headers and find the **Authorization** header.
   - Copy the entire value starting from **Bearer** to the end.
   - Paste that value into a file named `query.txt`.

5. **Set Up Proxy (Optional)**  
   To use a proxy, create a file named `proxy.txt` and add your proxies in the following format:

   ```
   http://username:password@ip:port
   ```

   - Only HTTP and HTTPS proxies are supported.

6. **Run the Bot**  
   Execute the bot using the following command:

   ```bash
   python main.py
   ```

---

### 🔹 Want Free Proxies?

You can obtain free proxies from [Webshare.io](https://www.webshare.io/).

---

## 🛠️ **Contributing**

This project is developed by **Livexords**. If you have suggestions, questions, or would like to contribute, feel free to contact us:

<div align="center">
  <a href="https://t.me/livexordsscript" target="_blank">
    <img src="https://img.shields.io/static/v1?message=Livexords&logo=telegram&label=&color=2CA5E0&logoColor=white&labelColor=&style=for-the-badge" height="25" alt="telegram logo" />
  </a>
</div>

---
