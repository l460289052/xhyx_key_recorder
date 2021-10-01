import { Input, Table } from "antd";
import { useEffect, useState } from "react";
import axios from "axios"

const columns = [
    {
        title: '文件',
        dataIndex: 'file',
        key: 'file'
    },
    {
        title: '编码',
        dataIndex: 'code',
        key: 'code'
    },
    {
        title: '词条',
        dataIndex: 'word',
        key: 'word'
    }
]

function Search() {
    var [text, setText] = useState("")
    var [data, setData] = useState([])

    useEffect(() => {
        axios.get(
            '/api/search', { params: { code: text } })
            .then(rep => setData(rep.data.data))
    }, [text])

    return (
        <>
            <Input value={text} onChange={e => setText(e.target.value)} />
            <Table columns={columns} dataSource={data} />
        </>
    )
}

export default Search;