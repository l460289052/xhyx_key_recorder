const express = require("express")
const PORT = process.env.PORT || 3001;
const app = express();
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

app.post("/api/set_hook_state", (res, rep) => {
    console.log(`${new Date().toISOString()} /api/set_hook_state ${res.query.running}`)
    rep.json({})
})

app.get("/api/get_hook_state", (res, rep) => {
    console.log(`${new Date().toISOString()} /api/get_hook_state`)
    rep.json({running:true})
})

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`)
})