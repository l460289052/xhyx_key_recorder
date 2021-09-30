const express = require("express")
const PORT = process.env.PORT || 3001;
const app = express();
app.get("/api", (res, rep) => {
    rep.json({ message: "Hello from express" })
})

app.get("/api/hello", (res, rep) => {
    rep.json({ message: "Hello from express" })
})

app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`)
})