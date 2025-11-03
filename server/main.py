from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import time
from browser_use import Agent, ChatGoogle
from typing import Any, Dict, List, Optional
from utils import (
    store_long_term_memory,
    get_long_term_memory,
    get_all_long_term_memories,
    store_conversation_history,
    get_conversation_history,
    get_cached_response,
    cache_response
)
import requests
import json

load_dotenv()
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow requests from Next.js client
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Request models
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {"message": "Hello fromddddwdwdw Redis hackathon server! peace sign"}

@app.get("/health")
def health_check():
    return {"status": "healthy ppde"}

def _format_agent_step(action: Any, index: int) -> Dict[str, Any]:
    description_candidates: List[str] = []

    if getattr(action, "extracted_content", None):
        description_candidates.append(action.extracted_content)
    if getattr(action, "long_term_memory", None):
        description_candidates.append(action.long_term_memory)
    if getattr(action, "error", None):
        description_candidates.append(f"Error: {action.error}")

    metadata = getattr(action, "metadata", None)
    if not description_candidates and metadata:
        description_candidates.append(str(metadata))

    description = description_candidates[0] if description_candidates else "No description provided."

    return {
        "step": index,
        "description": description,
        "is_done": getattr(action, "is_done", False),
        "success": getattr(action, "success", None),
    }


