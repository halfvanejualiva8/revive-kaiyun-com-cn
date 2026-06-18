from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

SAMPLE_URL = "https://www.revive-kaiyun.com.cn"
SAMPLE_KEYWORD = "开云"

@dataclass
class KeywordNote:
    """Represents a single keyword note with metadata."""
    keyword: str
    url: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    tags: List[str] = field(default_factory=list)
    priority: int = 5
    note: Optional[str] = None

    def short_display(self) -> str:
        """Return a compact one-line summary."""
        tag_str = ", ".join(self.tags) if self.tags else "无标签"
        return f"[{self.priority}] {self.keyword} ({self.url}) | 标签: {tag_str} | {self.created_at}"

    def full_display(self) -> str:
        """Return a detailed multi-line formatted string."""
        lines = [
            f"关键词: {self.keyword}",
            f"来源URL: {self.url}",
            f"创建时间: {self.created_at}",
            f"优先级: {self.priority}",
            f"标签: {', '.join(self.tags) if self.tags else '无'}",
        ]
        if self.note:
            lines.append(f"备注: {self.note}")
        return "\n".join(lines)


@dataclass
class KeywordCollection:
    """Manages a list of KeywordNote objects and provides formatting utilities."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def sort_by_priority(self, reverse: bool = True) -> None:
        self.notes.sort(key=lambda x: x.priority, reverse=reverse)

    def list_short(self) -> str:
        """Return a newline-separated list of short summaries."""
        return "\n".join(n.short_display() for n in self.notes)

    def report(self) -> str:
        """Generate a full formatted report for all notes."""
        if not self.notes:
            return "（暂无关键词笔记）"
        parts = [f"关键词笔记报告（共 {len(self.notes)} 条）", "=" * 40]
        for n in self.notes:
            parts.append(n.full_display())
            parts.append("-" * 30)
        return "\n".join(parts)


def create_demo_collection() -> KeywordCollection:
    """Create a sample collection with pre-defined notes for demonstration."""
    collection = KeywordCollection()
    collection.add(KeywordNote(
        keyword=SAMPLE_KEYWORD,
        url=SAMPLE_URL,
        tags=["开源", "社区", "示例"],
        priority=4,
        note="这是一个演示关键词，用于展示笔记功能。"
    ))
    collection.add(KeywordNote(
        keyword="Python",
        url="https://www.python.org",
        tags=["编程", "语言"],
        priority=5,
    ))
    collection.add(KeywordNote(
        keyword="开云平台",
        url="https://www.revive-kaiyun.com.cn/about",
        tags=["开云", "平台"],
        priority=3,
        note="平台介绍页面"
    ))
    return collection


def main() -> None:
    """Run a simple demonstration of the keyword notes system."""
    print("=== 关键词笔记演示 ===\n")
    
    collection = create_demo_collection()
    
    print("所有笔记（紧凑格式）：")
    print(collection.list_short())
    print()
    
    print("完整报告：")
    print(collection.report())
    print()
    
    print("按关键词 '开云' 过滤：")
    for note in collection.filter_by_keyword("开云"):
        print(note.short_display())
    print()
    
    print("按优先级排序后：")
    collection.sort_by_priority(reverse=True)
    print(collection.list_short())


if __name__ == "__main__":
    main()