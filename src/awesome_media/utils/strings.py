from urllib.parse import urlparse


def url_to_filename(url: str) -> str:
    """
    Converts a website URL to the expected YAML filename format.
    Examples:
        https://gunaz.tv/fa -> gunaz.tv.fa.yaml
        https://www.dw.com/fa-ir/ -> dw.com.fa-ir.yaml
    """
    try:
        parsed = urlparse(url)
        # Remove 'www.' and convert to lowercase
        netloc = parsed.netloc.replace("www.", "").lower()

        # Remove leading/trailing slashes from path and replace internal ones with dots
        path = parsed.path.strip("/").replace("/", ".")

        # Combine
        if path:
            filename = f"{netloc}.{path}.yaml"
        else:
            filename = f"{netloc}.yaml"

        return filename
    except Exception:
        return "unknown.yaml"


def truncate_text(text: str, length: int = 120) -> str:
    if not text:
        return ""
    clean = text.replace("\n", " ").strip()
    return clean[:length] + "..." if len(clean) > length else clean
