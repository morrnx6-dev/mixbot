import streamlit as st
import time
import random
import re
from cocktails import get_matching_cocktails, get_matching_cocktail_recipe

# To Run:
# source myenv/bin/activate
# streamlit run mixbot_app.py

# --- Constants ---
ALL_SPIRITS = ["Tequila", "Vodka", "Peach Schnapps", "White Rum", "Whiskey", "Dark Rum", "Gin", "Amaretto", "Aperol", "Prosecco"]
ALL_LIQUEUR = ["Triple Sec", "Grenadine", "Sugar Syrup", "Almond Syrup", "Elderflower Cordial", "Passion Fruit Liqueur", "Coffee Liqueur", "Orange Curaçao", "Blue Curaçao"]
ALL_INGREDIENTS = ["Ice", "Orange Juice", "Cranberry Juice", "Pineapple Juice", "Apple Juice", "Coconut Cream", "Espresso", "Sparkling Water", "Cola", "Bitters", "Lemon", "Lime", "Cherries", "Oranges", "Strawberries", "Watermelon", "Passion Fruit", "Mint", "Salt", "Egg White"]
ALL_MOODS = ["Happy", "Outgoing", "Energetic", "Nostalgic", "Buzzed", "Thirsty", "Lively", "Adventurous", "Excited", "Mysterious", "Goofy", "Tipsy"]
ALL_TASTES = ["Sour", "Citrusy", "Boozy", "Salty", "Sweet", "Fruity", "Bitter", "Yummy", "Classic"]
ALL_TYPES = ["Shaken", "Short", "Stirred", "Long"]

st.set_page_config(page_title="MixBot - AI Cocktail Recommendation", page_icon="🍸")

