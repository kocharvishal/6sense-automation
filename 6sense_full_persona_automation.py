# -*- coding: utf-8 -*-

import requests
import json
import pandas as pd
import time
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SixSenseFullPersonaAutomation:
    def __init__(self):
        self.base_url = "https://forageai.sales.6sense.com"
        self.session = requests.Session()
        self.org_id = 81778
        self.product_category = "forageai"
        self.account_summary_url = f"{self.base_url}/salesapp-graphql/?operationName=AccountSummary"
        self.persona_url = f"{self.base_url}/salesapp-graphql/?operationName=PersonaV2"
        # Headers and cookies (copy from working automation)
        self.headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'en-US,en;q=0.8',
            'authorization': '',
            'content-type': 'application/json',
            'origin': 'https://forageai.sales.6sense.com',
            'priority': 'u=1, i',
            'referer': 'https://forageai.sales.6sense.com/discovery?tab=Company',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'x-csrftoken': 'pd8Z7sPzUik6TMRZRtso5dUW68YIT0M8HC1EKje0YwygRaQv6L6MnT8hJUVI3G1d',
            # Set the Cookie header directly as copied from browser
            'Cookie': 'cf_clearance=9X62w8_e0y1t00e7H_ynySZZj0pKNtR70E0hGDj1_gA-1749135618-1.2.1.1-Rk48XogBwk2Nr4x8aYzKOcjGJAh.IpusGTSvXYJKPa5J8inUR5rH9nzQEZamA7.EJsQyUEwz_bQk8FW_Fqxb6hk171DsFyEeOgR5WeOPa7rVG.vnTHiuv.WEHve1yaxn6bhlXSqXinnOJBQu6.vK4lBQc_f3ZQrQzy0icn8ZTDLc9Gbkr08ad9hulBgLG1b01k1K02ZAcyJNQUu53ZmUKQRJEsaypslHlmwsZcy4dPEW9s2Hi4l_NZY7INDqMqt74R8bgJKjOYx8gYoUZBiaVOCyDtj_C252xhmYNqIBKPG83xSHDO6_ePU4.esVngdUDfgQMdDF0pSUxHYQ2dIFLwVzwzstUGq19MwK4XtZtG4; __Secure-6sisession=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIuNnNlbnNlLmNvbSIsImlhdCI6MTc1NDU1ODg0NiwiZXhwIjoxNzU0NTY2MDQ2LCJfY3NyZnRva2VuIjoic3ozUE4xekJlb29rOHk5R3BzT3lzUW92Tlc3YWtRcGYiLCJpbml0aWFsX2lhdCI6MTc1NDU1ODc0NSwidGltZV9zdGFydGVkIjoiMjAyNS0wOC0wNyAwNDoyNzoyNCIsIl9hdXRoX3VzZXJfaWQiOiIyMTUzNTIiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJzaXhzZW5zZV9hdXRoLmF1dGguYmFja2VuZHMuU2l4c2Vuc2VBdXRoQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImY3MGIxOGNlM2Y5NWJjNzRmNzlkODU0OTFhNjZjYTIyZjViZjJiMzExZjU2ZGViM2JiZTM0NDQ5ODk5YWU2NDMiLCJfYXV0aF9vcmdfdXNlcl9oYXNoIjoiY2JmMTE3ZWNlZWNjMDMzMjVjMzI5ZWM0OGUwMjM3OTdlNTVkM2ZkYmI0ZGQ0NjM1YzVkNTA2NTgzMDczZDc1NiIsImxhc3RfbG9naW4iOiIyMDI1LTA4LTA3IDA5OjI2OjIwIiwib3JnYW5pemF0aW9uIjoiZm9yYWdlYWkiLCJvcmdfYXV0aF9pZCI6ODExMjUsIm9yZ19leHRlcm5hbF9pZCI6ODE3NzgsInNsdWciOiJmb3JhZ2VhaSIsImF1dGhfdHlwZSI6WyJhcGlfa2V5IiwiaW5kX2NyZWQiXSwiaXNfc2luZ2xlX3VzZXJfb3JnIjpmYWxzZSwicm9sZSI6Ik9XTkVSIiwic2Vzc2lvbl91dWlkIjoiMWYzOGJjNzQtOTM5OC00OGFmLWI3MWUtMGQwMDU1YjJlNTg5IiwiYXBwX3JvbGVfaWRzIjpbeyJyb2xlX2lkIjoxNywiYXBwX2lkIjo0fSx7InJvbGVfaWQiOjI4LCJhcHBfaWQiOjJ9XSwicmJhY19yb2xlX2lkIjpudWxsLCJ1c2VyIjp7InVzZXJuYW1lIjoicHVuaXRoLnlhZGF2QGZvcmFnZS5haSIsImlkIjoyMTUzNTIsImlzX3N1cGVydXNlciI6ZmFsc2UsImlzX3N0YWZmIjpmYWxzZSwiaXNfaW50ZXJuYWx1c2VyIjpmYWxzZSwiaXNfZGV2IjpmYWxzZX0sInNpYmxpbmdfb3JnX2V4dGVybmFsX2lkcyI6WzgxNzc4XX0.oD0RKtEWfaupQAAN73hW_nngnjvNjRAl2ZAaM-os9Kc'
        }
        # Remove self.cookies usage, as Cookie header is now set directly

    def get_company_finder_payload(self, page: int = 1, page_size: int = 25) -> Dict:
        # Full payload copied from 6sense_full_automation.py
        return {"id":1278867,"filters":[{"variable":"headQuarterCountry","params":{"default":{"values":[{"label":"United States","value":"United States"},{"label":"United Kingdom","value":"United Kingdom"},{"label":"Canada","value":"Canada"},{"label":"France","value":"France"},{"label":"Germany","value":"Germany"}],"operator":"EqOp","data_type":"Const","valueRelationship":"ModelOr"}}},{"variable":"employeeRange","params":{"default":{"values":[{"label":"50 - 99","value":"50 - 99"},{"label":"100 - 249","value":"100 - 249"},{"label":"250 - 499","value":"250 - 499"},{"label":"500 - 999","value":"500 - 999"},{"label":"1,000 - 4,999","value":"1,000 - 4,999"},{"label":"5,000 - 9,999","value":"5,000 - 9,999"},{"label":"10,000+","value":"10,000+"}],"operator":"EqOp","data_type":"Const","valueRelationship":"ModelOr"}}},{"variable":"accountTempRange","params":{"default":{"values":[{"value":"Hot (New)"},{"value":"Hot"}],"operator":"EqOp","data_type":"Const","valueRelationship":"ModelOr"},"product":{"values":[{"label":"forageai","value":"forageai"}],"operator":"EqOp","data_type":"Const","valueRelationship":"ModelOr"}}},{"variable":"bomboraSurge","params":{"default":{"values":[{"label":"AI Automation","value":"AI Automation"},{"label":"Data Automation","value":"Data Automation"},{"label":"Data Extraction","value":"Data Extraction"},{"label":"Intelligent Document Processing","value":"Intelligent Document Processing"},{"label":"Unstructured Data","value":"Unstructured Data"},{"label":"B2B Data","value":"B2B Data"},{"label":"B2B Firmographic APIs","value":"B2B Firmographic APIs"},{"label":"Data Acquisition","value":"Data Acquisition"}],"operator":"EqOp","data_type":"Const","valueRelationship":"ModelOr"}}},{"variable":"keywordName","params":{"default":{"values":[{"label":"80legs","value":"80legs"},{"label":"ABBYY","value":"abbyy"},{"label":"Accurate Web Data","value":"accuratewebdata"},{"label":"Agentforce","value":"agentforce"},{"label":"Agentic AI for Data Extraction","value":"agenticaifordataextraction"},{"label":"AI powered data insights","value":"aipowereddatainsights"},{"label":"AI-powered Data Extraction","value":"aipowereddataextraction"},{"label":"Automated Data Extraction","value":"automateddataextraction"},{"label":"automated data solutions","value":"automateddatasolutions"},{"label":"Automated Financial Data Extraction","value":"automatedfinancialdataextraction"},{"label":"Automated Web Data Capture","value":"automatedwebdatacapture"},{"label":"Automated Web Data Extraction","value":"automatedwebdataextraction"},{"label":"B2B Data Extraction","value":"b2bdataextraction"},{"label":"Big Data Web Extraction","value":"bigdatawebextraction"},{"label":"Bright Data","value":"brightdata"},{"label":"data extraction","value":"dataextraction"},{"label":"Data Extraction from Documents","value":"dataextractionfromdocuments"},{"label":"datasets","value":"datasets"},{"label":"E-commerce Web Data","value":"ecommercewebdata"},{"label":"Employee Data Extraction","value":"employeedataextraction"},{"label":"Enterprise Web Data Strategy","value":"enterprisewebdatastrategy"},{"label":"firmographic data","value":"firmographicdata"},{"label":"Firmographic Data Extraction","value":"firmographicdataextraction"},{"label":"HR Data Extraction","value":"hrdataextraction"},{"label":"Influencer Data Extraction","value":"influencerdataextraction"},{"label":"metadata extraction","value":"metadataextraction"},{"label":"agentic solutions","value":"agenticsolutions"},{"label":"agentic workflows","value":"agenticworkflows"},{"label":"Social Media Data Extraction","value":"socialmediadataextraction"},{"label":"document extraction","value":"documentextraction"},{"label":"document parsing","value":"documentparsing"},{"label":"document processing","value":"documentprocessing"},{"label":"Docsumo","value":"docsumo"},{"label":"AI agent","value":"aiagent"},{"label":"AI agents","value":"aiagents"},{"label":"Automated News Website","value":"automatednewswebsite"},{"label":"automated retrieval","value":"automatedretrieval"},{"label":"automation","value":"automation"},{"label":"Web Data Automation","value":"webdataautomation"},{"label":"Web Data Automation Solutions","value":"webdataautomationsolutions"},{"label":"AutoScraper","value":"autoscraper"},{"label":"Automatio","value":"automatio"},{"label":"WebAutomation.io","value":"webautomationio"},{"label":"AI-powered Web Scraping","value":"aipoweredwebscraping"},{"label":"Dynamic Web Scraping","value":"dynamicwebscraping"},{"label":"Enterprise Web Scraping","value":"enterprisewebscraping"},{"label":"Low-code Web Scraping Platforms","value":"lowcodewebscrapingplatforms"},{"label":"Monitor Web Pages for Changes","value":"monitorwebpagesforchanges"},{"label":"Monitoring News Websites","value":"monitoringnewswebsites"},{"label":"News Aggregation Websites","value":"newsaggregationwebsites"},{"label":"No-code Web Scraping Solutions","value":"nocodewebscrapingsolutions"},{"label":"Real-time Web Scraping Techniques","value":"realtimewebscrapingtechniques"},{"label":"Scaling Web Scraping","value":"scalingwebscraping"},{"label":"Solutions to Web Scraping Problems","value":"solutionstowebscrapingproblems"},{"label":"web crawler","value":"webcrawler"},{"label":"Web Crawler Online","value":"webcrawleronline"},{"label":"Web Crawler Software","value":"webcrawlersoftware"},{"label":"web crawling","value":"webcrawling"},{"label":"Web Data Accuracy","value":"webdataaccuracy"},{"label":"Web Data Aggregation","value":"webdataaggregation"},{"label":"Web Data at Scale","value":"webdataatscale"},{"label":"Web Data Capture","value":"webdatacapture"},{"label":"Web Data Consistency","value":"webdataconsistency"},{"label":"Web Data Extraction","value":"webdataextraction"}],"operator":"EqOp","data_type":"Const","valueRelationship":"ModelOr"},"total_count":{"values":[{"value":1}],"operator":"GeOp","data_type":"IntConst","valueRelationship":"ModelOr"},"activityTimePeriod":{"values":[{"label":"Current Week","value":"current_week"}],"operator":"EqOp","data_type":"Const","valueRelationship":"ModelOr"}}},{"variable":"industry","params":{"default":{"values":[{"label":"Colleges & Universities","value":"Education: Colleges & Universities","selectedLabel":"Education: Colleges & Universities"},{"label":"Schools","value":"Education: Schools","selectedLabel":"Education: Schools"},{"label":"Government","value":"Government: Other","selectedLabel":"Government"}],"operator":"NotEqOp","data_type":"Const","valueRelationship":"ModelOr"}}},{"variable":"headQuarterCountry","params":{"default":{"values":[{"label":"India","value":"India"},{"label":"People's Republic of China","value":"People's Republic of China"}],"operator":"NotEqOp","data_type":"Const","valueRelationship":"ModelOr"}}},{"variable":"country","params":{"default":{"values":[{"label":"India","value":"India"},{"label":"People's Republic of China","value":"People's Republic of China"},{"label":"Pakistan","value":"Pakistan"},{"label":"Indonesia","value":"Indonesia"}],"operator":"NotEqOp","data_type":"Const","valueRelationship":"ModelOr"}}}],"relationship":{"children":[0,1,2,3,4,5,6,7],"operator":"ModelAnd"},"created":"2025-05-02T14:12:31.796087Z","updated":"2025-05-02T14:12:31.796138Z","is_deleted":False,"org_id":81778,"created_by":"punith.yadav@forage.ai","updated_by":"punith.yadav@forage.ai","updated_by_id":215352,"created_by_id":215352,"additional_fields":["company_logo_url","name","website","employee_range","employee_range_rank","industry_v2_ranked","city","state","country","phone_number","products_and_services","naics","sic","type","year_founded","total_funding_raised_range","revenue_range","revenue_range_rank","linkedin","facebook","twitter","usefulness_score"],"order_by":[{"name":"usefulness_score","desc":True}],"app":"sales"}

    def get_companies_list(self, page: int = 1, page_size: int = 25) -> List[Dict]:
        url = f"{self.base_url}/charcoal-sales/{self.org_id}/filterset/live_query/objects/account/?page={page}&page_size={page_size}"
        payload = self.get_company_finder_payload(page, page_size)
        try:
            response = self.session.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            companies = data.get('results', [])
            logger.info(f"API Response for page {page}:")
            for i, company in enumerate(companies):
                logger.info(f"  {i+1}. {company.get('name', 'Unknown')} (mid: {company.get('mid', 'No MID')})")
            logger.info(f"Retrieved {len(companies)} companies from page {page}")
            return companies
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            logger.error(f"Error fetching companies list: {e}")
            if 'response' in locals():
                logger.error(f"Response content: {response.text}")
            return []

    def get_intent_and_location(self, mid: str) -> Tuple[str, str]:
        query = """
        query AccountSummary($product: String!, $dateRange: String!, $mid: String, $orgId: Int, $refreshSummary: String, $externalId: String) {
          accountSummary(
            product: $product
            dateRange: $dateRange
            mid: $mid
            orgId: $orgId
            refreshSummary: $refreshSummary
            externalId: $externalId
          ) {
            status
            summary
            __typename
          }
        }
        """
        variables = {
            "product": self.product_category,
            "dateRange": "last_30_days",
            "mid": mid,
            "orgId": self.org_id,
            "refreshSummary": None,
            "externalId": None
        }
        payload = {
            "query": query,
            "variables": variables
        }
        try:
            response = self.session.post(self.account_summary_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            summary = data.get('data', {}).get('accountSummary', {}).get('summary', "")
            logger.info(f"AccountSummary summary for mid {mid}: {summary} (type: {type(summary)})")
            if isinstance(summary, dict):
                what_happened = summary.get('what_happened_last30', [])
                intent = "-"
                intent_location = "-"
                for item in what_happened:
                    if 'Third Party Intent' in item:
                        match = re.search(r'has shown interest in (.+?)(\.|$)', item)
                        if match:
                            intent = match.group(1).replace(' and ', ', ').replace('.', '').strip()
                    if 'Keywords' in item:
                        locations = []
                        b_tags = re.findall(r'<b>(.+?)</b>', item)
                        for phrase in [r'at <b>', r'in <b>', r'locations? like <b>', r'and <b>']:
                            split_item = re.split(phrase, item, flags=re.IGNORECASE)
                            if len(split_item) > 1:
                                after_phrase = split_item[1]
                                locs = re.findall(r'<b>(.+?)</b>', after_phrase)
                                locations.extend(locs)
                        if locations:
                            intent_location = ', '.join(sorted(set(locations)))
                return intent, intent_location
            elif isinstance(summary, str):
                return self.parse_intent_from_summary(summary)
            else:
                return "-", "-"
        except Exception as e:
            logger.warning(f"Error fetching intent/location for mid {mid}: {e}")
            return "-", "-"

    def parse_intent_from_summary(self, summary: str) -> Tuple[str, str]:
        intent = "-"
        intent_location = "-"
        if summary:
            keywords_match = re.search(r'<b>Keywords:</b>\s*(.*?)<', summary)
            if keywords_match:
                intent = keywords_match.group(1).strip()
            location_match = re.search(r'<b>Third Party Intent:</b>\s*(.*?)<', summary)
            if location_match:
                intent_location = location_match.group(1).strip()
        return intent, intent_location

    def extract_company_data(self, company: Dict, intent: str, intent_location: str) -> Dict:
        name = company.get("name", "-")
        city = company.get("city", "")
        state = company.get("state", "")
        country = company.get("country", "")
        location = ', '.join([v for v in [city, state, country] if v]) or "-"
        website = company.get("website", "-")
        employee_range = company.get("employee_range", "-")
        linkedin = company.get("linkedin", "-")
        if linkedin and not linkedin.startswith("http"):
            linkedin = "https://" + linkedin
        return {
            "Company name": name,
            "Company location": location,
            "Company website URL": website,
            "Company size": employee_range,
            "Company LinkedIn URL": linkedin,
            "Intent": intent,
            "Intent location": intent_location
        }

    def run_automation(self, max_pages: Optional[int] = None, delay_between_requests: float = 1.0):
        all_rows = []
        processed_mids = set()
        logger.info(f"Starting 6sense persona automation - fetching up to 25 companies with C-level, VP, Director, Managerial priority")
        page = 1
        company_count = 0
        max_companies = 25  # Now process up to 25 companies
        run_date = datetime.now().strftime('%a, %b %d')
        while True:
            if max_pages is not None and page > max_pages:
                logger.info(f"Reached max_pages limit: {max_pages}")
                break
            logger.info(f"Fetching page {page}...")
            companies = self.get_companies_list(page=page, page_size=25)
            if not companies:
                logger.info(f"No more companies found on page {page}. Stopping.")
                break
            logger.info(f"Processing {len(companies)} companies from page {page}")
            for i, company in enumerate(companies):
                if company_count >= max_companies:
                    logger.info(f"Processed {max_companies} companies, stopping.")
                    return all_rows
                mid = company.get("mid")
                company_name = company.get("name", "Unknown")
                if not mid:
                    logger.warning(f"Skipping company without master_id: {company_name}")
                    continue
                if mid in processed_mids:
                    logger.info(f"Skipping duplicate company: {company_name} (mid: {mid})")
                    continue
                processed_mids.add(mid)
                company_count += 1
                logger.info(f"Processing company {i+1}/{len(companies)} on page {page}: {company_name} (mid: {mid})")
                intent, intent_location = self.get_intent_and_location(mid)
                company_data = self.extract_company_data(company, intent, intent_location)
                logger.info(f"Calling get_personas for mid {mid} ({company_name})...")
                # Fetch all personas (not just 5) for filtering
                all_personas = self.get_personas(mid, return_all=True) if hasattr(self, 'get_personas') and 'return_all' in self.get_personas.__code__.co_varnames else self.get_personas(mid)
                logger.info(f"Raw personas response for {company_name}: {all_personas}")
                # Filter personas by job level priority using the 'job_level' field from the API
                def match_level(person, level):
                    jl = person.get('Job Level', '').strip().lower()
                    return jl == level
                def contains_level(person, level):
                    jl = person.get('Job Level', '').strip().lower()
                    return level in jl
                # Priority order using job_level string
                levels = [
                    ('c-level', lambda p: match_level(p, 'c-level')),
                    ('vice president', lambda p: match_level(p, 'vice president')),
                    ('director', lambda p: match_level(p, 'director')),
                    ('manager', lambda p: match_level(p, 'manager')),
                ]
                selected = []
                used = set()
                for level, match_fn in levels:
                    for p in all_personas:
                        if len(selected) >= 5:
                            break
                        if id(p) in used:
                            continue
                        if match_fn(p):
                            selected.append(p)
                            used.add(id(p))
                    if len(selected) >= 5:
                        break
                # If still less than 5, fill with any remaining that have a job_level in the allowed set
                allowed_levels = {'c-level', 'vice president', 'director', 'manager'}
                if len(selected) < 5:
                    for p in all_personas:
                        if len(selected) >= 5:
                            break
                        if id(p) in used:
                            continue
                        jl = p.get('Job Level', '').strip().lower()
                        if jl in allowed_levels:
                            selected.append(p)
                            used.add(id(p))
                # Write company name only in the first row for each company
                for idx, persona in enumerate(selected):
                    row = {**persona, **company_data}
                    # Always fill company name in all rows
                    if idx > 0:
                        row["Company LinkedIn URL"] = ""
                    else:
                        row["Company LinkedIn URL"] = company_data.get("Company LinkedIn URL", "")
                    row["Date"] = run_date
                    all_rows.append(row)
                # Do NOT add a separator row after each company block
                if i < len(companies) - 1 and company_count < max_companies:
                    time.sleep(delay_between_requests)
            page += 1
            time.sleep(delay_between_requests)
        logger.info(f"Collected {len(all_rows)} total rows from {len(processed_mids)} unique companies")
        return all_rows

    # Update get_personas to return job level for filtering
    def get_personas(self, master_id: str, return_all: bool = False) -> list:
        """Fetch personas for a company using PersonaV2 API. If return_all=True, return all, else up to 5."""
        query = """
        query PersonaV2($masterId: String!, $dateRange: String!, $product: String!, $orgId: Int!) {
          personaV2(
            masterId: $masterId
            dateRange: $dateRange
            productCategory: $product
            orgId: $orgId
          ) {
            contacts
            jrjlScoresRaw
            __typename
          }
        }
        """
        variables = {
            "masterId": master_id,
            "dateRange": "last_90_days",
            "product": self.product_category,
            "orgId": self.org_id
        }
        payload = {
            "query": query,
            "variables": variables
        }
        try:
            response = self.session.post(self.persona_url, headers=self.headers, json=payload)
            print("Persona API raw response:", response.text)  # For debugging
            response.raise_for_status()
            data = response.json()
            contacts = data.get('data', {}).get('personaV2', {}).get('contacts', [])
            if isinstance(contacts, str):
                try:
                    contacts = json.loads(contacts)
                except Exception:
                    contacts = []
            personas = []
            for person in contacts:
                first_name = person.get('full_name', '-').split(' ')[0] if person.get('full_name') else '-'
                last_name = ' '.join(person.get('full_name', '-').split(' ')[1:]) if person.get('full_name') and len(person.get('full_name').split(' ')) > 1 else '-'
                linkedin_url = person.get('linkedin_url', '-')
                if linkedin_url and not linkedin_url.startswith('http'):
                    linkedin_url = 'https://' + linkedin_url
                role_title = person.get('title', '-')
                job_level = person.get('job_level', '-')
                personas.append({
                    "First name": first_name,
                    "Last name": last_name,
                    "LinkedIn URL (Employee)": linkedin_url,
                    "E-mail address": "skipped",
                    "Role/Title": role_title,
                    "Job Level": job_level
                })
            if return_all:
                return personas
            return personas[:5]
        except Exception as e:
            logger.warning(f"Error fetching personas for master_id {master_id}: {e}")
            return []

    def save_to_csv(self, all_rows: List[Dict], filename: str = None):
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"6sense_full_persona_api_data_{timestamp}.csv"
        columns = [
            "First name", "Last name", "LinkedIn URL (Employee)", "E-mail address", "Role/Title",
            "Company name", "Company location", "Company website URL", 
            "Company LinkedIn URL", "Company size", "Intent", "Intent location", "Date"
        ]
        df = pd.DataFrame(all_rows)
        df = df.reindex(columns=columns, fill_value="-")
        df.to_csv(filename, index=False)
        logger.info(f"Data saved to {filename}")
        return filename

def main():
    automation = SixSenseFullPersonaAutomation()
    print("Fetching all available companies and personas...")
    all_rows = automation.run_automation(delay_between_requests=1.0)
    if all_rows:
        filename = automation.save_to_csv(all_rows)
        print(f"Completed! Found {len(all_rows)} rows.")
        print(f"Results saved to: {filename}")
    else:
        print("No data found. Please check your API credentials and filters.")

if __name__ == "__main__":
    main() 