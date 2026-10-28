# 🍹 MixBot - Your Virtual Bartender 🤖

MixBot is an cocktail recommendation app built with Streamlit. It helps you discover the perfect drink based on the ingredients you have on hand, your current mood, and your taste preferences. Whether you're looking for a boozy classic or a refreshing mocktail, MixBot has you covered!

## ✨ Features

- **🔧 Bar Setup**: Input your guest list and inventory your spirits, liqueurs, and ingredients.
- **🧠 Smart Matching**: Get cocktail recommendations based on:
  - **Available Ingredients**: Matches drinks you can actually make.
  - **Mood**: Select how you're feeling (e.g., Happy, Adventurous, Mysterious).
  - **Taste Profile**: Choose your preferred flavors (e.g., Sour, Citrusy, Sweet).
  - **Drink Style**: Filter by style (Shaken, Short, Stirred, Long).
- **🥤 Mocktail Mode**: A dedicated "Non-Alcoholic" toggle for teetotalers or designated drivers.
- **🔄 Mix Again**: Not feeling the first suggestion? Ask MixBot to find another matching drink.
- **🧾 Order History**: A sidebar that tracks everyone's orders, providing full recipes and step-by-step mixing instructions.
- **🎨 Custom Theme**: A curated aesthetic for a premium cocktail lounge experience.

## 🚀 Getting Started

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/morrnx6-dev/mixbot.git
   cd mixbot
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   streamlit run mixbot_app.py
   ```

## 🌐 Deployment

This app is designed to be deployed easily via **Streamlit Community Cloud**:

1. Push your code to GitHub.
2. Connect your GitHub account to [share.streamlit.io](https://share.streamlit.io).
3. Select the `mixbot` repository and the `main` branch.
4. Set the main file path to `mixbot_app.py` and deploy!

## 📂 Project Structure

```text
├── data/
│   ├── cocktails.json          # Cocktail metadata (moods, tastes, spirits)
│   └── cocktail_recipes.json    # Detailed recipes and methods
├── .streamlit/
│   └── config.toml             # Custom UI theme configurations
├── cocktails.py                # Matching logic and data loading utilities
├── mixbot_app.py               # Main Streamlit application entry point
└── requirements.txt            # Project dependencies
```

## 🛠️ Tech Stack

- **Language**: Python 3.12+
- **Frontend/Backend**: [Streamlit](https://streamlit.io/)
- **Data Format**: JSON
