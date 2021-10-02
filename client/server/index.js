const express = require("express")

const PORT = process.env.PORT || 3001;
const app = express();

app.use(express.json())

app.get("/api", (res, rep) => {
    rep.json({ message: "Hello from express" })
})

app.get("/api/hello", (res, rep) => {
    rep.json({ message: "Hello from express" })
})

app.get("/api/statistics", (res, rep) => {
    console.log(`${new Date().toISOString()} /api/statistics`)
    rep.json({
        data: [
            { word: "我们", count: 31 },
            { word: "的", count: 5 },
        ]
    })
})

app.get("/api/search", (res, rep) => {
    console.log(`${new Date().toISOString()} /api/search ${res.query.code}`)
    var data = Array()
    for (var i = 0; i < 30; ++i) {
        data.push({ file: "default", code: res.query.code, word: "这是测试123" })
    }
    rep.json({
        data: data
    })
})

app.get("/api/get_records", (res, rep) => {
    console.log(`${new Date().toISOString()} /api/get_records`)
    rep.json({
        data: ['record.log', 'record.log.2021-10-01']
    })
})

app.post("/api/get_article", (res, rep) => {
    console.log(`${new Date().toISOString()} /api/get_article ${res.body}`)
    rep.json({
        data: [{ 'code': 'vege', 'word': '这个', 'committer': '', 'type': 'Word' }, { 'code': 'ys', 'word': '用', 'committer': 'space', 'type': 'Word' }, {
            'code': 'pipvl', 'word': 'pipvl', 'committer': 'space', 'type':
                'Undefine'
        }, { 'code': 'vl', 'word': '装', 'committer': 'space', 'type': 'Word' }, { 'code': 'yyxk', 'word': '运行', 'committer': '', 'type': 'Word' }, { 'code': 'vltd', 'word': '状态', 'committer': '', 'type': 'Word' }, { 'code': 'space', 'word': ' ', 'committer': '', 'type': 'Sign' }, { 'code': 'szso', 'word': '搜索', 'committer': '', 'type': 'Word' }, { 'code': 'mabn', 'word': '码表', 'committer': '', 'type': 'Word' }, { 'code': 'space', 'word': ' ', 'committer': '', 'type': 'Sign' }, { 'code': 'anjm', 'word': '按键', 'committer': '', 'type': 'Word' }, { 'code': 'tsji', 'word': '统计', 'committer': '', 'type': 'Word' }, { 'code': 'space', 'word': ' ', 'committer': '', 'type': 'Sign' }, { 'code': 'space', 'word': ' ', 'committer': '', 'type': 'Sign' }, { 'code': 'ffxi', 'word': '分析', 'committer': '', 'type': 'Word' }, { 'code': 'space', 'word': ' ', 'committer': '', 'type': 'Sign' }, { 'code': 'jxzd', 'word': '加载', 'committer': '', 'type': 'Word' }, { 'code': 'g', 'word': '个', 'committer': 'space', 'type': 'Word' }, { 'code': 'r', 'word': '人', 'committer': 'space', 'type': 'Word' }, { 'code': 'jip', 'word': '及', 'committer': 'space', 'type': 'Word' }, { 'code': 'xits', 'word': '系统', 'committer': '', 'type': 'Word' }, { 'code': 'pwvi', 'word': '配置', 'committer': '', 'type': 'Word' }, { 'code': 'wfjm', 'word': '文件', 'committer': '', 'type': 'Word' }, { 'code': 'ys', 'word': '用', 'committer': 'space', 'type': 'Word' }, { 'code': 'l', 'word': '了', 'committer': 'space', 'type': 'Word' }, { 'code': '6', 'word': '6', 'committer': '', 'type': 'Num' }, { 'code': '7', 'word': '7', 'committer': '', 'type': 'Num' }, { 'code': '3', 'word': '3', 'committer': '', 'type': 'Num' }, { 'code': 'hcmn', 'word': '毫秒', 'committer': '', 'type': 'Word' }, { 'code': 'enter', 'word': 'enter', 'committer': 'enter', 'type': 'Sign' }, { 'code': 'guyi', 'word': '故意', 'committer': '', 'type': 'Word' }, { 'code': 'uuco', 'word': '输错', 'committer': '', 'type': 'Word' }, { 'code': ':', 'word': ':', 'committer': '', 'type': 'Sign' }, { 'code': 'qiui', 'word': '其实', 'committer': '', 'type': 'Word' }, { 'code': 'gfbf', 'word': '根本', 'committer': '', 'type': 'Word' }, { 'code': 'my', 'word': '没有', 'committer': 'space', 'type': 'Word' }, { 'code': 'co', 'word': '错', 'committer': 'space', 'type': 'Word' }, { 'code': 'd', 'word': '的', 'committer': 'space', 'type': 'Word' }, { 'code': 'lak', 'word': '啦', 'committer': 'space', 'type': 'Word' }, { 'code': 'space', 'word': ' ', 'committer': '', 'type': 'Sign' }]
    })
})

app.post("/api/set_hook_state", (res, rep) => {
    console.log(`${new Date().toISOString()} /api/set_hook_state ${res.query.running}`)
    rep.json({})
})

app.get("/api/get_hook_state", (res, rep) => {
    console.log(`${new Date().toISOString()} /api/get_hook_state`)
    rep.json({ running: true })
})

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`)
})