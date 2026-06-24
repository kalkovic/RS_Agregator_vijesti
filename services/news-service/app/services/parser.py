import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

class RSSParser:
    @staticmethod
    def parse_xml(xml_content: str) -> list[dict[str, str]]:
        articles = []
        try:
            root = ET.fromstring(xml_content)
            items = root.findall(".//item")
            
            for item in items:
                title_node = item.find("title")
                link_node = item.find("link")
                pub_date_node = item.find("pubDate")
                category_node = item.find("category")

                articles.append({
                    "title": title_node.text if title_node is not None else "",
                    "link": link_node.text if link_node is not None else "",
                    "pubDate": pub_date_node.text if pub_date_node is not None else "",
                    "category": category_node.text if category_node is not None else "Općenito"
                })
        except ET.ParseError as e:
            logger.error(f"Greška pri parsiranju XML-a: {str(e)}")
        
        return articles