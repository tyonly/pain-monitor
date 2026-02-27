import feedparser
import json
import time

def fetch_reddit_rss():
    """从 Reddit RSS 获取用户痛点"""
    print("📡 从 Reddit RSS 获取数据...")
    
    rss_sources = [
        {"name": "r/startups", "url": "https://www.reddit.com/r/startups/new/.rss"},
        {"name": "r/SaaS", "url": "https://www.reddit.com/r/SaaS/new/.rss"},
        {"name": "r/Entrepreneur", "url": "https://www.reddit.com/r/Entrepreneur/new/.rss"}
    ]
    
    pain_keywords = [
        "struggle", "frustrated", "expensive", "hard to",
        "alternative", "looking for", "doesn't work"
    ]
    
    all_posts = []
    
    for source in rss_sources:
        try:
            feed = feedparser.parse(source['url'])
            found_match = False
            # 对于每个RSS源，优先找匹配关键词的帖子
            for entry in feed.entries[:10]:
                text = (entry.title + " " + (entry.get('summary', '') or "")).lower()
                matched = [k for k in pain_keywords if k in text]
                
                if matched:
                    all_posts.append({
                        "platform": "Reddit",
                        "subreddit": source['name'],
                        "title": entry.title,
                        "content": entry.get('summary', '')[:300],
                        "matched_keywords": matched,
                        "url": entry.link
                    })
                    found_match = True
                    break  # 找到第一个匹配的就跳出循环，继续下一个RSS源
            
            # 如果该RSS源没有找到匹配的帖子，则取第一个帖子作为代表
            if not found_match and len(feed.entries) > 0:
                entry = feed.entries[0]
                all_posts.append({
                    "platform": "Reddit",
                    "subreddit": source['name'],
                    "title": entry.title,
                    "content": entry.get('summary', '')[:300],
                    "matched_keywords": [],
                    "url": entry.link
                })
        except Exception as e:
            print(f"⚠️ 读取 {source['name']} 失败: {e}")
    
    print(f"🎯 采集到 {len(all_posts)} 条")
    return all_posts

# 如果直接运行，则执行采集
if __name__ == "__main__":
    posts = fetch_reddit_rss()
    with open("posts.json", "w") as f:
        json.dump(posts, f, indent=2)
    print("已保存到 posts.json")