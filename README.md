# Regional IPTV

为电视自动生成一份精简频道列表。数据来自
[Free-TV/IPTV](https://github.com/Free-TV/IPTV)，每 6 小时由 GitHub Actions 更新。

筛选范围：

- 中国大陆、香港、澳门、台湾
- 日本、韩国及东南亚
- 澳大利亚、新西兰
- 英国、爱尔兰、美国、加拿大

列表会排除 Free-TV 标记为地区限制、YouTube、Twitch 的项目，以及购物频道，只保留
HTTP(S) 直连。Free-TV 本身是人工维护的可用频道集合，但实际流畅度仍取决于播放地点、
运营商网络和频道源的临时状态。

## OwnTV

订阅地址：

```text
https://raw.githubusercontent.com/akang943578/regional-iptv/main/playlist.m3u8
```

在 OwnTV 中将刷新策略设为“启动时刷新”即可每次启动获取仓库中最新生成的版本。

## 本地生成

```bash
python3 build_playlist.py
```
