import { Checkbox, Divider, Button, Space, Tooltip } from "antd"
import axios from "axios"
import { useEffect, useState } from "react"

function WordItem(item) {
    return (
        <Tooltip title={`编码"${item.code}" 触发按键 ${item.committer} `} color="#2db7f5">
            <ruby>{item.word}<rt>{item.code}{item.committer ? <span style={{ border: '.1em solid grey' }}>{item.committer}</span> : ""}</rt></ruby>
        </Tooltip>
    )
}

function RecordView(words) {
    console.log(words)
    return <Space style={{ background: "#FAFAFA" }} wrap>
        {words.map(WordItem)}
    </Space>
}

function Analysis() {
    const [options, setOptions] = useState([])
    const [checkedList, setCheckedList] = useState([])
    const [content, setContent] = useState(<div />)

    useEffect(() => {
        axios.get("/api/get_records")
            .then(rep => setOptions(rep.data.data))
    }, [])

    return (
        <>
            <Checkbox.Group options={options} value={checkedList} onChange={list => setCheckedList(list)} />
            <Divider />
            <Space>
                <Checkbox
                    indeterminate={checkedList.length > 0 && checkedList.length < options.length}
                    checked={checkedList.length === options.length}
                    onChange={e => setCheckedList(e.target.checked ? options : [])}>选择全部文件</Checkbox>
                <Button onClick={e =>
                    axios.post("/api/get_article", { records: checkedList })
                        .then(rep => setContent(RecordView(rep.data.data)))}>查看</Button>
                <Button type="primary">分析</Button>
            </Space>
            <Divider />
            {content}
        </>
    )
}

export default Analysis