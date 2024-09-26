import json
from dataclasses import dataclass, field, asdict
from datetime import date, timedelta
from enum import Enum, auto
from typing import List, Optional, Dict, Union

# Book categories
VALID_CATEGORIES = [
    "Action/Adventure fiction",
    "Children's fiction",
    "Classic fiction",
    "Contemporary fiction",
    "Fantasy",
    "Dark fantasy",
    "Fairy tales",
    "Folktales",
    "Heroic fantasy",
    "High fantasy",
    "Historical fantasy",
    "Low fantasy",
    "Magical realism",
    "Mythic fantasy",
    "Urban fantasy",
    "Graphic novel",
    "Historical fiction",
    "Horror",
    "Body horror",
    "Comedy horror",
    "Gothic horror",
    "Lovecraftian/Cosmic horror",
    "Paranormal horror",
    "Post-apocalyptic horror",
    "Psychological horror",
    "Quiet horror",
    "Slasher",
    "LGBTQ+",
    "Literary fiction",
    "Mystery",
    "Caper",
    "Cozy mystery",
    "Gumshoe/Detective mystery",
    "Historical mystery",
    "Howdunnits",
    "Locked room mystery",
    "Noir",
    "Procedural/Hard-boiled mystery",
    "Supernatural mystery",
    "New adult",
    "Romance",
    "Contemporary romance",
    "Dark romance",
    "Erotic romance",
    "Fantasy romance (Romantasy)",
    "Gothic romance",
    "Historical romance",
    "Paranormal romance",
    "Regency",
    "Romantic comedy",
    "Romantic suspense",
    "Sci-fi romance",
    "Satire",
    "Science fiction",
    "Apocalyptic sci-fi",
    "Colonization sci-fi",
    "Hard sci-fi",
    "Military sci-fi",
    "Mind uploading sci-fi",
    "Parallel world sci-fi",
    "Soft sci-fi",
    "Space opera",
    "Space western",
    "Steampunk",
    "Short story",
    "Thriller",
    "Action thriller",
    "Conspiracy thriller",
    "Disaster thriller",
    "Espionage thriller",
    "Forensic thriller",
    "Historical thriller",
    "Legal thriller",
    "Paranormal thriller",
    "Psychological thriller",
    "Religious thriller",
    "Western",
    "Women's fiction",
    "Young adult",
    "Art & photography",
    "Autobiography/Memoir",
    "Biography",
    "Essays",
    "Food & drink",
    "History",
    "How-To/Guides",
    "Humanities & social sciences",
    "Humor",
    "Parenting",
    "Philosophy",
    "Religion & spirituality",
    "Science & technology",
    "Self-help",
    "Travel",
    "True crime",
]

# Ebook formats
EBOOK_FORMATS = [
    "EPUB",
    "PDF",
    "MOBI",
    "AZW",
    "AZW3",
    "KFX",
    "IBA",
    "FB2",
    "LIT",
    "PRC",
    "TXT",
    "RTF",
    "HTML",
]

# Audiobook formats
AUDIOBOOK_FORMATS = [
    "MP3",
    "AAC",
    "M4A",
    "M4B",
    "WMA",
    "OGG",
    "FLAC",
    "WAV",
    "AA",
    "AAX",
]


class Category(Enum):
    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            for member in cls:
                if member.value.lower() == value.lower():
                    return member
        return None


class BookCategory(Category):
    def __new__(cls, category: str):
        if category not in VALID_CATEGORIES:
            raise ValueError(f"Invalid category {category}")
        obj = object.__new__(cls)
        obj._value_ = category  # pylint: disable=protected-access
        return obj

    @classmethod
    def create_categories(cls):
        return {category: cls(category) for category in VALID_CATEGORIES}


BookCategory = BookCategory.create_categories()


@dataclass
class LibraryLocation:
    category: BookCategory
    shelf: int

    @property
    def dict_representation(self) -> Dict[str, Union[str, int]]:
        return asdict(self)

    @property
    def json_representation(self) -> str:
        return json.dumps(self.dict_representation)

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> "LibraryLocation":
        return cls(category=data["category"], shelf=data["shelf"])

    @classmethod
    def from_json(cls, json_str: str) -> "LibraryLocation":
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __str__(self):
        return f"{self.category} - Shelf {self.shelf}"

    def __post_init__(self):
        if not isinstance(self.category, BookCategory):
            raise ValueError(f"Invalid category {self.category}")
        if not isinstance(self.shelf, int) or self.shelf < 1:
            raise ValueError(f"Invalid shelf number {self.shelf}")


