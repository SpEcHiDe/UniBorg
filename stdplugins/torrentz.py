import aiohttp
import asyncio
import cfscrape  # https://github.com/Anorov/cloudflare-scrape
import requests
from datetime import datetime
from bs4 import BeautifulSoup


@borg.on(slitu.admin_cmd(  # pylint:disable=E0602
    pattern="torrentz (torrentz2\.eu|idop\.se) (.*)"
))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_type = event.pattern_match.group(1)
    input_str = event.pattern_match.group(2)
    search_results = []
    if input_type == "torrentz2.eu":
        search_results = search_torrentz_eu(input_str)
    elif input_type == "idop.se":
        search_results = search_idop_se(input_str)
    # logger.info(search_results)  # pylint:disable=E0602
    output_str = ""
    i = 0
    for result in search_results:
        if i > 10:
            break
        message_text = "👉 <a href=https://t.me/TorrentSearchRoBot?start=" + result["hash"] +  ">" + result["title"] + ": " + "</a>" + " \r\n"
        message_text += " FILE SIZE: " + result["size"] + "\r\n"
        # message_text += " Uploaded " + result["date"] + "\r\n"
        message_text += " SEEDS: " + \
            result["seeds"] + " PEERS: " + result["peers"] + " \r\n"
        message_text += "===\r\n"
        output_str += message_text
        i += 1
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit(
        f"Scrapped {input_type} for {input_str} in {ms} seconds. Obtained Results: \n {output_str}",
        link_preview=False,
        parse_mode="html"
    )


def search_idop_se(search_query):
    r = []
    url = "https://idope.se/search/{}/".format(search_query)
    raw_json = requests.get(url).json()
    results = raw_json["result"]["items"]
    for item in results:
        """ The content scrapped on 24.09.2018 22:56:45
        """
        title = item["name"]
        hash = item["info_hash"]
        age = item["create_time"]
        size = item["length"]
        seeds = str(item["seeds"])
        r.append({
            "title": title,
            "hash": hash,
            "age": age,
            "size": slitu.humanbytes(size),
            "seeds": seeds,
            "peers": "NA"
        })
    return r


def search_torrentz_eu(search_query):
    r = []
    url = "https://torrentz2.eu/searchA?safe=1&f=" + search_query + ""
    scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
    raw_html = scraper.get(url).content
    # print(raw_html)
    soup = BeautifulSoup(raw_html, "html.parser")
    results = soup.find_all("div", {"class": "results"})
    # print(results)
    if len(results) > 0:
        results = results[0]
        for item in results.find_all("dl"):
            # print(item)
            """The content scrapped on 23.06.2018 15:40:35
            """
            dt = item.find_all("dt")[0]
            dd = item.find_all("dd")[0]
            #
            try:
                link_and_text = dt.find_all("a")[0]
                link = link_and_text.get("href")[1:]
                title = link_and_text.get_text()
                span_elements = dd.find_all("span")
                date = span_elements[1].get_text()
                size = span_elements[2].get_text()
                seeds = span_elements[3].get_text()
                peers = span_elements[4].get_text()
                #
                r.append({
                    "title": title,
                    "hash": link,
                    "date": date,
                    "size": size,
                    "seeds": seeds,
                    "peers": peers
                })
            except:
                pass
    return r


@borg.on(slitu.admin_cmd(pattern="piracy (TR|TMV|TB|TGY) (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    s_m_s = await slitu.edit_or_reply(event, "...")
    type_of_search = event.pattern_match.group(1)
    # no copyright infringement is intended by the use of this plugin
    # all below informations are available publicly available on the Internet
    # if you need to take-down any links, please contact the HOSTers Sites, yourselves
    # this plug-in / IDs does not "host" / "make available" any links
    # in any way / shape / or form. This plug-in does not provide a Directory Index
    # this plug-in uses Google Custom Search to search the informations
    # available on the Public Internet.
    # yet Another Legal Disclaimer
    all_srch_cx_dict = {
        "TR": "552cc5db2fc56e8d5",
        "TMV": "7e8cb098b23d01f34",
        "TB": "d9baba52ac11f8492",
        "TGY": "e0918a34523787dc4"
    }
    # the above CX ids are found publicly available on the Internet
    # https://t.me/ThankTelegram/759091
    input_str = event.pattern_match.group(2)
    input_url = "https://bots.shrimadhavuk.me/search/?cx={}&q={}".format(
        all_srch_cx_dict.get(type_of_search),
        input_str
    )
    headers = {"USER-AGENT": "UniBorg"}
    async with aiohttp.ClientSession() as requests:
        reponse = await requests.get(input_url, headers=headers)
        response = await reponse.json()
    output_str = " "
    for result in response["results"]:
        text = result.get("title")
        url = result.get("url")
        description = result.get("description")
        image = result.get("image")
        output_str += " 👉🏻  [{}]({}) \n\n".format(text, url)
    end = datetime.now()
    ms = (end - start).seconds
    await s_m_s.edit("searched {} for {} in {} seconds. \n{}".format(type_of_search, input_str, ms, output_str), link_preview=False)
    await asyncio.sleep(5)
    await s_m_s.edit("**{}**: {}\n{}".format(type_of_search, input_str, output_str), link_preview=False)
