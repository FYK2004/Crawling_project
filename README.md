## 简历匹配（爬虫模块）

### 输入输出
- 输入格式参照 [resume.json](../agent/template/resume.json)
- 输出格式参照 [task.json](../agent/template/task.json)


### 运行代码

```bash
python main.py
```

### 需要完成的内容
- [ ] 登录时自动填入账号密码，自动滑动滑块验证码
- [x] chromedriver 的路径配置独立到 `config/chrome.json` 文件中
- [ ] 将条件筛选单独拆成一个函数 `click_params`，简化 `conduct_scrape`
- [ ] `conduct_scrape` 是爬虫的主函数，需要将得到的简历信息存入字典列表 `RESUME_LISTS` 中，每存一个增加计数 `RESUME_COUNT`
- [ ] 程序 debug 时的输出需要改成 `logging.debug()`，避免混淆从 agent 启动爬虫程序时得到的 `stdout`
- [ ] 根据输入的条件进行筛选
  - [ ] 输入的条件均合法，将结果写入字典列表中
  - [ ] 输入的条件非法，需要处理错误，并将该爬虫程序的状态置为 `ERROR`