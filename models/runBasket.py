import requests
import streamlit as st


### Note used currently
basket = []

#Add to basket –––––
def AddToBasket(currency, item):
    global basket

    if basket and any(existing_currency != currency for existing_currency, _ in basket):
        raise ValueError("Different currencies in the basket are not allowed.")

    basket.append((currency, item))
    return basket

#Remove from basket –––––
def RemoveFromBasket(item):
    global basket

    basket.remove(item)
    return basket
    
#Get basket –––––
def getBasket():
    global basket

    basketDetails = {
        "basket": basket,
        "total_items": len(basket),
        "total_cost": sum([item[1] for item in basket])
    }
    return basketDetails


def GenerateBasketTable():
    global basket
    basketTable = st.table(basket)
    return basketTable
