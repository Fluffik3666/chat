import re
import socket
from urllib.parse import urlparse, quote

class Unblock:
    def __init__(
        self,
        base_url: str
    ):
        self.base_url = base_url
    
    # -------
    # CONTENT CHECKS
    # -------
    
    def can_handle_content(
        self,
        content: str = None
    ) -> tuple[bool, list[str]]: 
        if not content or content == "":
            return False, []
        
        urls = self._extract_urls(content)
        valid_urls = []
        
        for url in urls:
            normalized_url = self._normalize_url(url)
            if self._is_valid_url(normalized_url):
                valid_urls.append(normalized_url)
        
        return len(valid_urls) > 0, valid_urls
    
    def _extract_urls(
        self,
        text: str
    ) -> list:
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, text, re.IGNORECASE)
        
        domain_pattern = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
        potential_domains = re.findall(domain_pattern, text)
        
        return urls + potential_domains
    
    def _normalize_url(
        self,
        url: str
    ) -> str:
        url = url.strip()
        if not re.match(r'^https?://', url, re.IGNORECASE):
            url = 'https://' + url
        return url
    
    def _is_valid_url(
        self,
        url: str
    ) -> bool:
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return False
            
            hostname = parsed.netloc.split(':')[0]
            if not self._is_valid_hostname(hostname):
                return False
            
            return self._dns_lookup(hostname)
        except:
            return False
    
    def _is_valid_hostname(
        self,
        hostname: str
    ) -> bool:
        if len(hostname) > 253:
            return False
        
        hostname = hostname.rstrip('.')
        allowed = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$")
        
        return all(allowed.match(label) for label in hostname.split('.') if label)
    
    def _dns_lookup(
        self,
        hostname: str
    ) -> bool:
        try:
            socket.gethostbyname(hostname)
            return True
        except socket.gaierror:
            return False
    
    # -------
    # GENERATE URLs
    # -------
    
    def generate_proxied_urls(
        self,
        urls: list[str] 
    ) -> list[str]:
        if len(urls) == 0:
            return []
    
        proxied_urls = []
        for url in urls:
            encoded_url = quote(url, safe='')
            proxied_url = f"{self.base_url}/unblock/{encoded_url}"
            proxied_urls.append(proxied_url)
    
        return proxied_urls