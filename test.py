from nicegui import ui
import asyncio
import random
import json

from custom_elem.my_row import MyRow
from custom_elem.my_row_softload import MyRowSoftload

def supply_row(texts, bools):
    with ui.row().classes("w-full no-wrap items-center justify-center gap-0 [&_*]:items-center [&_*]:gap-0 [&_*]:flex-grow [&_*]:basis-0"):
        for i, (text, bool) in enumerate(zip(texts, bools)):
            with ui.column():
                ui.label(text).classes(f"text-xs text-black font-bold")
                if bool:
                    ui.icon("radio_button_checked").classes(f"text-red text-sm")
                else:
                    ui.icon("radio_button_unchecked").classes(f"text-red text-sm")

TEST_SIZE = 500

def rand_bools():
    # simulates disk access required to read a JSON file
    bools = [random.choice([True, False]) for _ in range(7)]
    
    # Write to a JSON file
    with open('bools.json', 'w') as f:
        json.dump(bools, f)

    del bools
    
    # Read from the JSON file
    with open('bools.json', 'r') as f:
        bools = json.load(f)
    
    return bools

@ui.page("/native/beforeconn/basic", response_timeout=60)
async def native_beforeconn_basic():
    ui.label("Here is my speedtest calendar!")
    text_calendar = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for i in range(TEST_SIZE):
        supply_row(text_calendar, rand_bools())
    # slow page load
    # 994217 bytes long page

@ui.page("/native/beforeconn/sleep", response_timeout=60)
async def native_beforeconn_sleep():
    ui.label("Here is my speedtest calendar!")
    spinner = ui.spinner()
    await asyncio.sleep(0.1)
    text_calendar = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for i in range(TEST_SIZE):
        supply_row(text_calendar, rand_bools())
    spinner.delete()
    # also slow page load, since the page is still served with the calendar
    # even worse, extra 0.1s delay

@ui.page("/native/beforeconn/js", response_timeout=60)
async def native_beforeconn_js():
    ui.label("Here is my speedtest calendar!")
    spinner = ui.spinner()
    await ui.run_javascript("1+1", timeout=10)
    text_calendar = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for i in range(TEST_SIZE):
        supply_row(text_calendar, rand_bools())
    spinner.delete()
    # literally doesn't work, 
    # since await ui.run_javascript holds indefinitely before client is connected
    # and the client will never connect until the page is ready, chicken-egg problem

@ui.page("/native/after_conn/basic", response_timeout=60)
async def native_after_conn_basic():
    ui.label("Here is my speedtest calendar!")
    spinner = ui.spinner()
    await ui.context.client.connected() # only after this can we await JS
    text_calendar = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for i in range(TEST_SIZE):
        supply_row(text_calendar, rand_bools())
    spinner.delete()
    # sends a 1968832 byte long websocket message
    # spinner get's stuck

@ui.page("/native/after_conn/js", response_timeout=60)
async def native_after_conn_js():
    ui.label("Here is my speedtest calendar!")
    spinner = ui.spinner()
    await ui.context.client.connected() # it would be the same if you have a button to show the calendar
    text_calendar = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for i in range(TEST_SIZE):
        supply_row(text_calendar, rand_bools())
        if i % 20 == 0:
            await ui.run_javascript("1+1", timeout=30) # force-push the calendar to the client, client must respond before next push
    spinner.delete()
    # sends ~40000 byte long websocket messages each
    # spinner stuttering less
    # generally takes longer because of latency for waiting the client to respond

@ui.page("/native/after_conn/sleep", response_timeout=60)
async def native_after_conn_sleep():
    ui.label("Here is my speedtest calendar!")
    spinner = ui.spinner()
    await ui.context.client.connected() # it would be the same if you have a button to show the calendar
    text_calendar = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for i in range(TEST_SIZE):
        supply_row(text_calendar, rand_bools())
        if i % 20 == 0:
            await asyncio.sleep(0.1) # force-push the calendar to the client, next push occurs regardless of client response
    spinner.delete()
    # sends ~40000 byte long websocket messages
    # spinner get's stuck by a lot, 
    # since 0.1s pacing doesn't consider browser rendering

@ui.page("/simple_custom/beforeconn/basic", response_timeout=60)
async def simple_custom_beforeconn_basic():
    ui.label("Here is my speedtest calendar!")
    text_calendar = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for i in range(TEST_SIZE):
        MyRow(texts=text_calendar, bools=rand_bools())
    # 134134 bytes long page
    # 4034 DOM elements

@ui.page("/adv_custom/beforeconn/basic", response_timeout=60)
async def simple_custom_beforeconn_basic():
    ui.label("Here is my speedtest calendar!")
    text_calendar = ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]
    for i in range(TEST_SIZE):
        MyRowSoftload(texts=text_calendar, bools=rand_bools())
    # 152185 bytes long page
    # 790 DOM elements

ui.run()