@app.get("/test/utils")
async def test_utils():
    print('new one!!')
    # Create real test calls 
    # store_long_term_memory('hello', 'test', 'test')
    # get_long_term_memory('hello', 'test')
    # get_all_long_term_memories('hello')
    # store_conversation_history('hello', 'test', 'test')
    # get_conversation_history('hello')
    # post to /agent/chat
    # response = await requests.get('http://localhost:4000/agent/execute')
    dummy_json = """
    {"history":[{"model_output":{"evaluation_previous_goal":"Agent initialized on a blank page. Verdict: Success","memory":"Starting the search for the 'Show HN' page.","next_goal":"Search for 'Show HN' using DuckDuckGo to find the correct URL.","action":[{"search":{"query":"Show HN","engine":"duckduckgo"}}],"thinking":"The user wants me to find the number 1 post on \"Show HN\". \"Show HN\" is a section of Hacker News. Since the current browser state is a blank page, I need to navigate to the correct website. I will start by searching for \"Show HN\" to find the Hacker News page for that section."},"result":[{"is_done":false,"long_term_memory":"Searched Duckduckgo for 'Show HN'","extracted_content":"Searched Duckduckgo for 'Show HN'","include_extracted_content_only_once":false,"include_in_memory":false}],"state":{"tabs":[{"url":"about:blank","title":"","target_id":"1EB0","parent_target_id":null}],"screenshot_path":null,"interacted_element":[null],"url":"about:blank","title":"Empty Tab"},"metadata":{"step_start_time":1762129857.9556754,"step_end_time":1762129862.3834171,"step_number":1},"state_message":"<agent_history>\nAgent initialized\n</agent_history>\n\n<agent_state>\n<user_request>\nFind the number 1 post on Show HN\n</user_request>\n<file_system>\n\n</file_system>\n<todo_contents>\n[empty todo.md, fill it when applicable]\n</todo_contents>\n<step_info>Step1 maximum:100\nToday:2025-11-03</step_info>\n</agent_state>\n<browser_state>\n<page_stats>Page appears empty (SPA not loaded?) - 0 links, 0 interactive, 0 iframes, 0 scroll containers, 0 total elements</page_stats>\n\nAvailable tabs:\nTab 1EB0: about:blank - \n\n<page_info>0.0 pages above, 0.0 pages below, 1.0 total pages</page_info>\n\nInteractive elements:\n[Start of page]\nEmpty DOM tree (you might have to wait for the page to load)\n[End of page]\n</browser_state>\n"},{"model_output":{"evaluation_previous_goal":"The search for 'Show HN' was initiated but the results are blocked by a CAPTCHA. Verdict: Failure","memory":"Blocked by CAPTCHA on DuckDuckGo search results page. Attempting direct navigation to Hacker News 'Show HN' section.","next_goal":"Navigate directly to the 'Show HN' page on Hacker News using the URL https://news.ycombinator.com/show.","action":[{"navigate":{"url":"https://news.ycombinator.com/show","new_tab":false}}],"thinking":"I attempted to search for 'Show HN' but was blocked by a CAPTCHA on DuckDuckGo. Since 'Show HN' is part of Hacker News, I will try to navigate directly to the likely URL, which is https://news.ycombinator.com/show, to bypass the CAPTCHA and find the number 1 post."},"result":[{"is_done":false,"long_term_memory":"Navigated to https://news.ycombinator.com/show","extracted_content":"🔗 Navigated to https://news.ycombinator.com/show","include_extracted_content_only_once":false,"include_in_memory":false}],"state":{"tabs":[{"url":"https://duckduckgo.com/?q=Show+HN","title":"Show HN at DuckDuckGo","target_id":"1EB0","parent_target_id":null}],"screenshot_path":"/tmp/browser_use_agent_06907f7b-d64e-7dc0-8000-9e853245b10b_1762129853/screenshots/step_2.png","interacted_element":[null],"url":"https://duckduckgo.com/?q=Show+HN","title":"Show HN at DuckDuckGo"},"metadata":{"step_start_time":1762129862.3838644,"step_end_time":1762129867.5907896,"step_number":2},"state_message":"<agent_history>\nAgent initialized\n<step>\nAgent initialized on a blank page. Verdict: Success\nStarting the search for the 'Show HN' page.\nSearch for 'Show HN' using DuckDuckGo to find the correct URL.\nResult\nSearched Duckduckgo for 'Show HN'\n</agent_history>\n\n<agent_state>\n<user_request>\nFind the number 1 post on Show HN\n</user_request>\n<file_system>\n\n</file_system>\n<todo_contents>\n[empty todo.md, fill it when applicable]\n</todo_contents>\n<step_info>Step2 maximum:100\nToday:2025-11-03</step_info>\n</agent_state>\n<browser_state>\n<page_stats>17 links, 7 interactive, 0 iframes, 1 scroll containers, 1 shadow(open), 0 shadow(closed), 207 total elements</page_stats>\nCurrent tab: 1EB0\nAvailable tabs:\nTab 1EB0: https://duckduckgo.com/?q=Show+HN - Show HN at DuckDuckGo\n\n<page_info>0.0 pages above, 0.2 pages below, 1.2 total pages</page_info>\n\nInteractive elements:\n[Start of page]\n|SCROLL|<html /> (0.0 pages above, 0.2 pages below)\n\tProtection. Privacy. Peace of mind.\n\tOpen menu\n\tAll\n\tImages\n\tVideos\n\tNews\n\tMaps\n\tShopping\n\tDuck.ai\n\tSearch Settings\n\tProtected\n\t<svg /> <!-- SVG content collapsed -->\n\tUnited Kingdom\n\t<svg /> <!-- SVG content collapsed -->\n\tSafe search: moderate\n\t<svg /> <!-- SVG content collapsed -->\n\tAny time\n\t<svg /> <!-- SVG content collapsed -->\n\t<svg /> <!-- SVG content collapsed -->\n\tSee What’s DuckDuckNew\n\tExplore DuckDuckGo’s latest product updates.\n\t[937]<a />\n\t\tLearn More\n\tLearn More\n\t[946]<a />\n\t\tCompare Privacy\n\t[949]<a />\n\t\tHelp Pages\n\t[952]<a />\n\t\tSearch Shortcuts\n\tGet More\n\t[959]<a />\n\t\tEmail Protection\n\t[962]<a />\n\t\tNewsletter\n\tUnfortunately, bots use DuckDuckGo too.\n\tPlease complete the following challenge to confirm this search was made by a human.\n\tSelect all squares containing a duck:\n\t[1036]<button />\n\t\tSubmit\n\tShare Feedback\n... 0.2 pages below ...\n</browser_state>\n"},{"model_output":{"evaluation_previous_goal":"Successfully navigated to the Hacker News 'Show HN' page. Verdict: Success","memory":"The number 1 post on Show HN is 'Show HN: Why write code if the LLM can just do the thing? (web app experiment)'.","next_goal":"Report the number 1 post on Show HN and complete the task.","action":[{"done":{"text":"The number 1 post on Show HN is: \"Show HN: Why write code if the LLM can just do the thing? (web app experiment)\"","success":true}}],"thinking":"I have successfully navigated to the Hacker News 'Show HN' page. I need to identify the title of the number 1 post. Based on the browser state, the first item is clearly marked as '1.' and its title is available immediately after.\n\nRank 1 post title: 'Show HN: Why write code if the LLM can just do the thing? (web app experiment)'.\n\nSince I have the information requested by the user, I will proceed to call the `done` action."},"result":[{"is_done":true,"success":true,"attachments":[],"long_term_memory":"Task completed: True - The number 1 post on Show HN is: \"Show HN: Why write code if the LLM can just do the thing? (web app - 13 more characters","extracted_content":"The number 1 post on Show HN is: \"Show HN: Why write code if the LLM can just do the thing? (web app experiment)\"","include_extracted_content_only_once":false,"include_in_memory":false}],"state":{"tabs":[{"url":"https://news.ycombinator.com/show","title":"Show | Hacker News","target_id":"1EB0","parent_target_id":null}],"screenshot_path":"/tmp/browser_use_agent_06907f7b-d64e-7dc0-8000-9e853245b10b_1762129853/screenshots/step_3.png","interacted_element":[null],"url":"https://news.ycombinator.com/show","title":"Show | Hacker News"},"metadata":{"step_start_time":1762129867.591782,"step_end_time":1762129870.827031,"step_number":3},"state_message":"<agent_history>\nAgent initialized\n<step>\nAgent initialized on a blank page. Verdict: Success\nStarting the search for the 'Show HN' page.\nSearch for 'Show HN' using DuckDuckGo to find the correct URL.\nResult\nSearched Duckduckgo for 'Show HN'\n<step>\nThe search for 'Show HN' was initiated but the results are blocked by a CAPTCHA. Verdict: Failure\nBlocked by CAPTCHA on DuckDuckGo search results page. Attempting direct navigation to Hacker News 'Show HN' section.\nNavigate directly to the 'Show HN' page on Hacker News using the URL https://news.ycombinator.com/show.\nResult\nNavigated to https://news.ycombinator.com/show\n</agent_history>\n\n<agent_state>\n<user_request>\nFind the number 1 post on Show HN\n</user_request>\n<file_system>\n\n</file_system>\n<todo_contents>\n[empty todo.md, fill it when applicable]\n</todo_contents>\n<step_info>Step3 maximum:100\nToday:2025-11-03</step_info>\n</agent_state>\n<browser_state>\n<page_stats>202 links, 350 interactive, 0 iframes, 0 scroll containers, 1 shadow(open), 0 shadow(closed), 2 images, 1052 total elements</page_stats>\nCurrent tab: 1EB0\nAvailable tabs:\nTab 1EB0: https://news.ycombinator.com/show - Show | Hacker News\n\n<page_info>0.0 pages above, 0.2 pages below, 1.2 total pages</page_info>\n\nInteractive elements:\n[Start of page]\n[1158]<a />\n[1163]<a />\n\tHacker News\n[1165]<a />\n\tnew\n[1168]<a />\n\tpast\n[1171]<a />\n\tcomments\n[1174]<a />\n\task\n[1177]<span />\n\t[1178]<a />\n\t\tshow\n[1181]<a />\n\tjobs\n[1184]<a />\n\tsubmit\n[1187]<span />\n\t[1188]<a />\n\t\tlogin\nPlease read the Show HN\n[1194]<a />\n\trules\nand\n[1198]<a />\n\ttips\nbefore posting. You can browse the newest Show HNs\n[1202]<a />\n\there\n[1209]<td />\n\t[1210]<span />\n\t\t1.\n[1212]<td />\n\t[1214]<a id=up_45783640 />\n[1132]<a />\n\tShow HN: Why write code if the LLM can just do the thing? (web app experiment)\n[1221]<a />\n\tgithub.com/samrolken\n[1229]<span id=score_45783640 />\n\t409 points\nby\n[1232]<a />\n\tsamrolken\n[1235]<span title=2025-11-01T17:45:18 1762019118 />\n\t[1236]<a />\n\t\t1 day ago\n[1241]<a />\n\t290 comments\n[1245]<td />\n\t[1246]<span />\n\t\t2.\n[1248]<td />\n\t[1250]<a id=up_45790443 />\n[1254]<a />\n\tShow HN: Anki-LLM – Bulk process and generate Anki flashcards with LLMs\n[1258]<a />\n\tgithub.com/raine\n[1266]<span id=score_45790443 />\n\t35 points\nby\n[1269]<a />\n\trane\n[1273]<a />\n\t10 hours ago\n[1278]<a />\n\t14 comments\n[1282]<td />\n\t[1283]<span />\n\t\t3.\n[1285]<td />\n\t[1287]<a id=up_45793684 />\n[1291]<a />\n\tShow HN: Give your coding agents the ability to message each other\n[1295]<a />\n\tgithub.com/dicklesworthstone\n[1303]<span id=score_45793684 />\n\t2 points\nby\n[1306]<a />\n\teigenvalue\n[1309]<span title=2025-11-02T21:39:52 1762119592 />\n\t[1310]<a />\n\t\t2 hours ago\n[1315]<a />\n\tdiscuss\n[1319]<td />\n\t[1320]<span />\n\t\t4.\n[1322]<td />\n\t[1324]<a id=up_45777810 />\n[1328]<a />\n\tShow HN: Strange Attractors\n[1332]<a />\n\tshashanktomar.com\n[1340]<span id=score_45777810 />\n\t767 points\nby\n[1343]<a />\n\tshashanktomar\n[1346]<span title=2025-10-31T23:23:59 1761953039 />\n\t[1347]<a />\n\t\t2 days ago\n[1352]<a />\n\t75 comments\n[1356]<td />\n\t[1357]<span />\n\t\t5.\n[1359]<td />\n\t[1361]<a id=up_45792040 />\n[1365]<a />\n\tShow HN: I built a smart blocker after destroying my dopamine baseline\n[1369]<a />\n\tchromewebstore.google.com\n[1377]<span id=score_45792040 />\n\t13 points\nby\n[1380]<a />\n\tRahul07oii\n[1383]<span title=2025-11-02T17:47:32 1762105652 />\n\t[1384]<a />\n\t\t6 hours ago\n[1389]<a />\n\t6 comments\n[1393]<td />\n\t[1394]<span />\n\t\t6.\n[1396]<td />\n\t[1398]<a id=up_45734865 />\n[1402]<a />\n\tShow HN: Pipelex – Declarative language for repeatable AI workflows\n[1406]<a />\n\tgithub.com/pipelex\n[1414]<span id=score_45734865 />\n\t116 points\nby\n[1417]<a />\n\tlchoquel\n[1420]<span title=2025-10-28T16:19:26 1761668366 />\n\t[1421]<a />\n\t\t2 days ago\n[1426]<a />\n\t26 comments\n[1430]<td />\n\t[1431]<span />\n\t\t7.\n[1433]<td />\n\t[1435]<a id=up_45771871 />\n[1439]<a />\n\tShow HN: A simple drag and drop tool to document and label fuse boxes\n[1443]<a />\n\tgithub.com/alexadam\n[1451]<span id=score_45771871 />\n\t25 points\nby\n[1454]<a />\n\teg312\n[1458]<a />\n\t23 hours ago\n[1463]<a />\n\t6 comments\n[1467]<td />\n\t[1468]<span />\n\t\t8.\n[1470]<td />\n\t[1472]<a id=up_45786533 />\n[1476]<a />\n\tShow HN: Duper – The Format That's Super\n[1480]<a />\n\tduper.dev.br\n[1488]<span id=score_45786533 />\n\t29 points\nby\n[1491]<a />\n\tepiceric\n[1494]<span title=2025-11-01T23:41:04 1762040464 />\n\t[1495]<a />\n\t\t1 day ago\n[1500]<a />\n\t14 comments\n[1504]<td />\n\t[1505]<span />\n\t\t9.\n[1507]<td />\n\t[1509]<a id=up_45790651 />\n[1513]<a />\n\tShow HN: Carrie, for what Calendly can't do\n[1517]<a />\n\tgetcarrie.com\n[1525]<span id=score_45790651 />\n\t6 points\nby\n[1528]<a />\n\teastraining\n[1531]<span title=2025-11-02T14:40:48 1762094448 />\n\t[1532]<a />\n\t\t9 hours ago\n[1537]<a />\n\tdiscuss\n[1541]<td />\n\t[1542]<span />\n\t\t10.\n[1544]<td />\n\t[1546]<a id=up_45786192 />\n[1550]<a />\n\tShow HN: KeyLeak Detector – Scan websites for exposed API keys and secrets\n[1554]<a />\n\tgithub.com/amal-david\n[1562]<span id=score_45786192 />\n\t24 points\nby\n[1565]<a />\n\tamaldavid\n[1568]<span title=2025-11-01T22:52:22 1762037542 />\n\t[1569]<a />\n\t\t1 day ago\n[1574]<a />\n\t7 comments\n[1578]<td />\n\t[1579]<span />\n\t\t11.\n[1581]<td />\n\t[1583]<a id=up_45790412 />\n[1587]<a />\n\tShow HN: Jv 0.1 – Zero-runtime Java sugar language for Java 25\n[1591]<a />\n\tgithub.com/project-jvlang\n[1599]<span id=score_45790412 />\n\t2 points\nby\n[1602]<a />\n\tasopitech\n[1606]<a />\n\t10 hours ago\n[1611]<a />\n\t1 comment\n[1615]<td />\n\t[1616]<span />\n\t\t12.\n[1618]<td />\n\t[1620]<a id=up_45790163 />\n[1624]<a />\n\tShow HN: I built a tool to version control datasets (like Git, but for data)\n[1628]<a />\n\tshodata.com\n[1636]<span id=score_45790163 />\n\t2 points\nby\n[1639]<a />\n\taliefe04\n[1643]<a />\n\t11 hours ago\n[1648]<a />\n\t2 comments\n[1652]<td />\n\t[1653]<span />\n\t\t13.\n[1655]<td />\n\t[1657]<a id=up_45790140 />\n[1661]<a />\n\tShow HN: CommoWatch – Alerts for Commodity Prices (Gold, Oil, Wheat, etc.)\n[1667]<span id=score_45790140 />\n\t2 points\nby\n[1670]<a />\n\tanthonytorre\n[1131]<a />\n\t11 hours ago\n[1678]<a />\n\t4 comments\n[1682]<td />\n\t[1683]<span />\n\t\t14.\n[1685]<td />\n\t[1687]<a id=up_45758421 />\n[1691]<a />\n\tShow HN: In a single HTML file, an app to encourage my children to invest\n[1695]<a />\n\troberdam.com\n[1703]<span id=score_45758421 />\n\t246 points\nby\n[1706]<a />\n\troberdam\n[1709]<span title=2025-10-30T10:39:21 1761820761 />\n\t[1710]<a />\n\t\t3 days ago\n[1715]<a />\n\t431 comments\n[1719]<td />\n\t[1720]<span />\n\t\t15.\n[1722]<td />\n\t[1724]<a id=up_45784331 />\n[1728]<a />\n\tShow HN: UnisonDB – Log-native KV database that replicates like a message bus\n[1732]<a />\n\tunisondb.io\n[1740]<span id=score_45784331 />\n\t16 points\nby\n[1743]<a />\n\tankuranand\n[1746]<span title=2025-11-01T19:01:12 1762023672 />\n\t[1747]<a />\n\t\t1 day ago\n[1752]<a />\n\tdiscuss\n[1756]<td />\n\t[1757]<span />\n\t\t16.\n[1759]<td />\n\t[1761]<a id=up_45767162 />\n[1765]<a />\n\tShow HN: Quibbler – A critic for your coding agent that learns what you want\n[1769]<a />\n\tgithub.com/fulcrumresearch\n[1777]<span id=score_45767162 />\n\t114 points\nby\n[1780]<a />\n\tetherio\n[1783]<span title=2025-10-31T00:43:57 1761871437 />\n\t[1784]<a />\n\t\t2 days ago\n[1789]<a />\n\t26 comments\n[1793]<td />\n\t[1794]<span />\n\t\t17.\n[1796]<td />\n\t[1798]<a id=up_45786094 />\n[1802]<a />\n\tShow HN: Find and download fonts from any website (weekend project)\n[1806]<a />\n\ttypecatch.com\n[1814]<span id=score_45786094 />\n\t16 points\nby\n[1817]<a />\n\tzdenham\n[1820]<span title=2025-11-01T22:40:44 1762036844 />\n\t[1821]<a />\n\t\t1 day ago\n[1826]<a />\n\t3 comments\n[1830]<td />\n\t[1831]<span />\n\t\t18.\n[1833]<td />\n\t[1835]<a id=up_45745566 />\n[1839]<a />\n\tShow HN: Learn German with Games\n[1843]<a />\n\tlearngermanwithgames.com\n[1851]<span id=score_45745566 />\n\t123 points\nby\n[1854]<a />\n\tpredictand\n[1857]<span title=2025-10-29T11:50:58 1761738658 />\n\t[1858]<a />\n\t\t4 days ago\n[1863]<a />\n\t106 comments\n[1867]<td />\n\t[1868]<span />\n\t\t19.\n[1870]<td />\n\t[1872]<a id=up_45694032 />\n[1876]<a />\n\tShow HN: Run a GitHub Actions step in a gVisor sandbox\n[1880]<a />\n\tgithub.com/geomys\n[1888]<span id=score_45694032 />\n\t85 points\nby\n[1891]<a />\n\tFiloSottile\n[1894]<span title=2025-10-24T12:42:31 1761309751 />\n\t[1895]<a />\n\t\t3 days ago\n[1900]<a />\n\t3 comments\n[1904]<td />\n\t[1905]<span />\n\t\t20.\n[1907]<td />\n\t[1909]<a id=up_45743232 />\n[1913]<a />\n\tShow HN: Front End Fuzzy and Substring and Prefix Search\n[1917]<a />\n\tgithub.com/m31coding\n[1925]<span id=score_45743232 />\n\t54 points\nby\n[1133]<a />\n\tkmschaal\n[1930]<span title=2025-10-29T06:12:46 1761718366 />\n\t[1931]<a />\n\t\t3 days ago\n[1936]<a />\n\t4 comments\n[1940]<td />\n\t[1941]<span />\n\t\t21.\n[1943]<td />\n\t[1945]<a id=up_45760321 />\n[1949]<a />\n\tShow HN: I made a heatmap diff viewer for code reviews\n[1953]<a />\n\t0github.com\n[1961]<span id=score_45760321 />\n\t263 points\nby\n[1964]<a />\n\tlawrencechen\n[1967]<span title=2025-10-30T14:21:58 1761834118 />\n\t[1968]<a />\n\t\t3 days ago\n[1973]<a />\n\t68 comments\n[1977]<td />\n\t[1978]<span />\n\t\t22.\n[1980]<td />\n\t[1982]<a id=up_45727819 />\n[1986]<a />\n\tShow HN: Settling the Score – A point-and-click adventure rhythm game\n[1990]<a />\n\teasel.games\n[1998]<span id=score_45727819 />\n\t20 points\nby\n[2001]<a />\n\tBSTRhino\n[2004]<span title=2025-10-27T23:59:44 1761609584 />\n\t[2005]<a />\n\t\t1 day ago\n[2010]<a />\n\t7 comments\n[2014]<td />\n\t[2015]<span />\n\t\t23.\n[2017]<td />\n\t[2019]<a id=up_45731366 />\n[2023]<a />\n\tShow HN: Bash Screensavers\n[2027]<a />\n\tgithub.com/attogram\n[2035]<span id=score_45731366 />\n\t246 points\nby\n[2038]<a />\n\tattogram\n[2041]<span title=2025-10-28T11:12:32 1761649952 />\n\t[2042]<a />\n\t\t5 days ago\n[2047]<a />\n\t77 comments\n[2051]<td />\n\t[2052]<span />\n\t\t24.\n[2054]<td />\n\t[2056]<a id=up_45734429 />\n[2060]<a />\n\tShow HN: Research Hacker News, ArXiv & Google with Hierarchical Bayesian Models\n[2064]<a />\n\tsturdystatistics.com\n[2072]<span id=score_45734429 />\n\t83 points\nby\n[2075]<a />\n\tkianN\n[2078]<span title=2025-10-28T15:49:51 1761666591 />\n\t[2079]<a />\n\t\t4 days ago\n[2084]<a />\n\t23 comments\n[2088]<td />\n\t[2089]<span />\n\t\t25.\n[2091]<td />\n\t[2093]<a id=up_45784368 />\n[2097]<a />\n\tShow HN: Micro-RLE ≤264-byte compression for UART/MCU logs, zero RAM growth\n[2101]<a />\n\tgithub.com/corelathe\n[2109]<span id=score_45784368 />\n\t7 points\nby\n[2112]<a />\n\tCoreLathe\n[2115]<span title=2025-11-01T19:04:55 1762023895 />\n\t[2116]<a />\n\t\t1 day ago\n[2121]<a />\n\t2 comments\n[2125]<td />\n\t[2126]<span />\n\t\t26.\n[2128]<td />\n\t[2130]<a id=up_45721352 />\n[2134]<a />\n\tShow HN: ISS in Real Time – 25 Years Aboard the International Space Station\n[2138]<a />\n\tissinrealtime.org\n[2146]<span id=score_45721352 />\n\t162 points\nby\n[2149]<a />\n\tbfeist\n[2152]<span title=2025-10-27T14:25:00 1761575100 />\n\t[2153]<a />\n\t\t5 days ago\n[2158]<a />\n\t24 comments\n[2162]<td />\n\t[2163]<span />\n\t\t27.\n[2165]<td />\n\t[2167]<a id=up_45783691 />\n[2171]<a />\n\tShow HN: Proxmox-GitOps: Container Automation Framework\n[2175]<a />\n\tgithub.com/stevius10\n[2183]<span id=score_45783691 />\n\t7 points\nby\n[2186]<a />\n\tgitopspm\n[2189]<span title=2025-11-01T17:49:45 1762019385 />\n\t[2190]<a />\n\t\t1 day ago\n[2195]<a />\n\t1 comment\n[2199]<td />\n\t[2200]<span />\n\t\t28.\n[2202]<td />\n\t[2204]<a id=up_45765328 />\n[2208]<a />\n\tShow HN: ekoAcademic – Convert ArXiv papers to interactive podcasts\n[2212]<a />\n\twadamczyk.io\n[2220]<span id=score_45765328 />\n\t52 points\nby\n[2223]<a />\n\twadamczyk\n[2226]<span title=2025-10-30T21:03:46 1761858226 />\n\t[2227]<a />\n\t\t3 days ago\n[2232]<a />\n\t14 comments\n[2236]<td />\n\t[2237]<span />\n\t\t29.\n[2239]<td />\n\t[2241]<a id=up_45715055 />\n[2245]<a />\n\tShow HN: MyraOS – My 32-bit operating system in C and ASM (Hack Club project)\n[2249]<a />\n\tgithub.com/dvir-biton\n[2257]<span id=score_45715055 />\n\t247 points\nby\n[2260]<a />\n\tdvirbt\n[2263]<span title=2025-10-26T20:43:40 1761511420 />\n\t[2264]<a />\n\t\t7 days ago\n[2269]<a />\n\t55 comments\n[2273]<td />\n\t[2274]<span />\n\t\t30.\n[2276]<td />\n\t[2278]<a id=up_45722826 />\n[2282]<a />\n\tShow HN: JSON Query\n[2286]<a />\n\tjsonquerylang.org\n[2294]<span id=score_45722826 />\n\t153 points\nby\n[2297]<a />\n\twofo\n[2300]<span title=2025-10-27T16:22:52 1761582172 />\n\t[2301]<a />\n\t\t6 days ago\n[2306]<a />\n\t70 comments\n[2313]<a />\n\tMore\n[2325]<a />\n\tConsider applying for YC's Winter 2026 batch! Applications are open till Nov 10\n[2331]<a />\n\tGuidelines\n[2334]<a />\n\tFAQ\n[2337]<a />\n\tLists\n[2340]<a />\n\tAPI\n[2343]<a />\n\tSecurity\n[2346]<a />\n\tLegal\n[2349]<a />\n\tApply to YC\n[2352]<a />\n\tContact\nSearch:\n|SHADOW(open)|[1135]<input type=text name=q autocomplete=off />\n... 0.2 pages below ...\n</browser_state>\n"}]}
    """
    
    # print('dummy_json: ', dummy_json)
    # turn response into a string
    # response_string = str(dummy_json)
    # cache_response('Find the number 1 post on Show HN', response_string)

    c = get_cached_response('Find the number 1 post on Show HN')
    print('cached_response: ', c)
    return {
        "message": "Utils test complete",
        "success": True,
    }


