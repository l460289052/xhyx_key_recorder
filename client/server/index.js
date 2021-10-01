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

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`)
})