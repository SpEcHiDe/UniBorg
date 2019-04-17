import cfscrape  # https://github.com/Anorov/cloudflare-scrape
import os
import requests
import urllib.parse
from datetime import datetime
from bs4 import BeautifulSoup
from telethon import events
from uniborg.util import admin_cmd


@borg.on(admin_cmd(  # pylint:disable=E0602
    "torrentz (torrentz2\.eu|idop\.se) (.*)"
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
    logger.info(search_results)  # pylint:disable=E0602
    output_str = ""
    i = 0
    for result in search_results:
        if i > 5:
            break
        url = "`" + result["hash"] + "`"
        message_text = " 👉🏻 " + result["title"] + ": " + url + " \r\n"
        message_text += " FILE SIZE: " + result["size"] + "\r\n"
        # message_text += " Uploaded " + result["date"] + "\r\n"
        message_text += " SEEDS: " + \
            result["seeds"] + " PEERS: " + result["peers"] + " \r\n"
        message_text += "===\r\n"
        output_str += message_text
        i = i + 1
    end = datetime.now()
    ms = (end - start).seconds
    await event.edit("Scrapped {} for {} in {} seconds. Obtained Results: \n {}".format(input_type, input_str, ms, output_str))


@borg.on(admin_cmd(  # pylint:disable=E0602
    "torrent (.*)"
))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    magnetic_link = get_magnetic_link(input_str)
    magnetic_link_file = "{}{}.txt".format(
        Config.TMP_DOWNLOAD_DIRECTORY, input_str)  # pylint:disable=E0602
    magnetic_link_caption = "Magnetic Link: `{}`".format(input_str)
    file_ponter = open(magnetic_link_file, "w+")
    file_ponter.write(magnetic_link)
    file_ponter.close()
    await borg.send_file(
        event.chat_id,
        magnetic_link_file,
        caption=magnetic_link_caption,
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id
    )
    os.remove(magnetic_link_file)
    if Config.HASH_TO_TORRENT_API is None:  # pylint:disable=E0602
        logger.info(  # pylint:disable=E0602
            "Torrent file cannot be send without setting the ENV variable")
    else:
        url = Config.HASH_TO_TORRENT_API.format(input_str)  # pylint:disable=E0602
        torrent_file_caption = "Torrent File: `{}`".format(input_str)
        if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):  # pylint:disable=E0602
            os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)  # pylint:disable=E0602
        # pylint:disable=E0602
        required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + " " + input_str + ".torrent"
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(required_file_name, "wb") as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)
            await borg.send_file(
                event.chat_id,
                required_file_name,
                caption=torrent_file_caption,
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id
            )
            os.remove(required_file_name)
        else:
            logger.info(  # pylint:disable=E0602
                "Torrent file cannot be send without setting the ENV variable")
    end = datetime.now()
    ms = (end - start).seconds
    output_str = "Obtained Magnetic Link and Torrent File for the Info Hash: `{}` in {} seconds.".format(
        input_str, ms)
    await event.edit(output_str)


def search_idop_se(search_query):
    r = []
    url = "https://idope.top/search/{}/".format(search_query)
    raw_html = requests.get(url).content
    soup = BeautifulSoup(raw_html, "html.parser")
    results = soup.find_all("div", {"class": "resultdiv"})
    for item in results:
        """ The content scrapped on 12.08.2018 22:00:45
        """
        title = item.find_all("div", {"class": "resultdivtopname"})[
            0].get_text().strip()
        hash = item.find_all("div", {"class": "resultdivbottonseed"})[
            0].get_text().strip()
        age = item.find_all("div", {"class": "resultdivbottontime"})[
            0].get_text().strip()
        size = item.find_all("div", {"class": "resultdivbottonlength"})[
            0].get_text().strip()
        r.append({
            "title": title,
            "hash": hash,
            "age": age,
            "size": size,
            "seeds": "NA",
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
    results = soup.find_all("div", {"class": "results"})[0]
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


def get_magnetic_link(info_hash):
    name = "UniBorgTorrent"
    trackers = [
        "udp://tracker.openbittorrent.com:80",
        "udp://opentor.org:2710",
        "udp://tracker.ccc.de:80",
        "udp://tracker.blackunicorn.xyz:6969",
        "udp://tracker.coppersurfer.tk:6969",
        "udp://tracker.leechers-paradise.org:6969",
        "udp://tracker.openbittorrent.com:80",
        "udp://tracker.publicbt.com:80",
        "udp://tracker.istole.it:80",
        "udp://tracker.btzoo.eu:80/announce",
        "http://opensharing.org:2710/announce",
        "udp://open.demonii.com:1337/announce",
        "http://announce.torrentsmd.com:8080/announce.php",
        "http://announce.torrentsmd.com:6969/announce",
        "http://bt.careland.com.cn:6969/announce",
        "http://i.bandito.org/announce",
        "http://bttrack.9you.com/announce",
    ]
    data = ""
    data += "magnet:"
    data += "?xt=urn:btih:"
    data += info_hash
    data += "&dn="
    data += urllib.parse.quote_plus(name)
    data += ""
    for tracker in trackers:
        data += "&tr="
        data += urllib.parse.quote_plus(tracker)
    return data