@app.post("/agent/chat")
async def chat_with_agent(request: ChatRequest):
    message = request.message
    print(f"Received message: {message}")

    # LangCache Semantic Caching
    cached_response = get_cached_response(message)

    print('cached response: ', cached_response)
    # Only treat as cache hit if response is not None and not empty
    if cached_response is not None and cached_response != "" and cached_response != "data=[]":
        print('cached_response: ', cached_response[:10])
        print(f"✓ Cache HIT for query: {message[:50]}...")
        return {
            "message": cached_response,
            "success": True,
        }
        
    else:
        print(f"✗ Cache MISS for query: {message[:50]}...")

        try:
            llm = ChatGoogle(model="gemini-flash-latest", api_key=os.getenv("GOOGLE_API_KEY"))
            agent = Agent(task=message, llm=llm)

            result = await agent.run()
            
            # Return the result as a message string
            result_message = str(result) if result else "Agent execution completed."
            
            print('result message: ', result_message)
            print('result message type: ', type(result_message))

            # Cache the response
            cache_response(message, result_message)
            
            return {
                "message": result_message,
                "success": True,
            }
            
        except Exception as e:
            print(f'Error executing agent: {e}')

            return {
                "message": f"Sorry, I encountered an error: {str(e)}",
                "success": False,
                "error": str(e),
            }

@app.get("/agent/execute")
async def execute_agent():
    print('agent executed')
    print('GOOGLE_API_KEY: ', os.getenv("GOOGLE_API_KEY"))

    llm = ChatGoogle(model="gemini-flash-latest", api_key=os.getenv("GOOGLE_API_KEY"))
    task = "Find the number 1 post on Show HN"
    agent = Agent(task=task, llm=llm)

    try:
        result = await agent.run()
        print('result: ', result)
    
        return {
            "summary": result,
            "steps": [],
            "success": True,
        }
    except Exception as e:
        print('error: ', e)
        return {
            "summary": "Error executing agent",
            "steps": [],
            "success": False,
            "error": str(e),
        }

def main():
    print("Hello from server!")

if __name__ == "__main__":
    main()