@dataclass
class BookSeries:
    series: str
    number: int

    @property
    def dict_representation(self) -> Dict[str, Union[str, int]]:
        return asdict(self)

    @property
    def json_representation(self) -> str:
        return json.dumps(self.dict_representation)

    @classmethod
    def from_dict(cls, data: Dict[str, Union[str, int]]) -> "BookSeries":
        return cls(series=data["series"], number=data["number"])

    @classmethod
    def from_json(cls, json_str: str) -> "BookSeries":
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __str__(self):
        return f"{self.series} - Book {self.number}"


class BookFormat(Enum):
    HARDCOVER = "Hardcover"
    PAPERBACK = "Paperback"
    AUDIOBOOK = "Audiobook"
    EBOOK = "E-book"

    @property
    def is_physical(self):
        return self in {BookFormat.HARDCOVER, BookFormat.PAPERBACK}


class BookStatus(Enum):
    AVAILABLE = auto()
    CHECKED_OUT = auto()
    ON_HOLD = auto()
    IN_REPAIR = auto()

    @classmethod
    def get_valid_statuses(cls, book_format: BookFormat) -> List["BookStatus"]:
        if book_format.is_physical:
            return list(cls)
        return [cls.AVAILABLE]


class DigitalFormat(Category):
    def __new__(cls, formats: str):
        if formats not in EBOOK_FORMATS + AUDIOBOOK_FORMATS:
            raise ValueError(f"Invalid digital format {formats}")
        obj = object.__new__(cls)
        obj._value_ = formats  # pylint: disable=protected-access
        return obj

    @classmethod
    def create_formats(cls):
        return {format: cls(format) for format in EBOOK_FORMATS + AUDIOBOOK_FORMATS}


DigitalFormat = DigitalFormat.create_formats()


class BookCondition(Enum):
    NEW = auto()
    EXCELLENT = auto()
    GOOD = auto()
    FAIR = auto()
    POOR = auto()

    @classmethod
    def get_valid_conditions(cls, book_format: BookFormat) -> List["BookCondition"]:
        if book_format.is_physical:
            return list(cls)
        return [cls.NEW]


@dataclass
class Book:
    title: str
    authors: list[str] = field(default_factory=list)
    isbn: str
    publication_date: date
    publisher: str
    edition: int
    genres: list[str] = field(default_factory=list)
    number_of_pages: int
    language: str
    format: BookFormat
    summary: str
    cover_image_url: str
    current_status: BookStatus
    location_in_library: Optional[LibraryLocation] = None
    date_added: date
    purchase_price: float
    replacement_cost: float
    dewey_decimal: str
    keywords: list[str] = field(default_factory=list)
    reading_level: str
    series_name_and_num: Optional[BookSeries] = None
    orig_pub_date: Optional[date] = None
    translator: Optional[str] = None
    illustrator: Optional[str] = None
    condition: BookCondition
    number_of_times_checked_out: int = 0
    user_ratings: Dict[str, int] = field(default_factory=dict)
    awards: list[str] = field(default_factory=list)
    barcode_number: str
    date_available: Optional[date] = None
    digital_file_format: Optional[DigitalFormat] = None
    digital_file_size: Optional[float] = None
    audiobook_length: Optional[timedelta] = None

    def __post_init__(self):
        valid_statuses = BookStatus.get_valid_statuses(self.format)
        if self.current_status not in valid_statuses:
            raise ValueError(
                f"Invalid status {self.current_status} for book format {self.format}"
            )

    def set_status(self, new_status: BookStatus):
        valid_statuses = BookStatus.get_valid_statuses(self.format)
        if new_status not in valid_statuses:
            raise ValueError(f"Cannot set status {new_status} for {self.format} book")
        self.current_status = new_status

    def format_audiobook_length(self) -> str:
        if self.audiobook_length is None:
            return "N/A"
        hours, remainder = divmod(self.audiobook_length.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
