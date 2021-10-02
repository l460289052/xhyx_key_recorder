import { Checkbox, Divider, Button, Space, Tooltip, Table } from "antd"
import axios from "axios"
import { useEffect, useState } from "react"

function WordItem(item) {
    return (
        <Tooltip title={`编码"${item.code}" 触发按键 ${item.committer} `} color="#2db7f5">
            <ruby>{item.word}<rt>{item.code}{item.committer ? <span style={{ border: '.1em solid grey' }}>{item.committer}</span> : ""}</rt></ruby>
        </Tooltip>
    )
}

function ArticleView(words) {
    return <Space style={{ background: "#FAFAFA" }} wrap>
        {words.map(WordItem)}
    </Space>
}

const columns = [
    {
        title: '输入',
        dataIndex: 'old',
        key: 'old',
        render: old_words => old_words.map(WordItem)
    },
    {
        title: '建议',
        dataIndex: 'new',
        key: 'new',
        render: new_words => new_words.map(WordItem)
    }
]

function OptimView(words) {
    return <Table columns={columns} dataSource={words} />

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
                        .then(rep => setContent(ArticleView(rep.data.data)))}>查看</Button>
                <Button type="primary" onClick={e =>
                    axios.post("/api/get_optim", { records: checkedList })
                        .then(rep => setContent(OptimView(rep.data.data)))}>分析</Button>
            </Space>
            <Divider />
            {content}
        </>
    )
}

export default Analysis