# --- Session State Initialization ---
for key, default in {
    "setup_complete": False,
    "orders": [],
    "user_names": [],
    "user_selected_spirits": [],
    "user_selected_liqueur": [],
    "user_selected_ingredients": [],
    "matched_cocktails": [],
    "current_match": None,
    "mix_again_triggered": False,
    "cannot_mix_again": False,
    "ask_mixbot_pressed": False,
    "order_confirmed": False,
    "new_name_input": "",
    "cannot_mix_again": False,
    "ask_mixbot_pressed": False,
    "order_confirmed": False,
    "new_name_input": "",
    "order_button_pressed": False,
    "non_alcoholic_only": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Setup Screen ---
if not st.session_state["setup_complete"]:
    st.title("🍹 Welcome to MixBot")
    with st.expander("📖 Instructions & How To's"):
        st.markdown("""
        👋 **Hello!**
       
        Your personal virtual bartender is here to help you discover your perfect cocktail! 🍸
       
        **How it works:**
        1. Enter the names of you and your guests who want a drink 📝
        2. Setup your bar by telling MixBot what alcohol & ingredients you have 🧪
        3. Tell MixBot how you're feeling and what flavour profile you prefer 🤪
        4. MixBot will recommend a cocktail that matches your provided items, mood and preferences 🧠
        5. Not happy with the recommendation? Ask MixBot to **Mix Again** to try something new! 🔍
                   
        🥤 **Teetotal? Designated Driver?** Just toggle the **Non-Alcoholic** checkbox in the mixing menu and MixBot will suggest a refreshing mocktail so you can still be part of the fun!
                   
        ✅ When you're happy with your choice, finalize your order and it'll be saved in your **Order History**
                   
        Cheers and happy mixing! 🍹
        """)
    st.header("🔧 Setup your Bar")
    st.markdown("Before we start mixing, tell MixBot who wants to be involved and what your items party has to hand!")

    def handle_add_person():
        name = st.session_state["new_name_input"].strip()
        if name and name.lower() not in {n.lower() for n in st.session_state["user_names"]}:
            st.session_state["user_names"].append(name)
        st.session_state["new_name_input"] = ""

    st.text_input("Enter a name and click 'Add':", key="new_name_input", placeholder="e.g., Alex")
    st.button("Add Person", on_click=handle_add_person)

    if st.session_state["user_names"]:
        st.markdown("**Guests added:**")
        st.write(", ".join(st.session_state["user_names"]))

    st.session_state["user_selected_spirits"] = st.multiselect("Tell me what **spirits** you have:", ALL_SPIRITS)
    st.session_state["user_selected_liqueur"] = st.multiselect("Let me know if you have any other **liqueur or syrups**:", ALL_LIQUEUR)
    st.caption("Be as creative as you want to be! Lemonade can be used as a substitute to sparkling water, whilst coconut milk is an equal alternative for coconut cream.")
    st.session_state["user_selected_ingredients"] = st.multiselect("Finally, select your **ingredients**:", ALL_INGREDIENTS)
    st.caption("The fruits listed can be used for juice and/or garnish when making the cocktails Mixbot recommends!")

    if st.button("Let's start Mixing! 🤪"):
        if not st.session_state["user_names"]:
            st.warning("Please add at least one person.")
        elif not st.session_state["user_selected_ingredients"]:
            st.warning("Please select at least one ingredient.")
        else:
            st.session_state["setup_complete"] = True
            st.rerun()

# --- Main Mixing UI ---
else:
    st.title("Hello, I'm MixBot! 🤖")
    st.header("Your Virtual Cocktail Expert!")

    person = st.selectbox("Who is making this order?", st.session_state["user_names"])

    if person:
        # Non-Alcoholic Toggle
        st.session_state["non_alcoholic_only"] = st.checkbox(
            "Only show Non-Alcoholic cocktails 🥤", 
            help="Still join in the fun even if you're teetotal, a designated driver or just wanting a break!",
            disabled=st.session_state["ask_mixbot_pressed"]
        )

        # Filter moods and tastes based on non-alcoholic selection
        available_moods = [m for m in ALL_MOODS if m != "Tipsy"] if st.session_state["non_alcoholic_only"] else ALL_MOODS
        available_tastes = [t for t in ALL_TASTES if t != "Boozy"] if st.session_state["non_alcoholic_only"] else ALL_TASTES

        # User selects their options - these are disabled when the Ask Mixbot button is pressed...
        user_selected_mood = st.multiselect(f"Hello {person}, how are you feeling today?", available_moods, max_selections=3, disabled=st.session_state["ask_mixbot_pressed"])
        user_selected_taste = st.multiselect(f"{person}, what flavours would you like your cocktail to have?", available_tastes, max_selections=3, disabled=st.session_state["ask_mixbot_pressed"])
        user_selected_type = st.selectbox(f"What is your preferred drink style {person}?", ALL_TYPES, disabled=st.session_state["ask_mixbot_pressed"])

        # --- Ask MixBot Button ---
        def press_ask_mixbot():
            st.session_state["ask_mixbot_pressed"] = True

        ask_mixbot_clicked = st.button(
            "🤖 Ask MixBot",
            disabled=st.session_state["ask_mixbot_pressed"],
            on_click=press_ask_mixbot
        )
        
        # Mix Again Triggered Variable
        mix_again_triggered = st.session_state["mix_again_triggered"]

        # -- Display Variable --
        cocktail_display = st.empty()

        # --- Cocktail Selection Logic ---
        if ask_mixbot_clicked or mix_again_triggered:
            if ask_mixbot_clicked:
                with st.spinner("Tasting pixels..."):
                    time.sleep(2)
            else:
                with st.spinner("Crafting an even better recommendation..."):
                    time.sleep(2)
            with st.spinner("Synthesizing spirits..."):
                time.sleep(2)
            with st.spinner("MixBot is mixing magic..."):
                time.sleep(2)

            if mix_again_triggered and st.session_state["current_match"]:
                print("Mix Again has been triggered")
                cocktail_display.empty() # Empty displayed cocktail
                matches = [c for c in st.session_state["matched_cocktails"] if c != st.session_state["current_match"]]
            else:
                category_filter = "Non-Alcoholic" if st.session_state["non_alcoholic_only"] else "Alcoholic"
                # Ensure 'Boozy' and 'Tipsy' are not passed if non-alcoholic is selected
                filtered_moods = [m for m in user_selected_mood if m != "Tipsy"] if st.session_state["non_alcoholic_only"] else user_selected_mood
                filtered_tastes = [t for t in user_selected_taste if t != "Boozy"] if st.session_state["non_alcoholic_only"] else user_selected_taste
                matches = get_matching_cocktails(
                    st.session_state["user_selected_spirits"],
                    st.session_state["user_selected_liqueur"],
                    st.session_state["user_selected_ingredients"],
                    filtered_moods,
                    filtered_tastes,
                    user_selected_type,
                    category_filter=category_filter,
                )

            if matches:
                st.session_state["matched_cocktails"] = matches
                st.session_state["current_match"] = random.choice(matches)
            else:
                st.error(f"😢 Sorry {person}, I couldn't find a cocktail for you. In a few seconds you'll be able to select different preferneces!")
                time.sleep(5)
                st.session_state["ask_mixbot_pressed"] = False
                st.rerun()
           
            st.session_state["mix_again_triggered"] = False

        # --- Display Current Cocktail in Container---
        if st.session_state["current_match"]:
            with cocktail_display.container():
                cocktail = st.session_state["current_match"]
                recipe = get_matching_cocktail_recipe(cocktail['name'])

                st.success(f"🍸 MixBot recommends: **{cocktail['name']}**")
                
                # Process description: lowercase the first letter, but capitalize after punctuation
                desc = recipe['description'].lower()
                desc = re.sub(r'([.!?]\s+)([a-z])', lambda m: m.group(1) + m.group(2).upper(), desc)
                
                st.markdown(f"**🗣️ MixBot says this is a {desc}!**")

                st.markdown("#### 🗒️ Ingredients")
                for ingredient in recipe['ingredients']:
                    st.markdown(f"- {ingredient}")

                st.markdown("### 🧪 How to make this cocktail")
                step_emojis = ["🔷", "🔶", "⭐️", "🌀", "🔥", "🎯", "✅"]
                steps = recipe["method"].split("\n\n")
                for i, step in enumerate(steps):
                    emoji = step_emojis[i % len(step_emojis)]
                    st.markdown(f"{emoji} **{step}**")

                st.caption("Press 'Mix Again' for another option or 'I'll take this one' to finalize!")
                
                # Initating columns for the two buttons
                col1, col2 = st.columns([0.3,1]) # Narrow gap betweem buttons

                # 'Mix Again' logic
                with col1:
                    if st.button("🔄 Mix Again!"):
                        if len(st.session_state["matched_cocktails"]) > 1:
                            print("There are additional cocktails that match criteria")
                            st.session_state["mix_again_triggered"] = True
                            st.rerun()
                        else:
                            st.session_state["cannot_mix_again"] = True
                
                # 'I'll Take This One' logic
                with col2:
                    if st.button("✅ I'll take this one!"):
                        st.session_state["order_button_pressed"] = True

        if st.session_state["cannot_mix_again"]:
            print("No more matches logic initiated")

            #Show warning that no more matches have been found
            cocktail_display.empty()
            st.warning("😢 I couldn't find any more matches! In a few seconds try changing your selections and ask Mixbot again!")
            time.sleep(5)

            # Re-initalize session states
            st.session_state["current_match"] = None
            st.session_state["matched_cocktails"] = []
            st.session_state["cannot_mix_again"] = False
            st.session_state["ask_mixbot_pressed"] = False
            st.rerun()
        
        # Placing the finalizing order spinner outside of the created columns
        if st.session_state["order_button_pressed"]:
            with st.spinner("MixBot is finalizing your order..."):
                    time.sleep(2)
            
            # Introducing logic toensure the randomly selected taste is in the cocktail tastes
            matching_tastes = list(set(user_selected_taste) & set(cocktail['tastes']))
            if matching_tastes:
                random_taste = random.choice(matching_tastes)
            else:
                random_taste = ""
            
            # Append order information
            st.session_state["orders"].append({
                "Person": person,
                "Taste": user_selected_taste,
                "Cocktail": cocktail['name'],
                "Mood": user_selected_mood,
                "Ingredients":recipe['ingredients'],
                "Method": recipe['method'],
                "Random Taste": random_taste
            })

            # Clear session states
            st.session_state["user_names"].remove(person)
            st.session_state["current_match"] = None
            st.session_state["ask_mixbot_pressed"] = False
            st.session_state["order_confirmed"] = True
                
        
        # Additional logic to host the success message of confirmed order outside of thecolumns
        # Introduced a countdown timer so that the page automatically refreshes for next guest each time
        if st.session_state["order_confirmed"]:
            st.warning(f"Saving {person}'s order...")
            st.caption("The cocktail information, recipe and method will become visible in the 'Orders' sidebar!")
            with st.spinner(f"The page will automatically refresh for the next guest to make their order!"):
                countdown_placeholder = st.empty()
                for i in range(5, 0, -1):
                    countdown_placeholder.info(f"⏳ Refreshing in {i} seconds...")
                    time.sleep(1)
                countdown_placeholder.empty()
            
            # Now show the success message for 2 seconds
            success_placeholder = st.empty()
            success_placeholder.success(f"Order saved for {person}. Enjoy your {cocktail['name']}! 🍹")
            time.sleep(2)
            success_placeholder.empty()  # Remove success message after 2 seconds
            
            # After countdown and success message, clear message and refresh
            cocktail_display.empty()
            st.session_state["order_confirmed"] = False
            st.session_state["user_selected_mood"] = []
            st.session_state["user_selected_taste"] = []
            st.session_state["user_selected_type"] = None
            st.session_state["ask_mixbot_pressed"] = False
            st.session_state["order_button_pressed"] = False
            st.rerun()

    # --- Sidebar: Order History ---
    st.sidebar.title("🧾 Order History")
    if st.session_state["orders"]:
        for order in st.session_state["orders"]:

            # Initiating Variables
            random_taste = order.get("Random Taste", "")

            # Initiating Markdown
            st.sidebar.markdown(f"""
                **{order['Person']}'s order:**
                - Cocktail: **{order['Cocktail']}**
                - Be sure to make it **{random_taste}**!
                """)
            
            # Initiating expander to store order instructions
            with st.sidebar.expander(f"**🎉 Open this to see the recipe for your {order['Cocktail']}, {order['Person']}!**"):
                st.markdown('#### 📋 Ingredients')
                for ingredient in order["Ingredients"]:
                    st.markdown(f"- {ingredient}")
                st.markdown('#### 🧪 Method')
                step_emojis = ["🔷", "🔶", "⭐️", "🌀", "🔥", "🎯", "✅"]
                steps = order["Method"].split("\n\n")
                for i, step in enumerate(steps):
                    emoji = step_emojis[i % len(step_emojis)]
                    st.markdown(f"{emoji} **{step}**")

            # Marjkdown toindicate the next order
            st.sidebar.markdown("---")
    else:
        st.sidebar.info("No drinks mixed yet. Ask MixBot!")

    # --- Restart ---
    st.sidebar.caption("Press 'Restart Mixbot' to start all over again!")
    if st.sidebar.button("🔁 Restart MixBot"):
        st.session_state.clear()
        st.rerun()


# --- Next Steps ---
        # Final touches on the logic and workings
        # Improve the UI - expand length of sidebar, differnet fonts, larger text to cover more page etc. 